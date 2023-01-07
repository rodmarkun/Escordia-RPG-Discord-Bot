import file_management
import text as text_module
import discord

async def on_character_not_created(ctx):
    await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

async def on_character_already_created(ctx):
    await ctx.send(f'You already have a character in the world of Escordia, {ctx.author.mention}.')

async def on_character_creation(ctx):
    await ctx.send(f'Welcome, {ctx.author.mention}, to the world of Escordia. We recommend you to play the `!tutorial`.')

async def on_wrong_command(ctx):
    await ctx.send(f'Something went wrong. Did you type the command correctly?')

async def not_in_fight(ctx):
    await ctx.send(f'You are not currently in a fight, {ctx.author.mention}')

async def help_message(ctx):
    command_string = text_module.help_text
    embed = discord.Embed(
        title='Bot Commands',
        description=command_string,
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

async def tutorial_message(ctx):
    embed = discord.Embed(
        title=f'Tutorial',
        description=text_module.tutorial_1,
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

async def players_message(ctx):
    embed = discord.Embed(
        title=f'Players - {ctx.guild.name}',
        description=file_management.get_all_players(),
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)