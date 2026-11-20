# ClassFabric 网站：设计与协作规范

所有页面改动必须遵守本文件。token 的唯一来源是 `assets/css/tokens.css`，由 `tools/lint_tokens.py` 校验。

## 1. 设计 token

| 类别 | 规则 |
|---|---|
| 主强调色 | 只有 `--accent`（深色 `--blue`，浅色 `#0a63c9`）。渐变只用于章节标题里的一个词（`.claim .g`）和首屏标题的一个词。 |
| 圆角 | 3 档：`--r-s` 4px（控件，Win11 控件圆角）、`--r-m` 8px（卡片、浮层，Win11 叠加层圆角）、`--r-l` 16px（大容器、舞台）。纯圆只用 `50%` / `999px`（圆点、胶囊）。 |
| 材质 | 依据微软官方规范与 WinUI 主题资源，**不是液态玻璃**。**Mica**：不透明基底层，壁纸只采样一次（`mica.webp`），不对页面内容做实时模糊，全站只用一次（`materials.css` 的 `html::before`）；其上用 `--card` / `--layer` 叠层，卡片 = `--card` + 1px `--stroke`。**Acrylic**：半透明（`--acrylic` + `--acrylic-blur` 30px/饱和 125% + `--noise`），只用于瞬时浮层（菜单、提示）和叠在滚动内容之上的导航；禁止叠放、禁止并排、禁止铺大面积（卡片、整块背景一律用 Mica 叠层，不得模糊）。**Smoke**：模态之下压暗，`--smoke`。关闭透明效果（`prefers-reduced-transparency`）或不支持模糊时，Acrylic 回退 `--acrylic-solid`，Mica 回退 `--mica-base`。禁止毛玻璃卡片、彩色光晕、液态玻璃。 |
| 阴影 | 只有 `--sh-1`（卡片）与 `--sh-win`（承托软件窗口）。 |
| 字号 | 5 档：`--fs-1` 13 / `--fs-2` 15 / `--fs-3` 17–21 / `--fs-4` 26–44 / `--fs-5` 40–96。复刻界面内部用 `em`。 |
| 间距 | 4/8 倍数：`--s-1`…`--s-8`（4、8、16、24、32、48、64、96）。 |
| 文字色 | `--fg`、`--muted`、`--faint`；壁纸之上用 `--on-wall*`。 |
| 动效 | 时长 `--t-base`/`--t-slow`，缓动 `--ease-out`；数字类实时读数的刷新间隔 `--tick`（2s，刻意放慢）。 |

## 2. 适用范围

- 适用：站点自身的版式（章节、卡片、按钮、文字、动效），即 `home2.css`、`dl.css`、`about.css`、`nf.css`、`modal.css`、`tokens.css`、`base.css`（按钮/徽标/折叠面板/页脚/首页首屏 `.hz`，全站共用）。基础色（`--bg/--fg/--muted/--line/--g1..g3` 等）与动效 token（`--t-*`、`--ease-*`）已统一在 `tokens.css`，不再散落在 `site.css`。
- 旧 `site.css` 现状：桌面页面渲染的非复刻元素已全部迁出（审计脚本零字面量）；仅剩手机页 `/m/` 专用的旧规则（stp4、axmap、fit2、rel、copy、thx、tu、pc、tv、blk 等）带字面量，属于遗留，改动手机页时顺手迁到 `m.css` 并换成 token，不要新增。标签页 `.n5-tx .sub-i`、`.chip` 的 token 版写在 `home2.css`（用 `:root` 前缀抬高优先级以盖过旧规则，旧规则删净后可去掉）。
- 不适用：对真实软件界面的忠实复刻（`.vwin`、`.sapp`、`.isl`、`.vtask` 内部配色与圆角）。这些数值来自真实截图，不得"优化"。复刻色集中放在 `tokens.css` 的 `--rep-*`（岛、托盘菜单的深/浅两套），壁纸偏亮时由 `wp.js` 写入 `html[data-wpi=light]` 切换；`--rep-*` 仅限复刻组件使用，站点自身 UI 不得引用。

