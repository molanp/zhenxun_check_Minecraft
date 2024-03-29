# 我的世界服务器状态查询插件，适配[zhenxun_bot](https://github.com/hibikier/zhenxun_bot)

简体中文|[English](README_en.md)

# 注意，请确保插件文件夹名字为`mc_check`，否则无法获取配置信息

## 若有什么好的功能建议，欢迎在[Issues](https://github.com/molanp/zhenxun_chafu_Minecraft/issues)中提出
***
## 如果你需要单文件的旧版本，请切换到分支`old`
***
## 已实现的功能

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

![测试截图](https://user-images.githubusercontent.com/104612722/210684756-883da1c2-44a5-4119-8c50-647a527aa68f.png)

此图使用v0.9版本↑
<!--图片地址：https://user-images.githubusercontent.com/104612722/210684756-883da1c2-44a5-4119-8c50-647a527aa68f.png-->

## 使用方法
- 安装
  - 将`mc_check`文件夹放入`extensive_plugin`文件夹或自定义文件夹内
- 使用
  - 查服 [ip]:[port]
  - 显示语言 (查看当前输出语言)
  - 设置语言 [Language] (设置输出语言)

# [下载地址](https://github.com/molanp/zhenxun_chafu_Minecraft/releases)

# 更新日志
<details>
<summary>更新日志</summary>

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
pip install "dnspython>=2.2.1,<2.5.0"
```

# 感谢
[minestat](https://github.com/FragLand/minestat): 一个多平台语言的我的世界服务器查询模块
