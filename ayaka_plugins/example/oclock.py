'''
    整点报时
'''
import datetime
from ayaka import AyakaApp
from random import choice, randint

app = AyakaApp("整点报时")

data = app.plugin_storage("data").load()


def divide(n: int):
    if n < 10:
        return [n]

    if n < 20:
        div_cnt = randint(1, 2)
    else:
        div_cnt = randint(1, 3)

    nums = []
    for i in range(div_cnt):
        min_left = 2 * (div_cnt - i)
        num = randint(2, n - min_left)
        n -= num
        nums.append(num)
    nums.append(n)
    return nums


def create(n: int):
    nums = divide(n)
    words = []
    for num in nums:
        word = choice(data[str(num)])
        words.append(word)
    return "".join(words)


@app.on_interval(3600, m=0, s=0)
async def every_hour():
    n = datetime.datetime.now().time().hour
    if n == 0:
        n = 24
    await app.t_send(bot_id=2317709898, group_id=666214666, message=create(n))


@app.on_everyday(h=23, m=59, s=59)
async def every_day():
    await app.t_send(bot_id=2317709898, group_id=666214666, message="呃呃呃一天要结束了")
