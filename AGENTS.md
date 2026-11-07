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

- 适用：站点自身的版式（章节、卡片、按钮、文字、动效），即 `home2.css`、`modal.css`、`tokens.css`。
- 不适用：对真实软件界面的忠实复刻（`.vwin`、`.sapp`、`.isl`、`.vtask` 内部配色与圆角）。这些数值来自真实截图，不得"优化"。

## 3. 禁止

- 新增颜色、圆角、阴影、字号档位。需要新值时，先改 `tokens.css` 并说明理由。
- 在 `home2.css` / `modal.css` 里写颜色字面量、`px` 圆角、`px` 字号。
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
