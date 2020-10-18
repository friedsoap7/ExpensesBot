import discord
from discord.ext import commands
from discord.ext.commands import Bot

bot = commands.Bot(command_prefix='$')

token = open("t.token")

users = {"Chris", "Colin", "Daniel", "Edward", "Thomas"}

id_to_user = {608015399975649301 : "Colin", 120713932171247617 : "Chris", 206933072078307328 : "Edward", 315890107699691521 : "Thomas", 214191543567908864 : "Daniel"}
user_to_id = {v: k for k, v in id_to_user.items()}

expenses = {}
counter = 1

@bot.event
async def on_ready():
    activity = discord.Game(name="Brawlers")
    await bot.change_presence(activity=activity)
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)



@bot.command(aliases=['ne', 'newexp'])
async def newexpense(ctx, *args):
    if len(args) < 3 or len(args) > 4:
        await ctx.channel.send("Incorrect syntax! Usage: ```$newexpense <description> <date> <total> [name1=amount1,name2=amount2,...]```")
        return

    payer = id_to_user[ctx.author.id]

    description = args[0]
    date = args[1]
    total = args[2]
    owers = {}

    if len(args) == 3:
        for user in users:
            if user != payer:
                owers[user] = round(float(total) / 5, 2)
    else:
        owemap = args[3].split(",")
        for pair in owemap:
            pair = pair.split("=")
            owers[pair[0]] = pair[1]
    newexp = Expense(description, payer, date, owers, total)
    expenses[newexp.eid] = newexp

@bot.command(aliases=['de', 'delexp'])
async def deleteexpense(ctx, arg):
    expenses.pop(int(arg))

@bot.command(aliases=['pay', 'payexp'])
async def payexpense(ctx, arg):
    if expenses[int(arg)] != None:
        expenses[int(arg)].paidlist.append(id_to_user[ctx.author.id])
    else:
        await ctx.channel.send("Invalid expense ID!")

@bot.command(aliases=['pre', 'prexp'])
async def printexpenses(ctx):
    for expense in expenses.values():
        await ctx.channel.send(embed=expense.createEmbed())

@bot.command(aliases=['pme', 'pmyexp'])
async def printmyexpenses(ctx):
    for expense in expenses.values():
        if id_to_user[ctx.author.id] in expense.owers.keys() and id_to_user[ctx.author.id] not in expense.paidlist:
            await ctx.channel.send(embed=expense.createEmbed())

@bot.command(aliases=['io', 'mydebts', 'mydebt', 'md'])
async def whoiowe(ctx):
    owelist = {user: 0 for user in users}
    author = id_to_user[ctx.author.id]
    owelist.pop(author)
    for expense in expenses.values():
        if author in expense.owers.keys():
            owelist[expense.payer] += expense.owers[author]
    embed = discord.Embed(title=author+" owes:", color=discord.Color.blue())
    total = 0
    for user in owelist.keys():
        embed.add_field(name=user+": $"+str(owelist[user]), value="\u2014"*10, inline=False)
        total += owelist[user]
    embed.add_field(name="Total: $"+str(total), value="\u2014"*10, inline=False)
    await ctx.channel.send(embed=embed)

@bot.command(aliases=['om', 'mycredits', 'mycredit', 'mc'])
async def whoowesme(ctx):
    owelist = {user: 0 for user in users}
    author = id_to_user[ctx.author.id]
    owelist.pop(author)
    for expense in expenses.values():
        if author == payer:
            for user in expenses.owers.keys():
                owelist[user] += expense.owers[user]
    embed = discord.Embed(title=author+" is owed:", color=discord.Color.purple())
    total = 0
    for user in owelist.keys():
        embed.add_field(name=user+": $"+str(owelist[user]), value="\u2014"*10, inline=False)
        total += owelist[user]
    embed.add_field(name="Total: $"+str(total), value="\u2014"*10, inline=False)
    await ctx.channel.send(embed=embed)


class Expense:
    def __init__(self, description, payer, date, owers, totalAmt):
        self.description = description
        self.payer = payer
        self.date = date
        self.owers = owers #dict with key payer : value amt
        self.totalAmt = round(float(totalAmt), 2)
        global counter
        self.eid = counter
        self.paidlist = []
        counter += 1

    def payExpense(self, payer):
        self.paidlist.append(payer)

    def createEmbed(self):
        embed = discord.Embed(title=self.eid, description=self.description, color=discord.Color.red())
        embed.add_field(name='Payer', value=self.payer, inline=True)
        embed.add_field(name='Total Amount:', value="$"+str(self.totalAmt), inline=True)
        embed.add_field(name='Date:', value=self.date, inline=True)
        for pair in self.owers.items():
            ower = pair[0]
            amount = "$" + str(round(float(pair[1]), 2))
            paidmessage = "~~" + amount + "~~ Paid"
            if ower not in self.paidlist:
                embed.add_field(name=ower, value=amount, inline=False)
            else:
                embed.add_field(name=ower, value=paidmessage, inline=False)

        return embed

bot.run(token.read(200))
