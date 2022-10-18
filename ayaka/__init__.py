'''安全起见，避免变量冲突'''
from .ayaka import AyakaApp, AyakaStorage, get_new_page
from .onebot.v11 import Message, MessageSegment
from .logger import logger
from .driver import run

# 初始化内置插件
from . import ayaka_master
