import React from 'react';
import {registerRoot, Composition, AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
const Scene=({caption='画面、旁白和字幕，正在同一条时间线上运行。'})=>{
 const frame=useCurrentFrame();
 const {durationInFrames}=useVideoConfig();
 const x=interpolate(frame,[0,durationInFrames-1],[95,445],{extrapolateRight:'clamp'});
 return <AbsoluteFill style={{backgroundColor:'#102438',color:'#f7f5ed',fontFamily:'Noto Sans CJK SC',padding:38}}>
 <div style={{fontSize:20,color:'#70dbd2',letterSpacing:3}}>SHORTVIDEO FACTORY / 工具链测试</div>
 <div style={{fontSize:48,fontWeight:700,lineHeight:1.25,marginTop:45}}>让内容<br/>动起来</div>
 <svg width="464" height="360" viewBox="0 0 540 360" style={{marginTop:35}}>
 <path d="M60 240 Q270 20 480 240" fill="none" stroke="#496d8b" strokeWidth="4"/>
 <circle cx={x} cy={240-120*Math.sin((x-60)/420*Math.PI)} r="32" fill="#ffc866"/>
 <path d="M55 290 L480 290" stroke="#70dbd2" strokeWidth="3"/>
 <text x="55" y="337" fill="#a9c4d5" fontSize="25">画面 → 配音 → 合成 → 检查</text>
 </svg>
 <div style={{position:'absolute',bottom:115,left:38,right:38,fontSize:28,lineHeight:1.5,textAlign:'center'}}>{caption}</div>
 <div style={{position:'absolute',bottom:48,left:38,right:38,height:5,background:'#304b62'}}><div style={{height:5,width:`${Math.min(100,frame/(durationInFrames-1)*100)}%`,background:'#70dbd2'}}/></div>
 </AbsoluteFill>;
};
const Root=()=> <Composition id="FactorySmoke" component={Scene} width={540} height={960} fps={24} durationInFrames={144} calculateMetadata={({props})=>({durationInFrames:props.durationInFrames||144})}/>;
registerRoot(Root);
