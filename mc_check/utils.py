import io
import re
import ujson
import os
import dns.resolver
import base64
import sys
import traceback
from zhenxun.services.log import logger
from .data_source import MineStat, SlpProtocols, ConnStatus
from .configs import lang_data, lang, message_type
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple, List
from nonebot import require
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Text
from nonebot_plugin_alconna import Image as NImage

async def handle_exception(e):
    error_type = type(e).__name__
    error_message = str(e)
    trace_info = traceback.extract_tb(sys.exc_info()[2])
    error_traceback = trace_info[-2] if len(trace_info) > 1 else trace_info[-1]
    result = f"ERROR:\nType: {error_type}\nMessage: {error_message}\nLine: {error_traceback.lineno}\nFile: {error_traceback.filename}\nFunction: {error_traceback.name}"
    logger.error(result)
    return Text(result)

async def change_language_to(language: str):
    global lang
    
    try:
        _ = lang_data[language]
    except KeyError:
        return f"No language named '{language}'!"
    else:
        if language == lang:
            return f"The language is already '{language}'!"
        else:
            lang = language
            return f"Change to '{language}' success!"

async def build_result(ms, type=0):
    """
    根据类型构建并返回查询结果。

    参数:
    - ms: 包含服务器信息的对象。
    - type: 结果类型，决定返回结果的格式，默认为0。

    返回:
    - 根据类型不同返回不同格式的查询结果。
    """
#    status = f"{ms.connection_status}|{lang_data[lang][str(ms.connection_status)]}"
    if type == 0:
        result = {
            "favicon": ms.favicon_b64 if ms.favicon else "no_favicon.png",
            "version": await parse_motd_to_html(ms.version),
            "slp_protocol": str(ms.slp_protocol),
            "address": ms.address,
            "port": ms.port,
            "delay": f"{ms.latency}ms",
            "gamemode": ms.gamemode,
            "motd": await parse_motd_to_html(ms.motd),
            "players": f"{ms.current_players}/{ms.max_players}",
#            "status": f"{ms.connection_status}|{lang_data[lang][str(ms.connection_status)]}",
            "lang": lang_data[lang]
        }
        from nonebot_plugin_htmlrender import template_to_pic
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        pic = await template_to_pic(
            template_path=template_dir,
            template_name="default.html",
            templates={"data": result},
        )
        return NImage(raw=pic)
    elif type == 1:
        motd_part = f"\n{lang_data[lang]['motd']}{await parse_motd(ms.motd)}[#RESET]"
        version_part = f"\n{lang_data[lang]['version']}{await parse_motd(ms.version)}[#RESET]"
    elif type == 2:
        motd_part = f"\n{lang_data[lang]['motd']}{ms.stripped_motd}"
        version_part = f"\n{lang_data[lang]['version']}{ms.version}"

    base_result = (
        f"{version_part}"
        f"\n{lang_data[lang]['slp_protocol']}{ms.slp_protocol}"
        f"\n{lang_data[lang]['address']}{ms.address}"
        f"\n{lang_data[lang]['port']}{ms.port}"
        f"\n{lang_data[lang]['delay']}{ms.latency}ms"
    )

    if "BEDROCK" in str(ms.slp_protocol):
        base_result += f"\n{lang_data[lang]['gamemode']}{ms.gamemode}"

    result = (
        base_result +
        motd_part +
        f"\n{lang_data[lang]['players']}{ms.current_players}/{ms.max_players}"
#        f"\n{lang_data[lang]['status']}{status}"
    )
    
    if type == 1:
        if ms.favicon is not None:
            return [
                NImage(raw=(await ColoredTextImage(result).draw_text_with_style()).pic2bytes()
                    ),
                Text("Favicon:"),
                NImage(raw=base64.b64decode(ms.favicon_b64.split(",")[1]))
            ]
        else:
            return NImage(raw=(await ColoredTextImage(result).draw_text_with_style()).pic2bytes())
    elif type == 2:
        if ms.favicon is not None:
            return [
                Text(result),
                Text("\nFavicon:"),
                NImage(raw=base64.b64decode(ms.favicon_b64.split(",")[1]))
            ]
        else:
            return [Text(result)]

