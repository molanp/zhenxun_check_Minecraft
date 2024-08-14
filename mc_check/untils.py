from PIL import Image, ImageDraw, ImageFont
import json
import io
import re
import ujson as json
import os
import dns.resolver

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)

dns.resolver.default_resolver.nameservers = ['223.5.5.5', '1.1.1.1']


def readInfo(file):
    with open(os.path.join(os.path.dirname(__file__), file), "r", encoding="utf-8") as f:
        return json.loads((f.read()).strip())


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


def parse_motd(json_data):
    """
    解析MOTD数据并转换为带有自定义十六进制颜色标记的字符串。

    参数:
    - json_data (str): MOTD数据。

    返回:
    - str: 带有自定义十六进制颜色标记的字符串。
    """

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
        '§0': "[#000]",  # black
        '§1': "[#00A]",  # dark blue
        '§2': "[#0A0]",  # dark green
        '§3': "[#0AA]",  # dark aqua
        '§4': "[#A00]",  # dark red
        '§5': "[#A0A]",  # dark purple
        '§6': "[#FFA]",  # gold
        '§7': "[#AAA]",  # gray
        '§8': "[#555]",  # dark gray
        '§9': "[#00F]",  # blue
        '§a': "[#0F0]",  # green
        '§b': "[#0FF]",  # aqua
        '§c': "[#F00]",  # red
        '§d': "[#FAF]",  # light purple
        '§e': "[#FF0]",  # yellow
        '§f': "[#FFF]",  # white
        '§l': "[#BOLD]",  # bold
        '§m': "[#STRIKETHROUGH]",  # strikethrough
        '§n': "[#UNDERLINE]",  # underline
        '§o': "[#ITALIC]",  # italic
        '§r': "[#RESET]"  # reset
    }

    try:
        json_data = json.loads(json_data)
    except json.JSONDecodeError:
        result = ""
        i = 0
        while i < len(json_data):
            if json_data[i] == '§':
                style_code = json_data[i:i+2]
                if style_code in standard_color_map:
                    result += standard_color_map[style_code]
                    i += 2
                    continue
            result += json_data[i]
            i += 1

        return result

    def parse_extra(extra):
        result = ""
        if isinstance(extra, dict) and "extra" in extra:
            result += parse_extra(extra["extra"])
        elif isinstance(extra, dict):
            color = extra.get("color", "")
            text = extra.get("text", "")

            # 将颜色转换为自定义十六进制颜色标记
            if color.startswith("#"):
                hex_color = color[1:]
                if len(hex_color) == 3:
                    hex_color = ''.join([c * 2 for c in hex_color])
                color_code = f"[#{hex_color.upper()}]"
            else:
                # 标准颜色
                color_code = standard_color_map.get(color, "")

            result += f"{color_code}{text}"
        elif isinstance(extra, list):
            for item in extra:
                result += parse_extra(item)
        else:
            result += str(extra)

        return result

    return parse_extra(json_data)


class ColoredTextImage:
    def __init__(self, text: str, background_color: tuple[int, int, int] = (249, 246, 242), padding: int = 10) -> None:
        """
        初始化一个用于绘制彩色文本图像的对象。
        """
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
        width, height = self._calculate_dimensions(text)
        self.image = Image.new('RGB', (width, height), self.background_color)
        self.draw = ImageDraw.Draw(self.image)
        self.draw_text_with_style(text)

    def _calculate_dimensions(self, text: str) -> tuple[int, int]:
        """
        计算图像的宽度和高度。
        """
        # Create a temporary image and draw object for calculating dimensions
        temp_image = Image.new('RGB', (1, 1))
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
        plain_text = re.sub(r'\[\#[^\]]*\]', '', text)

        max_width = 0
        total_height = 0
        line_height = self.font_size * 1.5

        for line in plain_text.split('\n'):
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

    def draw_text_with_style(self, text: str) -> None:
        """
        使用指定样式绘制文本。

        :param text: 需要绘制的文本字符串。
        """

        bold = italic = underline = strikethrough = False
        current_color = (0, 0, 0)
        line_height = self.font_size * 1.5
        x_offset = 50
        y_offset = 0

        for line in text.split('\n'):
            i = 0
            while i < len(line):
                if line[i] == '[':
                    if line[i:i+7] == '[#BOLD]':
                        bold = True
                        i += 7
                        continue

                    if line[i:i+9] == '[#ITALIC]':
                        italic = True
                        i += 9
                        continue

                    if line[i:i+12] == '[#UNDERLINE]':
                        underline = True
                        i += 12
                        continue

                    if line[i:i+16] == '[#STRIKETHROUGH]':
                        strikethrough = True
                        i += 16
                        continue

                    if line[i:i+8] == '[#RESET]':
                        bold = italic = underline = strikethrough = False
                        current_color = (0, 0, 0)
                        i += 8
                        continue

                    if line[i:i+2] == '[#':
                        close_bracket_index = line.find(']', i)
                        if close_bracket_index != -1:
                            hex_color = line[i+2:close_bracket_index].upper()
                            if len(hex_color) == 3:
                                hex_color = ''.join([c * 2 for c in hex_color])
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

    def save(self, filename: str) -> None:
        """
        将当前图像保存到文件。

        :param filename: 文件名，包括路径和扩展名。
        """
        self.image.save(filename, format='PNG')

    def pic2bytes(self) -> bytes:
        """
        将当前图像转换为字节流。

        :return: 返回一个包含图像数据的字节流。
        """
        byte_io = io.BytesIO()
        self.image.save(byte_io, format='PNG')
        byte_io.seek(0)
        return byte_io.getvalue()