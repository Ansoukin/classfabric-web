# ClassFabric 官网

[ClassFabric](https://github.com/Ansoukin/ClassFabric)（ClassIsland 的个人修改版）的官方网站源码，部署在 [ansoukin.top](https://ansoukin.top)。

纯静态站点：HTML + CSS + 原生 JS，**没有运行时依赖，不需要 `npm install`**。页面由 `tools/build.py` 生成，生成结果已提交，服务器上只需 `git pull`。

**当前站点版本：V1.0.8（2026-11-16）**

## 页面

| 页面 | 说明 |
| --- | --- |
| `/`（`index.html`） | 首页：可交互的 Windows 桌面演示（灵动岛、托盘菜单、软件窗口）、特性区块、常见问题 |
| `/download.html` | 下载页：实时读取 GitHub Releases，自动识别系统与架构；顶部为桌面场景舞台 |
| `/about.html` | 关于页：与 ClassIsland 的关系、如何切换、适合谁、进展、名字由来、常见问题 |
| `/m/` | 手机版首页。手机 UA 访问 `/` 时自动跳转，可用 `?view=pc` / `?view=m` 手动切换并记住 |

## 目录

```
index.html  download.html  about.html  m/       生成的页面（不要手改，改 tools/build.py）
assets/
  css/
    tokens.css       设计 token 的唯一来源（颜色、圆角、字号、间距、动效、材质）
    materials.css    Mica / Acrylic 材质与「降低透明度」回退
    nav.css          顶栏
    home2.css        首页区块
    dl.css           下载页
    about.css        关于页
    modal.css        对话框
    bento.css  display.css  m.css   手机首页与共用的大字区块
    site.css         历史共用样式与软件界面复刻（.isl / .tmenu / .vtask / 软件窗口），逐步清理中
  js/
    site.js          主题切换、导航、灵动岛演示循环、共用的 SelectorBar 指示条（window.cfBar）
    wp.js            壁纸随机（构建时内联到 <head>，见下）
    fx.js            入场动画、标题逐字、屏幕外动画暂停
    home.js  apps.js  widgets.js  bento.js   首页演示与可交互的软件窗口复刻
    dl.js            下载页：GitHub Releases、平台识别、舞台事件
    about.js         关于页：滚动联动的目录
    m.js             手机首页
  img/
    *.webp / *.png   软件截图、Logo、OG 图
    wp/              壁纸（每张两个尺寸：舞台用 1280 宽，首页用 2400 宽）
    win/             Windows 图标，取自真实截图
tools/
  build.py           页面生成脚本
  ui.py ui2.py ui3.py ui4.py   软件界面复刻的 HTML 生成（灵动岛、托盘菜单、设置、档案编辑……）
  lint_tokens.py     token 校验
  t_*.py             Playwright 回归测试
AGENTS.md            设计与协作规范
```

## 本地开发

```bash
python3 tools/build.py          # 重新生成页面；改文案、结构、复刻界面都改 tools/ 下的脚本
python3 tools/lint_tokens.py    # 必须输出 OK
python3 -m http.server 8080     # 在仓库根目录预览：http://localhost:8080
```

页面里的资源路径是以 `/` 开头的绝对路径，必须从**域名根目录**提供服务：不要双击打开 html，也不要放在子目录下。

`build.py` 会重写 `sitemap.xml`；只改样式或脚本时，用 `git checkout -- sitemap.xml` 还原即可。样式与脚本的 `?v=` 参数来自文件内容哈希，改了文件就会自动换新，不需要手动改缓存参数。

## 测试

回归测试基于 [Playwright](https://playwright.dev/python/)（`pip install playwright && playwright install chromium`），脚本自带本地服务器，直接运行：

```bash
python3 tools/t_wp.py   # 壁纸随机：时间段、不连续重复、各页面接入
python3 tools/t_dl3.py  # 下载页：舞台事件、点击下载、手机适配、减少动态
python3 tools/t_ab.py   # 关于页：锚点、滚动联动、溢出、CLS
python3 tools/t_contrast.py about dark 1440   # 对比度，只输出不达标项
```

## 设计规范

所有改动必须遵守 [AGENTS.md](AGENTS.md)。要点：

- 只使用 `tokens.css` 里已定的 token，**不新增 token，不写颜色/圆角/字号/时长字面量**；`lint_tokens.py` 负责校验。
- 材质依据 Windows 11 的 Mica / Acrylic，卡片为 `--card` + 1px `--stroke`；没有玻璃拟态、发光和渐变装饰。
- 对真实软件界面的复刻（灵动岛、托盘菜单、软件窗口）数值取自实机截图，不得「优化」；它们的深浅色皮肤集中在 `tokens.css` 的 `--rep-*`。
- 不虚构数据，Windows 图标只用 `assets/img/win/`。

## 壁纸随机

下载页舞台与首页的壁纸由 `assets/js/wp.js` 在每次加载时选择：

1. 先随机选一种方式：**跟随本地时间**，或**纯随机**；
2. 再从对应的池里随机选一张，且不与上一次相同。

每张壁纸按画面标注适合的时段（白天 / 晨昏 / 夜晚）；本地时间 07–17 点为白天，05–07 与 17–19 点为晨昏，其余为夜晚。壁纸偏亮时，灵动岛与托盘菜单会切换为浅色皮肤。新增壁纸：放入 `assets/img/wp/`（`名称.webp` 与 `名称-l.webp`），并在 `wp.js` 里登记时段与深浅。

## 数据来源

- 版本号、发布日期与下载文件列表：浏览器实时读取 GitHub Releases（`api.github.com/repos/Ansoukin/ClassFabric/releases`），本地缓存 1 小时；读取失败时回退到 GitHub Releases 页面。
- 灵动岛演示里的课表是一份固定的示例课表，按访客本机时间推演上课状态，不读取任何个人数据。
- 站点不使用统计脚本，也不加载任何外部 JS；仅个别插件图标引用 jsDelivr 上的上游仓库图片。

## 版本与发布

站点版本号与发布日期定义在 `tools/build.py` 的 `SITE_VER` 与 `RELEASE_DATE`，显示在页脚。只在明确要求发版时修改。

## 部署（1Panel）

1. 在 1Panel 创建「静态网站」，网站根目录指向本仓库目录；
2. 绑定域名 `ansoukin.top`，开启 HTTPS；
3. 保持同步：在服务器上 `git pull`（用 1Panel 计划任务定时执行，或用 GitHub Webhook 触发）。

## 许可

ClassFabric 基于 HelloWRC 的 ClassIsland，以 GPL-3.0 协议开源。站点中的软件截图来自 ClassFabric 2.1.1.3；壁纸为 Windows 11 自带壁纸，版权归微软所有，仅用于展示软件界面。
