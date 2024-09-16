from .configs import lang_data, lang
from .untils import (
    is_invalid_address,
    get_message_list,
    parse_host,
    change_language_to,
    handle_exception
)
from nonebot.plugin import PluginMetadata
from zhenxun.configs.utils import PluginCdBlock, PluginExtraData, RegisterConfig
from nonebot import require
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import on_alconna, Match, UniMessage, Text
from nonebot.plugin import PluginMetadata
from arclet.alconna import Args, Alconna


__plugin_meta__ = PluginMetadata(
    name="Minecraft查服",
    description="Minecraft服务器状态查询，支持IPv6",
    usage=f"""
    Minecraft服务器状态查询，支持IPv6
    用法：
        查服 [ip]:[端口] / 查服 [ip]
        设置语言 zh-cn
        当前语言
        语言列表
    eg:
        mcheck ip:port / mcheck ip
        set_lang en
        lang_now
        lang_list
    """.strip(),
    extra=PluginExtraData(
        author="molanp",
        version="1.16",
        limits=[PluginCdBlock(result=None)],
        menu_type="一些工具",
        configs=[
            RegisterConfig(
                key="LANGUAGE",
                value="zh-cn",
                help="Change the language(zh-cn, zh-tw, en etc.)",
                default_value="zh-cn",
            ),
            RegisterConfig(
                key="type",
                value=0,
                help="结果发送类型，0为发送HTML，1为发送图片, 2为发送文本",
                default_value=0,
                type=int,
            ),
        ],
    ).dict(),
)

check = on_alconna(
    Alconna("mcheck", Args["host?", str]),
    aliases={"查服"},
    priority=5,
    block=True,
)


lang_change = on_alconna(
    Alconna("set_lang", Args["language", str]),
    aliases={"设置语言"},
    priority=5,
    block=True,
)

lang_now = on_alconna(
    Alconna("lang_now"),
    aliases={"当前语言"},
    priority=5,
    block=True,
)

lang_list = on_alconna(
    Alconna("lang_list"),
    aliases={"语言列表"},
    priority=5,
    block=True,
)


@check.handle()
async def _(host: Match[str]):
    if host.available:
        check.set_path_arg("host", host.result)


@check.got_path("host", prompt=lang_data[lang]["where_ip"])
async def handle_check(host: str):
    address, port = await parse_host(host)

    if not str(port).isdigit() or not (0 <= int(port) <= 65535):
        await check.finish(Text(f'{lang_data[lang]["where_port"]}'), reply_to=True)

    if await is_invalid_address(address):
        await check.finish(Text(f'{lang_data[lang]["where_ip"]}'), reply_to=True)

    await get_info(address, port)


async def get_info(ip, port):
    global ms

    try:
        message_list = await get_message_list(ip, port)
        if any(isinstance(i, list) for i in message_list):
            for sublist in message_list:
                await check.send(UniMessage(sublist), reply_to=True)
        else:
            await check.send(UniMessage(message_list), reply_to=True)
    except BaseException as e:
        await check.send(await handle_exception(e), reply_to=True)

@lang_change.handle()
async def _(language: str):
    if language:
        await lang_change.send(Text(await change_language_to(language)), reply_to=True)
    else:
        await lang_change.send(Text(" Language?"), reply_to=True)
@lang_now.handle()
async def _():
    await lang_now.send(Text(f'Language: {lang}.'), reply_to=True)


@lang_list.handle()
async def _():
    i = '\n'.join(list(lang_data.keys()))
    await lang_list.send(Text(f"Language List:\n{i}"), reply_to=True)
