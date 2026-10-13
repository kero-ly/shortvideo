# 视频工厂技能分层实施计划

依据：用户批准统一入口、制作方法、风格组合、共用能力、项目锁定配置的架构。直接实施，保留历史案例与旧入口。

1. 建立video-production总入口、character-scenario方法、caption-alignment和video-qa能力；原2d-scenario-explainer作为兼容入口，迁移已有参考规范到实际所属技能。
2. 分离visual/layout/audio/format配置，生成两个版本化preset与registry；保留旧风格JSON为历史快照，禁止两套默认配置分别维护。
3. 建立项目production-plan JSON Schema与可复制模板；记录选择依据、版本、覆盖项、逐镜方法、工具实测状态和审批。系列配置只提供模板，不默认将上期风格设为全局默认。
4. 更新发现入口与工作流说明；验证skill格式、JSON引用、schema模板和旧路径兼容性；用新主题与字幕修订场景只读验证，不调用生产模型。
5. 本地Git提交，220检查状态后按sync分支快进同步；连接问题即时报告。

验收：主题可路由到具体方法和预设；不凭主题锁定画风；已有明确授权不重复审批；媒体不进Git；没有把规范声明为已实现调度器。
