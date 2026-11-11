# Software UI References · 软件设计参考资源库

做软件时直接可用的设计参考资源合集：UI 效果仓库、配色、字体、图标、纹理、样机、灵感站。

数据同步自 [ignoredone.space 设计导航](https://www.ignoredone.space/index.php/designwebsite/)（明日方舟美术社区出品的设计资源导航站，致谢原作者 [IgnoreDone](https://space.bilibili.com/4073074)）。

## 软件开发场景速查

| 需求 | 首选 | 说明 |
|---|---|---|
| 界面效果找实现 | [RARE UI](https://www.rareui.com/) | UI 效果 **带代码** 的仓库，可直接抄实现 |
| 响应式测试 | [Responsinator](https://gitussr.github.io/responsinator/) | 一个页面同时预览多设备，免费 |
| 配色 | [Coolors](https://coolors.co) / [Flat UI Colors](https://flatuicolors.com) | 生成器 / 现成色板 |
| 免费商用字体 | [Google Fonts](https://fonts.google.com) / [Fontshare](https://fontshare.com/) / [猫啃](https://www.maoken.com/all-fonts/)（中文） | Web 字体 / 高质量西文 / 中文开源 |
| 图标 | [iconfont](https://www.iconfont.cn/) / [iconmonstr](https://iconmonstr.com/) | 阿里矢量库 / 免费商用 |
| 网页灵感 | [Awwwards](https://www.awwwards.com/) / [CSSDA](https://www.cssdesignawards.com/) / [Dribbble](https://dribbble.com/) | 获奖站点 / 网页 UI / 移动端 |
| UI 动画灵感 | [UI Movement](https://uimovement.com) | 微交互动效展示 |
| 纹理背景 | [Pattern Monster](https://pattern.monster/) / [transparent textures](https://www.transparenttextures.com/) / [texturelabs](https://texturelabs.org/) | 无缝图案 / 透明纹理 / 材质 |
| 免费图片 | [Unsplash](https://unsplash.com) / [Pexels](https://pexels.com) / [undraw](https://undraw.co/illustrations)（矢量插画） | 摄影图 / 图+视频 / 插画 |
| 样机 | [mockups-design](https://mockups-design.com/) / [ls.graphics](https://www.ls.graphics/free-mockups) / [MockupWorld](https://www.mockupworld.co/all-mockups/) | 均免费 |

## 分类统计（共 66 条）

| 分类 | 条数 | 内容 |
|---|---|---|
| [设计工具](CATALOG.md#设计工具20-条) | 20 | 立体字/故障艺术/抖动/半调等视觉特效生成器，配色、抠图、Figma/Canva |
| [字体资源](CATALOG.md#字体资源14-条) | 14 | 下载平台 + 字体识别（求字体/识字体/Myfonts） |
| [灵感收集](CATALOG.md#灵感收集10-条) | 10 | Behance/Pinterest/站酷/花瓣，年报档案库（1945-2020）、工业蓝图库 |
| [图片素材](CATALOG.md#图片素材7-条) | 7 | 图库、矢量插画、像素画、论文图表 |
| [设计资源](CATALOG.md#设计资源8-条) | 8 | 图标库、笔刷、材质纹理、无缝图案 |
| [UI 参考](CATALOG.md#ui-参考5-条) | 5 | Awwwards/Dribbble/CSSDA/RARE UI/UI Movement |
| [样机素材](CATALOG.md#样机素材3-条) | 3 | 免费样机工程下载 |

完整清单见 **[CATALOG.md](CATALOG.md)**（自动生成，含每条的说明与备注）。

## 仓库结构

```
├── CATALOG.md        按分类的完整清单（脚本生成，勿手改）
├── data/sites.json   原始数据全字段：name/url/subtitle/categories/icon/broken/added_date
├── assets/icons/     66 个资源图标镜像（NN-slug.svg）
└── scripts/fetch.py  同步脚本
```

## 同步更新

上游导航站更新后，重新拉取最新数据与图标：

```bash
python scripts/fetch.py            # 全量同步（数据 + 图标 + CATALOG.md）
python scripts/fetch.py --skip-icons  # 只更新数据和清单
```

> 提取原理：该页面条目由前端 JS 动态渲染，普通抓取只能看到分类标签。完整数据内嵌在
> WordPress 渲染后的 HTML 中，走 `wp-json/wp/v2/pages/4730` 取 `content.rendered`
> 再正则提取 JSON 数组。注意不能在整个 API 响应上直接搜正则——响应的 `_links`
> 字段里也有 `[{"name":...}]` 结构会抢先命中。

## 数据备注

- 站方数据原样保存，未做修正或去重。
- 「抖动处理」与「多算法图像和视频抖动处理」为同址重复条目，CATALOG 已标注。
- 「Iconfinder」条目站方填写的链接实际指向 magnific.com/icons（应为作者笔误），使用时留意。
