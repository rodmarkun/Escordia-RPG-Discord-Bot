# Imports

import discord
import os
import json
import file_management
import random
import combat as combat_module
import player as player_module
import dungeons as dungeons_module
import fight as fight_module
import emojis as emojis_module
import shop as shop_module
import skills as skills_module
import text as text_module
import area as area_module

from discord.ext import commands
from StringProgressBar import progressBar

# Discord token from VENV
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

# Bot initialization
intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="!help")
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)
bot.remove_command('help')
shop_obj = shop_module.Shop()

# !help command
@bot.command()
async def help(ctx):
    command_string = text_module.help_text
    embed = discord.Embed(
        title='Bot Commands',
        description= command_string,
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

# !start command
@bot.command()
async def start(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        await ctx.send(f'You already have a character in the world of Escordia, {ctx.author.mention}.')
    else:
        create_player = player_module.Player(ctx.author.name)
        file_management.write_player(create_player)
        await ctx.send(f'Welcome, {ctx.author.mention}, to the world of Escordia.')

@bot.command()
async def area(ctx, arg=0):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        try:
            if arg == 0:
                current_area = area_module.areas[player_obj.currentArea - 1]
                areas_txt = area_module.show_areas()
                areas_txt += f'\nYou are currently in **{current_area.name}** (area {current_area.number})\n'
                embed = discord.Embed(
                    title=f'Areas',
                    description=areas_txt,
                    color=discord.Colour.red()
                )
                await ctx.send(embed=embed)
            else:
                if not player_obj.inDungeon:
                    if player_obj.defeatedBosses + 1 >= arg:
                        if player_obj.currentArea != arg:
                            player_obj.currentArea = arg
                            file_management.delete_player(player_obj.name)
                            file_management.write_player(player_obj)
                            await ctx.send(f'{ctx.author.mention} you are now in area {arg}')
                        else:
                            await ctx.send(f'{ctx.author.mention} you are already in area {arg}')
                    else:
                        await ctx.send(f'{ctx.author.mention} you first need to defeat the `!boss` of al previous areas.')
                else:
                    await ctx.send(f'{ctx.author.mention} you cannot travel while you are in a dungeon.')
        except:
            await ctx.send(f'Something went wrong. Did you type the command correctly?')

@bot.command()
async def boss(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        if file_management.check_if_in_fight(player_obj.name) is None or not player_obj.inDungeon:
            current_area = area_module.areas[player_obj.currentArea - 1]
            await begin_fight(ctx=ctx, player=player_obj, enemy=current_area.boss())
        else:
            await ctx.send(f'{ctx.author.mention} you cannot fight a boss while already in a fight or in a dungeon.')

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
                player_obj = player_module.createPlayer(res)
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
             try:
                if len(player_obj.inventory.items) >= int(arg):
                    info = player_obj.equip_item(player_obj.inventory.items[int(arg)-1])
                    await ctx.send(info)
                    file_management.update_player(player_obj)
                else:
                    await ctx.send(f'There is no item with that index in your inventory.')
             except:
                 await ctx.send(f'You need to provide a valid item index')

@bot.command()
async def use(ctx, arg=None):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        if arg is None:
            await ctx.send(f'You need to provide the item index from your inventory to be able to use it.')
        else:
             try:
                if len(player_obj.inventory.items) >= int(arg):
                    info = player_obj.use_item(player_obj.inventory.items[int(arg)-1])
                    await ctx.send(info)
                    file_management.update_player(player_obj)
                else:
                    await ctx.send(f'There is no item with that index in your inventory.')
             except:
                 await ctx.send(f'You need to provide a valid item index')

@bot.command()
async def aptitudes(ctx, apt=None, apt_points=None):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        if apt is None:
            embed = discord.Embed(
                title=f'{player_obj.name}\'s Aptitudes',
                description=player_obj.show_aptitudes(),
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
                        file_management.update_player(player_obj)
                        await ctx.send(f'{ctx.author.mention} you have succesfully upgraded your {apt.lower()} to {player_obj.aptitudes[apt.lower()]}')
                except:
                    await ctx.send(f'Something went wrong. Are you sure you typed the aptitude correctly, {ctx.author.mention}?')
            else:
                await ctx.send(f'You cannot upgrade aptitudes while in combat.')

@bot.command()
async def fight(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        if file_management.check_if_in_fight(ctx.author.name) is None or not player_obj.inDungeon:
            curr_area = area_module.areas[player_obj.currentArea - 1]
            enemy = random.choice(curr_area.enemyList)()
            await begin_fight(ctx=ctx, player=player_obj, enemy=enemy)
        else:
            await ctx.send(f'{ctx.author.mention} you cannot fight while already in a fight or in a dungeon.')
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@bot.command()
async def attack(ctx):
    in_fight = file_management.check_if_in_fight(ctx.author.name)
    if in_fight is None:
        await ctx.send(f'You are not currently in a fight, {ctx.author.mention}')
    else:
        in_fight.player = file_management.check_if_exists(ctx.author.name)
        fight_text = in_fight.normal_attack()
        await ctx.send(fight_text)

        file_management.update_player(in_fight.player)

        file_management.delete_fight(ctx.author.name)
        if not in_fight.enemy.alive:
            await win_fight(ctx, in_fight)
        else:
            file_management.write_fight(in_fight)
            await ctx.send(embed=embed_fight_msg(ctx=ctx, enemy=in_fight.enemy, player_obj=in_fight.player))

@bot.command()
async def dungeon(ctx, arg=None):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        curr_area = area_module.areas[player_obj.currentArea - 1]
        if arg is None:
            dungeons_txt = ''
            i = 1
            for dungeon_in_area in curr_area.dungeons:
                dungeons_txt += f'{i} - **{dungeon_in_area.name}** - Recommended lvl: {dungeon_in_area.recommended_lvl}\n'
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
                if not player_obj.inDungeon:
                    try:
                        area_dungeon = curr_area.dungeons[int(arg)-1]
                        dungeon_obj = dungeons_module.Dungeon(area_dungeon.name, area_dungeon.enemies, area_dungeon.loot_pool, area_dungeon.boss, area_dungeon.max_enemy_rooms, area_dungeon.max_loot_rooms, player_obj.name, area_dungeon.dungeon_number, area_dungeon.recommended_lvl)
                    
                        player_obj.inDungeon = True
                        file_management.update_player(player_obj)
                        await dungeon_room(ctx, dungeon_obj, player_obj)
                    except:
                        await ctx.send(f'Wrong command, {ctx.author.name}. You first need to choose a dungeon, example: `!dungeon 1`.')
                else:
                    if arg != "next":
                        await ctx.send(f'You are already in a dungeon! Use `!dungeon next`')
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
                spell = skills_module.createSpell(fight_obj.player.spells[arg-1])
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

@commands.cooldown(1, 1800, commands.BucketType.user)
@bot.command()
async def rest(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    in_fight = file_management.check_if_in_fight(ctx.author.name)

    if in_fight is None and player_obj is not None and not player_obj.inDungeon:
        combat_module.fully_heal(player_obj)
        combat_module.fully_recover_mp(player_obj)
        file_management.update_player(player_obj)
        await ctx.send(f'{player_obj.name}, you are now rested and have recovered all your HP and MP.')
    elif in_fight is not None:
        await ctx.send(f'{ctx.author.mention}, you need to be out of combat.')
    elif player_obj.inDungeon:
        await ctx.send(f'{ctx.author.mention}, you cannot rest inside a dungeon.')

@bot.command()
async def inn(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    in_fight = file_management.check_if_in_fight(ctx.author.name)

    if in_fight is None and player_obj is not None and not player_obj.inDungeon:
        cost = player_obj.lvl * 10
        if player_obj.money < cost:
            await ctx.send(f'{ctx.author.mention} you do not have enough money ({cost}G) to rest at the inn.')
        else:
            await ctx.send(f'{ctx.author.mention}, you are now rested and have recovered all your HP and MP. The Inn\'s fee is {cost}G.')
            player_obj.money -= cost
            combat_module.fully_heal(player_obj)
            combat_module.fully_recover_mp(player_obj)
            file_management.update_player(player_obj)
    elif in_fight is not None:
        await ctx.send(f'{ctx.author.mention}, you need to be out of combat.')
    elif player_obj.inDungeon:
        await ctx.send(f'{ctx.author.mention}, you cannot rest inside a dungeon.')

@bot.command()
async def inventory(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        inv_contents = player_obj.inventory.show_inventory()
        if inv_contents:
            embed = discord.Embed(
                title=f'{ctx.author.name}\'s Inventory',
                description=inv_contents + f'\n\nType `!use [item_number]` to use a certain item.\nType `!equip [item_number]` to equip a certain item.\nType`!sell [item_index] [quantity]` to sell items from your inventory at 50% its price value\n',
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'{ctx.author.mention} your inventory is empty.')
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@bot.command()
async def shop(ctx, arg=0, quant=1):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        if file_management.check_if_in_fight(player_obj.name) is None and not player_obj.inDungeon:
            if arg == 0:
                embed = discord.Embed(
                    title=f'Shop - Area {player_obj.currentArea}',
                    description=shop_obj.show(player_obj) + f'\nUse `!shop [item_index] [quantity]` to buy an item.\nYou currently have **{player_obj.money}G**',
                    color=discord.Colour.red()
                )
                await ctx.send(embed=embed)
            else:
                purchasable_items = shop_obj.purchasable_items(player_obj)
                if arg - 1 <= len(purchasable_items):
                    item_to_purchase = purchasable_items[arg-1]
                    if player_obj.money > item_to_purchase.individualValue * quant:
                        item_to_purchase.amount = quant
                        player_obj.inventory.add_item(item_to_purchase.create_item(quant))
                        player_obj.money -= item_to_purchase.individualValue * quant
                        await ctx.send(f'You have successfully purchased x{quant} {item_to_purchase.name} for {item_to_purchase.individualValue * quant}G')

                        file_management.update_player(player_obj)
                    else:
                        await ctx.send(f'You do not have enough money, {ctx.author.mention}')
                else:
                    await ctx.send(f'There is no item with that index, {ctx.author.mention}')
        else:
            await ctx.send(f'You cannot buy items while in combat or inside a dungeon, {ctx.author.mention}')
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@bot.command()
async def sell(ctx, arg=0, amount=1):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        if file_management.check_if_in_fight(player_obj.name) is None and not player_obj.inDungeon:
            if arg == 0:
                await ctx.send(f'You need to provide an item index to sell it: `!sell [item index] [quantity]`. You can see all of your items with `!inventory`.')
            else:
                item_name = player_obj.inventory.items[arg-1].name
                item_amount = player_obj.inventory.get_amount_item(arg-1)
                if item_amount >= amount:
                    sell_value = player_obj.inventory.sell_item(arg, amount)
                    player_obj.money += sell_value
                    await ctx.send(f'{ctx.author.mention}, you have sold {amount} {item_name}(s) for {sell_value}.')

                    file_management.update_player(player_obj)
                else:
                    await ctx.send(f'{ctx.author.mention}, you do not have that many {item_name}.')
        else:
            await ctx.send(f'You cannot sell items while in combat or inside a dungeon, {ctx.author.mention}')
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@bot.command()
async def reset_player(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        file_management.delete_player(ctx.author.name)
        await ctx.send(f'Character succesfully deleted, type !start again {ctx.author.mention}')

@rest.error
async def command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!",description=f"Try again in {error.retry_after:.2f}s.")
        await ctx.send(embed=em)

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
                    f'{emojis_module.RED_CIRCLE_EMOJI} Attack - !attack\n'
                    f'{emojis_module.RED_CIRCLE_EMOJI} Spells - !spells\n'
                    f'{emojis_module.RED_CIRCLE_EMOJI} Combos - !combos',
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

    if (curr_room == "Loot" or curr_room == "Enemy" and dungeon_obj.enemy_rooms == 0) and dungeon_obj.loot_rooms > 0:
        dungeon_obj.loot_rooms -= 1
        item = (random.choice(dungeon_obj.loot_pool).create_item(1))
        player_obj.inventory.add_item(item)

        await ctx.send(f'{ctx.author.mention}While traversing the dungeon, you find a {item.name}!')

        file_management.update_player(player_obj)
        file_management.delete_dungeon(ctx.author.name)
        file_management.write_dungeon(dungeon_obj)
    elif (curr_room == "Enemy" or curr_room == "Loot" and dungeon_obj.loot_rooms == 0) and dungeon_obj.enemy_rooms > 0:
        dungeon_obj.enemy_rooms -= 1
        enemy = random.choice(dungeon_obj.enemies)()
        await begin_fight(ctx, player_obj, enemy)
        file_management.update_player(player_obj)
        file_management.delete_dungeon(ctx.author.name)
        file_management.write_dungeon(dungeon_obj)
    elif dungeon_obj.loot_rooms == 0 and dungeon_obj.enemy_rooms == 0:
        await begin_fight(ctx, player_obj, dungeon_obj.boss())
        file_management.delete_dungeon(ctx.author.name)
        file_management.update_player(player_obj)
        print(f'END: {player_obj.inDungeon}')

async def win_fight(ctx, in_fight):
    lvl_up = in_fight.player.add_exp(in_fight.enemy.xpReward)
    in_fight.player.add_money(in_fight.enemy.goldReward)
    
    enemy_looted = False
    if combat_module.check_if_loot(in_fight.player, in_fight.enemy):
        enemy_looted = True

    await ctx.send(
        embed=embed_victory_msg(ctx=ctx, enemy=in_fight.enemy, player_obj=in_fight.player, xp=in_fight.enemy.xpReward,
                                gold=in_fight.enemy.goldReward, looted=enemy_looted))

    if in_fight.enemy.isBoss and not in_fight.player.inDungeon:
        if in_fight.player.currentArea > in_fight.player.defeatedBosses:
            in_fight.player.defeatedBosses = in_fight.player.currentArea
            await ctx.send(f'Congratulations {ctx.author.mention}, you can now access the next area.')

    if in_fight.enemy.isBoss and in_fight.player.inDungeon:
        in_fight.player.inDungeon = False
        await ctx.send(f'Congratulations {ctx.author.mention}, you have completed this dungeon.')

    file_management.update_player(in_fight.player)
    if lvl_up:
        await ctx.send(f'{ctx.author.mention} - {lvl_up}')

def embed_victory_msg(ctx, enemy, player_obj, xp, gold, looted):
    looted_str = ''
    if looted:
        looted_str = f'\nYou loot **{enemy.possibleLoot["name"]}**.'
    embed = discord.Embed(
        title=f'Victory!',
        description=f'{emojis_module.SPARKLER_EMOJI} **{ctx.author.name}** has slain a **{enemy.name}** {emojis_module.SPARKLER_EMOJI}\nYou earn {xp}xp and {gold} gold.\n' + looted_str,
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url=enemy.imageUrl)
    embed.set_image(url=ctx.author.avatar_url)
    return embed

bot.run(DISCORD_TOKEN)