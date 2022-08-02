import discord
import os
from discord.ext import commands

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
ENEMY = 'Wolf'

ATTACK_EMOJI = '\U0001F170'
SPELLS_EMOJI = '\U0001F1F8'
COMBOS_EMOJI = '\U0001F1E8'

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='Bot Commands',
        description='Welcome to the help section. Here are all the commands:',
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def start(ctx):
    await ctx.send(f'Welcome, {ctx.author.mention}, to the world of Escordia.')

@bot.command()
async def fight(ctx):
    embed = discord.Embed(
        title=f'Fight - {ctx.author}',
        description=f'You encounter a **{ENEMY}**.\n'
                    f'What will you do?\n\n'
                    f'{ATTACK_EMOJI} - Attack\n'
                    f'{SPELLS_EMOJI} - Spells\n'
                    f'{COMBOS_EMOJI} - Combos',
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url="https://i.postimg.cc/1R65TbDJ/Mountain-Wolf.png")
    embed.set_image(url=ctx.author.avatar_url)
    embed.set_footer(text='HP: 10/10\nMP: 20/20')
    fight_msg = await ctx.send(embed=embed)
    await fight_msg.add_reaction(ATTACK_EMOJI)
    await fight_msg.add_reaction(SPELLS_EMOJI)
    await fight_msg.add_reaction(COMBOS_EMOJI)


bot.run(DISCORD_TOKEN)