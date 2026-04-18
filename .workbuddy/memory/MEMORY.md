# 项目记忆 - 小红书内容分析系统

## 项目概述
工作空间：`d:/F/NW/小红书`
主文件：`d:/F/NW/小红书/index.html`

## 核心功能
- 关键词搜索（支持多关键词，回车添加）
- 时间段筛选（7天/30天/90天）
- 获取数量（50条/100条/200条）
- 笔记列表显示封面图
- 通过 REST API（http://localhost:18060/api/v1/feeds/search）获取真实笔记数据
- MCP 离线时自动切换为演示数据模式
- 笔记列表含可点击跳转链接（https://www.xiaohongshu.com/explore/{id}?xsec_token=...）
- 分析模块（「运营分析」Tab）：互动率分布图、发布时段热力、热门标签云、内容类型分布、智能运营洞察
- 产品洞察模块（「产品洞察」Tab）：
  - 产品形态关键词TOP20词频排名
  - 核心卖点短语高频词云
  - 互动量热度分布图（独立Canvas：engDistChart）
  - 使用场景提取（10种场景模式匹配）
  - 产品开发洞察简报（自动生成+可导出TXT）
- 消费者洞察模块（「消费者」Tab）：
  - 情感观点分布（正/负/中性占比+代表笔记）
  - 热点主题聚类（6大主题：品牌营销/DIY创意/收藏打卡/礼物/旅行文创/家居）
  - 用户画像（内容偏好/地域分布10城市/互动层次）
  - 需求与痛点（需求词+痛点词双列对比）
  - 互动行为偏好（雷达图 Canvas：behaviorChart）
  - 消费者洞察简报（自动生成+可导出TXT）
- 场景分析模块（「场景」Tab，2026-03-31新增）：
  - 热门地点TOP10（基于城市/景点关键词匹配）
  - 体验类型分布（美食探店/景点打卡/住宿体验/购物分享/活动参与）
- 竞品分析模块（「竞品」Tab，2026-03-31新增）：
  - 竞品提及分析（支持苹果/华为/小米/耐克/阿迪/雅诗兰黛/兰蔻等品牌）
  - 品牌口碑概览（正面/负面提及统计、口碑指数）
- 数据本地缓存：
  - localStorage缓存，有效期24小时
  - 按关键词+时间段+数量独立缓存
  - 支持缓存管理面板（查看/使用/清理/清空）
  - 搜索前自动检测缓存，提示用户选择
- 数据导出：CSV / JSON / 产品洞察简报TXT / 消费者洞察简报TXT

## 关键词智能检测与动态维度（2026-03-31新增）
- 自动检测关键词类型：品牌词/产品词/场景词/通用词
- 根据类型动态显示/隐藏分析Tab：
  - 品牌词：显示运营+消费者+竞品（隐藏产品）
  - 产品词：显示运营+产品+消费者（隐藏竞品/场景）
  - 场景词：显示运营+消费者+场景（隐藏产品/竞品）
  - 通用词：显示运营+产品+消费者（隐藏竞品/场景）
- 各维度分析内容根据关键词类型调整侧重点

## 技术栈
- 纯 HTML + CSS + JavaScript（无框架依赖）
- Chart.js 4.4.0（CDN引入）用于图表
- 调用 REST API `/api/v1/feeds/search?keyword=xxx`（MCP 协议有 bug，改用 REST）

## MCP 服务接口（实际用 REST API）
- 服务地址：`http://localhost:18060`（可在界面配置，填写 /mcp 后缀）
- REST API：`GET /api/v1/feeds/search?keyword=xxx&sort=general&filter_duration=2`
- 健康检查：`GET /health` → `{"success":true,"data":{"status":"healthy"}}`
- 真实数据结构（驼峰命名）：`feeds[].{ id, xsecToken, noteCard.{ type, displayTitle, user.{nickname}, interactInfo.{likedCount,collectedCount,commentCount}, cover.{urlDefault,urlPre} } }`
- 爬取耗时约 20~30 秒，前端超时设置 60s

## 已知问题与修复
- MCP 协议 `/mcp` 端点有 session bug（initialize 后仍报 invalid），改用 REST API
- 服务端爬取超时会 panic 返回 500（`context canceled`）→ 前端已处理，提示重试
- 字段名是驼峰（noteCard/displayTitle/likedCount），已在 normalizeNotes 中正确处理
- 超时时间：前端 60s（服务端爬取需 20~30s）
- 2026-03-31 修复API数据解析逻辑，增强调试日志
- 2026-03-31 15:10修改：时间段7天/30天/90天，数量50/100/200，显示笔记封面图，调整布局为分析在上笔记在下

## 本地预览
- Python HTTP 服务：`python -m http.server 3456 --directory "d:/F/NW/小红书"`
- 访问：http://localhost:3456/index.html
- MCP 服务启动：`cd d:/F/NW/小红书 && ./xiaohongshu-mcp-windows-amd64.exe`
