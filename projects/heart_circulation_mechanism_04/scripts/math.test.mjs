import test from 'node:test';
import assert from 'node:assert/strict';
let motion;
try { motion=await import('./math.mjs'); } catch {}
test('motion module exists',()=>assert.ok(motion,'Motion primitives not implemented'));
test('arc length sampling has uniform speed through differently sized segments',()=>{
 assert.ok(motion);
 const p=motion.makeTrack([[0,0],[10,0],[10,90]]);
 assert.deepEqual(motion.sampleTrack(p,.5),{x:10,y:40,angle:90});
 assert.equal(p.length,100);
});
test('loop wrapping keeps a closed curve continuous',()=>{
 assert.ok(motion);
 const p=motion.makeTrack([[0,0],[100,0],[100,100],[0,100],[0,0]]);
 const a=motion.sampleTrack(p,.999999),b=motion.sampleTrack(p,1.000001);
 assert.ok(Math.hypot(a.x-b.x,a.y-b.y)<.001);
 assert.deepEqual(motion.sampleTrack(p,.25),motion.sampleTrack(p,1.25));
});
test('cell sampling is deterministic across frame order and negative offsets',()=>{
 assert.ok(motion);
 const p=motion.makeTrack([[0,0],[100,0],[0,0]]);
 const first=motion.cellPosition(p,75,30,2,5,4);
 motion.cellPosition(p,200,30,2,5,4);
 assert.deepEqual(first,motion.cellPosition(p,75,30,2,5,4));
 assert.ok(Number.isFinite(motion.cellPosition(p,-10,30,0,5,4).x));
});
