# SVG机制组件：选择与适配

这是一份已执行案例的代码导航，不是独立组件库。源码[Heart-v10.jsx](../../../projects/heart_circulation_mechanism_04/scripts/Heart-v10.jsx)、[math.mjs](../../../projects/heart_circulation_mechanism_04/scripts/math.mjs)，证据[v10 QA](../../../projects/heart_circulation_mechanism_04/review/v10-QA.md)、[运动分镜](../../../projects/heart_circulation_mechanism_04/review/v10-motion-plan.md)。参数外观见[SVG机制引导](../../../styles/visual/svg-mechanism-guidance.json)。

| 需求 | 实现 | 必须适配与验证 |
|---|---|---|
| 沿管道流动 | makeTrack/sampleTrack/cellPosition | 新路径的方向、弧长、分支、闭环接缝；不要复用心脏路径坐标 |
| 明确起点→终点 | Arrow/RouteGuide | 箭头按同一track切线；全程含返回路径；按真实词级时间到站；手机尺度验证粗细 |
| 局部强调 | Focus | 圆角四角、暗底描边、金色内线，案例1.2Hz/68–100%呼吸；对新器官重设包围框 |
| 器官拟人/跳动 | Face/Diagram | 简单眼口、四肢与局部形变；连接锚点不脱离，非复杂骨骼绑定 |
| 宏观→局部 | Body/BodyZoom/Vessel | 原图先指出局部；细节原点匹配同一屏幕锚点，再平移缩放，背景同步推近；不能用单纯交叉淡化冒充连续运镜 |
| 粒子不穿管壁 | Vessel clipPath | 新形状重新检查所有运动极值与裁切；颜色含义在两镜一致 |

复用前复制所需源码到本期并登记源hash/修改理由。Heart-v10.jsx带Composition注册和心脏专有数据，不能当纯库直接导入新主题。保留历史源，记录新结构→分层资产→动作→渲染的关系；不建设素材库。

代表验证包含起点、途中、终点、返回、高亮明暗、运镜边界两侧和运动中间帧，再看短片动态。新器官、比例、分支必须依据事实重新构造；心脏案例不证明肾脏过滤/神经信号等结构正确。

实际渲染/抽帧在220。参考render-v10.sh/finalize-v10.sh但改唯一episode/run路径，检查输入像素范围后转换BT.709/yuv420p，不能盲套full-range转换。只改画面优先复用最新已选AAC，v10采用的是v9音乐而非v8；复制后核对音轨hash与时序。实际听审/用户效果认可仍pending，当前证据为case-tested。
