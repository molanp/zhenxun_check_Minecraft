from nonebot import on_command  # type: ignore
from zhenxun.services.log import logger  # type: ignore
from nonebot.plugin import PluginMetadata  # type: ignore
from nonebot.params import Arg, CommandArg, ArgPlainText  # type: ignore
from nonebot.matcher import Matcher  # type: ignore
from zhenxun.configs.config import Config  # type: ignore
from zhenxun.configs.utils import PluginCdBlock, PluginExtraData, RegisterConfig  # type: ignore
from nonebot.exception import FinishedException  # type: ignore
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot  # type: ignore
from .untils import (
    is_invalid_address,
    ColoredTextImage,
    parse_motd,
    readInfo,
    get_mc,
    resolve_srv
)
import re
import traceback
import sys
import base64

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
        version="1.9",
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
                help="结果发送类型，0为发送图片，1为发送文字",
                default_value=0,
                type=int,
            ),
        ],
    ).dict(),
)


message_type = Config.get_config("mc_check", "type")
lang = Config.get_config("mc_check", "LANGUAGE")
lang_data = readInfo("language.json")

check = on_command("查服", aliases={'mcheck'}, priority=5, block=True)
lang_change = on_command("设置语言", aliases={'set_lang'}, priority=5, block=True)
lang_now = on_command("当前语言", aliases={'lang_now'}, priority=5, block=True)
lang_list = on_command("语言列表", aliases={'lang_list'}, priority=5, block=True)


@check.handle()
async def handle_first_receive(bot_: Bot, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        global bot
        bot = bot_
        matcher.set_arg("host", args)


@check.got("host", prompt="IP?")
async def handle_host(host_name: str = ArgPlainText("host")):
    address, port = parse_host(host_name)

    if not str(port).isdigit() or not (0 <= int(port) <= 65535):
        await check.finish(lang_data[lang]["where_port"], at_sender=True)

    if is_invalid_address(address):
        await check.finish(lang_data[lang]["where_ip"], at_sender=True)

    await get_info(address, port)


async def get_info(ip, port):
    global bot, ms

    try:
        srv = await resolve_srv(ip, port)
        ms = await get_mc(srv[0], int(srv[1]), timeout = 1)
        if ms.online:
            if message_type == 0:
                result = build_result(ms)
                await send_image_message(result, ms.favicon, ms.favicon_b64)
            else:
                result = build_result(ms, text=True)
                await send_text_message(result, ms.favicon, ms.favicon_b64)
        else:
            await check.finish(Message(f'{lang_data[lang]["offline"]}'), at_sender=True)
    except FinishedException:
        pass
    except BaseException as e:
        await handle_exception(e)


def parse_host(host_name):
    if '.' in host_name:
        parts = host_name.strip().split(':')
        address = parts[0]
        port = parts[1] if len(parts) > 1 else 0
    else:
        pattern = r'\[(.+)\](?::(\d+))?$'
        match = re.match(pattern, host_name)
        address = match.group(1)
        port = match.group(2) if match.group(2) else 0

    return address, port


def build_result(ms, text=False):
    status = f'{ms.connection_status}|{lang_data[lang][str(ms.connection_status)]}'
    base_result = (
        f'\n{lang_data[lang]["version"]}{ms.version}'
        f'\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}'
        f'\n{lang_data[lang]["address"]}{ms.address}'
        f'\n{lang_data[lang]["port"]}{ms.port}'
        f'\n{lang_data[lang]["delay"]}{ms.latency}ms'
    )

    if 'BEDROCK' in str(ms.slp_protocol):
        base_result += f'\n{lang_data[lang]["gamemode"]}{ms.gamemode}'
    if text:
        motd_part = f'\n{lang_data[lang]["motd"]}{parse_motd(ms.stripped_motd)}'
    else:
        motd_part = f'\n{lang_data[lang]["motd"]}{parse_motd(ms.motd)}[#RESET]'

    result = (
        base_result +
        motd_part +
        f'\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}'
        f'\n{lang_data[lang]["status"]}{status}'
    )

    return result


async def send_text_message(result, favicon, favicon_b64):
    if favicon is not None and favicon != "":
        await check.finish(Message([
            Message(result),
            MessageSegment.text('favicon:'),
            MessageSegment.image(base64.b64decode(favicon_b64.split(",")[1]))
        ]), at_sender=True)
    else:
        await check.finish(Message(result), at_sender=True)


async def send_image_message(result, favicon, favicon_b64):
    if favicon is not None and favicon != "":
        await check.finish(Message([
            MessageSegment.image(
                (await ColoredTextImage(result).draw_text_with_style()).pic2bytes()
            ),
            MessageSegment.text('Favicon:'),
            MessageSegment.image(base64.b64decode(favicon_b64.split(",")[1]))
        ]), at_sender=True)
    else:
        await check.finish(MessageSegment.image(
            (await ColoredTextImage(result).draw_text_with_style()).pic2bytes()
        ), at_sender=True)


async def handle_exception(e):
    error_type = type(e).__name__
    error_message = str(e)
    error_traceback = traceback.extract_tb(sys.exc_info()[2])[-2]

    result = f'ERROR:\nType: {error_type}\nMessage: {error_message}\nLine: {error_traceback.lineno}\nFile: {error_traceback.filename}\nFunction: {error_traceback.name}'
    logger.error(result)
    try:
        await check.finish(Message(result), at_sender=True)
    except FinishedException:
        pass


@lang_change.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("lang_", args)


@lang_change.got("lang_", prompt="Language?")
async def handle_host(lang_: Message = Arg(), language_name: str = ArgPlainText("lang_")):
    await lang_change.finish(Message(await change(language_name)), at_sender=True)


async def change(language: str):
    global lang
    try:
        a = lang_data[language]
    except:
        return f'No language named "{language}"!'
    else:
        if language == lang:
            return f'The language is already "{language}"!'
        else:
            lang = language
            return f'Change to "{language}" success!'


@lang_now.handle()
async def _():
    await lang_now.send(Message(f' Language: {lang}.'), at_sender=True)


@lang_list.handle()
async def _():
    i = '\n'.join(list(lang_data.keys()))
    await lang_list.send(Message(f"Language:\n{i}"), at_sender=True)
