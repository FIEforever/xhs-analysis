# 单文件部署到 Vercel

## 方法一：Vercel CLI（推荐，最快）

### 第一步：安装 Vercel CLI
```powershell
npm install -g vercel
```

### 第二步：部署
```powershell
cd d:/F/NW/小红书

# 第一次部署需要登录，按提示操作
vercel

# 或者直接指定目录部署
vercel --yes
```

### 第三步：回答问题
```
? Set up and deploy? … Yes
? Which scope? … 选择你的账号
? Link to existing project? … No
? Project name? … xhs-analysis（随便起名）
? Directory? … ./
? Override settings? … No
```

### 第四步：等待部署
看到 `Ready!` 就成功了，会显示你的 URL，类似：
```
https://xhs-analysis-xxx.vercel.app
```

---

## 方法二：拖拽部署（最简单）

1. 打开 https://vercel.com/new
2. 登录账号
3. 看到 "Import Project" 页面
4. 选择 **"Or drop a folder here"**（拖拽文件夹）
5. 把 `d:/F/NW/小红书` 文件夹拖进去
6. 等待部署完成
7. 获得 URL

---

## 方法三：GitHub + Vercel（推荐长期）

### 第一步：创建 GitHub 仓库
1. 打开 https://github.com/new
2. 仓库名：`xhs-analysis`
3. 不要勾选 README
4. 创建空仓库

### 第二步：上传 index.html
```powershell
cd d:/F/NW/小红书
git init
git add index.html
git commit -m "小红书内容分析平台"
git branch -M main
git remote add origin https://github.com/你的用户名/xhs-analysis.git
git push -u origin main
```

### 第三步：Vercel 导入
1. 打开 https://vercel.com/new
2. Import Git Repository
3. 选择刚创建的 GitHub 仓库
4. Deploy

---

## 验证部署成功

部署完成后，打开显示的 URL，确认：
- 页面能正常加载
- 演示数据正常显示
- Tab 切换正常

把这个 URL 填入 Demo Wall 的"项目链接"字段。

---

## 常见问题

| 问题 | 解决 |
|------|------|
| Vercel 需要注册吗？ | 需要，免费，用邮箱注册 |
| 部署收费吗？ | 免费， hobby plan 足够 |
| URL 永久有效吗？ | 免费版 inactive 30天后会休眠，但提交作品够了 |
| 能否自定义域名？ | 可以，但需要额外配置 |
