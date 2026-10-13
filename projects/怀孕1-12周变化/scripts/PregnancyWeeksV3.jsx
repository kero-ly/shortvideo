import React from 'react';
import {registerRoot,Composition,AbsoluteFill,Sequence,OffthreadVideo,staticFile,useCurrentFrame} from 'remotion';
const Video=({shots,cues,assetBase})=>{const frame=useCurrentFrame();const now=frame/24;const shot=shots.find(s=>frame>=s.start&&frame<s.start+s.frames)||shots[0];const cue=cues.find(c=>now>=c.start&&now<c.end);return <AbsoluteFill style={{background:'#fff6e7',fontFamily:'Noto Sans CJK SC',color:'#344338'}}>
{shots.map(s=><Sequence key={s.id} from={s.start} durationInFrames={s.frames}><OffthreadVideo muted src={staticFile(`${assetBase}/${s.id}.mp4`)} style={{width:'100%',height:'100%',objectFit:'cover'}}/></Sequence>)}
<div style={{position:'absolute',top:175,left:76,right:160,fontSize:43,fontWeight:700,letterSpacing:3}}>怀孕 1—12 周变化</div>
<div style={{position:'absolute',top:250,left:76,right:160,fontSize:66,fontWeight:800,lineHeight:1.3}}>{shot.phase}</div>
<div style={{position:'absolute',top:350,left:78,right:166,display:'flex',gap:8}}>{Array.from({length:12},(_,i)=><div key={i} style={{height:9,flex:1,borderRadius:8,background:i<Number(shot.phase.match(/第(\d+)周/)?.[1]||0)?'#d59b6f':'#dfdfcc'}}/>)}</div>
{cue&&<div style={{position:'absolute',left:90,right:90,top:460,padding:'23px 28px',borderRadius:24,background:'rgba(255,250,238,.94)',boxShadow:'0 3px 15px rgba(50,45,30,.08)',fontSize:55,fontWeight:700,lineHeight:1.48,textAlign:'center',whiteSpace:'pre-wrap'}}>{cue.text}</div>}
<div style={{position:'absolute',left:76,top:78,fontSize:26,color:'#586459'}}>孕周按末次月经起算，个体发育和感受有差异</div>
</AbsoluteFill>};
registerRoot(()=> <Composition id="PregnancyWeeks" component={Video} fps={24} width={1080} height={1920} durationInFrames={2151} calculateMetadata={({props})=>({durationInFrames:props.total_frames})}/>);
