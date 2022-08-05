import discord
import os
from discord.ext import commands

import combat
import enemies
import player
import json
import fight as fight_module
import file_management
import random

import skills

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
    command_string = '!help - Display all commands\n' \
                     '!start - Create a player in Escordia RPG\n' \
                     '!profile - Check your current profile and stats\n' \
                     '!fight - Fight against a monster\n' \
                     '!attack - Perform a normal attack against your opponent\n' \
                     '!spells - See a list with all of your spells\n' \
                     '!spells [number] - Cast a certain spell\n' \
                     '!heal - Fully heal your character\n' \
                     '!mana - Fully replenish your mana'
    embed = discord.Embed(
        title='Bot Commands',
        description= command_string,
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def start(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
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
                player_obj = player.createPlayer(res)
                player_description = f'**Stats**: {player_obj.stats}\n' \
                                     f'**Lvl**: {player_obj.lvl}\n' \
                                     f'**Xp**: {player_obj.xp}\n' \
                                     f'**Xp to level up**: {player_obj.xpToNextLvl}\n' \
                                     f'**Alive**: {player_obj.alive}\n' \
                                     f'**Aptitudes**: {player_obj.aptitudes}\n' \
                                     f'**Aptitude points**: {player_obj.aptitudePoints}\n' \
                                     f'**Equipment**: {player_obj.equipment}\n' \
                                     f'**Money**: {player_obj.money}\n' \
                                     f'**Combos**: {player_obj.combos}\n' \
                                     f'**Spells**: {player_obj.spells}\n'
                embed = discord.Embed(
                    title=f'Profile - {ctx.author.name}',
                    description=player_description,
                    color = discord.Colour.red()
                )
                embed.set_image(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
    await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@bot.command()
async def fight(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    enemy = random.choice(enemies.enemies_by_zones[1])()

    in_fight = file_management.check_if_in_fight(ctx.author.name)
    if in_fight is not None:
        await ctx.send(f'You are already in a fight against **{in_fight.enemy.name}**, {ctx.author.mention}')
        return

    if player_obj is not None:
        fight_msg = await ctx.send(embed=embed_fight_msg(ctx=ctx, enemy=enemy, player_obj=player_obj))

        fight_obj = fight_module.Fight(player=player_obj, enemy=enemy, fight_msg=fight_msg.id)
        file_management.write_fight(fight_obj)
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@bot.command()
async def attack(ctx):
    in_fight = file_management.check_if_in_fight(ctx.author.name)
    if in_fight is None:
        await ctx.send(f'You are not currently in a fight, {ctx.author.mention}')
    else:
        fight_text = in_fight.normal_attack()
        await ctx.send(fight_text)

        file_management.delete_fight(ctx.author.name)
        if not in_fight.enemy.alive:
            await win_fight(ctx, in_fight)
        else:
            file_management.write_fight(in_fight)
            await ctx.send(embed=embed_fight_msg(ctx=ctx, enemy=in_fight.enemy, player_obj=in_fight.player))

@bot.command()
async def spells(ctx, arg=0):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        if arg == 0:
            spell_str = f"**{ctx.author.name}'s Spells:**\n"
            i = 1
            for spell in player_obj.spells:
                spell_str += f"{i} - {spell['name']}\n"
                i += 1
            await ctx.send(spell_str)
        else:
            fight_obj = file_management.check_if_in_fight(ctx.author.name)
            if fight_obj is not None:
                spell = skills.createSpell(fight_obj.player.spells[arg-1])
                info_str = fight_obj.spell(spell)
                file_management.delete_fight(ctx.author.name)
                await ctx.send(info_str)
                if fight_obj.enemy.alive:
                    file_management.write_fight(fight_obj)
                    await ctx.send(embed=embed_fight_msg(ctx=ctx, enemy=fight_obj.enemy, player_obj=fight_obj.player))
                else:
                    await win_fight(ctx, in_fight=fight_obj)
            else:
                await ctx.send(f'You are not currently in a fight, {ctx.author.mention}')
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')


@bot.command()
async def heal(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    in_fight = file_management.check_if_in_fight(ctx.author.name)

    if in_fight is None and player_obj is not None:
        combat.fully_heal(player_obj)
        file_management.delete_player(player_obj.name)
        file_management.write_player(player_obj)
        await ctx.send(f'{player_obj.name}, you have fully healed.')

@bot.command()
async def mana(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    in_fight = file_management.check_if_in_fight(ctx.author.name)

    if in_fight is None and player_obj is not None:
        combat.fully_recover_mp(player_obj)
        file_management.delete_player(player_obj.name)
        file_management.write_player(player_obj)
        await ctx.send(f'{player_obj.name}, you have fully recovered your MP.')

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

async def win_fight(ctx, in_fight):
    in_fight.player.add_exp(in_fight.enemy.xpReward)
    in_fight.player.add_money(in_fight.enemy.goldReward)
    file_management.delete_player(in_fight.player.name)
    file_management.write_player(in_fight.player)
    await ctx.send(
        embed=embed_victory_msg(ctx=ctx, enemy=in_fight.enemy, player_obj=in_fight.player, xp=in_fight.enemy.xpReward,
                                gold=in_fight.enemy.goldReward))

def embed_victory_msg(ctx, enemy, player_obj, xp, gold):
    embed = discord.Embed(
        title=f'Victory!',
        description=f'{SPARKLER_EMOJI} **{ctx.author.name}** has slain a **{enemy.name}** {SPARKLER_EMOJI}\nYou earn {xp}xp and {gold} gold.',
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url=enemy.imageUrl)
    embed.set_image(url=ctx.author.avatar_url)
    return embed

bot.run(DISCORD_TOKEN)