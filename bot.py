import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$newexpense'):
        expense = Expense("test", "colin", {"thomas":5}, 5)
        embed = expense.printExpense()
        await message.channel.send(embed=embed)

class Expense:
    counter = 0

    def __init__(self, description, payer, owers, totalAmt):
        self.description = description
        self.payer = payer
        self.owers = owers #dict with key payer : value amt
        self.totalAmt = totalAmt
        self.eid = Expense.counter
        Expense.counter += 1

    def printExpense(self):
        embed = discord.Embed(title=self.eid, description=self.description, color=discord.Color.red())
        embed.add_field(name='Payer', value=self.payer, inline=True)
        embed.add_field(name='Total Amount:', value=self.totalAmt, inline=True)
        for pair in self.owers.items():
            embed.add_field(name=pair[0], value=pair[1], inline=False)

        return embed

client.run('NzYzMjc3ODU2ODMzOTI5MjY2.X31X5g.3qvyznwcCfjRN_h9Scjz4syHsNc')
