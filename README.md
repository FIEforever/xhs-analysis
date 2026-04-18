# 小红书内容智能分析平台

> 基于 Trae SOLO + MCP 的小红书内容数据分析系统

## 功能特性

- **关键词搜索**：支持多关键词组合搜索
- **时间筛选**：7天 / 30天 / 90天
- **4维分析**：
  - 运营分析：互动量分布、发布时间热力图、标签词云、内容类型
  - 产品洞察：关键词频次、使用场景、产品形态
  - 消费者画像：情感分析、需求词/痛点词、互动偏好
  - 数据缓存：localStorage 本地缓存
- **真实数据**：通过 MCP 协议获取小红书真实笔记数据
- **演示模式**：无需网络，内置50条演示数据

## 技术栈

- HTML5 + CSS3 + JavaScript（纯前端，无框架依赖）
- Chart.js 4.4.0（可视化图表）
- Canvas API（词云手写实现）
- MCP REST API（数据来源）

## 快速开始

### 方式一：在线演示

直接访问演示地址即可体验（演示模式，无需配置）

### 方式二：本地运行

1. 克隆项目
```bash
git clone https://github.com/FIEforever/xhs-analysis.git
cd xhs-analysis
```

2. 启动本地服务器
```bash
python -m http.server 3456
```

3. 浏览器打开：http://localhost:3456

### 方式三：真实数据模式

1. 下载小红书 MCP 程序
2. 运行 `./xiaohongshu-mcp-windows-amd64.exe`
3. 浏览器访问 http://localhost:18060/health 验证
4. 打开 index.html → ⚙️ 设置 → 填入 http://localhost:18060

## 项目结构

```
├── index.html          # 主文件（完整单页应用）
├── README.md           # 项目说明
└── .gitignore          # Git忽略配置
```

## API 接口

```
健康检查：GET http://localhost:18060/health
搜索接口：GET http://localhost:18060/api/v1/feeds/search?keyword=xxx&sort=general&filter_duration=2
```

## 提效数据

| 任务 | 传统方式 | 使用本系统 |
|------|---------|-----------|
| 生成分析系统 | 3-5 天 | 30 分钟 |
| 搜索100条笔记 | 2-3 小时 | 30 秒 |
| 生成可视化图表 | 手动制作 | 自动渲染 |

## 相关项目

- [Trae SOLO](https://solo.trae.cn) - AI 编程工具
- [小红书 MCP](https://github.com/...) - 字节跳动官方 MCP 服务

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
