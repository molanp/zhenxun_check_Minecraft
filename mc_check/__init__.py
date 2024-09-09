import base64
import sys
import traceback
import os
from .untils import (
    is_invalid_address,
    ColoredTextImage,
    parse_motd,
    parse_motd_to_html,
    readInfo,
    get_mc,
    parse_host,
    resolve_srv
)
from zhenxun.services.log import logger
from nonebot.plugin import PluginMetadata
from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginCdBlock, PluginExtraData, RegisterConfig
from nonebot import require
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import on_alconna, Match, UniMessage, Text, Image
from nonebot.plugin import PluginMetadata
from nonebot.exception import FinishedException
from arclet.alconna import (
    Args,
    Alconna,
)


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
        version="1.14",
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

message_type = Config.get_config("mc_check", "type", 0)
lang = Config.get_config("mc_check", "LANGUAGE", "zh-cn")
lang_data = readInfo("language.json")

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
        await check.finish(Text(f' {lang_data[lang]["where_port"]}'), reply_to=True)

    if await is_invalid_address(address):
        await check.finish(Text(f' {lang_data[lang]["where_ip"]}'), reply_to=True)

    await get_info(address, port)


async def get_info(ip, port):
    global ms

    try:
        srv = await resolve_srv(ip, port)
        ms = await get_mc(srv[0], int(srv[1]), timeout=3)
        if ms.online:
            result = await build_result(ms, message_type)
            await send_message(message_type, result, ms.favicon, ms.favicon_b64)
        else:
            await check.finish(Text(f' {lang_data[lang][str(ms.connection_status)]}'), reply_to=True)
    except FinishedException:
        pass
    except BaseException as e:
        await handle_exception(e)


async def build_result(ms, type=0):
    status = f'{ms.connection_status}|{lang_data[lang][str(ms.connection_status)]}'
    if type == 0:
        return {
            "favicon": ms.favicon_b64 if ms.favicon_b64 is not None and ms.favicon_b64 != "" else "no_favicon.png",
            "version": await parse_motd_to_html(ms.version),
            "slp_protocol": str(ms.slp_protocol),
            "address": ms.address,
            "port": ms.port,
            "delay": f"{ms.latency}ms",
            "gamemode": ms.gamemode,
            "motd": await parse_motd_to_html(ms.motd),
            "players": f'{ms.current_players}/{ms.max_players}',
            "status": f'{ms.connection_status}|{lang_data[lang][str(ms.connection_status)]}',
            "lang": lang_data[lang]
        }
    elif type == 1:
        motd_part = f'\n{lang_data[lang]["motd"]}{await parse_motd(ms.motd)}'
        version_part = f'\n{lang_data[lang]["version"]}{await parse_motd(ms.version)}'
    elif type == 2:
        motd_part = f'\n{lang_data[lang]["motd"]}{ms.stripped_motd}'
        version_part = f'\n{lang_data[lang]["version"]}{ms.version}'

    base_result = (
        f' {version_part}'
        f'\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}'
        f'\n{lang_data[lang]["address"]}{ms.address}'
        f'\n{lang_data[lang]["port"]}{ms.port}'
        f'\n{lang_data[lang]["delay"]}{ms.latency}ms'
    )

    if 'BEDROCK' in str(ms.slp_protocol):
        base_result += f'\n{lang_data[lang]["gamemode"]}{ms.gamemode}'

    result = (
        base_result +
        motd_part +
        f'\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}'
        f'\n{lang_data[lang]["status"]}{status}'
    )

    return result


async def send_message(type, result, favicon, favicon_b64):
    if type == 0:
        await send_html_message(result)
    elif type == 1:
        await send_image_message(result, favicon, favicon_b64)
    elif type == 2:
        await send_text_message(result, favicon, favicon_b64)


async def send_text_message(result, favicon, favicon_b64):
    if favicon is not None:
        await check.finish(UniMessage([
            Text(result),
            Text('\nFavicon:'),
            Image(raw=base64.b64decode(favicon_b64.split(",")[1]))
        ]), reply_to=True)
    else:
        await check.finish(UniMessage(result), reply_to=True)


async def send_html_message(result):
    from nonebot_plugin_htmlrender import template_to_pic
    template_dir = os.path.join(os.path.dirname(__file__), "templates")

    pic = await template_to_pic(
        template_path=template_dir,
        template_name="default.html",
        templates={"data": result},
    )
    await check.finish(UniMessage(Image(raw=pic)), reply_to=True)


async def send_image_message(result, favicon, favicon_b64):
    if favicon is not None:
        await check.finish(UniMessage([
            Image(raw=(await ColoredTextImage(result).draw_text_with_style()).pic2bytes()
                  ),
            Text('Favicon:'),
            Image(raw=base64.b64decode(favicon_b64.split(",")[1]))
        ]), reply_to=True)
    else:
        await check.finish(UniMessage(Image(raw=(await ColoredTextImage(result).draw_text_with_style()).pic2bytes()
                                            )), reply_to=True)


async def handle_exception(e):
    error_type = type(e).__name__
    error_message = str(e)
    trace_info = traceback.extract_tb(sys.exc_info()[2])
    error_traceback = trace_info[-2] if len(trace_info) > 1 else trace_info[-1]

    result = f' ERROR:\nType: {error_type}\nMessage: {error_message}\nLine: {error_traceback.lineno}\nFile: {error_traceback.filename}\nFunction: {error_traceback.name}'
    logger.error(result)
    try:
        await check.finish(Text(result), reply_to=True)
    except FinishedException:
        pass


@lang_change.handle()
async def _(language: str):
    if language:
        await lang_change.finish(Text(await change_language_to(language)), reply_to=True)
    else:
        await lang_change.finish(Text(" Language?"), reply_to=True)


async def change_language_to(language: str):
    global lang
    try:
        a = lang_data[language]
    except:
        return f' No language named "{language}"!'
    else:
        if language == lang:
            return f' The language is already "{language}"!'
        else:
            lang = language
            return f' Change to "{language}" success!'


@lang_now.handle()
async def _():
    await lang_now.send(Text(f' Language: {lang}.'), reply_to=True)


@lang_list.handle()
async def _():
    i = '\n'.join(list(lang_data.keys()))
    await lang_list.send(Text(f" Language:\n{i}"), reply_to=True)
