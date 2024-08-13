from typing import List, Tuple
import re
import ujson as json
import dns.resolver


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
def parse_minecraft_colors(motd: str) -> List[Tuple[str, Tuple[int, int, int]]]:
    """
    Parses Minecraft color codes into RGB tuples and extracts the text.
    
    Parameters:
        motd (str): The MOTD string containing Minecraft color codes.
    
    Returns:
        List[Tuple[str, Tuple[int, int, int]]]: A list of tuples where each tuple contains the text and its corresponding RGB color.
    """
    color_codes = {
        "§0": (0, 0, 0),
        "§1": (0, 0, 170),
        "§2": (0, 170, 0),
        "§3": (0, 170, 170),
        "§4": (170, 0, 0),
        "§5": (170, 0, 170),
        "§6": (255, 170, 0),
        "§7": (170, 170, 170),
        "§8": (85, 85, 85),
        "§9": (85, 85, 255),
        "§a": (85, 255, 85),
        "§b": (85, 255, 255),
        "§c": (255, 85, 85),
        "§d": (255, 85, 255),
        "§e": (255, 255, 85),
        "§f": (255, 255, 255),
    }
    
    parsed_text = []
    current_color = (0, 0, 0)  # Default white color
    i = 0
    while i < len(motd):
        if motd[i:i+2] in color_codes:
            current_color = color_codes[motd[i:i+2]]
            i += 2
        else:
            parsed_text.append((motd[i], current_color))
            i += 1
    
    return parsed_text

def parse_json_colors(json_data: str) -> List[Tuple[str, Tuple[int, int, int]]]:
    """
    Parses JSON chat components into RGB tuples and extracts the text.
    
    Parameters:
        json_data (str): The JSON string containing chat components.
    
    Returns:
        List[Tuple[str, Tuple[int, int, int]]]: A list of tuples where each tuple contains the text and its corresponding RGB color.
    """
    data = json.loads(json_data)
    parsed_text = []
    
    for component in data.get('extra', []):
        color_name = component.get('color', 'white')
        color = {
            "black": (0, 0, 0),
            "dark_blue": (0, 0, 170),
            "dark_green": (0, 170, 0),
            "dark_aqua": (0, 170, 170),
            "dark_red": (170, 0, 0),
            "dark_purple": (170, 0, 170),
            "gold": (255, 170, 0),
            "gray": (170, 170, 170),
            "dark_gray": (85, 85, 85),
            "blue": (85, 85, 255),
            "green": (85, 255, 85),
            "aqua": (85, 255, 255),
            "red": (255, 85, 85),
            "light_purple": (255, 85, 255),
            "yellow": (255, 255, 85),
            "white": (255, 255, 255),
        }.get(color_name, (0, 0, 0))
        
        text = component.get('text', '')
        parsed_text.append((text, color))
    
    return parsed_text