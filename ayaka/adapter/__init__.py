import uvicorn
from .onebot import MessageEvent, GroupMessageEvent, Message, MessageSegment, Bot
from .bot import on_event, on_connect, on_send
from .app import server_app
from .logger import logger

# 启动服务
def run(host="127.0.0.1", port=19900, reload=True):
    uvicorn.run(
        app=f"{__name__}:server_app",
        host=host,
        port=port,
        reload=reload,
    )
