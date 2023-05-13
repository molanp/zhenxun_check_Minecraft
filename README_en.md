# Minecraft_server_check_plugins for [zhenxun_bot](https://github.com/hibikier/zhenxun_bot)

English|[简体中文](https://github.com/molanp/zhenxun_chafu_Minecraft/blob/main/README.md)

## If you have any good functional suggestions, please put forward them in [Issues](https://github.com/molanp/zhenxun_chafu_Minecraft/issues)
***
## If you need an older version of a single file, switch to branch `old`
***
## Implemented functions

- [x] Query server nickname
- [x] Query the maximum number of servers, the current number of people
- [x] Query server motd
- [x] returns the server address and port
- [x] Returns the server online status
- [x] Query server latency
- [x] More precise delay
- [x] UDP server is supported
- [x] Error message feedback
- [x] Port autocompletion
- [x] Wisdom~~Barrier~~ can determine whether the IP address is correct
- [x] Get the JSON version of the server motd (only if the server motd is set to JSON format)
- [x] Does not depend on any external API :)
- [x] Support special port queries (e.g. `2`, `80`, `443` etc.)
- [x] Query server favicon
- [x] Multilingual
- [x] SRV support 

## Future functions

- [ ] Get server protocol number
- [ ] Get server official website (if any)
- [ ] And more...

## Test screenshot

![picture](https://user-images.githubusercontent.com/104612722/210684756-883da1c2-44a5-4119-8c50-647a527aa68f.png)

This diagram uses version v0.9↑
<!--address：https://user-images.githubusercontent.com/104612722/210684756-883da1c2-44a5-4119-8c50-647a527aa68f.png-->

## How to use
- Install
  - Put `mc_check` folder in `extensive_plugin` folder or custom folder.
- Use
  - minecheck [ip]:[port]
  - lang_now (view current output language)
  - set_lang [Language] (set output language)

# [Download](https://github.com/molanp/zhenxun_chafu_Minecraft/releases)

# Update log
<details>
<summary>Update log</summary>

## 2023/02/22
### v1.3
[add support for the Query / GamSpot4 / UT3 protocol](https://github.com/FragLand/minestat/pull/166)
  
## 2023/02/05
### v1.2
SRV support

## 2023/01/14
### v1.1
The socket return value is fault-tolerant
Multilingual file configuration

## 2023/01/12
Sending favicon is supported.

## 2023/01/08
### v1.0
Remove external dependencies and use local dependencies
No longer rely on external API.

## 2023/01/05
### v0.9
Change the command trigger rule, and prompt for input when there are no parameters.

## 2022/12/26
### v0.8
Change the bedrock version to use the Chinese API source

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

# depend
```powershell
pip install dnspython
```

# Thanks
[minestat] (https://github.com/FragLand/minestat): A multi-platform Minecraft server query module
