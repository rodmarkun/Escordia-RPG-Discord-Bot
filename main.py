import discord
import os
from discord.ext import commands
from StringProgressBar import progressBar

import combat
import inventory as player_inv
import player
import items
import json
import fight as fight_module
import file_management
import random
from area import areas

import skills

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
ENEMY = 'Wolf'

ATTACK_EMOJI = '\U0001F170'
SPELLS_EMOJI = '\U0001F1F8'
COMBOS_EMOJI = '\U0001F1E8'
RED_CIRCLE_EMOJI = '\U0001F534'
SPARKLER_EMOJI = '\U0001F387'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.command()
async def help(ctx):
    command_string = '!help - Display all commands\n' \
                     '!start - Create a player in Escordia RPG\n' \
                     '!profile - Check your current profile and stats\n' \
                     '!profile [player name] - Show profile of a certain player\n' \
                     '!aptitudes - Show your current aptitudes\n' \
                     '!aptitudes [aptitude] [points] - Spend points on upgrading aptitudes\n' \
                     '!area - Show info about your current area \n' \
                     '!fight - Fight against a monster in your area\n' \
                     '!attack - Perform a normal attack against your opponent\n' \
                     '!spells - See a list with all of your spells\n' \
                     '!spells [number] - Cast a certain spell\n' \
                     '!heal - Fully heal your character\n' \
                     '!mana - Fully replenish your mana\n' \
                     '!players - Show all players of Escordia RPG\n'
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
async def area(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        current_area = areas[player_obj.currentArea - 1]
        await ctx.send(f'You are currently in **{current_area.name}** (area {current_area.number})\n')

@bot.command()
async def boss(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        current_area = areas[player_obj.currentArea - 1]
        await begin_fight(ctx=ctx, player=player_obj, enemy=current_area.boss())


@bot.command()
async def players(ctx):
    players_string = ''
    with open("players.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            players_string += res['name'] + '\n'
    embed = discord.Embed(
        title=f'Players - {ctx.guild.name}',
        description=players_string,
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@bot.command()
async def profile(ctx, arg=None):
    with open("players.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            search = ctx.author.name
            if arg is not None:
                search = arg
            if res['name'] == search:
                player_obj = player.createPlayer(res)
                embed = discord.Embed(
                    title=f'Profile - {player_obj.name}',
                    description=player_obj.show_info(),
                    color = discord.Colour.red()
                )
                fetched_user = discord.utils.get(ctx.guild.members, name=search)
                embed.set_image(url=fetched_user.avatar_url)
                await ctx.send(embed=embed)
                return
    if arg is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        await ctx.send(f'User does not have a character in Escordia yet. Make sure to just type the player\'s name after !profile. You can see current players in !players')

@bot.command()
async def equip(ctx, arg=None):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        if arg is None:
            await ctx.send(f'You need to provide the item index from your inventory to be able to equip it.')
        else:
            # try:
                if len(player_obj.inventory.items) >= int(arg):
                    info = player_obj.equip_item(player_obj.inventory.items[int(arg)-1])
                    await ctx.send(info)
                    file_management.delete_player(ctx.author.name)
                    file_management.write_player(player_obj)
                else:
                    await ctx.send(f'There is no item with that index in your inventory.')
            # except:
            #     await ctx.send(f'You need to provide a valid item index')

@bot.command()
async def aptitudes(ctx, apt=None, apt_points=None):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        if apt is None:
            player_apts = f'**---APTITUDES---**\n' \
               f'**STR**: {player_obj.aptitudes["str"]}\n' \
               f'**DEX**: {player_obj.aptitudes["dex"]}\n' \
               f'**INT**: {player_obj.aptitudes["int"]}\n' \
               f'**WIS**: {player_obj.aptitudes["wis"]}\n' \
               f'**CONST**: {player_obj.aptitudes["const"]}\n\n' \
               f'To upgrade an aptitude, use !aptitudes [aptitude_name] [points]\n' \
               f'Example: !aptitudes dex 1\n' \
               f'You currently have {player_obj.aptitudePoints} aptitude points.'
            embed = discord.Embed(
                title=f'Aptitudes - {player_obj.name}',
                description=player_apts,
                color=discord.Colour.red()
            )
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif apt is not None and apt_points is not None:
            if file_management.check_if_in_fight(ctx.author.name) is None:
                try:
                    if player_obj.aptitudePoints < int(apt_points):
                        await ctx.send(f'{ctx.author.mention}, you do not have that many aptitude points.')
                        return
                    else:
                        player_obj.aptitudes[apt.lower()] += int(apt_points)
                        player_obj.update_stats_to_aptitudes(apt.lower(), int(apt_points))
                        player_obj.aptitudePoints -= int(apt_points)
                        file_management.delete_player(ctx.author.name)
                        file_management.write_player(player_obj)
                        await ctx.send(f'{ctx.author.mention} you have succesfully upgraded your {apt.lower()} to {player_obj.aptitudes[apt.lower()]}')
                except:
                    await ctx.send(f'Something went wrong. Are you sure you typed the aptitude correctly, {ctx.author.mention}?')
            else:
                await ctx.send(f'You cannot upgrade aptitudes while in combat.')



@bot.command()
async def fight(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    curr_area = areas[player_obj.currentArea - 1]
    enemy = random.choice(curr_area.enemyList)()
    await begin_fight(ctx=ctx, player=player_obj, enemy=enemy)

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

@bot.command()
async def item_test(ctx):
    item1 = items.longsword
    item2 = items.dagger
    player_obj = file_management.check_if_exists(ctx.author.name)
    player_obj.inventory.add_item(item1)
    player_obj.inventory.add_item(item2)

    await ctx.send(player_obj.inventory.show_inventory())

    file_management.delete_player(ctx.author.name)
    file_management.write_player(player_obj)

@bot.command()
async def inventory(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        inv_contents = player_obj.inventory.show_inventory()
        if inv_contents:
            await ctx.send(inv_contents)
        else:
            await ctx.send(f'{ctx.author.mention} your inventory is empty.')
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')


async def begin_fight(ctx, player, enemy):
    in_fight = file_management.check_if_in_fight(ctx.author.name)
    if in_fight is not None:
        await ctx.send(f'You are already in a fight against **{in_fight.enemy.name}**, {ctx.author.mention}')
        return

    if player is not None:
        fight_msg = await ctx.send(embed=embed_fight_msg(ctx=ctx, enemy=enemy, player_obj=player))

        fight_obj = fight_module.Fight(player=player, enemy=enemy, fight_msg=fight_msg.id)
        file_management.write_fight(fight_obj)
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

def embed_fight_msg(ctx, enemy, player_obj):
    hp_bar = progressBar.filledBar(enemy.stats['maxHp'], enemy.stats['hp'], size=10)
    embed = discord.Embed(
        title=f'Fight - {ctx.author}',
        description=f'You are fighting a **{enemy.name}**.\n'
                    f'HP: {hp_bar[0]} - {enemy.stats["hp"]}/{enemy.stats["maxHp"]}\n'
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
    lvl_up = in_fight.player.add_exp(in_fight.enemy.xpReward)
    in_fight.player.add_money(in_fight.enemy.goldReward)
    
    enemy_looted = False
    if combat.check_if_loot(in_fight.player, in_fight.enemy):
        enemy_looted = True
        
    file_management.delete_player(in_fight.player.name)
    file_management.write_player(in_fight.player)
    await ctx.send(
        embed=embed_victory_msg(ctx=ctx, enemy=in_fight.enemy, player_obj=in_fight.player, xp=in_fight.enemy.xpReward,
                                gold=in_fight.enemy.goldReward, looted=enemy_looted))
    if lvl_up:
        await ctx.send(f'{ctx.author.mention} - {lvl_up}')

def embed_victory_msg(ctx, enemy, player_obj, xp, gold, looted):
    looted_str = ''
    if looted:
        looted_str = f'You loot **{enemy.possibleLoot["name"]}**.'
    embed = discord.Embed(
        title=f'Victory!',
        description=f'{SPARKLER_EMOJI} **{ctx.author.name}** has slain a **{enemy.name}** {SPARKLER_EMOJI}\nYou earn {xp}xp and {gold} gold.\n' + looted_str,
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url=enemy.imageUrl)
    embed.set_image(url=ctx.author.avatar_url)
    return embed

bot.run(DISCORD_TOKEN)