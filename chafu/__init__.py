from nonebot import on_command
from services.log import logger
from utils.message_builder import image
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, GroupMessageEvent, Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from utils.http_utils import AsyncHttpx
from ping3 import ping
import ast, base64

__zx_plugin_name__ = "我的世界查服"
__plugin_usage__ = """
usage：
    我的世界服务器状态查询
    用法：
      Java服务器：
        查服 [ip]:[端口]
       或
        查服 [ip]
      基岩服务器：
        b查 [ip]:[端口]
       或
        b查 [ip]
      [若不响应消息，请@bot_name]
""".strip()
__plugin_des__ = "用法：查服 ip:port"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["查服","b查"]
__plugin_version__ = 0.9
__plugin_author__ = "YiRanEL"#觉得还是写GitHub名称比较好
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查服",'b查'],
}
__plugin_cd_limit__ = {
    "cd": 5,   
    "rst": "查坏了...再等等吧"
}

chafu_java = on_command("查服", priority=5, block=True)
chafu_bedrock = on_command("b查", priority=5, block=True)


@chafu_java.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("host", args)  # 如果用户发送了参数则直接赋值

@chafu_java.got("host", prompt="IP是?")
async def handle_host(host: Message = Arg(), host_name: str = ArgPlainText("host")):
  if "." not in host_name:  # 如果参数不符合要求，则提示用户重新输入
        # 可以使用平台的 Message 类直接构造模板消息
    await chafu_java.reject(host.template("不知道你服务器的IP在哪里，在你心里吗?"))
  result = await get_info_java(host_name)
  await chafu_java.finish(result)

async def get_info_java(host_name: str):
    try:
        host = host_name.strip()
        if 1==1:
          ip = host.split(':')[0]
          try:
            port = host.split(':')[1]
          except:
            port = '25565'
          finally:
            #组合api#
           url = f"https://mcapi.us/server/status?ip={ip}&port={port}"
        #############获取数据######
           data = (await AsyncHttpx.get(url, timeout=5)).json()
           ##获取延迟####
           ms = ping(ip)
           if ms != None:
             ms = int(ms * 1000)
           else:
             ms = "超时"
           ms = f'{ms}ms'
           ##获取延迟####
           ##重构变量##
           data = str(data)
           data = ast.literal_eval(data)
           server = f'{data["server"]}'
           players = f'{data["players"]}'
           status = f'{data["status"]}'
           #
           server = ast.literal_eval(server)
           players = ast.literal_eval(players)
           ####整理文字###
           result = f'\n名称：{server["name"]}\n类型：JAVA\n地址：{ip}\n端口：{port}\n延迟：{ms}\n在线：{data["online"]}\nmotd：{data["motd"]}\n人数：{players["now"]}/{players["max"]}\n状态码：{data["status"]}\nFavicon:'
           ######发送favicon###
           if status != "error":
             base0 = str(f'{data["favicon"]}')
             if base0 != "null":
               base = base0[22:]
               img = base64.b64decode(base)
               end = Message ([
                  MessageSegment.text(result),
                  MessageSegment.image(img)
               ])
           else:
             end = result
        await chafu_java.send(Message(end), at_sender=True)
    except BaseException as e:
      error = f"查服发生了一些错误:\n{e.__dict__['_request']}"
      await chafu_java.send(Message(error), at_sender=True)
      
##以下为基岩服务器查询

@chafu_bedrock.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("host", args)  # 如果用户发送了参数则直接赋值

@chafu_bedrock.got("host", prompt="IP是?")
async def handle_host(host: Message = Arg(), host_name: str = ArgPlainText("host")):
  if "." not in host_name:  # 如果参数不符合要求，则提示用户重新输入
        # 可以使用平台的 Message 类直接构造模板消息
    await chafu_bedrock.reject(host.template("不知道你服务器的IP在哪里，在你心里吗?"))
  result = await get_info_bedrock(host_name)
  await chafu_bedrock.finish(result)

async def get_info_bedrock(host_name: str):
    try:
        host = host_name.strip()
        if 1==1:
          ip = host.split(':')[0]
          try:
            port = host.split(':')[1]
          except:
            port = '19132'
          finally:
          #组合api#
           url = f"https://api.imlazy.ink/mcapi/?type=json&be=true&host={ip}&port={port}"
        ########获取数据######
           data = (await AsyncHttpx.get(url, timeout=5)).json()#若获取无结果，请修改timeout=后的数字
           data = str(data)
           #从网页获取数据#
           data = ast.literal_eval(data) #转换成字典
            ##获取延迟####
           ms = ping(ip)
           if ms != None:
             ms = int(ms * 1000)
           else:
             ms = "超时"
           ##获取延迟####
           ####整理文字###
           result = f'\n版本：{data["version"]}\n类型：Bedrock_server\n地址：{data["host"]}\n端口：{port}\n延迟：{ms}ms\nmotd：{data["motd"]}\n人数：{data["players_online"]}/{data["players_max"]}\n状态：{data["status"]}'#\n平台：{data["platform"]}\n存档名：{data["map"]}\n游戏类型：{data["gametype"]}
        await chafu_bedrock.send(Message(result), at_sender=True)
    except BaseException as e:
      error = f"查服发生了一些错误:\n{e.__dict__['_request']}"
      await chafu_bedrock.send(Message(error), at_sender=True)