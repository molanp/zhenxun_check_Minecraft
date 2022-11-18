# Minecraft_server_plugins.Adaptation [zhenxun_bot](https://github.com/hibikier/zhenxun_bot)
# English|[中文](https://github.com/molanp/zhenxun_chafu_Minecraft/blob/master/README.md)
## If you have any good functional suggestions, please put forward them in [Issues](https://github.com/molanp/zhenxun_chafu_Minecraft/issues)
***
## Implemented functions

- [x] Query server nickname
- [x] Query the maximum and current headcount of the server.
- [x] Query server MOTD
- [x] Query the server favicon[If it exists]
- [x] Return the server address and port.
- [x] Return the server to online status.
- [x] Query server delay
- [x] More accurate delay
- [x] UDP server support
- [x] Error feedback
- [x] Automatic port completion
- [x] Judge whether the intelligent~~amentia~~ address is correct.

## Future functions

- [ ] Get server protocol number [Implemented but undeveloped]
- [ ] Get server official website (if any)
- [ ] Get JSON of server MOTD [implemented but undeveloped]
- [ ] Add configuration file [immature technology]
- [ ] And more...

## Test screenshot

![picture](https://user-images.githubusercontent.com/104612722/201504468-d9b96fdf-fca2-4200-b740-51acfc6dff4c.jpg)

This diagram uses version v0.6↑
<!--address：https://user-images.githubusercontent.com/104612722/201504468-d9b96fdf-fca2-4200-b740-51acfc6dff4c.jpg-->

## How to use
- Install
  - Put `__init__.py` files `plugins` pp folder or custom folder.
  - If the module is missing, please execute `pip install ping3`~~(Theoretically, this module must be missing.)~~
- Use
  - 查服 [ip]:[port]  {Java}
  - b查 [ip]:[port]    {Bedrock}

# I will adapt to English commands as soon as possible.

# Download

[Download](https://github.com/molanp/zhenxun_chafu_Minecraft/releases)

# Update log
<details>
<summary>Update log</summary>

## 2022/11/14
### v0.7
Unified input format.

Optimize code logic.

Specification variable name.

The api call is restricted.

The timeout judgment is cancelled, but the response time may become longer.

If you frequently report errors, you may encounter network fluctuations (the bedrock version of the api site is unstable).Please try restarting the bot.

If there is no port (and no `:`) after `IP` is entered, the default port [25565/19132] will be used automatically.
## 2022/11/13
### v0.6-plus
README file rewriting.

Sending error messages is supported.

Support query UDP protocol server.
### v0.6[beta]
Query UDP protocol server is supported, but the command conflicts.[Repaired]
## 2022/11/12
### v0.5
README file rewriting.

Sort out the code.

More accurate server latency.
## 2022/11/09
### v0.4-fix[The first version in releases]
Rename file
### v0.4
Fix the error caused when favicon does not exist.
### v0.3
Sending favicon is supported.

More sensitive trigger mode.
## 2022/10/31
### vfix-0.2
Update usage.
## 2022/10/25
### v0.1[tag new,first version]
Support JAVA server query.

Support query server delay.
</details>
