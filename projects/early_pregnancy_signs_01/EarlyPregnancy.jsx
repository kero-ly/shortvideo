import React from 'react';
import {registerRoot,Composition,Still,AbsoluteFill,useCurrentFrame,interpolate} from 'remotion';
const C={ink:'#293e40',teal:'#388982',coral:'#dc7968',cream:'#faf5eb',skin:'#f4c5a4',muted:'#788d88'};
const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
const Woman=({x=285,y=195,scale=1,mood='calm',t=0,pose=''})=>{
 const breathe=Math.sin(t*2)*2,blink=Math.floor(t*2.3)%11===0;
 const tilt=['tired','nausea','smell'].includes(mood)?-7:Math.sin(t)*2;
 return <g transform={`translate(${x},${y+breathe}) scale(${scale})`} stroke={C.ink} strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round">
 <ellipse cx="0" cy="324" rx="91" ry="12" fill="#ddd9ce" stroke="none"/>
 <path d={mood==='tired'?'M-47 194 Q-46 232-13 235 L34 231 L48 293 L70 293 L62 212 Q60 194 40 194Z':'M-47 194 L-46 293 Q-39 308-20 297 L-8 213 L8 213 L22 298 Q40 307 46 293 L46 194'} fill="#4e6267"/>
 <path d={mood==='tired'?'M48 292L70 292L90 311Q94 319 46 315Z':'M-48 292 L-18 292 L-16 315 L-62 315 Q-68 305-48 292 M21 292 L46 292 L62 311 Q64 319 18 315Z'} fill="#f4e9d7"/>
 <path d="M-43 55 Q-72 68-67 131 L-53 207 Q0 220 54 207 L66 127 Q73 73 41 55Z" fill={C.teal}/>
 <path d="M-19 58 L0 88 L20 58 L28 208 L-27 208Z" fill={C.coral}/>
 <path d="M-57 76 Q-92 106-76 165 L-55 176 L-40 151 L-54 127" fill={C.teal}/>
 {['nausea','smell','sensitive'].includes(mood)?<path d="M56 79 Q83 107 47 134 L8 74 Q3 56 14 56 L59 102" fill={C.skin}/>:<path d={`M58 80 Q86 129 62 ${165+Math.sin(t*2)*4} Q53 178 44 163 L50 123`} fill={C.teal}/>}
 <path d={mood==='food'?`M-55 156 Q-93 169 ${-112-Math.min(t*5,14)} 173 L${-129-Math.min(t*5,14)} 161 Q-138 153-126 150 L-103 155 L-53 137Z`:'M-55 156 Q-32 156-20 130 Q-12 115-4 123 L-10 151 Q-29 179-52 181Z'} fill={C.skin}/>
 {pose==='phone'&&<rect x="-19" y="98" width="29" height="49" rx="5" fill="#f7e7bd" transform="rotate(15)"/>}
 <g transform={`rotate(${tilt})`}>
 <path d="M-54-12 Q-57-79 0-80 Q58-79 58-13 L63 60 L-61 60Z" fill="#354348"/>
 <path d="M-14 39 L-14 60 Q0 79 15 59 L15 38" fill={C.skin}/>
 <ellipse cx="-42" cy="3" rx="9" ry="14" fill={C.skin}/><ellipse cx="42" cy="3" rx="9" ry="14" fill={C.skin}/>
 <path d="M-41-29 Q-41-58 0-57 Q43-59 43-28 L40 15 Q35 49 0 51 Q-33 48-40 17Z" fill={C.skin}/>
 <path d="M-46-19 Q-49-66 0-67 Q49-65 47-13 Q19-19 7-42 Q-8-22-46-19Z" fill="#354348"/>
 <path d="M-26-9 Q-18-14-11-9 M13-9 Q22-14 29-8" fill="none"/>
 {blink||mood==='tired'?<path d="M-26 3 L-13 5 M14 5 L28 3" fill="none"/>:<><ellipse cx="-19" cy="4" rx="3" ry="5" fill={C.ink}/><ellipse cx="21" cy="4" rx="3" ry="5" fill={C.ink}/></>}
 <path d="M1 6 L-2 17 L4 18" fill="none" strokeWidth="2"/>
 <path d={mood==='nausea'||mood==='smell'?'M-9 31 Q0 25 9 31':mood==='tired'?'M-8 31 L8 31':'M-10 29 Q0 37 11 29'} fill="none" strokeWidth="2.5"/>
 <ellipse cx="-28" cy="20" rx="8" ry="4" fill="#e9a38f" stroke="none"/><ellipse cx="29" cy="20" rx="8" ry="4" fill="#e9a38f" stroke="none"/>
 </g></g>;
};
const Calendar=({x=70,y=120,t=0})=><g transform={`translate(${x},${y})`} stroke={C.ink} strokeWidth="3"><rect width="135" height="152" rx="13" fill="white"/><path d="M0 38H135"/><path d="M2 14Q2 1 15 1H120Q134 1 134 14V38H2Z" fill={C.coral} stroke="none"/>{Array.from({length:12},(_,i)=><circle key={i} cx={27+i%4*27} cy={65+Math.floor(i/4)*30} r="4" fill="#a2b4ab" stroke="none"/>)}<circle cx="81" cy="125" r={13+Math.sin(t)*2} fill="none" stroke={C.coral}/><path d="M31-8V14M104-8V14"/></g>;
const Room=({kind,t})=><g stroke={C.ink} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
 <rect x="0" y="0" width="540" height="600" fill="#f1eadc" stroke="none"/><path d="M0 459H540" stroke="#c8c5b7"/>
 <rect x="41" y="43" width="151" height="177" rx="12" fill="#c8dfd6" stroke="#b4ccc0"/><path d="M116 43V220M41 129H192" stroke="#fffaf0" strokeWidth="8"/><circle cx="153" cy="81" r="22" fill="#f6d48b" stroke="none"/>
 <path d="M449 440V355M449 393Q396 383 418 354Q448 359 449 393 M449 381Q492 356 482 339Q451 339 449 381" fill="#85a893" stroke="#688c7b"/><path d="M424 426H474L464 469H434Z" fill="#d99b7e"/>
 {['intro','calendar','truth'].includes(kind)&&<Calendar t={t}/>}
 {kind==='tired'&&<><rect x="35" y="304" width="336" height="131" rx="35" fill="#e7b896"/><path d="M56 402V464M350 402V464"/><rect x="34" y="348" width="338" height="71" rx="24" fill="#e8c8a8"/><text x="82" y={268-Math.sin(t)*5} fontSize="45" fill={C.muted} stroke="none">z z</text></>}
 {['nausea','smell','food'].includes(kind)&&<><rect x="26" y="366" width="238" height="27" rx="9" fill="#c8976d"/><path d="M49 393V487M243 393V487"/><ellipse cx="116" cy="353" rx="58" ry="14" fill="white"/><path d="M91 351Q113 299 139 351" fill="#8eaf79"/><rect x="177" y="305" width="43" height="56" rx="7" fill="#fffaf2"/><path d="M220 314Q244 314 231 342H220" fill="none"/>{[0,1,2].map(i=><path key={i} d={`M${177+i*17} ${291-Math.sin(t*2+i)*7}q-10-16 0-32q10-16 0-28`} fill="none" stroke="#b99f87" opacity=".6"/>)}</>}
 {kind==='bathroom'&&<><rect x="32" y="124" width="155" height="334" rx="4" fill="#c3d6cd"/><rect x="59" y="146" width="102" height="88" rx="8" fill="#faf5eb"/><text x="110" y="204" textAnchor="middle" fontSize="29" fill={C.teal} stroke="none">洗手间</text><circle cx="161" cy="310" r="6" fill={C.ink}/><circle cx="413" cy="139" r="43" fill="#fffaf0"/><path d={`M413 139L${413+Math.sin(t)*27} ${139-Math.cos(t)*27}M413 139L430 149`} fill="none"/></>}
 {kind==='mood'&&<><path d="M51 260Q83 212 116 260T182 260" stroke={C.coral} fill="none" strokeWidth="6"/><circle cx={51+(t*22)%131} cy="259" r="9" fill={C.coral} stroke="none"/></>}
 </g>;
