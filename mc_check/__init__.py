from nonebot import on_command
from services.log import logger
from utils.message_builder import image
from utils.image_utils import text2image
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageSegment,
    Message)
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from configs.config import Config
from .data_source import *
import nonebot
import base64
import os
import re
import ujson
import dns.resolver
import traceback
import sys

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)

dns.resolver.default_resolver.nameservers = ['223.5.5.5', '1.1.1.1']

__zx_plugin_name__ = "我的世界查服"
__plugin_usage__ = """
usage：
    我的世界服务器状态查询，支持IPv6
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
""".strip()
__plugin_des__ = "用法：查服 ip:port / mcheck ip:port"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["查服/mcheck", "设置语言/set_lang",
                  "当前语言/lang_now", "语言列表/lang_list"]
__plugin_version__ = 1.6
__plugin_author__ = "molanp"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查服", 'mcheck', '设置语言', 'set_lang', '当前语言', 'lang_now', "语言列表", "lang_list"],
}
__plugin_configs__ = {
    "JSON_BDS": {"value": False, "help": "基岩版查服是否显示json版motd|Bedrock Edition checks whether the JSON version of MODD is displayed", "default_value": False},
    "JSON_JAVA": {"value": False, "help": "JAVA版查服是否显示json版motd|Java Edition checks whether the JSON version of motd is displayed", "default_value": False},
    "LANGUAGE": {"value": "zh-cn", "help": "Change the language(zh-cn, zh-tw, en etc.)", "default_value": "zh-cn"},
    "type":  {"value": 0, "help": "防封号选项，0为发送图片消息，1为文本消息", "default": 0}
}


def readInfo(file):
    with open(os.path.join(path, file), "r", encoding="utf-8") as f:
        return ujson.loads((f.read()).strip())


def is_invalid_address(address):
    domain_pattern = r"^(?:(?!_)(?!-)(?!.*--)[a-zA-Z0-9\u4e00-\u9fa5\-_]{1,63}\.?)+[a-zA-Z\u4e00-\u9fa5]{2,}$"
    ipv4_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    ipv6_pattern = r"^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$"

    match_domain = re.match(domain_pattern, address)
    match_ipv4 = re.match(ipv4_pattern, address)
    match_ipv6 = re.match(ipv6_pattern, address)

    return (match_domain is None) and (match_ipv4 is None) and (match_ipv6 is None)


def resolve_srv(ip, port=0):
    try:
        result = dns.resolver.query(
            '_minecraft._tcp.' + ip, 'SRV', raise_on_no_answer=False)

        for rdata in result:
            address = str(rdata.target).strip('.')
            if (port == 0):
                port = rdata.port
            return [address, port]
    except dns.resolver.NXDOMAIN:
        pass

    return [ip, port]


message_type = Config.get_config("mc_check", "type")
path = os.path.dirname(__file__)
lang = Config.get_config("mc_check", "LANGUAGE")
if lang == None:
    lang = "Chinese"
lang_data = readInfo("language.json")

check = on_command("查服", aliases={'mcheck'}, priority=5, block=True)
lang_change = on_command("设置语言", aliases={'set_lang'}, priority=5, block=True)
lang_now = on_command("当前语言", aliases={'lang_now'}, priority=5, block=True)
lang_list = on_command("语言列表", aliases={'lang_list'}, priority=5, block=True)


