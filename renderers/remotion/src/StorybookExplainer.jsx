import React from 'react';
import {AbsoluteFill,Composition,Still,Img,OffthreadVideo,Sequence,registerRoot,staticFile,useCurrentFrame,interpolate} from 'remotion';
const ink='#684630', cream='#fff4de';
const infoFor=(kind,seconds)=>{
 const cards={truth:[['有这些反应','不能直接确认怀孕'],['没有明显反应','也不能排除怀孕']],test:[['月经日期清楚','月经推迟的第一天起测'],['不知道下次月经日期','上次无保护性行为\n至少 21 天后再测']],retest:[['测得太早，结果阴性','过几天再测一次'],['复测阴性，月经仍没来','可以咨询医生']],care:[['明显腹痛或阴道出血','请及时就医'],['先确认，再决定下一步','不用一个人靠猜']]};
 const thresholds={truth:4.4,test:3.15,retest:3.9,care:3.7};return cards[kind]?.[seconds<(thresholds[kind]||4)?0:1];
};
const Film=({scenes=[],captions=[],assetBase='',durationInFrames=240,subtitleLayout='classic'})=>{
 const f=useCurrentFrame();const s=scenes.find(x=>f>=x.start&&f<x.start+x.frames)||scenes[0];if(!s)return null;
 const local=(f-s.start)/24;const card=infoFor(s.kind,local);const cap=captions.find(x=>f/24>=x.start&&f/24<x.end);
 const alpha=interpolate(f-s.start,[0,5],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 return <AbsoluteFill style={{background:cream,color:ink,fontFamily:'Noto Sans CJK SC, sans-serif'}}>
 {scenes.map((x,i)=><Sequence key={x.id} from={x.start} durationInFrames={x.frames}><OffthreadVideo muted src={staticFile(`${assetBase}/shot_${x.shot_id||String(i+1).padStart(2,'0')}.mp4`)} style={{width:'100%',height:'100%',objectFit:'cover'}}/></Sequence>)}
 {subtitleLayout!=='lower-single'&&<div style={{position:'absolute',top:228,left:78,right:110,textAlign:'center',opacity:alpha}}>
 <div style={{fontSize:card?58:68,fontWeight:900,lineHeight:1.4,color:ink,background:'rgba(255,232,157,.94)',display:'inline-block',padding:'4px 20px',borderRadius:16}}>{s.number?`${s.number} · `:''}{s.title}</div>
 {!card&&s.kind!=='intro'&&<div style={{display:'block',width:'fit-content',margin:'12px auto 0',padding:'5px 18px',borderRadius:14,background:'#fff8eced',fontSize:34,fontWeight:500}}>{s.note}</div>}
 </div>}
 {subtitleLayout!=='lower-single'&&card&&<div style={{position:'absolute',top:345,left:100,right:115,textAlign:'center',padding:'16px 24px',borderRadius:20,background:'rgba(255,248,232,.95)',boxShadow:'0 4px 18px #76553918'}}><div style={{fontSize:34,marginBottom:6}}>{card[0]}</div><div style={{fontSize:48,fontWeight:800,lineHeight:1.35,whiteSpace:'pre-line'}}>{card[1]}</div></div>}
 <div style={{position:'absolute',...(subtitleLayout==='lower-single'?{bottom:280}:{top:1460}),left:88,right:125,minHeight:90,display:'flex',alignItems:'center',justifyContent:'center',textAlign:'center'}}>{cap&&<div style={{padding:'10px 24px',borderRadius:18,background:'rgba(255,249,238,.95)',fontSize:62,fontWeight:700,lineHeight:1.48,whiteSpace:'pre-line'}}>{cap.text==='就在上次无保护性行为至少二十一天后测'?'就在上次无保护性行为\n至少二十一天后测':cap.text}</div>}</div>
 <div style={{position:'absolute',left:subtitleLayout==='lower-single'?28:70,top:subtitleLayout==='lower-single'?32:112,fontSize:28,color:ink,padding:subtitleLayout==='lower-single'?0:'8px 14px',textShadow:'0 1px 3px rgba(255,250,240,.95)'}}>个人观点仅限参考，无不良引导</div>
 </AbsoluteFill>;
};
const Cover=({assetBase=''})=><AbsoluteFill style={{fontFamily:'Noto Sans CJK SC, sans-serif',background:cream,color:ink}}><Img src={staticFile(`${assetBase}/cover-source.png`)} style={{width:'100%',height:'100%',objectFit:'cover'}}/><div style={{position:'absolute',left:80,right:95,top:200,textAlign:'center',fontSize:68,fontWeight:900,lineHeight:1.3,color:ink,background:'rgba(255,232,157,.94)',padding:20,borderRadius:24}}>早孕可能出现的<br/><span style={{fontSize:100}}>8 个信号</span></div><div style={{position:'absolute',top:1470,left:100,right:115,padding:18,borderRadius:22,background:'#fff8eced',fontSize:36,textAlign:'center'}}>症状不是答案，按时验孕确认</div></AbsoluteFill>;
registerRoot(()=> <><Composition id="StorybookExplainer" component={Film} width={1080} height={1920} fps={24} durationInFrames={240} calculateMetadata={({props})=>({durationInFrames:props.durationInFrames||240})}/><Still id="StorybookCover" component={Cover} width={1080} height={1920}/></>);
