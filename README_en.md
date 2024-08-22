# ✨ Minecraft_server_check_plugins for [zhenxun_bot](https://github.com/hibikier/zhenxun_bot)

[Other Version](https://github.com/molanp/nonebot_plugin_mccheck/)

English|[简体中文](README.md)

## 🤓 If you have any good functional suggestions, please put forward them in [Issues](https://github.com/molanp/zhenxun_chafu_Minecraft/issues)
***
_If you need an older version of a single file, switch to branch `old`_
***
## 📈 Implemented functions

- [x] Adapted unicode full fonts and glyphs
- [x] Render Motd styles
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

## 📑 Future functions

- [ ] Get server protocol number
- [ ] Get server official website (if any)
- [ ] And more...

## 🖼️ Renderings

v1.9

Picture Message
![1.9 pic](https://github.com/user-attachments/assets/abcda34f-0783-4c1e-b5c1-de9228047a69)

HTML Message
![1.9 html](https://github.com/user-attachments/assets/18069f2a-4f7e-4994-837b-2b9e0cbf1f74)

## 💿 Install

  - Put `mc_check` folder in `extensive_plugin` folder or custom folder.

## 🎉 Usage

| Command | Parameter | Scope | Description |
|:-------:|:---------:|:-----:|:-----------:|
| `mcheck` | `[ip]:[port]` or `[ip]` | Private/Group Chat | Check Minecraft server status |
| `set_lang` | Language name | Private/Group Chat | Set the language used by the plugin for rendering images |
| `lang_now` | None | Private/Group Chat | View the current language used by the plugin for rendering images |
| `lang_list` | None | Private/Group Chat | View the list of languages supported by the plugin |

## ⚙️ Configuration

| Configuration Item | Required | Default Value | Description |
|:-----:|:----:|:----:|:----:|
| `language` | False | `zh-cn` | Languages used by the plugin to render images<br>Available languages: [`zh-cn`,`zh-tw`,`en`] |
| `type` | False | `0` | The type of message the plugin sends (`0` for HTML, `1` for image, `2` for text) |


# [Download](https://github.com/molanp/zhenxun_chafu_Minecraft/releases)

# Update log
<details>
<summary>Update log</summary>

## 2024/08/22

Added html rendering, adapted unicode full fonts and glyphs


## 2024/08/21-22

refactor(mc_check): optimize untils function and refactor network calls

Remove useless dependencies

Render colored characters in Version

## 2024/08/14
### v1.8

Fully adapted to dev Zhenxun Bot, migrate the plugin configuration to `PluginMetadata`

Format the code to increase readability

## 2024/08/12

Adapt to the dev version of Zhenxun Bot.

## 2023/11/01
### v1.5
fix SRV resolver

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
pip install "dnspython>=2.2.1,<2.5.0"
```

# Thanks
[minestat] (https://github.com/FragLand/minestat): A multi-platform Minecraft server query module
