# 角色挑选画册

入口：[角色挑选画册](../review/character-lookbook-v1.html)。按项目浏览、搜索、放大原图，复制角色编号后可在后续制作中指定使用。

这是历史角色的只读挑选页，不迁移原素材，也不是全历史素材完整归档声明。确认状态分开标注；未核对确认记录的历史候选不视作已批准。新片仍需核对角色适配和授权范围。

## 更新

在工程根目录运行 `python3 scripts/build_character_lookbook.py`。生成页面和 JSON 索引；已有路径保留角色编号。新增项目在脚本 groups 中显式登记。图片继续保存在各期目录，Git 仅跟踪脚本、页面、索引和 QA；媒体单独同步到 220 并核对 SHA256。

索引：`review/character-lookbook-v1.json`；本次检查：`review/character-lookbook-v1-QA.json`。画册与原图需保持工程相对目录结构。

本次原图链接、SHA256 和 JavaScript 语法已检查；实际浏览器视觉检查因本地页面 URL 被工具安全策略拦截，仍为 pending。
