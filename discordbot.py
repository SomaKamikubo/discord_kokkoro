from discord.ext import commands
from os import getenv
import traceback
import random
from googletrans import Translator
import api
import json

bot = commands.Bot(command_prefix='/')
API = api.API()

'#メッセージ受信時に実行される処理'
@bot.event
async def on_message(message):
    '#on_messageイベントの取得とコマンド機能を併用する際に必要な処理'
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send("コマンドの使い方が間違っています。")


@bot.command()
async def HowTo(ctx):
    f = open('readme.txt', 'r', encoding='UTF-8')
    data = f.read()
    await ctx.send(data)
    f.close()


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

@bot.command()
async def t(ctx, *arg):
    tr = Translator()
    en = ''
    for val in arg:
        en += val + ' '
    result = tr.translate(en, src="en", dest="ja").text
    await ctx.send(result)

def printTextFile(arg,pas):
    try:
        arg = int(arg)
    except ValueError:
        return("引数が変かも") 
    if(arg == 0):
        f = open(pas, 'r', encoding='UTF-8')
        data = f.read()
        return data[:-1]
    
    f = open(pas, 'r', encoding='UTF-8')
    datalist = f.readlines()
    f.close()
    return printData(arg,datalist)[:-1]

def printJsonFile(arg,pas):
    try:
        arg = int(arg)
    except ValueError:
        return("引数が変かも")  

    f = open(pas, 'r', encoding='UTF-8')
    json_load = json.load(f)
    f.close()

    if(arg == 0):
        return json_load
    

    datalist =  []
    for i in json_load:
        for j in json_load[i]:
            datalist.append(j)
    return printData(arg,datalist)
    

def printData(arg,datalist):
    if(arg > len(datalist)):
        return "引数が取得したいデータの総数より多いです。"
    result = ""
    for _ in range(arg):
        r = random.randint(1,len(datalist))
        index = r-1 #randientが0を持ってこれないため
        result += datalist[index]
        del datalist[index]
    return result #最後の改行をなくす



@bot.command()
async def smash(ctx,arg=1):
    await ctx.send(printTextFile(arg,'Data/Data_SmaBra/SmashChara.txt'))


@bot.command()
async def apeC(ctx,arg=1):
    await ctx.send(printTextFile(arg,'Data/Data_Apex/ApexChara.txt'))

@bot.command()
async def apeB(ctx,arg=1):
    await ctx.send(printJsonFile(arg,'Data/Data_Apex/ApexBullet.json'))


@bot.command()
async def apeBT(ctx,arg=1,arg2=None):
    f = open('Data/Data_Apex/ApexBullet.json', 'r', encoding='UTF-8')
    json_load = json.load(f)
    f.close()
    try:
        datalist = json_load[arg2]
    except KeyError:
        await ctx.send("正しい武器種を選択してください。") 
        return


    if(arg == 0):
        arg = len(datalist)

    if(int(arg) > len(datalist)):
        await ctx.send("引数が武器の総数より多いです。") 
        return
    result = ""
    for _ in range(int(arg)):
        r = random.randint(1,len(datalist))
        index = r-1 #randientが0を持ってこれないため
        result += datalist[index] + "\n"
        del datalist[index]
    await ctx.send(result)#最後の改行をなくす
    

"""
---------------------
ここからAPI
---------------------
"""
"""
APIkeyの設定
"""
WeatherKey = getenv('WEATHER-API-KEY')
TRNKey = getenv('TRN-API-KEY')
# async def playAPI(ctx,func,*arg):
#     await ctx.send("取得中です")
   
#     res = func(*arg)
#     async for message in ctx.channel.history(limit=1):
#         await message.delete()
#     await ctx.send(res)


@bot.command()
async def dog(ctx):
    await ctx.send("取得中です")
   
    res= API.dog()
    async for message in ctx.channel.history(limit=1):
        await message.delete()
    await ctx.send(res)

@bot.command()
async def address(ctx, arg):
    await ctx.send("取得中です")
   
    res= API.address(arg)
    async for message in ctx.channel.history(limit=1):
        await message.delete()
    await ctx.send(res)

@bot.command()
async def teach(ctx, *arg):
    await ctx.send("取得中です")
   
    res= API.wiki(*arg)
    async for message in ctx.channel.history(limit=1):
        await message.delete()
    await ctx.send(res)

@bot.command()
async def weather(ctx,arg):
    await ctx.send("取得中です")
   
    res= API.weather(WeatherKey,arg)
    async for message in ctx.channel.history(limit=1):
        await message.delete()
    await ctx.send(res)

@bot.command()
async def apex(ctx,arg):
    await ctx.send("取得中です")
   
    res= API.apex(TRNKey,arg)
    async for message in ctx.channel.history(limit=1):
        await message.delete()
    await ctx.send(res)
    

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
