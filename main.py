import discord
import os
from discord.ext import commands

import enemies
import player
import json
import fight as fight_module

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
ENEMY = 'Wolf'

ATTACK_EMOJI = '\U0001F170'
SPELLS_EMOJI = '\U0001F1F8'
COMBOS_EMOJI = '\U0001F1E8'
RED_CIRCLE_EMOJI = '\U0001F534'
SPARKLER_EMOJI = '\U0001F387'

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
    player_obj = check_if_exists(ctx.author.name)
    if player_obj is not None:
        await ctx.send(f'You already have a character in the world of Escordia, {ctx.author.mention}.')
    else:
        create_player = player.Player(ctx.author.name)
        with open("players.txt", "a") as file:
            file.write(create_player.toJSON() + '\n')
        await ctx.send(f'Welcome, {ctx.author.mention}, to the world of Escordia.')

@bot.command()
async def profile(ctx):
    with open("players.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['name'] == ctx.author.name:
                embed = discord.Embed(
                    title=f'Profile - {ctx.author.name}',
                    description=res,
                    color = discord.Colour.red()
                )
                embed.set_image(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
    await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@bot.command()
async def fight(ctx):
    player_obj = check_if_exists(ctx.author.name)
    enemy = enemies.Wolf()

    in_fight = check_if_in_fight(ctx.author.name)
    if in_fight is not None:
        await ctx.send(f'You are already in a fight against **{in_fight.enemy.name}**, {ctx.author.mention}')
        return

    if player_obj is not None:
        fight_msg = await ctx.send(embed=embed_fight_msg(ctx=ctx, enemy=enemy, player_obj=player_obj))

        fight_obj = fight_module.Fight(player=player_obj, enemy=enemy, fight_msg=fight_msg.id)
        write_fight(fight_obj)
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@bot.command()
async def attack(ctx):
    in_fight = check_if_in_fight(ctx.author.name)
    if in_fight is None:
        await ctx.send(f'You are not currently in a fight, {ctx.author.mention}')
    else:
        in_fight.normal_attack()

        delete_fight(ctx.author.name)
        if not in_fight.enemy.alive:
            await ctx.send(embed=embed_victory_msg(ctx=ctx, enemy=in_fight.enemy, player_obj=in_fight.player))
        else:
            write_fight(in_fight)
            await ctx.send(embed=embed_fight_msg(ctx=ctx, enemy=in_fight.enemy, player_obj=in_fight.player))

def embed_fight_msg(ctx, enemy, player_obj):
    embed = discord.Embed(
        title=f'Fight - {ctx.author}',
        description=f'You are fighting a **{enemy.name}** [HP:{enemy.stats["hp"]}].\n'
                    f'What will you do?\n\n'
                    f'{RED_CIRCLE_EMOJI} Attack - !attack\n'
                    f'{RED_CIRCLE_EMOJI} Spells - !spells\n'
                    f'{RED_CIRCLE_EMOJI} Combos - !combos',
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url=enemy.imageUrl)
    embed.set_image(url=ctx.author.avatar_url)
    embed.set_footer(
        text=f'{player_obj.name}\nHP: {player_obj.stats["hp"]}/{player_obj.stats["maxHp"]}\nMP: {player_obj.stats["mp"]}/{player_obj.stats["maxMp"]}')
    return embed

def embed_victory_msg(ctx, enemy, player_obj):
    embed = discord.Embed(
        title=f'Victory!',
        description=f'{SPARKLER_EMOJI} **{ctx.author.name}** has slain a **{enemy.name}** {SPARKLER_EMOJI}',
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url=enemy.imageUrl)
    embed.set_image(url=ctx.author.avatar_url)
    return embed

def check_if_exists(player_name):
    with open("players.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['name'] == player_name:
                return player.createPlayer(res)
    return None

def delete_fight(player_name):
    with open("fights.txt", "r") as file:
        lines = file.readlines()
    with open("fights.txt", "w") as file:
        for line in lines:
            res = json.loads(line)
            if res['player']['name'] != player_name:
                file.write(line)

def write_fight(fight_obj):
    with open("fights.txt", "a") as file:
        file.write(fight_obj.toJSON() + '\n')

def check_if_in_fight(player_name):
    with open("fights.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['player']['name'] == player_name:
                return fight_module.createFight(res)
    return None

bot.run(DISCORD_TOKEN)