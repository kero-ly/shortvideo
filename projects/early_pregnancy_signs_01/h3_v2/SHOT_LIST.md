# 分镜与文件对照

实际生成和剪辑版本；所有文件路径相对本目录，H3 原片路径见 `review/h3-clips.json`。

| 镜头 | 分组 | 内容 | 参考图 | 动作 / 运镜 prompt | 剪辑秒数 |
|---|---|---|---|---|---|
| shot_01 | A 开场 | 月经没来，先别急着猜 | `references/shots/openlux_shot_01_v1.png` | `prompts/shot_01_h3.txt` | 7.792 |
| shot_02 | B 八种变化 | 月经推迟 | `references/shots/openlux_shot_02_v1.png` | `prompts/shot_02_h3.txt` | 5.083 |
| shot_03 | B 八种变化 | 比平时更容易累 | `references/shots/openlux_shot_03_v1.png` | `prompts/shot_03_h3.txt` | 4.792 |
| shot_04 | B 八种变化 | 乳房胀痛或敏感 | `references/shots/openlux_shot_04_v1.png` | `prompts/shot_04_h3.txt` | 4.500 |
| shot_05 | B 八种变化 | 恶心不只在早晨 | `references/shots/openlux_shot_05_v1.png` | `prompts/shot_05_h3.txt` | 4.083 |
| shot_06 | B 八种变化 | 对气味更敏感 | `references/shots/openlux_shot_06_v1.png` | `prompts/shot_06_h3.txt` | 4.458 |
| shot_07 | B 八种变化 | 小便次数增多 | `references/shots/openlux_shot_07_v1.png` | `prompts/shot_07_h3.txt` | 4.667 |
| shot_08 | B 八种变化 | 口味变化 | `references/shots/openlux_shot_08_v1.png` | `prompts/shot_08_h3.txt` | 4.375 |
| shot_09 | B 八种变化 | 情绪起伏 | `references/shots/openlux_shot_09_v1.png` | `prompts/shot_09_h3.txt` | 5.208 |
| shot_10 | C 确认与行动 | 症状不能确认或排除怀孕 | `references/shots/openlux_shot_10_v1.png` | `prompts/shot_10_h3_v3.txt` | 9.375 |
| shot_11 | C 确认与行动 | 验孕时间规则 | `references/shots/openlux_shot_11_v1.png` | `prompts/shot_11_h3.txt` | 9.083 |
| shot_12 | C 确认与行动 | 阴性后复测与咨询 | `references/shots/openlux_shot_12_v1.png` | `prompts/shot_12_h3.txt` | 7.792 |
| shot_13 | C 确认与行动 | 及时就医，先确认再决定 | `references/shots/openlux_shot_13_v1.png` | `prompts/shot_13_h3.txt` | 8.375 |

总长 1910 帧 / 24fps = 79.583 秒。H3 输出按模型帧数规则向上取整，剪辑按旁白真实时间线截取。每镜图像提示词位于 `prompts/shot_XX_image.txt`；实际 OpenLux 请求另存 `review/openlux_shot_XX_v1.json`。

第 10 镜 v1、v2 因气泡或多余道具被拒绝；v3 使用 baseline20，其他镜头使用 Turbo8。原始 workflow、seed、prompt 与输入图哈希保存在各自 run 目录。
