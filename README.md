# 我的世界服务器状态查询插件，适配真寻bot
## 若有什么好的功能建议，欢迎在[Issues](https://github.com/YiRanEL/zhenxun_chafu_Minecraft/issues)中提出
***
## 已实现的功能

- [x] 查询服务器昵称
- [x] 查询服务器最大人数,当前人数
- [x] 查询服务器motd
- [x] 查询服务器favicon[无则不发送]
- [x] 返回服务器地址及端口
- [x] 返回服务器在线状态
- [x] 查询服务器延迟
- [x] 更精确的延迟
- [x] 整理了~~屎山~~代码
- [x] 错误信息反馈

## 未来的功能

- [ ] 获取服务器协议号[没什么用，未开发]
- [ ] 获取服务器官网[如果存在]
- [ ] 获取服务器motd的json版本[已实现但未启用]
- [ ] 添加配置文件
- [ ] 敬请期待

## 测试截图

![测试截图](https://user-images.githubusercontent.com/104612722/201504468-d9b96fdf-fca2-4200-b740-51acfc6dff4c.jpg)

此图使用v0.6版本↑
<!--图片地址：https://user-images.githubusercontent.com/104612722/201504468-d9b96fdf-fca2-4200-b740-51acfc6dff4c.jpg-->

## 使用方法
- 安装
  - 将`chafu`文件夹放入`plugins`文件夹或自定义文件夹内
  - 若提示缺少依赖，请执行`pip install ping3`~~(理论上来说必定缺少此模块)~~
- 使用
  - 查服 [ip]?[port]

# 下载地址

## 建议直接copy源码，releases内更新不及时
[下载地址](https://github.com/YiRanEL/zhenxun_chafu_Minecraft/releases)

# 更新日志
<details>
<summary>更新日志</summary>

## 2022/11/13
### v0.6
README文件重编写
支持发送错误信息
## 2022/11/12
### v0.5
README文件重编写
整理了代码
更精确的服务器延迟[使用ping服务]
## 2022/11/09
### v0.4-fix[releases中第一个版本]
重命名文件[错误的文件名]
### v0.4
修复favicon不存在造成的消息发送失败问题
### v0.3
编写readme文件
支持发送favicon
## 2022/10/31
### vfix-0.2
更新usage
## 2022/10/25
### v0.1
支持发送服务器各个信息(favicon除外)
支持发送延迟[实际上是api处理响应时间，不精确]

</details>