async def get_mc(host: str, port: int, timeout: int = 5) -> List[Tuple[Optional[MineStat], Optional[ConnStatus]]]:
    """
    获取Java版和Bedrock版的MC服务器信息。

    参数:
    - host (str): 服务器的IP地址。
    - port (int): 服务器的端口。
    - timeout (int): 请求超时时间，默认为5秒。

    返回:
    - list: 包含Java版和Bedrock版服务器信息的列表，如果列表为空则返回None。
    """
    return [
        await get_java(host, port, timeout),
        await get_bedrock(host, port, timeout)
    ]


async def get_message_list(ip: str, port: int, timeout: int = 5) -> list:
    """
    异步函数，根据IP和端口获取消息列表。

    参数:
    - ip (str): 服务器的IP地址。
    - port (int): 服务器的端口。
    - timeout (int, 可选): 超时时间，默认为5秒。

    返回:
    - list: 包含消息的列表。
    """
    try:
        srv = await resolve_srv(ip, port)
    except (dns.resolver.LifetimeTimeout, dns.resolver.NoNameservers):
        return [Text(f"{lang_data[lang]['dns_fail']}")]
    messages = []
    ms = await get_mc(srv[0], int(srv[1]), timeout)
    for i in ms:
        if i[0] is not None:
            messages.append(await build_result(i[0], message_type))
    if len(messages) == 0:
        messages.append(next((Text(f"{lang_data[lang][str(item[1])]}") for item in ms if item[1] != ConnStatus.CONNFAIL),
            Text(f"{lang_data[lang][str(ConnStatus.CONNFAIL)]}")))
    return messages


async def get_bedrock(host: str, port: int, timeout: int = 5) -> Tuple[Optional[MineStat], Optional[ConnStatus]]:
    """
    异步函数，用于通过指定的主机名、端口和超时时间获取Minecraft Bedrock版服务器状态。

    参数:
    - host: 服务器的主机名。
    - port: 服务器的端口号。
    - timeout: 连接超时时间，默认为5秒。

    返回:
    - MineStat实例，包含服务器状态信息，如果服务器在线的话；否则可能返回None。
    """
    result = MineStat(host, port, timeout, SlpProtocols.BEDROCK_RAKNET)

    if result.online:
        return result, ConnStatus.SUCCESS
    else:
        return None, result.connection_status


async def get_java(host: str, port: int, timeout: int = 5) -> Tuple[Optional[MineStat], Optional[ConnStatus]]:
    """
    异步函数，用于通过指定的主机名、端口和超时时间获取Minecraft Java版服务器状态。

    参数:
    - host: 服务器的主机名。
    - port: 服务器的端口号。
    - timeout: 连接超时时间，默认为5秒。

    返回:
    - MineStat 实例，包含服务器状态信息，如果服务器在线的话；否则可能返回 None。
    """
    # Minecraft 1.4 & 1.5 (legacy SLP)
    result = MineStat(host, port, timeout, SlpProtocols.LEGACY)

    # Minecraft Beta 1.8 to Release 1.3 (beta SLP)
    if result.connection_status not in [ConnStatus.CONNFAIL, ConnStatus.SUCCESS]:
        result = MineStat(host, port, timeout, SlpProtocols.BETA)

    # Minecraft 1.6 (extended legacy SLP)
    if result.connection_status is not ConnStatus.CONNFAIL:
        result = MineStat(host, port, timeout, SlpProtocols.EXTENDED_LEGACY)

    # Minecraft 1.7+ (JSON SLP)
    if result.connection_status is not ConnStatus.CONNFAIL:
        result = MineStat(host, port, timeout, SlpProtocols.JSON)

    if result.online:
        return result, ConnStatus.SUCCESS
    else:
        return None, result.connection_status


