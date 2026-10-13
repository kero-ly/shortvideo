import React from 'react';
import {AbsoluteFill,Composition,registerRoot,useCurrentFrame} from 'remotion';
import {makeTrack,cellPosition,bezier,sampleTrack} from './math.mjs';
const ink='#64372e',red='#ed685b',blue='#859ac8';
const paths=[[[465,660],[130,630],[180,310],[425,315]],[[635,315],[855,310],[830,650],[610,660]],[[625,760],[960,760],[920,1170],[630,1200]],[[450,1200],[130,1180],[120,785],[465,760]]];
const tracks=paths.map(p=>makeTrack(bezier(p)));
const d=p=>`M ${p[0]} C ${p[1]} ${p[2]} ${p[3]}`;
const ease=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)};
function Face({x=0,y=0,scale=1,f=0}){const blink=f%117<5;return <g transform={`translate(${x} ${y}) scale(${scale})`} stroke={ink} strokeWidth="6" strokeLinecap="round" fill="none"><path d={blink?'M -34 -12 l 12 0 M 22 -12 l 12 0':'M -28 -18 l 0 12 M 28 -18 l 0 12'}/><path d="M -17 13 Q 0 35 20 10"/><ellipse cx="-44" cy="9" rx="11" ry="6" fill="#e9857d" stroke="none"/><ellipse cx="43" cy="9" rx="11" ry="6" fill="#e9857d" stroke="none"/></g>}
function Cell({x,y,s=1,a=0,color=red,face=false,f=0}){return <g transform={`translate(${x} ${y}) rotate(${a}) scale(${s})`}><ellipse rx="27" ry="19" cy="5" fill="#9a4149"/><ellipse rx="27" ry="19" fill={color} stroke={ink} strokeWidth="2.5"/><ellipse rx="14" ry="8" fill="#bc4f58" opacity=".42"/><path d="M -18 -7 Q -6 -16 9 -10" stroke="#ffc4ac" strokeWidth="3" fill="none" strokeLinecap="round"/>{face&&<Face scale={.35} f={f}/>}</g>}
// Directional cues share the blood-cell tracks. Gold indicates attention only.
function Focus({x,y,w,h,f,opacity=1}) {
 const a=.68+.32*(.5+.5*Math.sin(f/30*Math.PI*2*1.2));
 const r=12,l=Math.min(26,w/3);
 const corner=`M ${-w/2} ${-h/2+l} V ${-h/2+r} Q ${-w/2} ${-h/2} ${-w/2+r} ${-h/2} H ${-w/2+l}`;
 return <g transform={`translate(${x} ${y})`} opacity={opacity*a} fill="none" strokeLinecap="round" strokeLinejoin="round">
 {[0,1,2,3].map(i=><g key={i} transform={`scale(${i%2?-1:1} ${i>1?-1:1})`}>
 <path d={corner} stroke="#ffc83e" strokeWidth="20" opacity=".2"/>
 <path d={corner} stroke={ink} strokeWidth="10"/>
 <path d={corner} stroke="#ffdd65" strokeWidth="6"/></g>)}
 </g>;
}
function Arrow({track,t,lead=false}) {
 const p=sampleTrack(tracks[track],t);
 return <g transform={`translate(${p.x} ${p.y}) rotate(${p.angle}) scale(${lead?1.15:.82})`}>
 <path d="M -29 -22 L -4 0 L -29 22 M 0 -22 L 25 0 L 0 22" fill="none" stroke={ink} strokeWidth="17" strokeLinecap="round" strokeLinejoin="round"/>
 <path d="M -29 -22 L -4 0 L -29 22 M 0 -22 L 25 0 L 0 22" fill="none" stroke="#fff5ab" strokeWidth="10" strokeLinecap="round" strokeLinejoin="round"/>
 </g>;
}
function RouteGuide({shot,local,under=false}) {
 if(![1,2,4].includes(shot))return null;
 const lung=shot===1,back=shot===4,pulmonary=shot===2&&local<77;
 const k=lung?0:back?3:pulmonary?1:2;
 const start=lung?44:back?10:pulmonary?9:79,end=lung?86:back?62:pulmonary?65:114;
 const progress=Math.max(0,Math.min(1,(local-start)/(end-start)));
 const alpha=ease((local-4)/8),arrival=ease((local-end)/8);
 const origin=lung?[499,750,86,110]:back?[540,1180,230,330]:pulmonary?[540,323,350,290]:[579,750,86,110];
 const dest=lung?[540,323,350,290]:back||pulmonary?[back?499:579,750,86,110]:[540,1180,230,330];
 if(under)return <g opacity={alpha} fill="none" strokeLinecap="round">
 <path d={d(paths[k])} stroke="#ffc940" strokeWidth="85" opacity=".18"/>
 <path d={d(paths[k])} pathLength="1" stroke="#ffcd45" strokeWidth="77" strokeDasharray={`${Math.max(.001,progress)} 1`}/>
 </g>;
 const label=lung?'右心 → 肺部':back?'全身 → 右心':pulmonary?'肺部 → 左心':'左心 → 全身';
 return <g opacity={alpha}>
 <Focus x={origin[0]} y={origin[1]} w={origin[2]} h={origin[3]} f={local} opacity={1-arrival*.7}/>
 <Focus x={dest[0]} y={dest[1]} w={dest[2]} h={dest[3]} f={local} opacity={arrival}/>
 {progress>0&&<Arrow track={k} t={Math.min(.97,Math.max(.035,progress))} lead/>}
 {[.22,.46,.70].filter(t=>progress>t+.14).map(t=><Arrow key={t} track={k} t={t}/>)}
 <g transform={`translate(540 ${lung?490:940})`}>
 <rect x="-137" y="-28" width="274" height="52" rx="26" fill="#fff1b9" stroke="#c79335" strokeWidth="3"/>
 <text textAnchor="middle" y="8" fontSize="29" fontWeight="800" fill={ink}>{label}</text></g>
 </g>;
}
function Body({f,detail=false}) {
 return <g transform="translate(540 1193)" strokeLinecap="round" strokeLinejoin="round">
 <circle cy="-139" r="30" fill="#ffe0b5" stroke={ink} strokeWidth="6"/>
 <path d="M -24 -104 Q -45 -107 -57 -84 L -94 -12 Q -100 4 -83 10 Q -72 13 -66 0 L -43 -45 L -40 16 L -53 117 Q -55 134 -38 135 Q -24 136 -22 122 L 0 42 L 22 122 Q 26 138 42 134 Q 56 131 52 116 L 40 16 L 43 -45 L 66 0 Q 73 14 87 9 Q 101 4 94 -12 L 57 -84 Q 44 -107 24 -104 Z" fill="#ffdfac" stroke={ink} strokeWidth="6"/>
 <g fill="none" strokeWidth="7">
 <path d="M 90 7 H 13 V -91 M 13 -68 L 43 -62 L 76 -5 M 13 7 V 35 L 36 113" stroke={red}/>
 <path d="M -90 7 H -13 V -91 M -13 -68 L -43 -62 L -76 -5 M -13 7 V 35 L -36 113" stroke={blue}/>
 <path d="M 13 -84 Q 0 -105 -13 -84 M 36 113 Q 0 130 -36 113 M 76 -5 Q 83 28 13 22 M -13 22 Q -83 28 -76 -5" stroke="#c68987" strokeWidth="4"/>
 </g>
 {detail&&<Focus x={0} y={7} w={86} h={60} f={f}/>}
 </g>;
}
function Diagram({f,shot,revision,local}){const pulse=Math.pow(Math.max(0,Math.sin(f/30*Math.PI*2*1.15)),4),breath=Math.sin(f/30*2);return <g>
<RouteGuide shot={shot} local={local} under/>
{paths.map((p,i)=><g key={i}><path d={d(p)} fill="none" stroke={ink} strokeWidth="61" strokeLinecap="round"/><path d={d(p)} fill="none" stroke={i===0||i===3?blue:red} strokeWidth="49" strokeLinecap="round"/><path d={d(p)} fill="none" stroke="#fff2df" strokeOpacity=".35" strokeWidth="29" strokeLinecap="round"/></g>)}
{tracks.map((track,k)=>Array.from({length:9},(_,i)=>{let p=cellPosition(track,f,30,i,9,5.8);return <Cell key={k+'-'+i} {...p} s={.55} a={p.angle+Math.sin(f*.07+i)*8} color={k===0||k===3?'#9692c4':red}/>;}))}
<g transform={`translate(540 323) scale(${1+breath*.018} ${1+breath*.035})`} stroke={ink} strokeWidth="7" strokeLinejoin="round"><path d="M -20 -107 C -92 -138 -174 -25 -160 68 Q -153 115 -64 91 Q -22 80 -22 32 Z" fill="#ffb9a0"/><path d="M 20 -107 C 92 -138 174 -25 160 68 Q 153 115 64 91 Q 22 80 22 32 Z" fill="#ffb9a0"/><path d="M 0 -146 L 0 -42 M 0 -42 L -84 16 M 0 -42 L 84 16 M -84 16 l -34 31 M -84 16 l -3 49 M 84 16 l 34 31 M 84 16 l 3 49" fill="none" stroke="#af6960" strokeWidth="13" strokeLinecap="round"/><Face x={-95} y={-30} scale={.5} f={f}/><Face x={95} y={-30} scale={.5} f={f+20}/></g>
<g transform="translate(540 720)"><path d={`M -75 -60 C ${-145+pulse*15} ${-169+pulse*10} -12 -160 9 -103 C 108 -162 ${150-pulse*15} -51 79 39 Q 32 99 0 121 Q -72 80 -75 -60 Z`} fill="#ee7365" stroke={ink} strokeWidth="8"/><path d="M 9 -96 Q -12 -20 7 79" fill="none" stroke="#bc514e" strokeWidth="5"/><path d={`M -89 1 Q -136 ${-17-pulse*23} -158 -3 M 97 -6 Q 137 ${-35-pulse*25} 151 -53`} fill="none" stroke={ink} strokeWidth="9" strokeLinecap="round"/><circle cx="-158" cy="-3" r="12" fill="#ffb29c" stroke={ink} strokeWidth="5"/><circle cx="151" cy="-53" r="12" fill="#ffb29c" stroke={ink} strokeWidth="5"/><Face x={3} y={-24} scale={.8} f={f}/><path d={`M -33 88 L -44 ${141-pulse*8} l -28 0 M 35 87 L 48 ${140+pulse*8} l 27 0`} stroke={ink} strokeWidth="9" strokeLinecap="round" fill="none"/><text x="-36" y="54" textAnchor="middle" fontSize="23" fill="#702e35">右</text><text x="40" y="54" textAnchor="middle" fontSize="23" fill="#702e35">左</text></g>
<Body f={f} detail={shot===2&&local>114||shot===3}/>
{revision>1&&Array.from({length:5},(_,i)=>{const t=((f/90+i/5)%1),x=650-t*150,y=1160-65*Math.sin(t*Math.PI);return <g key={i} opacity={Math.sin(t*Math.PI)}><circle cx={x} cy={y} r="15" fill="#fff9d5" stroke="#bc9050" strokeWidth="2"/><text x={x} y={y+5} textAnchor="middle" fontSize="14" fill={ink}>O₂</text></g>})}
<g fill={ink} textAnchor="middle" fontSize="32" fontWeight="700">{shot!==1&&<text x="540" y="480">肺部 · 气体交换</text>}{shot!==2&&<text x="540" y="1380">全身 · 人体示意</text>}</g>
<g fontSize="23" fill={ink} textAnchor="middle">{[[340,551,'↑ 去肺部'],[721,551,'回心脏 ↓'],[705,1010,'送往全身 ↓'],[352,1010,'↑ 返回']].map(([x,y,t])=><g key={t}><rect x={x-81} y={y-28} width="162" height="43" rx="21" fill="#fff0d0"/><text x={x} y={y}>{t}</text></g>)}</g>
{revision>1&&<g><g transform={`translate(540 ${580+Math.sin(f*.09)*5})`}><rect x="-90" y="-23" width="180" height="43" rx="21" fill="#fff5d8"/><text textAnchor="middle" y="7" fontSize="23" fill={ink}>{pulse>.3?'收缩 · 推出':'舒张 · 充盈'}</text></g>{Array.from({length:4},(_,i)=>{const t=(f/100+i/4)%1;return <g key={i} opacity={Math.sin(t*Math.PI)} transform={`translate(${660-t*100} ${205+t*155})`}><circle r="17" fill="#fff6cf" stroke="#b18f62" strokeWidth="2"/><text y="6" textAnchor="middle" fill={ink} fontSize="16">O₂</text></g>})}</g>}
<RouteGuide shot={shot} local={local}/>
</g>}
function Vessel({f,revision}){return <g><path d="M -100 530 C 300 350 710 830 1200 575 L 1200 1000 C 710 1255 300 775 -100 955 Z" fill="#efafa0" stroke={ink} strokeWidth="10"/><path d="M -100 600 C 300 420 710 900 1200 645 L 1200 930 C 710 1185 300 705 -100 885 Z" fill="#f8cab5"/>
<defs><clipPath id="vessel"><path d="M -100 610 C 300 430 710 910 1200 655 L 1200 920 C 710 1175 300 695 -100 875 Z"/></clipPath></defs><g clipPath="url(#vessel)">{Array.from({length:12},(_,i)=>{const t=((f/240+i/12)%1);let x=-120+t*1350,y=750+Math.sin(t*Math.PI*2-1.7)*100+(i%3-1)*55;return <Cell key={i} x={x} y={y} s={1.2+(i%3)*.35} a={Math.sin(f*.035+i)*22} face={i%3===0} f={f}/>})}{Array.from({length:22},(_,i)=><circle key={i} cx={((i*173+f*2)%1250)-100} cy={620+i%6*50} r="4" fill="#fff4d6"/>)}</g>
<g transform="translate(570 1150)">{[-260,-90,90,260].map((x,i)=><g key={i} transform={`translate(${x} ${Math.sin(f*.04+i)*8})`}><rect x="-69" y="-46" width="138" height="125" rx="44" fill="#ffdda0" stroke={ink} strokeWidth="5"/><Face y={12} scale={.6} f={f+i*12}/></g>)}</g>
{Array.from({length:7},(_,i)=>{const t=(f/70+i/7)%1;return <g transform={`translate(${200+i*110} ${900+t*230})`} opacity={Math.sin(t*Math.PI)}><circle r="22" fill="#fff6ca" stroke="#a98050" strokeWidth="3"/><text textAnchor="middle" y="8" fontSize="21" fill={ink}>O₂</text></g>})}<text x="540" y="440" textAnchor="middle" fill={ink} fontSize="40" fontWeight="700">红细胞，出发！</text><text x="540" y="1330" textAnchor="middle" fill={ink} fontSize="32">把氧送到身体各处</text></g>}
function BodyZoom({f,local,revision}) {
 const e=ease(local/42),scale=.055+(1.04-.055)*e;
 const x=520+(533.6-520)*e,y=1319.96+(785.4-1319.96)*e;
 const bgZoom=1.2+1.8*e,cy=880+320*e;
 return <g>
 <g opacity={1-ease(local/30)} transform={`translate(520 959) scale(${bgZoom*.94}) translate(-540 ${-cy})`}>
 <Diagram f={f} shot={3} revision={revision} local={local}/>
 </g>
 <g transform={`translate(${x} ${y}) scale(${scale}) translate(-540 -760)`}>
 <defs><clipPath id="detailWindow"><rect x="-100" y="390" width="1300" height="1020" rx="60"/></clipPath></defs>
 <g clipPath="url(#detailWindow)">
 <Vessel f={f} revision={revision}/>
 </g>
 </g>
 {local<42&&<g opacity={1-ease((local-30)/12)}><rect x="342" y="1410" width="356" height="56" rx="28" fill="#ffdc68"/><text x="520" y="1448" textAnchor="middle" fontSize="30" fontWeight="800" fill={ink}>放大看：体内的一段血管</text></g>}
 </g>;
}
const titles=['心脏的小小运输队','第一站：去肺部换气','第二站：奔向全身','红细胞，送氧到站','两条循环，一直运转'];
export function Heart({shots,totalFrames,revision=1}){let f=useCurrentFrame(),idx=shots.findIndex(s=>f<s.start+s.frames);if(idx<0)idx=4;const shot=shots[idx],local=f-shot.start,t=local/shot.frames;let zoom=idx===0?1+.13*ease(t):idx===1?1.25:idx===2?1.18:1;const cx=540;let cy=idx===1?495:idx===2?850:760;if(revision>1){const e=ease(local/24);if(idx===1){zoom=1.13+(1.34-1.13)*e;cy=760+(515-760)*e;}if(idx===2){zoom=1.34+(1.2-1.34)*e;cy=515+(880-515)*e;}if(idx===4){zoom=1.07-.07*ease(t);}}const lines=shot.text.replace('。','').split('，');return <AbsoluteFill style={{background:'#fff0d8',fontFamily:'"Noto Sans CJK SC",sans-serif'}}><svg viewBox="0 0 1080 1920" width="100%" height="100%"><defs><radialGradient id="bg"><stop stopColor="#fff7e9"/><stop offset="1" stopColor="#f6e3c7"/></radialGradient><clipPath id="scene"><rect x="0" y="405" width="1080" height="1515"/></clipPath><linearGradient id="captionFade" x1="0" y1="0" x2="0" y2="1"><stop stopColor="#fff0d8" stopOpacity="0"/><stop offset=".28" stopColor="#fff0d8" stopOpacity=".96"/></linearGradient></defs>
<rect width="1080" height="1920" fill="url(#bg)"/>
<g textAnchor="middle" fontWeight="900" fontSize="103" stroke={ink} strokeWidth="14" paintOrder="stroke" strokeLinejoin="round"><text x="515" y="244" fill="#fffaf0">心脏一跳</text><text x="515" y="367" fill="#ffd65b">血液去哪儿？</text></g>
<g clipPath="url(#scene)">
 {idx===3?<BodyZoom f={f} local={local} revision={revision}/>:<g transform={`translate(520 959) scale(${zoom*.94}) translate(${-cx} ${-cy})`}><Diagram f={f} shot={idx} revision={revision} local={local}/></g>}
 </g>
<rect x="0" y="1430" width="1080" height="490" fill="url(#captionFade)"/>
<g fill="#fffaf0" stroke={ink} strokeWidth="8" paintOrder="stroke" strokeLinejoin="round" textAnchor="middle" fontSize="49" fontWeight="900" opacity={ease(local/7)}>{lines.map((line,i)=><text key={i} x="515" y={1640+i*73}>{line}</text>)}</g>
<g transform="translate(165 1850)" fontSize="21" fill="#8d705d"><circle r="7" fill={red}/><text x="17" y="7">氧较多</text><circle cx="136" r="7" fill={blue}/><text x="153" y="7">氧较少</text><text x="296" y="7">颜色与比例为示意</text></g></svg></AbsoluteFill>}

const defaults={shots:[0,1,2,3,4].map((i)=>({start:i*180,frames:180,text:'心脏推动血液，循环持续运转。'})),totalFrames:900};
registerRoot(()=> <Composition id="HeartCirculation" component={Heart} width={1080} height={1920} fps={30} durationInFrames={900} defaultProps={defaults} calculateMetadata={({props})=>({durationInFrames:props.totalFrames})}/>);
