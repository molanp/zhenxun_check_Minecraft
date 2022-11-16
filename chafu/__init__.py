from nonebot import on_command
from services.log import logger
from utils.message_builder import image
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, GroupMessageEvent, Message
from nonebot.typing import T_State
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
__plugin_version__ = 0.7
__plugin_author__ = "molanp"#觉得还是写GitHub名称比较好
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查服",'b查'],
}
__plugin_cd_limit__ = {
    "cd": 10,   
    "rst": "查坏了...再等等吧"
}
##自定义错误信息
error = "\n查服发生了一些错误...\n这绝对不是俺的问题！\n绝对不是！！"
##自定义错误信息
chafu = on_command("查服", priority=5, block=True)

@chafu.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    try:
        ####判断是否存在地址标识，防止有人捣乱##
        content = str(event.get_message()).strip()
        temp = content.find(".")#防君子不防小人
        if temp == (-1):
          end = "\n输入信息有误\n请重新输入"
        else:
           temp = content.find(":")
           ##截取数据##
           if temp == (-1): 
             ip = content[2:].strip()
             port = "25565"
           else:
             ip = content[2:temp].strip()
             temp = temp + 1
             port = content[temp:]
            #组合api#
           url = "https://mcapi.us/server/status?ip=" + ip + "&port=" + port
        #############获取数据######
           data = (await AsyncHttpx.get(url, timeout=5)).json()#若获取无结果，请修改timeout=后的数字
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
           result = f'\n名称：{server["name"]}\n地址：{ip}\n端口：{port}\n延迟：{ms}\n在线：{data["online"]}\nmotd：{data["motd"]}\n人数：{players["now"]}/{players["max"]}\n状态码：{data["status"]}\nFavicon:'
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
        await chafu.send(Message(end), at_sender=True)
        logger.info(
              f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送信息:\n"
            + end 
           )
    except:
      await chafu.send(Message(error), at_sender=True)
      logger.info(error)
      
##以下为基岩服务器查询

bds = on_command("b查", priority=5, block=True)

@bds.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    try:
        content = str(event.get_message()).strip()
        ####判断是否存在地址标识，防止有人捣乱##
        temp = content.find(".")
        if temp == (-1):
          result = "\n输入信息有误\n请检查"
        else:
           temp = content.find(":")
           if temp == (-1): 
             host = content[2:].strip()
             host = f'{host}:19132'
           else: 
             host = content[2:].strip()
          #组合api#
           url = "https://motdbe.blackbe.xyz/api?host=" + host
        #############获取数据######
           data = (await AsyncHttpx.get(url, timeout=5)).json()#若获取无结果，请修改timeout=后的数字
           data = str(data)
           #从网页获取数据#
           data = ast.literal_eval(data) #转换成字典
           ####整理文字###
           result = f'\n版本：{data["version"]}\n地址：{data["host"]}\n延迟：{data["delay"]}ms\nmotd：{data["motd"]}\n人数：{data["online"]}/{data["max"]}\n存档名：{data["level_name"]}\n游戏模式：{data["gamemode"]}\n状态码：{data["status"]}'
        await bds.send(Message(result), at_sender=True)
        logger.info(
         f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送信息:\n"
         + result 
        )
    except:
      await bds.send(Message(error), at_sender=True)
      logger.info(error)
