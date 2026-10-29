# ClassFabric 官网

ClassFabric（ClassIsland 个人修改版）的官方网站源码。纯静态站点：HTML + CSS + 原生 JS，**没有构建依赖**，不需要 `npm install`。

## 目录

| 路径 | 说明 |
| --- | --- |
| `index.html` / `download.html` / `about.html` | 首页、下载页、关于页（由 `tools/build.py` 生成，已提交） |
| `assets/css/site.css` | 全站样式，含亮/暗主题（跟随系统，也可手动切换） |
| `assets/js/site.js` | 灵动岛演示（滚动到可见区域才播放）、GitHub Release 自动填充、语言切换（translate.js，按需加载） |
| `assets/img/` | 真实软件截图（WebP）、壁纸、Logo、OG 图 |
| `tools/build.py` | 页面生成脚本：改文案/结构请改它，然后 `python3 tools/build.py` |

## 本地预览

```bash
python3 -m http.server 8080   # 在仓库根目录执行，然后打开 http://localhost:8080
```

页面里的资源路径是以 `/` 开头的绝对路径，所以必须从**域名根目录**提供服务（不要直接双击打开 html 文件，也不要放在子目录下）。

## 部署（1Panel）

1. 在 1Panel 创建一个「静态网站」，网站根目录指向本仓库所在目录。
2. 绑定域名 `ansoukin.top`，开启 HTTPS。
3. 保持同步：在服务器上 `git pull`（可用 1Panel 计划任务每分钟/每几分钟执行一次，或用 GitHub Webhook 触发）。

## 数据来源

- 下载页和首页的版本号、下载文件列表在浏览器里实时读取 `https://api.github.com/repos/Ansoukin/ClassFabric/releases`，读取失败时按钮会回退到 GitHub Releases 页面。
- 多语言使用 [translate.js](https://github.com/xnx3/translate)，用户切换语言时才从 CDN 加载，默认简体中文不依赖任何外部脚本。

## 许可

站点内的软件截图来自 ClassFabric 2.1.1.3。ClassFabric 基于 HelloWRC 的 ClassIsland，以 GPL-3.0 协议开源。