### 动效规范（下载页起适用）

- 只动 `transform` / `opacity`（含独立的 `translate`/`scale` 属性）；不动画 `box-shadow`、`filter`、布局属性（折叠高度用 `grid-template-rows` 或 `::details-content` + `interpolate-size`）。
- 时长只用 `--t-fast` / `--t-base` / `--t-slow`（入场可用其倍数 `calc(var(--t-slow) * 2)`）；进入用 `--ease-out`，退出用 `--ease-in`。不新增曲线。
- 每个动效回答一个问题：让用户知道发生了什么（入场编排、点击反馈、选中指示）。装饰性循环动效不做。
- 全部放进 `@media(prefers-reduced-motion:no-preference)`；滚动联动放进 `@supports(animation-timeline:scroll())`；离屏/页面隐藏时暂停。
- 禁止 3D 倾斜、光斑跟随、光晕、粒子。

### 滚动与粘性（sticky）规范（桌面端，2026-11 起适用；依据 Chrome 追踪实测 + taste-skill 的 Scroll 章）

- **滚动只推动"主角时刻"**：首屏收缩成卡片、粘性面板（`.n5-pn`）、宣言逐字。其余卡片/行/块一律不在滚动时淡入、上移、错峰；不做视差漂移、滚动进度线、scroll-snap、平滑滚动库。`.rv` 在 ≥900px 下始终可见，`.in` 仍会添加，只供区块内演示动画触发。
- **粘性靠 `position:sticky` + 原生滚动**（`animation-timeline:scroll()/view()` 擦洗），不用 JS 劫持滚动。
- **被滚动时间线驱动的 `@keyframes` 只许 `transform` / `opacity`**（合成器线程）。禁止在其中动画 `clip-path`、`filter`、`background-*`、`width/height/margin`：实测把首屏 `clip-path` 换成 `transform` 后，光栅耗时从 2119ms 降到 254ms。需要"从满屏收缩成圆角卡片"时，做法见 `home2.css` 的 `hzbg`：卡片按终态尺寸静态排版（含圆角、`overflow:hidden`），起点用 `scale()`+`translateY()` 放大盖满视口。
- **滚动监听**：优先 IntersectionObserver / CSS 时间线；确需 `scroll` 事件时用 `{passive:true}`，`requestAnimationFrame` 合帧，且只在目标靠近视口时挂载，不在回调里读布局后立即写样式。
- `tools/t_scroll.py` 守护以上规则，改动首页滚动效果后必须通过。

## 3. 禁止

- **无论如何不得偏离 Fluent Design 与既定 token，不新增 token**（唯一例外：经用户明确放行的软件复刻色 `--rep-*`）。
- 新增颜色、圆角、阴影、字号档位。需要新值时，先改 `tokens.css` 并说明理由。
- 在 `home2.css` / `dl.css` / `about.css` / `nf.css` / `modal.css` 里写颜色字面量、`px` 圆角、`px` 字号、动画时长字面量（延迟除外）。
- 往 `site.css` 追加覆盖旧规则的补丁。重做某个 section，就在新文件里用新类名完整重写，并删除被取代的旧规则。
- 自绘 Windows 图标。图标只用 `assets/img/win/`（取自真实截图）与用户提供的图片。

## 4. 素材

- 开始按钮：用户提供的 `win/start.png`。其余任务栏图标：从真实 Win11 截图裁取并去底。
- 主题预览：用户提供的程序内图片 `theme-*-bar.webp`。
- 禁止虚构数据与功能；复刻界面的文字取自真实截图。

## 5. 流程

1. 一次只改一个 section，改完运行 `python3 tools/build.py` 与 `python3 tools/snap.py` 截图。
2. 对照 token 表与用户参考图逐项自检，再汇报。
3. `python3 tools/lint_tokens.py` 必须通过。
4. 版本号只在用户明确要求时修改。V1.0.6 的推送必须得到用户明确同意。
