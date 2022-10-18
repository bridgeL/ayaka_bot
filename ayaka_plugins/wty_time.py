from ayaka import *
import datetime

app = AyakaApp('wty-time')
app.help = '''wty现在几点了
- wty/wt
'''


@app.on_command(['wty', "wt"])
async def test():
    time_i = datetime.datetime.now().timestamp() + 3600*11
    time_s = datetime.datetime.fromtimestamp(time_i).time()
    await app.send(str(time_s).split(".")[0])
