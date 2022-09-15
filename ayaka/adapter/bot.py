import json
import asyncio
from fastapi import WebSocket
from collections import defaultdict
from typing import Any, Callable, Awaitable, Dict, List
from .onebot import Bot, FastAPIWebSocket, Event, json_to_event
from .app import server_app
from .logger import logger


def on_send(func: Callable[[Bot, str, dict], Awaitable]):
    async def _func(bot: Bot, api: str, data: dict):
        if api not in ["send_msg", "send_group_msg", "send_private_msg", "send_group_forward_msg"]:
            return
        await func(bot, api, data)
    Bot.on_call(_func)


on_connect_calls: List[Callable[[Bot], Awaitable]] = []


def on_connect(func: Callable[[Bot], Awaitable]):
    on_connect_calls.append(func)


@server_app.websocket("/ayakabot")
async def endpoint(websocket: WebSocket):
    self_id = websocket.headers.get("x-self-id")
    ws = FastAPIWebSocket(websocket)
    bot = Bot(ws, self_id)

    # 建立ws连接
    await ws.accept()

    for call in on_connect_calls:
        await call(bot)

    try:
        # 监听循环
        while True:
            data = await ws.receive()
            json_data = json.loads(data)
            # 将json解析为对应的event
            event = json_to_event(json_data)

            if not event:
                continue

            asyncio.create_task(deal(bot, event))

    except:
        logger.exception("连接中断")
    finally:
        # 结束ws连接
        await ws.close()


class PriorityCall:
    def __init__(self, priority, call: Callable[[Bot, Event], Awaitable]) -> None:
        self.priority = priority
        self.call = call


cls_calls: Dict[Any, List[PriorityCall]] = defaultdict(list)


def on_event(cls, priority=5):
    '''输入事件类型，注册处理回调

    priority越小，优先级越高'''
    def decorator(call: Callable[[Bot, Event], Awaitable]):
        cls_calls[cls].append(PriorityCall(priority, call))
    return decorator


async def deal(bot: Bot, event: Event):
    tasks = []
    for cls, calls in cls_calls.items():
        if isinstance(event, cls):
            calls.sort(key=lambda x: x.priority)
            for call in calls:
                task = asyncio.create_task(call.call(bot, event))
                tasks.append(task)

    try:
        await asyncio.gather(*tasks)
    except:
        logger.exception("执行event处理回调时发生未知错误")
