# 我的世界服务器状态查询插件，适配[zhenxun_bot](https://github.com/hibikier/zhenxun_bot)

[Other Version](https://github.com/molanp/nonebot_plugin_mccheck/)

简体中文|[English](README_en.md)

# 注意，请确保插件文件夹名字为`mc_check`，否则无法获取配置信息

## 若有什么好的功能建议，欢迎在[Issues](https://github.com/molanp/zhenxun_chafu_Minecraft/issues)中提出
***
_如果你需要单文件的旧版本，请切换到分支`old`_
***
## 已实现的功能

- [x] 适配Unicode全字体与字形
- [x] 渲染Motd样式
- [x] 查询服务器昵称
- [x] 查询服务器最大人数,当前人数
- [x] 查询服务器motd
- [x] 返回服务器地址及端口
- [x] 返回服务器在线状态
- [x] 查询服务器延迟
- [x] 更精确的延迟
- [x] 支持UDP服务器
- [x] 错误信息反馈
- [x] 端口自动补全
- [x] 智~~障~~能判断IP地址是否正确
- [x] 获取服务器motd的json版本(仅当服务器motd设置为json格式时)
- [x] 不依赖任何外部api
- [x] 支持特殊端口查询(如`2`,`80`,`443`等)
- [x] 查询服务器favicon
- [x] 多语言
- [x] SRV支持

## 未来的功能

- [ ] 获取服务器协议号
- [ ] 获取服务器官网[如果存在]
- [ ] 敬请期待

## 测试截图

v1.9

图片消息
![1.9 pic](https://github.com/user-attachments/assets/abcda34f-0783-4c1e-b5c1-de9228047a69)

HTML消息
![1.9 html](https://github.com/user-attachments/assets/d0ecffa1-672d-4936-a404-2e12e964ec1e)

## 安装
  - 将`mc_check`文件夹放入`extensive_plugin`文件夹或自定义文件夹内

## 🎉 使用
| 命令 | 参数 | 范围 | 说明 |
|:---:|:---:|:---:|:---:|
| `查服` | `[ip]:[端口]` 或 `[ip]` | 私聊/群聊 | 查询Minecraft服务器状态 |
| `设置语言` | 语言名称 | 私聊/群聊 | 设置插件渲染图片所使用的语言 |
| `当前语言` | 无 | 私聊/群聊 | 查看当前插件渲染图片所使用的语言 |
| `语言列表` | 无 | 私聊/群聊 | 查看插件支持的语言列表 |

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| `language` | 否 | `zh-cn` | 插件渲染图片所使用的语言<br>可用语言:[`zh-cn`,`zh-tw`,`en`] |
| `type` | 否 | `0` | 插件发送的消息类型(`0`为HTML, `1`为图片, `2`为文本) |

# [下载地址](https://github.com/molanp/zhenxun_chafu_Minecraft/releases)

# 更新日志
<details>
<summary>更新日志</summary>

## 2024/08/22

新增html渲染，适配unicode全字体与字形

## 2024/08/21-22

refactor(mc_check): 优化untils函数并重构网络调用

删除无用依赖

渲染Version中的彩色字符

## 2024/08/14
### v1.8

完全适配dev真寻，迁移插件配置至`PluginMetadata`

格式化代码，增加可读性

## 2024/08/12

适配dev版本真寻

## 2023/11/01
### v1.5
修复SRV解析

## 2023/02/22
### v1.3
[添加对Query / GamSpot4 / UT3协议的支持](https://github.com/FragLand/minestat/pull/166)

## 2023/02/05
### v1.2
SRV解析支持

## 2023/01/14
### v1.1
socket返回值进行容错处理
多语言文件配置

## 2023/01/12
支持发送favicon

## 2023/01/08
### v1.0
删除外置依赖，使用本地依赖
不再依赖外部api

## 2023/01/05
### v0.9
更改命令触发规则，无参数时提示输入

## 2022/12/26
### v0.8
更换基岩版查服api，使用国内api源

## 2022/11/14
### v0.7
统一输入格式

优化代码逻辑

规范变量名

对api调用进行限制

取消了超时判断，但可能会造成响应时间变长

若频繁报错则可能遇到了网络波动(基岩版查服api站点不稳定)，请尝试重启bot

输入时若`ip`后若无端口(且无`:`)，自动使用默认端口[25565/19132]
## 2022/11/13
### v0.6-plus
支持发送错误信息

支持查询UDP协议服务器
### v0.6[beta内部测试]
支持查询UDP服务器,但命令冲突[已修复]
## 2022/11/12
### v0.5
更精确的服务器延迟
## 2022/11/09
### v0.4-fix[releases中第一个版本]
重命名文件
### v0.4
修复favicon不存在造成的消息发送失败问题
### v0.3
支持发送favicon

更灵敏的触发
## 2022/10/31
### vfix-0.2
更新usage
## 2022/10/25
### v0.1[标签new,初版本]
支持查询JAVA服务器

支持发送延迟

</details>

# 依赖
```powershell
pip install dnspython
```

# 感谢
[minestat](https://github.com/FragLand/minestat): 一个多平台语言的我的世界服务器查询模块
