from discord.ext import commands
from os import getenv
import traceback
import random
'#from googletrans import Translator'
import requests
'#import json'
'#import urllib.request as req'

bot = commands.Bot(command_prefix='/')

'#メッセージ受信時に実行される処理'
@bot.event
async def on_message(message):
    '#on_messageイベントの取得とコマンド機能を併用する際に必要な処理'
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def helpp(ctx):
    f = open('readme.txt', 'r', encoding='UTF-8')
    data = f.read()
    await ctx.send(data)
    f.close()


@bot.command()
async def print(ctx, *, arg):
    await ctx.send(arg)

@bot.command()
async def prints(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(arguments)


@bot.command()
async def r(ctx, *arg):
    for i in arg:
        try:
            int(i)
        except ValueError:
            await ctx.send("randomの引数はintのみです。")
            return

    if(len(arg) == 1):
        result = random.randint(1, int(arg[0]) + 1)
        await ctx.send(result)
    elif(len(arg) == 2):
        result = random.randint(int(arg[0]), int(arg[1]) + 1)
        await ctx.send(result)
    elif(len(arg) == 3):
        result = random.randrange(int(arg[0]), int(arg[1]) + 1, int(arg[2]))
        await ctx.send(result)
    else:
        await ctx.send("引数が多すぎます")

@bot.command()
async def rw(ctx, amount, *arg):
    try:
        int(amount)
        random.sample(arg, int(amount))
    except ValueError:
        await ctx.send("「第一引数が数字でない」か「取り出す単語の数が実際の単語の数より多い」可能性があります。")
        return
    result = ','.join(random.sample(arg, int(amount)))
    await ctx.send(result)

@bot.command()
async def cw(ctx, arg):
    result = len(arg)
    await ctx.send("{}文字です。".format(result))

# @bot.command()
# async def t(ctx, *arg):
#     tr = Translator()
#     en = ''
#     for val in arg:
#         en += val + ' '
#     result = tr.translate(en, src="en", dest="ja").text
#     await ctx.send(result)

@bot.command()
async def address(ctx, arg):
    url = 'https://api.zipaddress.net/?zipcode={}'.format(arg)
    try:
        response = requests.get(url)
        response.raise_for_status()     # ステータスコード200番台以外は例外とする
    except requests.exceptions.RequestException as e:
        print("Error:{}".format(e))
    data = response.json()
    await ctx.send(data['data']['fullAddress'])


# @bot.command()
# async def weather(ctx):
#     # URLや保存ファイル名を指定
#     url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/010000.json'
#     filename = 'tenki.json'
#     # ダウンロード
#     req.urlretrieve(url, filename)
#     with open('tenki.json', 'r', encoding="UTF-8") as f:
#         data = json.load(f)

#     for area in data:
#         name = area['name']
#         await ctx.send("[", name, "]")
#         for ts in area['srf']['timeSeries']:
#             times = [n for n in ts['timeDefines']]
#             if 'weathers' in ts['areas']:
#                 for i,v in enumerate(ts['areas']['weathers']):
#                     await ctx.send(times[i], ":", v)
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
