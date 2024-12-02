# ✨ Minecraft_server_check_plugins for [zhenxun_bot](https://github.com/hibikier/zhenxun_bot)

[Nonebot Version](https://github.com/molanp/nonebot_plugin_mccheck/)

English|[简体中文](README.md)

## 🤓 If you have any good functional suggestions, please put forward them in [Issues](https://github.com/molanp/zhenxun_chafu_Minecraft/issues)

## 📈 Implemented functions

- [x] Full platform adapter support
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
- [x] Fully colored underlined/strikethrough

## 📑 Future functions

- [ ] Get server protocol number
- [ ] Get server official website (if any)
- [ ] And more...

## 🖼️ Renderings

v1.16

Text message
![1.16 text](https://github.com/user-attachments/assets/7099ded9-9c8c-482f-89e5-a68bd014e67a)

Picture message
![1.16 pic](https://github.com/user-attachments/assets/3ba422a4-bc41-4401-85c7-f5da2f693b03)

HTML message
![1.16 html](https://github.com/user-attachments/assets/09396694-16a4-4907-8b25-3863b181a725)

Geyser server double check(More than just HTML messages are supported, only one is shown here)
![1.16 geyser](https://github.com/user-attachments/assets/3982c18a-7cc5-4eb2-9f0f-9ec2a16fed2f)

## 💿 Install

  - Put `mc_check` folder in `plugins` folder or custom folder.

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

## 🎲 Comparison of message types

| Type | Special Styles | Favicon | Colored underline/strikethrough | Full Unicode font support |
|:-----:|:-----:|:-----:|:-----:|:-----:|
| Text | ❌ | ⭕ | ❌ | ⭕ |
| Picture | ⭕ | ⭕ | ⭕ | ❌ |
| HTML | ⭕ | ⭕ | ⭕ | ⭕ |

# [Download](https://github.com/molanp/zhenxun_chafu_Minecraft/releases)


## Requirement
```shell
pip install "dnspython>=2.2.1,<2.5.0"
```

## Thanks
* [minestat](https://github.com/FragLand/minestat): A multi-platform Minecraft server query module
* [@tzdtwsj](https://github.com/tzdtwsj): For the project, suggestions for image rendering function, color rendering function and implementation ideas of interoperability query scheme are proposed.
