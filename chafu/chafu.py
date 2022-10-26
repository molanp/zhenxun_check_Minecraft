from nonebot import on_regex
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from utils.http_utils import AsyncHttpx
import ast

__zx_plugin_name__ = "我的世界查服"
__plugin_usage__ = """
usage：
    作者:ioew
    我的世界服务器状态查询
    用法：
        查服 [ip]?[端口]<?==>'空格'>
        查服 ip:端口(端口必须五位)
    tips:汉字与ip间可以有空格
""".strip()
__plugin_des__ = "我的世界服务器状态查询"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["查服"]
__plugin_version__ = 0.1
__plugin_author__ = "ioew"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查服"],
}
__plugin_cd_limit__ = {
    "cd": 10,   
    "rst": "查坏了...请等10s恢复"
}

chafu = on_regex(r".{0,10}查服(.*){0,10}", priority=5, block=True)

@chafu.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    n = '查服'
    n = str(n)
    q = str(event.get_message()).strip()
    t = q.find(n)
    if t == (-1):
       u = str(q)
    else:
       s = q[2:].strip()
       s = s[:-6].strip()
       port = q[-5:]
       ip = str(s)
    
    url = "https://mcapi.us/server/status?ip=" + ip + "&port=" + port
####判断端口是否全部为数字，防止有人捣乱####
    temp = str(port.isdigit())
#######################################
    data = (await AsyncHttpx.get(url, timeout=5)).json()
    if temp == "False":
        result = "输入信息不完整\n请重新输入"
        await chafu.send(result)
    else:
        #######获取数据######
        temp = f'{data["players"]}'
        tmp = temp.index("sample")
        tmp = tmp - 3
        tmp = temp[:tmp]
        temp = tmp[1:]
        tmp = temp.index(",")
        tmp = tmp + 1
        q = temp[:tmp]
        tmp = tmp +1
        s = temp[tmp:]
        temp = q + s
###########重构变量##############
        players = "{" + temp + "}"
        players = ast.literal_eval(players)
        temp = f'{data["server"]}'
        temp = ast.literal_eval(temp)
###########字典查询###############
        server = str(temp["name"])
        max = str(players["max"])
        now = str(players["now"])
        ############
        result = "名称：" + server + "\n地址：" + ip + "\n端口：" + port + f'\n在线：{data["online"]}\nmotd：{data["motd"]}\n人数：' + now + "/" + max + f'\n状态码：{data["status"]}'# + "\napi：" + url
        await chafu.send(result)
        logger.info(
           f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送信息:\n"
         + result 
        )
###发送favicon正在编写####
'''
    base0 = str(f'{data["favicon"]}')
    if base0 != "null":
        base = base0[22:]
'''
#######################
