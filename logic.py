import discord

import emojis
import file_management
import random
import combat as combat_module
import player as player_module
import dungeons as dungeons_module
import fight as fight_module
import emojis as emojis_module
import area as area_module

from StringProgressBar import progressBar

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

async def travel_area(player_obj, ctx, area):
    if not player_obj.inDungeon:
        if player_obj.defeatedBosses + 1 >= area:
            if player_obj.currentArea != area:
                player_obj.currentArea = area
                file_management.delete_player(player_obj.name)
                file_management.write_player(player_obj)
                await ctx.send(f'{ctx.author.mention} you are now in area {area}')
            else:
                await ctx.send(f'{ctx.author.mention} you are already in area {area}')
        else:
            await ctx.send(f'{ctx.author.mention} you first need to defeat the `!boss` of al previous areas.')
    else:
        await ctx.send(f'{ctx.author.mention} you cannot travel while you are in a dungeon.')

async def level_up_aptitudes(player_obj, ctx, apt, apt_points):
    if player_obj.aptitudePoints < int(apt_points):
        await ctx.send(f'{ctx.author.mention}, you do not have that many aptitude points.')
        return
    else:
        player_obj.aptitudes[apt.lower()] += int(apt_points)
        player_obj.update_stats_to_aptitudes(apt.lower(), int(apt_points))
        player_obj.aptitudePoints -= int(apt_points)
        file_management.update_player(player_obj)
        await ctx.send(
            f'{ctx.author.mention} you have succesfully upgraded your {apt.lower()} to {player_obj.aptitudes[apt.lower()]}')

async def player_normal_attack(fight, ctx):
    fight.player = file_management.check_if_exists(ctx.author.name)
    fight.player.addComboPoints(1)
    fight_text = fight.normal_attack()
    await ctx.send(fight_text)

async def finish_turn(fight, ctx):
    if fight.player.alive:
        if not fight.enemy.alive:
            await win_fight(ctx, fight)
        else:
            file_management.write_fight(fight)
            file_management.update_player(fight.player)
            await ctx.send(embed=embed_fight_msg(ctx=ctx, enemy=fight.enemy, player_obj=fight.player))
    else:
        embed = discord.Embed(
            title=f'{fight.player.name} - Death {emojis_module.SKULL_EMOJI}',
            description=f'You have died, {fight.player.name}. You have lost half your gold and retreated to safety.',
            color=discord.Colour.red()
        )
        embed.set_image(url=ctx.author.avatar.url)
        fight.player.alive = True
        fight.player.comboPoints = 0
        file_management.update_player(fight.player)
        await ctx.send(embed=embed)

async def dungeon_logic(player_obj, curr_area, arg, ctx):
    if not player_obj.inDungeon:
        try:
            area_dungeon = curr_area.dungeons[int(arg) - 1]
            dungeon_obj = dungeons_module.Dungeon(area_dungeon.name, area_dungeon.enemies, area_dungeon.loot_pool,
                                                  area_dungeon.boss, area_dungeon.min_enemy_rooms,
                                                  area_dungeon.min_loot_rooms, area_dungeon.max_enemy_rooms,
                                                  area_dungeon.max_loot_rooms, player_obj.name,
                                                  area_dungeon.dungeon_number, area_dungeon.recommended_lvl)

            player_obj.inDungeon = True
            file_management.update_player(player_obj)
            await dungeon_room(ctx, dungeon_obj, player_obj)
        except:
            await ctx.send(
                f'Wrong command, {ctx.author.name}. You first need to choose a dungeon, example: `!dungeon 1`.')
    else:
        if arg != "next":
            await ctx.send(f'You are already in a dungeon! Use `!dungeon next`')
        else:
            dungeon_obj = file_management.check_if_in_dungeon(ctx.author.name)
            await dungeon_room(ctx, dungeon_obj, player_obj)


async def dungeon_room(ctx, dungeon_obj, player_obj):
    room_choice = ["Loot", "Enemy"]
    curr_room = random.choice(room_choice)

    if (curr_room == "Loot" or curr_room == "Enemy" and dungeon_obj.enemy_rooms == 0) and dungeon_obj.loot_rooms > 0:
        dungeon_obj.loot_rooms -= 1
        item = (random.choice(dungeon_obj.loot_pool).create_item(1))
        player_obj.inventory.add_item(item)

        desc = f'{ctx.author.mention}While traversing the dungeon, you find a {emojis.obj_to_emoji[item.objectType]} {item.name}!'
        embed = discord.Embed(
            title=f'{emojis.ESC_CHEST_ICON} Treasure!',
            description=desc,
            color=discord.Colour.red()
        )
        await ctx.send(embed=embed)
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

    in_fight.player.comboPoints = 0
    file_management.update_player(in_fight.player)
    if lvl_up:
        await ctx.send(f'{ctx.author.mention} - {lvl_up}')

# Embeds

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
    embed.set_image(url=ctx.author.avatar.url)
    embed.set_footer(
        text=f'{player_obj.name}\nHP: {player_obj.stats["hp"]}/{player_obj.stats["maxHp"]} | {player_hp_bar[0]}\nMP: {player_obj.stats["mp"]}/{player_obj.stats["maxMp"]} | {player_mp_bar[0]}\nCombo Points: {player_obj.comboPoints}')
    return embed

async def send_area_embed(player_obj, ctx):
    current_area = area_module.areas[player_obj.currentArea - 1]
    areas_txt = area_module.show_areas()
    areas_txt += f'\nYou are currently in **{current_area.name}** (area {current_area.number})\n'
    embed = discord.Embed(
        title=f'Areas',
        description=areas_txt,
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

async def send_player_profile(player_json, ctx, search):
    player_obj = player_module.createPlayer(player_json)
    embed = discord.Embed(
        title=f'Profile - {player_obj.name}',
        description=player_obj.show_info(),
        color=discord.Colour.red()
    )
    fetched_user = discord.utils.get(ctx.guild.members, name=search)
    embed.set_image(url=fetched_user.avatar.url)
    await ctx.send(embed=embed)

async def send_aptitudes_embed(player_obj, ctx):
    embed = discord.Embed(
        title=f'{player_obj.name}\'s Aptitudes',
        description=player_obj.show_aptitudes(),
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

async def show_current_dungeons(curr_area, player_obj, ctx):
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
    embed.set_image(url=ctx.author.avatar.url)
    return embed

async def show_player_spells(player_obj, ctx):
    embed = discord.Embed(
        title=f'{player_obj.name}\'s spells',
        description=player_obj.show_spells(),
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

async def show_player_combos(player_obj, ctx):
    embed = discord.Embed(
        title=f'{player_obj.name}\'s combos',
        description=player_obj.show_combos(),
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

def show_player_masteries(player_obj, ctx):
    embed = discord.Embed(
        title=f'{player_obj.name}\'s masteries',
        description=player_obj.show_masteries(),
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)