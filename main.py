'''
 /////////////////////////////// ESCORDIA RPG ///////////////////////////////
                Made by @RodmarKun, Pablo Rodríguez Martín
                        https://github.com/rodmarkun
'''

# Imports
import asyncio
import os
import json

import shop as shop_module
import skills as skills_module
import text as text_module

from logic import *
from discord.ext import commands

# Discord token from VENV
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

# Bot initialization
intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="!help")
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)
bot.remove_command('help')
shop_obj = shop_module.Shop()


@bot.command()
async def help(ctx):
    '''
    !help command
    Shows info of all commands
    '''
    command_string = text_module.help_text
    embed = discord.Embed(
        title='Bot Commands',
        description= command_string,
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def start(ctx):
    '''
    !start command
    Creates a new character
    '''
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        await ctx.send(f'You already have a character in the world of Escordia, {ctx.author.mention}.')
    else:
        create_player = player_module.Player(ctx.author.name)
        file_management.write_player(create_player)
        await ctx.send(f'Welcome, {ctx.author.mention}, to the world of Escordia. We recommend you to play the `!tutorial`.')

@bot.command()
async def tutorial(ctx):
    '''
    !tutorial command
    Shows a small intro/tutorial
    '''
    embed = discord.Embed(
        title=f'Tutorial',
        description=text_module.tutorial_1,
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def area(ctx, arg=0):
    '''
    !area command
    Shows all areas or travels to a certain area
    :param arg: Area to travel to. If 0, just shows all areas
    '''
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        try:
            if arg == 0:
                await send_area_embed(player_obj, ctx)
            else:
               await travel_area(player_obj, ctx, arg)
        except:
            await ctx.send(f'Something went wrong. Did you type the command correctly?')

@bot.command()
async def boss(ctx):
    '''
    !boss command
    Fight against the boss of current area
    '''
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
    '''
    !players command
    Shows all players in Escordia RPG
    '''
    embed = discord.Embed(
        title=f'Players - {ctx.guild.name}',
        description=file_management.get_all_players(),
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

@bot.command()
async def profile(ctx, arg=None):
    '''
    !profile command
    Shows profile of specified player
    :param arg: Player whose profile will be shown. If None, shows self profile
    '''
    with open("players.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            search = ctx.author.name
            if arg is not None:
                search = arg
            if res['name'] == search:
                await send_player_profile(res, ctx, search)
                return
    if arg is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        await ctx.send(f'User does not have a character in Escordia yet. Make sure to just type the player\'s name after !profile. You can see current players in !players')

@bot.command()
async def equip(ctx, arg=None):
    '''
    !equip command
    Equips a certain item
    :param arg: Index of item to equip
    '''
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
    '''
    !use command
    Uses a certain item
    :param arg: Index of item to use
    '''
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        if arg is None:
            await ctx.send(f'You need to provide the item index from your inventory to be able to use it.')
        else:
                if len(player_obj.inventory.items) >= int(arg):
                    info = player_obj.use_item(player_obj.inventory.items[int(arg)-1])
                    await ctx.send(info)
                    file_management.update_player(player_obj)
                else:
                    await ctx.send(f'There is no item with that index in your inventory.')

@bot.command()
async def aptitudes(ctx, apt=None, apt_points=None):
    '''
    !aptitudes command
    Shows current aptitudes or upgrades an aptitude by x points
    :param apt: Aptitude to level up. If none, just shows up all aptitudes
    :param apt_points: Number of aptitude points to spend
    '''
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')
    else:
        if apt is None:
            await send_aptitudes_embed(player_obj, ctx)
        elif apt is not None and apt_points is not None:
            if file_management.check_if_in_fight(ctx.author.name) is None:
                try:
                    await level_up_aptitudes(player_obj, ctx, apt, apt_points)
                except:
                    await ctx.send(f'Something went wrong. Are you sure you typed the aptitude correctly, {ctx.author.mention}?')
            else:
                await ctx.send(f'You cannot upgrade aptitudes while in combat.')

@bot.command()
async def fight(ctx):
    '''
    !fight command
    Makes the player fight a random enemy from current area
    '''
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        if file_management.check_if_in_fight(ctx.author.name) is None and not player_obj.inDungeon:
            curr_area = area_module.areas[player_obj.currentArea - 1]
            enemy = random.choice(curr_area.enemyList)()
            await begin_fight(ctx=ctx, player=player_obj, enemy=enemy)
        else:
            await ctx.send(f'{ctx.author.mention} you cannot fight while already in a fight or in a dungeon.')
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@bot.command()
async def attack(ctx):
    '''
    !attack command
    Attack enemy fighting the player
    '''
    in_fight = file_management.check_if_in_fight(ctx.author.name)
    if in_fight is None:
        await ctx.send(f'You are not currently in a fight, {ctx.author.mention}')
    else:
        await player_normal_attack(in_fight, ctx)

        file_management.update_player(in_fight.player)
        file_management.delete_fight(ctx.author.name)

        await finish_turn(in_fight, ctx)
    await asyncio.sleep(0.3)

@bot.command()
async def dungeon(ctx, arg=None):
    '''
    !dungeon command
    Shows all dungeons or enter a specific dungeon
    :param arg: Specifies index of dungeon to enter. If none, shows all dungeons in current area.
    '''
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        curr_area = area_module.areas[player_obj.currentArea - 1]
        if arg is None:
            await show_current_dungeons(curr_area, player_obj, ctx)
        else:
            in_fight = file_management.check_if_in_fight(ctx.author.name) 
            if in_fight is None:
                await dungeon_logic(player_obj, curr_area, arg, ctx)
            elif player_obj.inDungeon:
                await ctx.send(f'You cannot traverse further into the dungeon while you are in combat, {ctx.author.name}')
            else:
                await ctx.send(f'You cannot enter a dungeon while you are in combat, {ctx.author.mention}')


@bot.command()
async def spells(ctx, arg=0):
    '''
    !spells command
    Shows all spells or casts a certain spell
    :param arg: Index of spell to cast. If 0, shows all spells.
    '''
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        if arg == 0:
            await show_player_spells(player_obj, ctx)
        else:
            fight_obj = file_management.check_if_in_fight(ctx.author.name)
            if fight_obj is not None:
                spell = skills_module.createSpell(fight_obj.player.spells[arg-1])
                info_str = fight_obj.skill(spell)
                file_management.delete_fight(ctx.author.name)
                await ctx.send(info_str)

                await finish_turn(fight_obj, ctx)
            else:
                await ctx.send(f'You are not currently in a fight, {ctx.author.mention}')
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@bot.command()
async def combos(ctx, arg=0):
    '''
    !combos command
    Shows all combos or performs a certain combo
    :param arg: Index of combo to perform. If 0, shows all combo.
    '''
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        if arg == 0:
            await show_player_combos(player_obj, ctx)
        else:
            fight_obj = file_management.check_if_in_fight(ctx.author.name)
            if fight_obj is not None:
                combo = skills_module.createCombo(fight_obj.player.combos[arg-1])
                info_str = fight_obj.skill(combo)
                file_management.delete_fight(ctx.author.name)
                await ctx.send(info_str)

                await finish_turn(fight_obj, ctx)
            else:
                await ctx.send(f'You are not currently in a fight, {ctx.author.mention}')
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@bot.command()
async def masteries(ctx):
    '''
    !masteries command
    Shows current mastery levels
    '''
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        show_player_masteries(player_obj, ctx)
    else:
        await ctx.send(f'You do not have a character in Escordia yet, {ctx.author.mention}. Create one typing !start.')

@commands.cooldown(1, 1800, commands.BucketType.user)
@bot.command()
async def rest(ctx):
    '''
    !rest command
    Fully heal player's character. Cooldown of 30min
    '''
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
    '''
    !inn command
    Fully heal player's character. It costs 10 * Player's Lvl
    '''
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
    '''
    !inventory command
    Shows player's inventory
    '''
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
    '''
    !shop command
    Shows shop's items or buys a certain quantity of an item
    :param arg: Index of item to buy. If 0, shows all shop's items
    :param quant: Quantity to buy of specified item
    '''
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
                    if player_obj.money >= item_to_purchase.individualValue * quant:
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
    '''
    !sell command
    Sell a certain item from your inventory
    :param arg: Index of item to sell.
    :param quant: Quantity to sell of specified item
    '''
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

bot.run(DISCORD_TOKEN)