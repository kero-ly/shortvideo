import React from 'react';
import {AbsoluteFill,Composition,Still,Img,OffthreadVideo,Sequence,registerRoot,staticFile,useCurrentFrame,interpolate} from 'remotion';
const C={ink:'#243a39',teal:'#407f78',coral:'#ce7666'};
const TextPanel=({title,children})=><div style={{background:'rgba(255,252,243,.95)',borderRadius:24,padding:'28px 32px',marginBottom:20,boxShadow:'0 8px 30px #18372c12'}}><div style={{fontSize:27,color:C.teal,marginBottom:10}}>{title}</div><div style={{fontSize:38,fontWeight:700,lineHeight:1.45}}>{children}</div></div>;
const Film=({scenes=[],captions=[],durationInFrames=240,assetBase=''})=>{
 const f=useCurrentFrame();const s=scenes.find(x=>f>=x.start&&f<x.start+x.frames)||scenes[0];if(!s)return null;
 const caption=captions.find(c=>f/24>=c.start&&f/24<c.end);const info=['truth','test','retest','care'].includes(s.kind);
 const fade=interpolate(f-s.start,[0,8],[0,1],{extrapolateRight:'clamp'});
 return <AbsoluteFill style={{background:'#faf5eb',fontFamily:'Noto Sans CJK SC, sans-serif',color:C.ink}}>
 {scenes.map((scene,i)=><Sequence key={scene.id} from={scene.start} durationInFrames={scene.frames}><OffthreadVideo muted src={staticFile(`${assetBase}/shot_${String(i+1).padStart(2,'0')}.mp4`)} style={{position:'absolute',left:135,top:340,width:810,height:1440,objectFit:'cover',borderRadius:28}}/></Sequence>)}
 <AbsoluteFill style={{background:'linear-gradient(180deg,rgba(250,245,235,.99) 0%,rgba(250,245,235,.94) 16%,rgba(250,245,235,0) 29%,rgba(250,245,235,0) 71%,rgba(250,245,235,.95) 82%,rgba(250,245,235,.99) 100%)'}}/>
 <div style={{position:'absolute',left:82,right:82,top:156,opacity:fade}}>
 <div style={{fontSize:25,color:C.teal,letterSpacing:4,marginBottom:27}}>身体的小信号 · 温柔了解自己</div>
 <div style={{fontSize:s.title.length>12?49:58,fontWeight:800,lineHeight:1.35}}>{s.number&&<span style={{color:C.coral,marginRight:22}}>{s.number}</span>}{s.title}</div>
 <div style={{fontSize:29,color:'#687c75',marginTop:18}}>{s.note}</div></div>
 {info&&<div style={{position:'absolute',left:80,top:555,width:450,opacity:fade}}>
 {s.kind==='truth'&&<><TextPanel title="有几条症状">不能直接确认怀孕</TextPanel><TextPanel title="没有明显反应">也不能排除怀孕</TextPanel></>}
 {s.kind==='test'&&<><TextPanel title="月经日期清楚">月经推迟的<br/>第一天起测</TextPanel><TextPanel title="不知道月经什么时候来">距上次无保护性行为<br/><span style={{fontSize:57,color:C.coral}}>至少 21 天</span></TextPanel></>}
 {s.kind==='retest'&&<><TextPanel title="测得太早，结果阴性">过几天再测一次</TextPanel><TextPanel title="复测阴性，月经仍没来">咨询医生</TextPanel></>}
 {s.kind==='care'&&<><TextPanel title="明显腹痛 / 阴道出血">请及时就医</TextPanel><TextPanel title="先确认，再决定下一步">不用一个人靠猜</TextPanel></>}
 </div>}
 <div style={{position:'absolute',top:1512,left:85,right:85,minHeight:150,display:'flex',alignItems:'center',justifyContent:'center',textAlign:'center',fontSize:43,fontWeight:600,lineHeight:1.6}}>{caption?.text||''}</div>
 <div style={{position:'absolute',top:1740,left:85,right:85,display:'flex',justifyContent:'space-between',fontSize:22,color:'#657f76'}}><span>症状不能确认或排除怀孕</span><span>AI 画面 · 健康科普</span></div>
 <div style={{position:'absolute',left:85,right:85,top:1800,height:4,background:'#dbe3d9'}}><div style={{width:`${100*f/durationInFrames}%`,height:4,background:C.teal}}/></div>
 </AbsoluteFill>;
};
const Cover=({assetBase=''})=><AbsoluteFill style={{background:'#faf5eb',fontFamily:'Noto Sans CJK SC, sans-serif',color:C.ink}}>
 <Img src={staticFile(`${assetBase}/cover-source.png`)} style={{position:'absolute',left:90,top:580,width:900,height:1190,objectFit:'cover',objectPosition:'center 35%',borderRadius:32}}/>
 <div style={{position:'absolute',left:85,top:160,fontSize:29,color:C.teal,letterSpacing:4}}>给正在猜答案的你</div>
 <div style={{position:'absolute',left:85,top:254,fontSize:83,fontWeight:800,lineHeight:1.28}}>早孕可能有的<br/><span style={{fontSize:128,color:C.coral}}>8</span> 个信号</div>
 <div style={{position:'absolute',left:90,top:532,fontSize:31,color:C.teal}}>最后告诉你，什么时候测</div>
 <div style={{position:'absolute',left:70,right:70,top:1800,textAlign:'center',fontSize:28,color:C.teal}}>症状不是答案 · 先确认，再决定下一步</div>
 </AbsoluteFill>;
registerRoot(()=> <><Composition id="EarlyPregnancyH3" component={Film} width={1080} height={1920} fps={24} durationInFrames={240} calculateMetadata={({props})=>({durationInFrames:props.durationInFrames||240})}/><Still id="EarlyPregnancyH3Cover" component={Cover} width={1080} height={1920}/></>);
