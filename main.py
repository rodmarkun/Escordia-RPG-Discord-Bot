import discord
import os
from discord.ext import commands
from StringProgressBar import progressBar

import combat
import inventory as player_inv
import player
import items
import json
import dungeons
import fight as fight_module
import emojis
import file_management
import random
from area import areas

import skills

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
ENEMY = 'Wolf'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.command()
async def help(ctx):
    command_string = f'{emojis.STAR_EMOJI} **General** {emojis.STAR_EMOJI}\n' \
                     '`!help` - Display all commands\n' \
                     '`!start` - Create a player in Escordia RPG\n' \
                     '`!players` - Show all players of Escordia RPG\n' \
                     f'{emojis.CHARACTER_EMOJI} **Character** {emojis.CHARACTER_EMOJI}\n' \
                     '`!profile` - Check your current profile and stats\n' \
                     '`!profile [player name]` - Show profile of a certain player\n' \
                     '`!inventory` - Show all items from your inventory\n' \
                     '`!spells` - See a list with all of your spells\n' \
                     '`!aptitudes` - Show your current aptitudes\n' \
                     '`!aptitudes [aptitude] [points]` - Spend points on upgrading aptitudes\n' \
                     f'{emojis.DAGGER_EMOJI} **Combat** {emojis.DAGGER_EMOJI}\n' \
                     '`!area` - Show info about your current area \n' \
                     '`!fight` - Fight against a monster in your area\n' \
                     '`!dungeon` - Show all dungeons in this area\n' \
                     '`!attack` - Perform a normal attack against your opponent\n' \
                     '`!spells [number]` - Cast a certain spell\n' \
                     '`!heal` - Fully heal your character\n' \
                     '`!mana` - Fully replenish your mana\n' 
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
            player_apts = f'**STR**: {player_obj.aptitudes["str"]} - [+1 ATK]\n' \
               f'**DEX**: {player_obj.aptitudes["dex"]} - [+1 SPEED, +1 CRITCH]\n' \
               f'**INT**: {player_obj.aptitudes["int"]} - [+1 MATK]\n' \
               f'**WIS**: {player_obj.aptitudes["wis"]} - [+3 MAXMP, +1 MDEF]\n' \
               f'**CONST**: {player_obj.aptitudes["const"]} - [+2 MAXHP, +1 DEF]\n\n' \
               f'To upgrade an aptitude, use `!aptitudes [aptitude_name] [points]`\n' \
               f'Example: `!aptitudes dex 1`\n' \
               f'You currently have {player_obj.aptitudePoints} aptitude points.'
            embed = discord.Embed(
                title=f'{player_obj.name}\'s Aptitudes',
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
async def dungeon(ctx, arg=None):
    player_obj = file_management.check_if_exists(ctx.author.name)
    print(player_obj.inDungeon)
    if player_obj is not None:
        curr_area = areas[player_obj.currentArea - 1]
        if arg is None:
            dungeons_txt = ''
            i = 1
            for dungeon in curr_area.dungeons:
                dungeons_txt += f'{i} - {dungeon.name}\n'
                i += 1
            dungeons_txt += f'\nUse `!dungeon [dungeon_number]` to enter a certain dungeon.\nUse `!dungeon next` inside the dungeon to progress.'
            embed = discord.Embed(
                title=f'Area {player_obj.currentArea} - Dungeons',
                description=dungeons_txt,
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed)
        else:
            in_fight = file_management.check_if_in_fight(ctx.author.name) 
            if in_fight is None:
                if player_obj.inDungeon == False:
                    try:
                        area_dungeon = curr_area.dungeons[int(arg)-1]
                        dungeon_obj = dungeons.Dungeon(area_dungeon.name, area_dungeon.enemies, area_dungeon.loot_pool, area_dungeon.boss, area_dungeon.max_enemy_rooms, area_dungeon.max_loot_rooms, player_obj.name, area_dungeon.dungeon_number)
                    
                        player_obj.inDungeon = True
                        await dungeon_room(ctx, dungeon_obj, player_obj)
                    except:
                        await ctx.send(f'Wrong command, {ctx.author.name}. You first need to choose a dungeon, example: !dungeon 1.')
                else:
                    if arg != "next":
                        await ctx.send(f'You are already in a dungeon! Use [!dungeon next]')
                    else:
                        dungeon_obj = file_management.check_if_in_dungeon(ctx.author.name)
                        await dungeon_room(ctx, dungeon_obj, player_obj)
            elif player_obj.inDungeon:
                await ctx.send(f'You cannot traverse further into the dungeon while you are in combat, {ctx.author.name}')
            else:
                await ctx.send(f'You cannot enter a dungeon while you are in combat, {ctx.author.mention}')


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
    elif in_fight is not None:
        await ctx.send(f'{ctx.author.mention}, you need to be out of combat.')

@bot.command()
async def mana(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    in_fight = file_management.check_if_in_fight(ctx.author.name)

    if in_fight is None and player_obj is not None:
        combat.fully_recover_mp(player_obj)
        file_management.delete_player(player_obj.name)
        file_management.write_player(player_obj)
        await ctx.send(f'{player_obj.name}, you have fully recovered your MP.')
    elif in_fight is not None:
        await ctx.send(f'{ctx.author.mention}, you need to be out of combat.')

@bot.command()
async def item_test(ctx):
    item1 = items.weapon_rustySword
    item2 = items.armor_noviceArmor
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
            embed = discord.Embed(
                title=f'{ctx.author.name}\'s Inventory',
                description=inv_contents,
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed)
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
    player_hp_bar = progressBar.filledBar(player_obj.stats['maxHp'], player_obj.stats['hp'], size=10)
    player_mp_bar = progressBar.filledBar(player_obj.stats['maxMp'], player_obj.stats['mp'], size=10)
    embed = discord.Embed(
        title=f'Fight - {ctx.author}',
        description=f'You are fighting a **{enemy.name}**.\n'
                    f'HP: {hp_bar[0]} - {enemy.stats["hp"]}/{enemy.stats["maxHp"]}\n'
                    f'What will you do?\n\n'
                    f'{emojis.RED_CIRCLE_EMOJI} Attack - !attack\n'
                    f'{emojis.RED_CIRCLE_EMOJI} Spells - !spells\n'
                    f'{emojis.RED_CIRCLE_EMOJI} Combos - !combos',
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url=enemy.imageUrl)
    embed.set_image(url=ctx.author.avatar_url)
    embed.set_footer(
        text=f'{player_obj.name}\nHP: {player_obj.stats["hp"]}/{player_obj.stats["maxHp"]} | {player_hp_bar[0]}\nMP: {player_obj.stats["mp"]}/{player_obj.stats["maxMp"]} | {player_mp_bar[0]}')
    return embed

async def dungeon_room(ctx, dungeon_obj, player_obj):
    room_choice = ["Loot", "Enemy"]
    curr_room = random.choice(room_choice)
    if curr_room == "Loot" and dungeon_obj.loot_rooms > 0:
        dungeon_obj.loot_rooms -= 1
        item = (random.choice(dungeon_obj.loot_pool).create_item(1))
        player_obj.inventory.add_item(item)

        await ctx.send(f'{ctx.author.mention}While traversing the dungeon, you find a {item.name}!')

        file_management.delete_player(ctx.author.name)
        file_management.write_player(player_obj)
        file_management.delete_dungeon(ctx.author.name)
        file_management.write_dungeon(dungeon_obj)
    elif curr_room == "Enemy" and dungeon_obj.enemy_rooms > 0:
        dungeon_obj.enemy_rooms -= 1
        enemy = random.choice(dungeon_obj.enemies)()
        await begin_fight(ctx, player_obj, enemy)
        file_management.delete_player(ctx.author.name)
        file_management.write_player(player_obj)
        file_management.delete_dungeon(ctx.author.name)
        file_management.write_dungeon(dungeon_obj)
    else:
        await begin_fight(ctx, player_obj, dungeon_obj.boss())
        file_management.delete_dungeon(ctx.author.name)
        player_obj.inDungeon = False
        file_management.delete_player(ctx.author.name)
        file_management.write_player(player_obj)
        print(f'END: {player_obj.inDungeon}')

async def win_fight(ctx, in_fight):
    lvl_up = in_fight.player.add_exp(in_fight.enemy.xpReward)
    in_fight.player.add_money(in_fight.enemy.goldReward)
    
    enemy_looted = False
    if combat.check_if_loot(in_fight.player, in_fight.enemy):
        enemy_looted = True

    await ctx.send(
        embed=embed_victory_msg(ctx=ctx, enemy=in_fight.enemy, player_obj=in_fight.player, xp=in_fight.enemy.xpReward,
                                gold=in_fight.enemy.goldReward, looted=enemy_looted))
   
    if in_fight.enemy.isBoss and in_fight.player.inDungeon:
        in_fight.player.inDungeon = False
        await ctx.send(f'Congratulations {ctx.author.name}, you have completed this dungeon.')

    file_management.delete_player(in_fight.player.name)
    file_management.write_player(in_fight.player)
    if lvl_up:
        await ctx.send(f'{ctx.author.mention} - {lvl_up}')

def embed_victory_msg(ctx, enemy, player_obj, xp, gold, looted):
    looted_str = ''
    if looted:
        looted_str = f'\nYou loot **{enemy.possibleLoot["name"]}**.'
    embed = discord.Embed(
        title=f'Victory!',
        description=f'{emojis.SPARKLER_EMOJI} **{ctx.author.name}** has slain a **{enemy.name}** {emojis.SPARKLER_EMOJI}\nYou earn {xp}xp and {gold} gold.\n' + looted_str,
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url=enemy.imageUrl)
    embed.set_image(url=ctx.author.avatar_url)
    return embed

bot.run(DISCORD_TOKEN)