async def parse_host(host_name) -> Tuple[str, int]:
    """
    解析主机名（可选端口）。

    该函数尝试从主机名中提取IP地址和端口号。如果主机名中未指定端口，
    则默认端口号为0。

    参数:
    host_name (str): 主机名，可能包含端口。

    返回:
    Tuple[str, int]: 一个元组，包含两个元素：
    - 第一个元素是主机的IP地址（字符串形式）。
    - 第二个元素是主机的端口号（整数形式），如果主机名中未指定端口，则为0。
    """
    pattern = r"(?:\[(.+?)\]|(.+?))(?::(\d+))?$"
    match = re.match(pattern, host_name)

    if match:
        address = match.group(1) or match.group(2)
        port = int(match.group(3)) if match.group(
            3) else None

        port = port if port is not None else 0

    else:
        return host_name, 0

    return address, port


async def is_invalid_address(address: str) -> bool:
    """
    异步判断给定的地址是否为无效的域名或IP地址。

    参数:
    address (str): 需要验证的地址，可以是电子邮件地址或IP地址。

    返回:
    bool: 如果地址无效则返回True，否则返回False。
    """
    domain_pattern = r"^(?:(?!_)(?!-)(?!.*--)[a-zA-Z0-9\u4e00-\u9fa5\-_]{1,63}\.?)+[a-zA-Z\u4e00-\u9fa5]{2,}$"
    ipv4_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    ipv6_pattern = r"^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$"

    match_domain = re.match(domain_pattern, address)
    match_ipv4 = re.match(ipv4_pattern, address)
    match_ipv6 = re.match(ipv6_pattern, address)

    return (match_domain is None) and (match_ipv4 is None) and (match_ipv6 is None)


