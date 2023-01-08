from nonebot import on_command
from services.log import logger
from utils.message_builder import image
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, GroupMessageEvent, Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from utils.http_utils import AsyncHttpx
from .data_source import *
import ast#, base64

__zx_plugin_name__ = "我的世界查服"
__plugin_usage__ = """
usage：
    我的世界服务器状态查询
    用法：
        查服 [ip]:[端口]
       或
        查服 [ip]
    eg:
        minecheck ip:port
       or
        minecheck ip
      [若不响应消息，请@bot_name]
""".strip()
__plugin_des__ = "用法：查服 ip:port / minecheck ip:port"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["查服","minecheck"]
__plugin_version__ = 0.9
__plugin_author__ = "YiRanEL"#觉得还是写GitHub名称比较好
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查服",'minecheck'],
}
__plugin_cd_limit__ = {
    "cd": 5,   
    "rst": "查坏了...再等等吧"
}

chafu = on_command("查服", aliases={'minecheck'}, priority=5, block=True)


@chafu.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("host", args)  # 如果用户发送了参数则直接赋值

@chafu.got("host", prompt="IP是?")
async def handle_host(host: Message = Arg(), host_name: str = ArgPlainText("host")):
  if "." not in host_name:  # 如果参数不符合要求，则提示用户重新输入
    await chafu.reject(host.template("不知道你服务器的IP在哪里，在你心里吗?"))
  if ":" not in host_name:
    await chafu.reject(host.template("端口呢端口呢端口呢?"))
  result = await get_info(host_name)
  await chafu.finish(result)

async def get_info(host_name: str):
    try:
        host = host_name.strip()
        ip = host.split(':')[0]
        try:
          port = host.split(':')[1]
        except:
          port = '25565'
        finally:
          if len(port) <= 5:
            ms = MineStat(ip,int(port),timeout=1)
            if ms.online:
              #JSON_motd = 'JSON版motd: %s' % ms.motd
              result = f'\n名称：{ms.version}\n协议：{ms.slp_protocol}\n地址：{ip}\n端口：{port}\n延迟：{ms.latency}ms\nmotd：{ms.stripped_motd}\n人数：{ms.current_players}/{ms.max_players}'
              # Bedrock specific attribute:
              if ms.slp_protocol is SlpProtocols.BEDROCK_RAKNET:
                result = f'\n名称：{ms.version}\n协议：{ms.slp_protocol}\n游戏模式：{ms.gamemode}\n地址：{ip}\n端口：{port}\n延迟：{ms.latency}ms\nmotd：{ms.stripped_motd}\n人数：{ms.current_players}/{ms.max_players}'
            else:
              result = 'Server is offline!'
          else:
            result ='你看看这是正经端口吗？'
           ######发送favicon###
           #if status != "error":
             #base0 = str(f'{data["favicon"]}')
             #if base0 != "null":
               #base = base0[22:]
               #img = base64.b64decode(base)
               #end = Message ([
                  #MessageSegment.text(result),
                  #MessageSegment.image(img)
               #])
           #else:
             #end = result
        await chafu.send(Message(result), at_sender=True)
    except BaseException as e:
      error = f"查服发生了一些错误:\n{format(e)}"
      await chafu.send(Message(error), at_sender=True)