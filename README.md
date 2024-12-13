# ✨ 我的世界服务器状态查询插件，适配[zhenxun_bot](https://github.com/hibikier/zhenxun_bot)

[Nonebot Version](https://github.com/molanp/nonebot_plugin_mccheck/)

简体中文|[English](README_en.md)

## 🤔 若有什么好的功能建议，欢迎在[Issues](https://github.com/molanp/zhenxun_chafu_Minecraft/issues)中提出

## 📈 已实现的功能

- [x] 支持全平台适配器
- [x] 适配Unicode全字体与字形
- [x] 渲染Motd样式
- [x] 查询服务器昵称
- [x] 查询服务器最大人数,当前人数
- [x] 查询服务器motd
- [x] 返回服务器地址及端口
- [x] 返回服务器在线状态
- [x] 查询服务器延迟
- [x] 更精确的延迟
- [x] 支持互通服务器双次查询
- [x] 错误信息反馈
- [x] 端口自动补全
- [x] 智能判断IP地址是否正确
- [x] 不依赖任何外部api
- [x] 支持特殊端口查询(如`2`,`80`,`443`等)
- [x] 查询服务器favicon
- [x] 多语言
- [x] SRV支持
- [x] 完全彩色下划线/删除线
- [x] 获取服务器协议号

## 📑 未来的功能

- [ ] 敬请期待

## 🖼️ 效果图

v1.22

![v1.22](https://github.com/user-attachments/assets/fb4bf897-0b06-4f97-91f8-3fd81f741ab3)


## 💿 安装

### 快捷安装
  - 使用命令`添加插件 mc_check`快速安装
  - 使用命令`更新插件 mc_check`快速更新插件

### 手动安装
  - 将`mc_check`文件夹放入`plugins`文件夹或自定义文件夹内


## 🎉 使用

| 命令 | 参数 | 范围 | 说明 |
|:---:|:---:|:---:|:---:|
| `查服` | `[ip]:[端口]` 或 `[ip]` | 私聊/群聊 | 查询Minecraft服务器状态 |
| `设置语言` | 语言名称 | 私聊/群聊 | 设置插件渲染图片所使用的语言 |
| `当前语言` | 无 | 私聊/群聊 | 查看当前插件渲染图片所使用的语言 |
| `语言列表` | 无 | 私聊/群聊 | 查看插件支持的语言列表 |

## ⚙️ 配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| `language` | 否 | `zh-cn` | 插件渲染图片所使用的语言<br>可用语言:[`zh-cn`,`zh-tw`,`en`] |
| `type` | 否 | `0` | 插件发送的消息类型(`0`为HTML渲染图片, `1`为图片, `2`为普通文本) |

## 🎲 消息类型对比

| 类型 | 特殊样式 | Favicon | 彩色下划线/删除线 | 全Unicode字体支持 |
|:-----:|:-----:|:-----:|:-----:|:-----:|
| 文本 | ❌ | ⭕ | ❌ | ⭕ |
| 图片 | ⭕ | ⭕ | ⭕ | ❌ |
| HTML | ⭕ | ⭕ | ⭕ | ⭕ |

# [下载地址](https://github.com/molanp/zhenxun_chafu_Minecraft/releases)


##  依赖
```shell
pip install dnspython
```

## 感谢
* [minestat](https://github.com/FragLand/minestat): 一个多平台语言的我的世界服务器查询模块
* [@tzdtwsj](https://github.com/tzdtwsj): 为该项目提出了图片渲染功能、颜色渲染功能建议和互通服查询方案实现思路等贡献