async def resolve_srv(ip: str, port: int = 0) -> list:
    """
    通过DNS解析服务器地址和端口。

    如果指定的端口为0，则表示需要通过SRV记录解析端口。

    参数:
        ip (str): 服务器IP地址。
        port (int): 服务器端口，如果为0则需要通过SRV记录获取。

    返回:
        list: 包含服务器地址和端口的列表。
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["223.5.5.5", "1.1.1.1"]

    try:
        response = resolver.resolve(f"_minecraft._tcp.{ip}", "SRV")

        if not response:
            return [ip, port]

        for rdata in response:
            address = str(rdata.target).rstrip(".")
            if port == 0:
                port = rdata.port
            return [address, port]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        pass
    return [ip, port]


async def parse_motd(json_data: Optional[str]) -> Optional[str]:
    """
    解析MOTD数据并转换为带有自定义十六进制颜色标记的字符串。

    参数:
    - json_data (str | None): MOTD数据。

    返回:
    - str | None: 带有自定义十六进制颜色标记的字符串。
    """
    if json_data is None:
        return None

    standard_color_map = {
        "black": "[#000]",
        "dark_blue": "[#00A]",
        "dark_green": "[#0A0]",
        "dark_aqua": "[#0AA]",
        "dark_red": "[#A00]",
        "dark_purple": "[#A0A]",
        "gold": "[#FFA]",
        "gray": "[#AAA]",
        "dark_gray": "[#555]",
        "blue": "[#00F]",
        "green": "[#0F0]",
        "aqua": "[#0FF]",
        "red": "[#F00]",
        "light_purple": "[#FAF]",
        "yellow": "[#FF0]",
        "white": "[#FFF]",
        "reset": "[#RESET]",
        "bold": "[#BOLD]",
        "italic": "[#ITALIC]",
        "underline": "[#UNDERLINE]",
        "strikethrough": "[#STRIKETHROUGH]",
        "§0": "[#000]",  # black
        "§1": "[#00A]",  # dark blue
        "§2": "[#0A0]",  # dark green
        "§3": "[#0AA]",  # dark aqua
        "§4": "[#A00]",  # dark red
        "§5": "[#A0A]",  # dark purple
        "§6": "[#FFA]",  # gold
        "§7": "[#AAA]",  # gray
        "§8": "[#555]",  # dark gray
        "§9": "[#00F]",  # blue
        "§a": "[#0F0]",  # green
        "§b": "[#0FF]",  # aqua
        "§c": "[#F00]",  # red
        "§d": "[#FAF]",  # light purple
        "§e": "[#FF0]",  # yellow
        "§f": "[#FFF]",  # white
        "§g": "[#DDD605]",  # minecoin gold
        "§h": "[#E3D4D1]",  # material quartz
        "§i": "[#CECACA]",  # material iron
        "§j": "[#443A3B]",  # material netherite	
        "§l": "[#BOLD]",  # bold
        "§m": "[#STRIKETHROUGH]",  # strikethrough
        "§n": "[#UNDERLINE]",  # underline
        "§o": "[#ITALIC]",  # italic
        "§p": "[#DEB12D]",  # material gold
        "§q": "[#47A036]",  # material emerald
        "§r": "[#RESET]",  # reset
        "§s": "[#2CBAA8]",  # material diamond
        "§t": "[#21497B]",  # material lapis
        "§u": "[#9A5CC6]"   # material amethyst
    }

    try:
        json_data = ujson.loads(json_data)
    except ujson.JSONDecodeError:
        result = ""
        i = 0
        while i < len(json_data):
            if json_data[i] == "§":
                style_code = json_data[i:i+2]
                if style_code in standard_color_map:
                    result += standard_color_map[style_code]
                    i += 2
                    continue
            result += json_data[i]
            i += 1

        return result

    async def parse_extra(extra):
        result = ""
        extra_str = ""
        if isinstance(extra, dict) and "extra" in extra:
            for key in extra:
               if key == "extra":
            	   result += await parse_extra(extra[key])
               elif key == "text":
            	   result += await parse_extra(extra[key])
        elif isinstance(extra, dict):
            color = extra.get("color", "")
            text = extra.get("text", "")

            if color.startswith("#"):
                hex_color = color[1:]
                if len(hex_color) == 3:
                    hex_color = "".join([c * 2 for c in hex_color])
                color_code = f"[#{hex_color.upper()}]"
            else:
                color_code = standard_color_map.get(color, "")
             
            if extra.get("bold") is True:
            		extra_str += standard_color_map.get("bold")
            if extra.get("italic") is True:
            		extra_str += standard_color_map.get("italic")
            if extra.get("underline") is True:
            		extra_str += standard_color_map.get("underline")
            if extra.get("strikethrough") is True:
            		extra_str += standard_color_map.get("strikethrough")

            result += f"{extra_str}{color_code}{text}[#RESET]"
        elif isinstance(extra, list):
            for item in extra:
                result += await parse_extra(item)
        else:
            result += str(extra)

        return result

    return await parse_extra(json_data)


async def parse_motd_to_html(json_data: Optional[str]) -> Optional[str]:
    """
    解析MOTD数据并转换为带有自定义颜色的HTML字符串。

    参数:
    - json_data (str|None): MOTD数据。

    返回:
    - str | None: 带有自定义颜色的HTML字符串。
    """
    if json_data is None:
        return None

    standard_color_map = {
        "black": ("<font color=\"#000000\">", "</font>"),
        "dark_blue": ("<font color=\"#0000AA\">", "</font>"),
        "dark_green": ("<font color=\"#00AA00\">", "</font>"),
        "dark_aqua": ("<font color=\"#00AAAA\">", "</font>"),
        "dark_red": ("<font color=\"#AA0000\">", "</font>"),
        "dark_purple": ("<font color=\"#AA00AA\">", "</font>"),
        "gold": ("<font color=\"#FFAA00\">", "</font>"),
        "gray": ("<font color=\"#AAAAAA\">", "</font>"),
        "dark_gray": ("<font color=\"#555555\">", "</font>"),
        "blue": ("<font color=\"#0000FF\">", "</font>"),
        "green": ("<font color=\"#00AA00\">", "</font>"),
        "aqua": ("<font color=\"#00AAAA\">", "</font>"),
        "red": ("<font color=\"#AA0000\">", "</font>"),
        "light_purple": ("<font color=\"#FFAAFF\">", "</font>"),
        "yellow": ("<font color=\"#FFFF00\">", "</font>"),
        "white": ("<font color=\"#FFFFFF\">", "</font>"),
        "reset": ("</strong></i></u></s>", ""),
        "bold": ("<strong>", "</strong>"),
        "italic": ("<i>", "</i>"),
        "underline": ("<u>", "</u>"),
        "strikethrough": ("<s>", "</s>"),
        "§0": ("<font color=\"#000000\">", "</font>"),  # black
        "§1": ("<font color=\"#0000AA\">", "</font>"),  # dark blue
        "§2": ("<font color=\"#00AA00\">", "</font>"),  # dark green
        "§3": ("<font color=\"#00AAAA\">", "</font>"),  # dark aqua
        "§4": ("<font color=\"#AA0000\">", "</font>"),  # dark red
        "§5": ("<font color=\"#AA00AA\">", "</font>"),  # dark purple
        "§6": ("<font color=\"#FFAA00\">", "</font>"),  # gold
        "§7": ("<font color=\"#AAAAAA\">", "</font>"),  # gray
        "§8": ("<font color=\"#555555\">", "</font>"),  # dark gray
        "§9": ("<font color=\"#0000FF\">", "</font>"),  # blue
        "§a": ("<font color=\"#00AA00\">", "</font>"),  # green
        "§b": ("<font color=\"#00AAAA\">", "</font>"),  # aqua
        "§c": ("<font color=\"#AA0000\">", "</font>"),  # red
        "§d": ("<font color=\"#FFAAFF\">", "</font>"),  # light purple
        "§e": ("<font color=\"#FFFF00\">", "</font>"),  # yellow
        "§f": ("<font color=\"#FFFFFF\">", "</font>"),  # white
        "§g": ("<font color=\"#DDD605\">", "</font>"),  # minecoin gold
        "§h": ("<font color=\"#E3D4D1\">", "</font>"),  # material quartz
        "§i": ("<font color=\"#CECACA\">", "</font>"),  # material iron
        "§j": ("<font color=\"#443A3B\">", "</font>"),  # material netherite	
        "§l": ("<strong>", "</strong>"),  # bold
        "§m": ("<s>", "</s>"),  # strikethrough
        "§n": ("<u>", "</u>"),  # underline
        "§o": ("<i>", "</i>"),  # italic
        "§p": ("<font color=\"#DEB12D\">", "</font>"),  # material gold
        "§q": ("<font color=\"#47A036\">", "</font>"),  # material emerald
        "§r": ("</strong></i></u></s>", ""),  # reset
        "§s": ("<font color=\"#2CBAA8\">", "</font>"),  # material diamond
        "§t": ("<font color=\"#21497B\">", "</font>"),  # material lapis
        "§u": ("<font color=\"#9A5CC6\">", "</font>")   # material amethyst
    }

    async def parse_extra(extra, styles=[]):
        result = ""
        if isinstance(extra, dict) and "extra" in extra:
            for key in extra:
               if key == "extra":
            	   result += await parse_extra(extra[key], styles)
               elif key == "text":
            	   result += await parse_extra(extra[key], styles)
        elif isinstance(extra, dict):
            color = extra.get("color", "")
            text = extra.get("text", "")
            
            # 将颜色转换为 HTML 的 font 标签
            if color.startswith("#"):
                hex_color = color[1:]
                if len(hex_color) == 3:
                    hex_color = "".join([c * 2 for c in hex_color])
                color_code = (
                    f"<font color=\"#{hex_color.upper()}\">", "</font>")
            else:
                # 标准颜色
                color_code = standard_color_map.get(color, ("", ""))

            # 更新样式栈
            open_tag, close_tag = color_code
            if extra.get("bold") is True:
            		open_tag_, close_tag_ = standard_color_map.get("bold")
            		open_tag += open_tag_
            		close_tag = close_tag_ + close_tag
            if extra.get("italic") is True:
            		open_tag_, close_tag_ = standard_color_map.get("italic")
            		open_tag += open_tag_
            		close_tag = close_tag_ + close_tag
            if extra.get("underline") is True:
            		open_tag_, close_tag_ = standard_color_map.get("underline")
            		open_tag += open_tag_
            		close_tag = close_tag_ + close_tag
            if extra.get("strikethrough") is True:
            		open_tag_, close_tag_ = standard_color_map.get("strikethrough")
            		open_tag += open_tag_
            		close_tag = close_tag_ + close_tag
            styles.append(close_tag)
            result += open_tag + text + close_tag
        elif isinstance(extra, list):
            for item in extra:
                result += await parse_extra(item, styles)
        else:
            # 处理换行符
            result += str(extra).replace("\n", "<br>")
        return result

    try:
        json_data = ujson.loads(json_data)
    except ujson.JSONDecodeError:
        result = ""
        i = 0
        styles = []
        while i < len(json_data):
            if json_data[i] == "§":
                style_code = json_data[i:i+2]
                if style_code in standard_color_map:
                    open_tag, close_tag = standard_color_map[style_code]

                    # 如果是重置，则清空样式栈
                    if open_tag == "</strong></i></u></s>":
                        # 清空样式栈并关闭所有打开的样式
                        for tag in styles:
                            result += tag
                        styles.clear()
                    else:
                        styles.append(close_tag)
                        result += open_tag
                    i += 2
                    continue
            # 处理换行符
            if json_data[i] == "\n":
                result += "<br>"
                i += 1
                continue
            result += json_data[i]
            i += 1

        # 在字符串末尾关闭所有打开的样式
        for tag in styles:
            result += tag

        return result

    return await parse_extra(json_data)


class ColoredTextImage:
    def __init__(self, text: str, background_color: tuple[int, int, int] = (249, 246, 242), padding: int = 10) -> None:
        """
        初始化一个用于绘制彩色文本图像的对象。
        """
        self.text = text
        self.padding = padding
        self.background_color = background_color
        self.font_path = os.path.join(
            os.path.dirname(__file__), "font", "Regular.ttf")
        self.bold_font_path = os.path.join(
            os.path.dirname(__file__), "font", "Bold.ttf")
        self.bold_and_italic_font_path = os.path.join(
            os.path.dirname(__file__), "font", "Bold_Italic.ttf")
        self.italic_font_path = os.path.join(
            os.path.dirname(__file__), "font", "Italic.ttf")
        self.font_size = 40

    def _calculate_dimensions(self, text: str) -> tuple[int, int]:
        """
        计算图像的宽度和高度。
        """
        # Create a temporary image and draw object for calculating dimensions
        temp_image = Image.new("RGB", (1, 1))
        temp_draw = ImageDraw.Draw(temp_image)
        font = self.get_font()

        max_width, total_height = self._calculate_plain_text_dimensions(
            text, font, temp_draw)

        # Add padding to the dimensions
        width = max_width + 2 * self.padding
        height = total_height + 2 * self.padding
        return int(width), int(height)

    def _calculate_plain_text_dimensions(self, text, font, temp_draw):
        """
        计算普通文本的尺寸，忽略颜色标记。
        """
        # 移除颜色标记
        plain_text = re.sub(r"\[\#[^\]]*\]", "", text)

        max_width = 0
        total_height = 0
        line_height = self.font_size * 1.5

        for line in plain_text.split("\n"):
            bbox = temp_draw.textbbox((0, 0), line, font=font)
            width = bbox[2] - bbox[0] + 50
            max_width = max(max_width, width)
            total_height += line_height

        return max_width, total_height

    def get_font(self, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
        """
        根据指定的样式获取字体。

        :param bold: 是否使用粗体，默认为 False。
        :param italic: 是否使用斜体，默认为 False。
        :return: 返回一个 `ImageFont.FreeTypeFont` 对象。
        """
        if bold and italic:
            return ImageFont.truetype(self.bold_and_italic_font_path, self.font_size)
        elif bold:
            return ImageFont.truetype(self.bold_font_path, self.font_size)
        elif italic:
            return ImageFont.truetype(self.italic_font_path, self.font_size)
        return ImageFont.truetype(self.font_path, self.font_size)

    async def draw_text_with_style(self) -> "ColoredTextImage":
        """
        使用指定样式绘制文本。

        :param text: 需要绘制的文本字符串。
        """
        text = self.text
        width, height = self._calculate_dimensions(text)
        self.image = Image.new("RGB", (width, height), self.background_color)
        self.draw = ImageDraw.Draw(self.image)

        bold = italic = underline = strikethrough = False
        current_color = (0, 0, 0)
        line_height = self.font_size * 1.5
        x_offset = 50
        y_offset = 0

        for line in text.split("\n"):
            i = 0
            while i < len(line):
                if line[i] == "[":
                    if line[i:i+7] == "[#BOLD]":
                        bold = True
                        i += 7
                        continue

                    if line[i:i+9] == "[#ITALIC]":
                        italic = True
                        i += 9
                        continue

                    if line[i:i+12] == "[#UNDERLINE]":
                        underline = True
                        i += 12
                        continue

                    if line[i:i+16] == "[#STRIKETHROUGH]":
                        strikethrough = True
                        i += 16
                        continue

                    if line[i:i+8] == "[#RESET]":
                        bold = italic = underline = strikethrough = False
                        current_color = (0, 0, 0)
                        i += 8
                        continue

                    if line[i:i+2] == "[#":
                        close_bracket_index = line.find("]", i)
                        if close_bracket_index != -1:
                            hex_color = line[i+2:close_bracket_index].upper()
                            if len(hex_color) == 3:
                                hex_color = "".join([c * 2 for c in hex_color])
                            try:
                                current_color = tuple(
                                    int(hex_color[j:j+2], 16) for j in (0, 2, 4))
                            except ValueError:
                                pass
                            i = close_bracket_index + 1
                            continue

                # 处理普通字符
                char = line[i]
                font_mod = self.get_font(bold, italic)
                bbox = self.draw.textbbox(
                    (x_offset, y_offset), char, font=font_mod)
                width = bbox[2] - bbox[0]

                self.draw.text((x_offset, y_offset), char,
                               fill=current_color, font=font_mod)

                if underline:
                    underline_y = y_offset + self.font_size
                    self.draw.line((x_offset, underline_y, x_offset + width, underline_y),
                                   fill=current_color, width=1)

                if strikethrough:
                    strikethrough_y = y_offset + self.font_size / 2
                    self.draw.line((x_offset, strikethrough_y, x_offset + width, strikethrough_y),
                                   fill=current_color, width=1)

                x_offset += width
                i += 1
            y_offset += line_height
            x_offset = 50
        return self

    def save(self, filename: str) -> None:
        """
        将当前图像保存到文件。

        :param filename: 文件名，包括路径和扩展名。
        """
        self.image.save(filename, format="PNG")

    def pic2bytes(self) -> bytes:
        """
        将当前图像转换为字节流。

        :return: 返回一个包含图像数据的字节流。
        """
        byte_io = io.BytesIO()
        self.image.save(byte_io, format="PNG")
        byte_io.seek(0)
        return byte_io.getvalue()
