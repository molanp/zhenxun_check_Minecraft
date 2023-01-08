# Minecraft_server_plugins.Adaptation [zhenxun_bot](https://github.com/hibikier/zhenxun_bot)
# English|[中文](https://github.com/molanp/zhenxun_chafu_Minecraft/blob/master/README.md)
## If you have any good functional suggestions, please put forward them in [Issues](https://github.com/molanp/zhenxun_chafu_Minecraft/issues)
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

## Future functions

- [ ] Get server protocol number
- [ ] Get server official website (if any)
- [ ] Add configuration file
- [ ] Query server favicon (waiting for package update)
- [ ] And more...

## Test screenshot

![picture](https://user-images.githubusercontent.com/104612722/210684756-883da1c2-44a5-4119-8c50-647a527aa68f.png)

This diagram uses version v0.9↑
<!--address：https://user-images.githubusercontent.com/104612722/210684756-883da1c2-44a5-4119-8c50-647a527aa68f.png-->

## How to use
- Install
  - Put `__init__.py` files `plugins` pp folder or custom folder.
- Use
  - minecheck [ip]:[port]

# I will adapt to English commands as soon as possible.

# Download

[Download](https://github.com/molanp/zhenxun_chafu_Minecraft/releases)

# Update log
<details>
<summary>Update log</summary>

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

# Thanks
[minestat] (https://github.com/FragLand/minestat): A multi-platform Minecraft server query module