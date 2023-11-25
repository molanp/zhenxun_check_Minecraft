from nonebot import on_command
from services.log import logger
from nonebot.adapters.onebot.v11 import (
  MessageSegment,
  Message)
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from configs.config import Config
from .data_source import *
import base64, os, ujson, dns.resolver, traceback, sys

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)

dns.resolver.default_resolver.nameservers = ['223.5.5.5', '1.1.1.1']

__zx_plugin_name__ = "我的世界查服"
__plugin_usage__ = """
usage：
    我的世界服务器状态查询
    用法：
        查服 [ip]:[端口] / 查服 [ip]
        设置语言 Chinese
        当前语言
        语言列表
    eg:
        mcheck ip:port / mcheck ip
        set_lang English
        lang_now
        lang_list
""".strip()
__plugin_des__ = "用法：查服 ip:port / mcheck ip:port"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["查服/mcheck","设置语言/set_lang","当前语言/lang_now","语言列表/lang_list"]
__plugin_version__ = 1.5
__plugin_author__ = "molanp"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查服",'mcheck','设置语言','set_lang','当前语言','lang_now',"语言列表","lang_list"],
}
__plugin_configs__ = {
    "JSON_BDS": {"value": False, "help": "基岩版查服是否显示json版motd|Bedrock Edition checks whether the JSON version of MODD is displayed", "default_value": False},
    "JSON_JAVA": {"value": False, "help": "JAVA版查服是否显示json版motd|Java Edition checks whether the JSON version of motd is displayed", "default_value": False},
    "LANGUAGE": {"value": "Chinese", "help": "Change the language(Chinese , English etc.)", "default_value": "Chinese"}
}

def readInfo(file):
    with open(os.path.join(path, file), "r", encoding="utf-8") as f:
        return ujson.loads((f.read()).strip())
        
def resolve_srv(hostname):
    ip = hostname.split(':')[0]
    try:
        port = int(hostname.split(':')[1])
    except:
        port = 0
    try:
        # 解析 SRV 记录
        result = dns.resolver.query('_minecraft._tcp.' + ip, 'SRV', raise_on_no_answer=False)
        
        # 获取真正的地址和端口
        for rdata in result:
            address = str(rdata.target).strip('.')
            if(port == 0):
              port = rdata.port
            return [address, port]
    except dns.resolver.NXDOMAIN:
        pass
    
    # 如果没有找到 SRV 记录，则返回原始的地址和默认端口
    return [ip,port]

path = os.path.dirname(__file__)
lang = Config.get_config("mc_check", "LANGUAGE")
if lang == None: 
  lang = "Chinese"
lang_data = readInfo("language.json")

check = on_command("查服", aliases={'mcheck'}, priority=5, block=True)
lang_change = on_command("设置语言",aliases={'set_lang'},priority=5,block=True)
lang_now = on_command("当前语言",aliases={'lang_now'},priority=5,block=True)
lang_list = on_command("语言列表", aliases={'lang_list'}, priority=5, block=True)

@check.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("host", args)

@check.got("host", prompt="IP?")
async def handle_host(host: Message = Arg(), host_name: str = ArgPlainText("host")):
  if "." not in host_name:
    await check.finish(host.template(lang_data[lang]["where_ip"]),at_sender=True)
  if len(host_name.strip().split(':')) == 2:
    port = host_name.strip().split(':')[1]
    if not port.isdigit() or not (0 <= int(port) <= 65535):
       await check.finish(lang_data[lang]["where_port"],at_sender=True)
  await get_info(host_name)

async def get_info(host_name: str):
    try:
        host = host_name.strip()
        ip = host.split(':')[0]
        srv = resolve_srv(host)
        ms = MineStat(srv[0], srv[1], timeout=1)
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
            result = f'\n{lang_data[lang]["version"]}{ms.version}\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}\n{lang_data[lang]["address"]}{ip}\n{lang_data[lang]["port"]}{ms.port}\n{lang_data[lang]["delay"]}{ms.latency}ms\n{lang_data[lang]["motd"]}{ms.stripped_motd}\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}\n{lang_data[lang]["status"]}{status}'
          # Bedrock specific attribute:
          #if ms.gamemode:
          if 'BEDROCK' in str(ms.slp_protocol):
            if Config.get_config("mc_check", "JSON_BDS"):
              result = f'\n{lang_data[lang]["version"]}{ms.version}\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}\n{lang_data[lang]["gamemode"]}{ms.gamemode}\n{lang_data[lang]["address"]}{ip}\n{lang_data[lang]["port"]}{ms.port}\n{lang_data[lang]["delay"]}{ms.latency}ms\n{lang_data[lang]["motd"]}{ms.motd}\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}\n{lang_data[lang]["status"]}{status}'
            else:
              result = f'\n{lang_data[lang]["version"]}{ms.version}\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}\n{lang_data[lang]["gamemode"]}{ms.gamemode}\n{lang_data[lang]["address"]}{ip}\n{lang_data[lang]["port"]}{ms.port}\n{lang_data[lang]["delay"]}{ms.latency}ms\n{lang_data[lang]["motd"]}{ms.stripped_motd}\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}\n{lang_data[lang]["status"]}{status}'
          # Send favicon
          if ms.favicon_b64 != None and ms.favicon_b64 != "":
            try:
              base0 = str(ms.favicon_b64)
              if base0 != None and base0 != '':
                base = base0[22:]
                img = base64.b64decode(base)
            except:
              pass
            else:
                result = Message ([
                MessageSegment.text(f'{result}favicon:'),
                MessageSegment.image(img)
                ])
        else:
          result = f'{lang_data[lang]["offline"]}'
    except BaseException as e:
      error_type = type(e).__name__  # 获取错误类型名称
      error_message = str(e)  # 获取错误信息
      #error_traceback = traceback.extract_tb(sys.exc_info()[2])[-2]  # 获取函数 b() 的堆栈跟踪信息

      result = f'ERROR:\nType: {error_type}\nMessage: {error_message}'#\nLine: {error_traceback.lineno}\nFile: {error_traceback.filename}\nFunction: {error_traceback.name}'
      logger.error(result)
    await check.send(Message(result), at_sender=True)
@lang_change.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("lang_", args)

@lang_change.got("lang_", prompt="Language?")
async def handle_host(lang_: Message = Arg(), language_name: str = ArgPlainText("lang_")):
  result = await change(language_name)
  await lang_change.finish(Message(result),at_sender=True)

async def change(language:str):
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
  await lang_now.send(Message(f' Language: {lang}.'),at_sender=True)

@lang_list.handle()
async def _():
  i = '\n'.join(list(lang_data.keys()))
  await lang_list.send(Message(f"Language:\n{i}"),at_sender=True)