const Info=({scene,t})=>{
 let rows=scene.kind==='test'?[['月经日期清楚','月经推迟的第一天起'],['不知道什么时候来','距上次无保护性行为','至少 21 天']]:scene.kind==='retest'?[['测得太早，结果阴性','过几天再测一次'],['复测阴性，月经仍没来','咨询医生']]:scene.kind==='truth'?[['有几条症状','不能直接确认怀孕'],['没有明显反应','也不能排除怀孕']]:[['明显腹痛 / 阴道出血','及时就医'],['先确认，再决定下一步','不用一个人靠猜']];
 return <div style={{position:'absolute',top:665,left:100,right:100}}>{rows.map((r,i)=><div key={i} style={{opacity:interpolate(t,[i*0.8,i*0.8+.45],[0,1],clamp),transform:`translateY(${interpolate(t,[i*.8,i*.8+.45],[20,0],clamp)}px)`,background:i===0?'#e0eee5':'#fffaf2',border:'2px solid #d6ded1',borderRadius:32,padding:'38px 38px',marginBottom:24}}>{r.map((s,j)=><div key={j} style={{fontSize:j===0?32:44,fontWeight:j===0?400:700,color:j===0?C.muted:C.ink,marginBottom:12,lineHeight:1.5}}>{s}</div>)}</div>)}</div>
};
const Episode=({scenes=[],captions=[],durationInFrames=240})=>{
 const f=useCurrentFrame(); const scene=scenes.find(s=>f>=s.start&&f<s.start+s.frames)||scenes[0];if(!scene)return null;
 const t=(f-scene.start)/24;const info=['truth','test','retest','care'].includes(scene.kind);
 const caption=captions.find(c=>f/24>=c.start&&f/24<c.end);
 const mood=scene.kind;const enter=interpolate(t,[0,.4],[35,0],clamp);
 return <AbsoluteFill style={{background:C.cream,color:C.ink,fontFamily:'Noto Sans CJK SC, sans-serif'}}>
 <div style={{position:'absolute',left:85,top:152,fontSize:24,letterSpacing:5,color:C.teal}}>身体的小信号 · 温柔了解自己</div>
 <div style={{position:'absolute',left:85,top:229,right:85,display:'flex',alignItems:'center',gap:28}}>{scene.number&&<span style={{fontSize:69,fontWeight:800,color:C.coral}}>{scene.number}</span>}<div style={{fontSize:scene.title.length>11?49:59,fontWeight:800,lineHeight:1.4}}>{scene.title}</div></div>
 <div style={{position:'absolute',left:90,top:354,fontSize:29,color:C.muted}}>{scene.note}</div>
 {!info?<div style={{position:'absolute',left:70,top:463,width:940,height:1030,borderRadius:48,overflow:'hidden',transform:`translateY(${enter}px)`}}><svg viewBox="0 0 540 600" width="940" height="1044"><Room kind={scene.kind} t={t}/><Woman x={scene.kind==='bathroom'?310-Math.min(t*13,90):scene.kind==='tired'?235:336} y={184} scale={.91} mood={mood} t={t} pose={['intro','mood'].includes(scene.kind)?'phone':''}/>{scene.kind==='intro'&&<g><circle cx="251" cy="87" r="39" fill="#fffaf2"/><text x="250" y="102" textAnchor="middle" fontSize="47" fill={C.coral}>?</text></g>}</svg></div>:<><div style={{position:'absolute',left:85,top:466,fontSize:28,color:C.coral,letterSpacing:2}}> {scene.kind==='care'?'照顾好自己':scene.kind==='truth'?'重要提醒':'把下一步说清楚'}</div><Info scene={scene} t={t}/></>}
 <div style={{position:'absolute',left:80,right:80,top:1515,minHeight:138,display:'flex',alignItems:'center',justifyContent:'center',textAlign:'center',fontSize:43,fontWeight:600,lineHeight:1.55}}>{caption?.text||''}</div>
 <div style={{position:'absolute',left:90,right:90,top:1726,display:'flex',justifyContent:'space-between',fontSize:23,color:C.muted}}><span>症状不能确认或排除怀孕</span><span>健康科普 · 非个体诊断</span></div>
 <div style={{position:'absolute',left:90,right:90,top:1790,height:5,background:'#e2e5dc'}}><div style={{height:5,width:`${100*f/durationInFrames}%`,background:C.teal}}/></div>
 </AbsoluteFill>;
};
const Cover=()=> <AbsoluteFill style={{background:C.cream,color:C.ink,fontFamily:'Noto Sans CJK SC, sans-serif',padding:85}}>
 <div style={{marginTop:85,fontSize:29,color:C.teal,letterSpacing:5}}>给正在猜答案的你</div>
 <div style={{fontSize:86,fontWeight:800,lineHeight:1.25,marginTop:50}}>早孕可能有的<br/><span style={{color:C.coral,fontSize:140}}>8</span> 个信号</div>
 <div style={{fontSize:34,color:C.muted,marginTop:28}}>最后告诉你，什么时候测</div>
 <svg viewBox="0 0 540 600" style={{width:910,height:1000,marginTop:12}}><Room kind="intro" t={1}/><Woman x={331} y={184} scale={1} t={1} pose="phone"/></svg>
 <div style={{fontSize:29,marginTop:32,textAlign:'center',color:C.teal}}>症状不是答案 · 先确认，再决定下一步</div>
 </AbsoluteFill>;
const Root=()=> <><Composition id="EarlyPregnancy" component={Episode} width={1080} height={1920} fps={24} durationInFrames={240} calculateMetadata={({props})=>({durationInFrames:props.durationInFrames||240})}/><Still id="EarlyPregnancyCover" component={Cover} width={1080} height={1920}/></>;
registerRoot(Root);