@check.handle()
async def handle_first_receive(bot_: Bot, event_: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        global bot, event
        bot, event = bot_, event_
        matcher.set_arg("host", args)


@check.got("host", prompt="IP?")
async def handle_host(host_name: str = ArgPlainText("host")):
    address = ''
    port = 0
    if '.' in host_name:
        parts = host_name.strip().split(':')
        address = parts[0]
        if len(parts) > 1:
            port = parts[1]
    else:
        pattern = r'\[(.+)\](?::(\d+))?$'
        match = re.match(pattern, host_name)
        if match:
            address = match.group(1)
            port = match.group(2) if match.group(2) else 0

    if not str(port).isdigit() or not (0 <= int(port) <= 65535):
        await check.finish(lang_data[lang]["where_port"], at_sender=True)

    if is_invalid_address(address):
        await check.finish(lang_data[lang]["where_ip"], at_sender=True)

    await get_info(address, port)


async def get_info(ip, port):
    global bot, event
    try:
        srv = resolve_srv(ip, port)
        ms = MineStat(srv[0], int(srv[1]), timeout=1)
        if ms.online:
            if ms.connection_status == ConnStatus.SUCCESS:
                status = f'{ms.connection_status}|{lang_data[lang]["status_success"]}'
            elif ms.connection_status == ConnStatus.CONNFAIL:
                status = f'{ms.connection_status}|{lang_data[lang]["status_connfail"]}'
            elif ms.connection_status == ConnStatus.TIMEOUT:
                status = f'{ms.connection_status}|{lang_data[lang]["status_timeout"]}'
            elif ms.connection_status == ConnStatus.UNKNOWN:
                status = f'{ms.connection_status}|{lang_data[lang]["status_unknown"]}'
            if Config.get_config("mc_check", "JSON_JAVA"):
                result = f'\n{lang_data[lang]["version"]}{ms.version}\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}\n{lang_data[lang]["address"]}{ip}\n{lang_data[lang]["port"]}{ms.port}\n{lang_data[lang]["delay"]}{ms.latency}ms\n{lang_data[lang]["motd"]}{ms.motd}\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}\n{lang_data[lang]["status"]}{status}\n'
            else:
                result = f'\n{lang_data[lang]["version"]}{ms.version}\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}\n{lang_data[lang]["address"]}{ip}\n{lang_data[lang]["port"]}{ms.port}\n{lang_data[lang]["delay"]}{ms.latency}ms\n{lang_data[lang]["motd"]}{ms.stripped_motd}\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}\n{lang_data[lang]["status"]}{status}\n'
            # Bedrock specific attribute:
            if 'BEDROCK' in str(ms.slp_protocol):
                if Config.get_config("mc_check", "JSON_BDS"):
                    result = f'\n{lang_data[lang]["version"]}{ms.version}\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}\n{lang_data[lang]["gamemode"]}{ms.gamemode}\n{lang_data[lang]["address"]}{ip}\n{lang_data[lang]["port"]}{ms.port}\n{lang_data[lang]["delay"]}{ms.latency}ms\n{lang_data[lang]["motd"]}{ms.motd}\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}\n{lang_data[lang]["status"]}{status}'
                else:
                    result = f'\n{lang_data[lang]["version"]}{ms.version}\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}\n{lang_data[lang]["gamemode"]}{ms.gamemode}\n{lang_data[lang]["address"]}{ip}\n{lang_data[lang]["port"]}{ms.port}\n{lang_data[lang]["delay"]}{ms.latency}ms\n{lang_data[lang]["motd"]}{ms.stripped_motd}\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}\n{lang_data[lang]["status"]}{status}'
                if message_type == 0:
                    await check.finish(Message(
                            image(
                                b64=(
                                    await text2image(result, color="#f9f6f2", padding=10)
                                ).pic2bs4()
                            )
                        ),at_sender=True)
                else:
                   await check.finish(Message(result),at_sender=True)
            # Send favicon
            else:
                if message_type == 0:
                    msg_list = []
                    if ms.favicon is not None and ms.favicon != "":
                        msg_list.append({
                            "type": "node",
                            "data": {
                                "name": "查服机器人",
                                "uin": "2854196310",
                                "content": "[CQ:image,file={}]".format(
                            (await text2image(result, color="#f9f6f2", padding=10,)).pic2bs4()
                            )
                            },
                        })

                        msg_list.append({
                            "type": "node",
                            "data": {
                                "name": "查服机器人",
                                "uin": "2854196310",
                                "content": "[CQ:image,file={}]".format("base64://"+
                           ms.favicon_b64.split(",")[1]
                            )
                            },
                        })
                        if isinstance(event, GroupMessageEvent):
                            await bot.send_group_forward_msg(group_id=event.group_id, messages=msg_list)
                        else:
                            for msg in msg_list:
                                await bot.send_private_msg(user_id=event.user_id, message=msg)
                    else:
                        await check.finish(Message(
                                image(
                                    b64=(
                                        await text2image(result, color="#f9f6f2", padding=10)
                                    ).pic2bs4()
                                )
                            ),at_sender=True)
                else:
                    if ms.favicon is not None and ms.favicon != "":
                        await check.finish(Message([
                                MessageSegment.text(f'{result}favicon:'),
                                MessageSegment.image(base64.b64decode(ms.favicon_b64.split(",")[1]))
                            ]),at_sender=True)
                    else:
                        await check.finish(Message(result),at_sender=True)
        else:
            await check.finish(Message(f'{lang_data[lang]["offline"]}'),at_sender=True)
    except nonebot.exception.FinishedException as e:
        pass
    except BaseException as e:
        error_type = type(e).__name__
        error_message = str(e)
        error_traceback = traceback.extract_tb(
            sys.exc_info()[2])[-2]

        result = f'ERROR:\nType: {error_type}\nMessage: {error_message}\nLine: {error_traceback.lineno}\nFile: {error_traceback.filename}\nFunction: {error_traceback.name}'
        logger.error(result)
        await check.finish(Message(result),at_sender=True)


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
