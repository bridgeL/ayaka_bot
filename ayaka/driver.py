import json
import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket
from typing import Callable, Awaitable, List

from .logger import logger
from .onebot.v11 import Bot, FastAPIWebSocket, json_to_event, MessageEvent

app = FastAPI()


class Driver:
    on_connect_calls: List[Callable[[Bot], Awaitable]] = []
    on_disconnect_calls: List[Callable[[Bot], Awaitable]] = []
    deal_event = None

    def deal(self, bot, event):
        if self.deal_event:
            if isinstance(event, MessageEvent):
                asyncio.create_task(self.deal_event(bot, event))

    async def bot_connect(self, bot: Bot):
        ts = []
        for call in self.on_connect_calls:
            t = asyncio.create_task(call(bot))
            ts.append(t)
        await asyncio.gather(*ts)

    def on_bot_connect(self, func: Callable[[Bot], Awaitable]):
        self.on_connect_calls.append(func)

    async def bot_disconnect(self, bot: Bot):
        ts = []
        for call in self.on_disconnect_calls:
            t = asyncio.create_task(call(bot))
            ts.append(t)
        await asyncio.gather(*ts)

    def on_bot_disconnect(self, func: Callable[[Bot], Awaitable]):
        self.on_disconnect_calls.append(func)

    def on_startup(self, func):
        app.on_event("startup")(func)

    def on_shutdown(self, func):
        app.on_event("shutdown")(func)


driver = Driver()


# 启动服务
def run(host="127.0.0.1", port=19900, reload=True):
    uvicorn.run(
        app=f"{__name__}:app",
        host=host,
        port=port,
        reload=reload,
    )


@app.websocket("/ayakabot")
async def endpoint(websocket: WebSocket):
    self_id = websocket.headers.get("x-self-id")
    ws = FastAPIWebSocket(websocket)
    bot = Bot(ws, self_id)

    # 建立ws连接
    await ws.accept()
    await driver.bot_connect(bot)

    try:
        # 监听循环
        while True:
            data = await ws.receive()
            json_data = json.loads(data)
            # 将json解析为对应的event
            event = json_to_event(json_data)

            if not event:
                continue

            driver.deal(bot, event)

    except:
        logger.exception("连接中断")
    finally:
        # 结束ws连接
        await driver.bot_disconnect(bot)
        await ws.close()
