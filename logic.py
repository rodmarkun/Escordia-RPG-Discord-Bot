import discord

import area
import emojis
import file_management
import random
import combat as combat_module
import items
import messages
import skills as skills_module
import player as player_module
import dungeons as dungeons_module
import fight as fight_module
import emojis as emojis_module
import area as area_module
import crafting as crafting_module
from StringProgressBar import progressBar

'''
Menus & Interface
'''

class Menu(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx
        self.in_fight = file_management.check_if_in_fight(self.ctx.author.name)

    @discord.ui.button(label="Attack", style=discord.ButtonStyle.red)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        '''
        in_fight = file_management.check_if_in_fight(self.ctx.author.name)
        if in_fight is None:
            await self.ctx.send(f'You are not currently in a fight, {self.ctx.author.mention}')
        else:
        '''
        await player_normal_attack(self.in_fight, self.ctx, interaction)

        file_management.update_player(self.in_fight.player)
        file_management.delete_fight(self.ctx.author.name)

        await finish_turn(self.in_fight, self.ctx)

    @discord.ui.button(label="Skill", style=discord.ButtonStyle.primary)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.ctx.send("Skills", view=SelectView(self.in_fight.player.spells, 'skills', self.ctx))
        await interaction.response.defer()

    @discord.ui.button(label="Item", style=discord.ButtonStyle.green)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Item!")

class SkillSelect(discord.ui.Select):
    def __init__(self, skills : [skills_module.Skill], ctx):
        options = [discord.SelectOption(label=i["name"]) for i in skills]
        super().__init__(placeholder="Choose a skill: ", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        fight_obj = file_management.check_if_in_fight(self.ctx.author.name)
        if fight_obj is not None:
            selected_spell = [x for x in fight_obj.player.spells if x['name'] == self.values[0]]
            spell = skills_module.createSpell(selected_spell[0])
            info_str = fight_obj.skill(spell)
            file_management.delete_fight(self.ctx.author.name)

            await interaction.response.send_message(info_str)
            await finish_turn(fight_obj, self.ctx)
        else:
            await messages.not_in_fight(self.ctx)

class AreaSelect(discord.ui.Select):
    def __init__(self, area_list, ctx):
        options = [discord.SelectOption(label=f"Area {idx+1}") for idx, area in enumerate(area_list)]
        super().__init__(placeholder="Choose an area: ", max_values=1, min_values=1, options=options)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        player_obj = file_management.check_if_exists(self.ctx.author.name)
        await travel_area(player_obj, self.ctx, int(self.values[0].split(' ')[1]), interaction)

class SelectView(discord.ui.View):
    def __init__(self, list, type_select, ctx, *, timeout=30):
        super().__init__(timeout=timeout)
        if type_select == 'skills':
            self.add_item(SkillSelect(list, ctx))
        elif type_select == 'areas':
            self.add_item(AreaSelect(list, ctx))

'''
Areas
'''

async def show_areas(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is None:
        await messages.on_character_not_created(ctx)
    else:
        await send_area_embed(player_obj, ctx)

async def travel_area(player_obj, ctx, area, interaction):
    '''
    Travels to a certain area if unlocked

    :param player_obj: Player object
    :param ctx: Discord CTX
    :param area: Area number player wants to travel to
    '''
    if not player_obj.inDungeon:
        if player_obj.defeatedBosses + 1 >= area:
            if player_obj.currentArea != area:
                player_obj.currentArea = area
                file_management.delete_player(player_obj.name)
                file_management.write_player(player_obj)
                await interaction.response.send_message(f'{ctx.author.mention} you are now in area {area}')
            else:
                await interaction.response.send_message(f'{ctx.author.mention} you are already in area {area}')
        else:
            await interaction.response.send_message(f'{ctx.author.mention} you first need to defeat the `!boss` of al previous areas.')
    else:
        await interaction.response.send_message(f'{ctx.author.mention} you cannot travel while you are in a dungeon.')

'''
Player logic
'''

async def initialize_player(ctx):
    player_obj = file_management.check_if_exists(ctx.author.name)
    if player_obj is not None:
        await messages.on_character_already_created(ctx)
    else:
        create_player = player_module.Player(ctx.author.name)
        file_management.write_player(create_player)
        await messages.on_character_creation(ctx)

'''
Fighting Logic
'''

async def begin_fight(ctx, player, enemy):
    '''
    Begins a fight between a player and an enemy

    :param ctx: Discord CTX
    :param player: Player object
    :param enemy: Enemy object
    '''
    in_fight = file_management.check_if_in_fight(ctx.author.name)
    if in_fight is not None:
        await ctx.send(f'You are already in a fight against **{in_fight.enemy.name}**, {ctx.author.mention}')
        return

    if player is not None:
        fight_obj = fight_module.Fight(player=player, enemy=enemy)
        file_management.write_fight(fight_obj)
        await ctx.send(embed=embed_fight_msg(ctx=ctx, enemy=enemy, player_obj=player), view=Menu(ctx))
    else:
        await messages.on_character_not_created(ctx)

async def player_normal_attack(fight, ctx, interaction):
    '''
    Player performs a normal attack

    :param fight: Fight object
    :param ctx: Discord CTX
    '''
    fight.player = file_management.check_if_exists(ctx.author.name)
    fight.player.addComboPoints(1)
    fight_text = fight.normal_attack()
    if interaction is None:
        await ctx.send(fight_text)
    else:
        await interaction.response.send_message(fight_text)

async def level_up_aptitudes(player_obj, ctx, apt, apt_points):
    '''
    Levels up an aptitude by X points

    :param player_obj: Player object
    :param ctx: Discord CTX
    :param apt: Aptitude to upgrade
    :param apt_points: Points invested into leveling aptitude
    '''
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

async def finish_turn(fight, ctx):
    '''
    Finishes actual turn

    :param fight: Fight object
    :param ctx: Discord CTX
    '''
    if fight.player.alive:
        if not fight.enemy.alive:
            await win_fight(ctx, fight)
        else:
            file_management.write_fight(fight)
            file_management.update_player(fight.player)
            await ctx.send(embed=embed_fight_msg(ctx=ctx, enemy=fight.enemy, player_obj=fight.player), view=Menu(ctx))
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
    '''
    Controls logic to enter a dungeon or advancing inside one

    :param player_obj: Player object
    :param curr_area: Player's current area
    :param arg: Area number or 'next' if player is advancing in the dungeon
    :param ctx: Discord CTX
    '''
    if not player_obj.inDungeon:
        try:
            area_dungeon = curr_area.dungeons[int(arg) - 1]
            dungeon_obj = dungeons_module.Dungeon(area_dungeon.name, area_dungeon.enemy_list, area_dungeon.loot_pool,
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
    '''
    Creates a new dungeon room

    :param ctx: Discord CTX
    :param dungeon_obj: Dungeon object
    :param player_obj: Player object
    '''
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
        enemy = random.choice(dungeon_obj.enemy_list)()
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
    '''
    Player wins a fight.

    :param ctx: Discord CTX
    :param in_fight: Fight object
    '''
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

async def gather_resources(ctx, player_obj, action):
    '''
    Player gathers resources

    :param ctx: Discord CTX
    :param player_obj: Player object
    :param action: Gathering method (string)
    '''
    gathering_nodes = items.gathering_nodes
    tier = 1
    if action == "mining":
        tier = player_obj.gathering_tiers["miningTier"]
    elif action == "chopping":
        tier = player_obj.gathering_tiers["choppingTier"]
    acquire_list = gathering_nodes[action][tier-1]
    obtained_txt = ''
    for i in range(random.randint(1, 3)):
        item = random.choice(acquire_list).create_item()
        player_obj.inventory.add_item(item)
        obtained_txt += f'You obtained {item.emoji} x{item.amount} {item.name}!\n'
    file_management.update_player(player_obj)
    embed = discord.Embed(
        title=f'{action.capitalize()}',
        description=obtained_txt,
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

async def craft_item(ctx, object_name, player_obj):
    '''
    Crafts a certain item

    :param ctx: Discord CTX
    :param object_name: Object name, lowercased and spaces replaced with underscores (ex: bronze_armor)
    :param player_obj: Player object
    '''
    recipes = crafting_module.all_recipes
    for recipe_tier in recipes:
        for recipe in recipe_tier:
            if recipe["craft"].name.lower().replace(" ", "_") == object_name.lower():
                all_materials_needed = True
                i = 0
                for item in recipe["items"]:
                    if not player_obj.inventory.check_for_item_and_amount(item.name, recipe["quantity"][i]):
                        all_materials_needed = False
                    i += 1
                if all_materials_needed:
                    i = 0
                    for item in recipe["items"]:
                        player_obj.inventory.decrease_item_amount(item, recipe["quantity"][i])
                        i += 1
                    player_obj.inventory.add_item(recipe["craft"].create_item(1))
                    file_management.update_player(player_obj)
                    await ctx.send(f'{ctx.author.mention}, you successfully crafted a {recipe["craft"].name}.')
                else:
                    await ctx.send(f'{ctx.author.mention}, you do not have enough materials to craft {recipe["craft"].name}.')

# Embeds

def embed_fight_msg(ctx, enemy, player_obj):
    '''
    Sends embed used while fighting

    :param ctx: Discord CTX
    :param enemy: Enemy object
    :param player_obj: Player object
    '''
    hp_bar = progressBar.filledBar(enemy.stats['maxHp'], enemy.stats['hp'], size=10)
    player_hp_bar = progressBar.filledBar(player_obj.stats['maxHp'], player_obj.stats['hp'], size=10)
    player_mp_bar = progressBar.filledBar(player_obj.stats['maxMp'], player_obj.stats['mp'], size=10)
    embed = discord.Embed(
        title=f'Fight - {ctx.author}',
        description=f'You are fighting a **{enemy.name}**.\n'
                    f'HP: {hp_bar[0]} - {enemy.stats["hp"]}/{enemy.stats["maxHp"]}\n'
                    f'What will you do?\n\n',
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url=enemy.imageUrl)
    #embed.set_image(url=ctx.author.avatar.url)
    embed.set_footer(
        text=f'{player_obj.name}\nHP: {player_obj.stats["hp"]}/{player_obj.stats["maxHp"]} | {player_hp_bar[0]}\nMP: {player_obj.stats["mp"]}/{player_obj.stats["maxMp"]} | {player_mp_bar[0]}\nCombo Points: {player_obj.comboPoints}')
    return embed

async def send_area_embed(player_obj, ctx):
    '''
    Send an embed of all areas

    :param player_obj: Player object
    :param ctx: Discord CTX
    '''
    current_area = area_module.areas[player_obj.currentArea - 1]
    areas_txt = area_module.show_areas()
    areas_txt += f'\nYou are currently in **{current_area.name}** (area {current_area.number})\n'
    embed = discord.Embed(
        title=f'Areas',
        description=areas_txt,
        color=discord.Colour.red()
    )
    embed.set_image(url="https://i.postimg.cc/nLTrXZZV/Map.png")
    await ctx.send(embed=embed, view=SelectView(area.areas, 'areas', ctx))

async def send_player_profile(player_json, ctx, search):
    '''
    Sends profile embed of a certain player

    :param player_json: Player in JSON format
    :param ctx: Discord CTX
    :param search: Player name
    '''
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
    '''
    Sends an embed with aptitude info from one player

    :param player_obj: Player object
    :param ctx: Discord CTX
    '''
    embed = discord.Embed(
        title=f'{player_obj.name}\'s Aptitudes',
        description=player_obj.show_aptitudes(),
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

async def show_current_dungeons(curr_area, player_obj, ctx):
    '''
    Shows dungeon in current area

    :param curr_area: Area where the player is currently located
    :param player_obj: Player object
    :param ctx: Discord CTX
    '''
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
    '''
    Sends an embed when victorious in combat

    :param ctx: Discord CTX
    :param enemy: Enemy object
    :param player_obj: Player object
    :param xp: XP obtained
    :param gold: Gold obtained
    :param looted: Whether the player get to loot the enemy or not
    '''
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

async def show_player_crafting_tiers(player_obj, ctx):
    '''
    Shows crafting tiers locked and unlocked by a player

    :param player_obj: Player object
    :param ctx: Discord CTX
    '''
    tiers_txt = "These are your unlocked crafting tiers. Use `!craft [tier]` to see all recipes from that tier. " \
                "For example: `!craft tier1` (Recipes from Tier 1).\n\n"
    i = 1
    for tier in crafting_module.all_recipes:
        if player_obj.defeatedBosses + 1 >= i:
            tiers_txt += f'Tier{i} - **Unlocked**\n'
        else:
            tiers_txt += f'Tier{i} - Locked\n'
        i += 1
    embed = discord.Embed(
        title=f'Crafting Tiers',
        description=tiers_txt + f'\nTo unlock more tiers you will need to defeat the !boss of the next areas.',
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

async def show_player_crafts(player_obj, tier, ctx):
    '''
    Shows crafts from a certain tier

    :param player_obj: Player object
    :param tier: Tier to see recipes from
    :param ctx: Discord CTX
    '''
    embed = discord.Embed(
        title=f'Crafting - Tier {tier}',
        description=crafting_module.show_crafting_recipes(tier, player_obj),
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

async def show_player_spells(player_obj, ctx):
    '''
    Sends an embed with all the spells a player knows

    :param player_obj: Player object
    :param ctx: Discord CTX
    '''
    embed = discord.Embed(
        title=f'{player_obj.name}\'s spells',
        description=player_obj.show_spells(),
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

async def show_player_combos(player_obj, ctx):
    '''
    Sends an embed with all the combos a player knows

    :param player_obj: Player object
    :param ctx: Discord CTX
    '''
    embed = discord.Embed(
        title=f'{player_obj.name}\'s combos',
        description=player_obj.show_combos(),
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)

async def show_player_masteries(player_obj, ctx):
    '''
    Shows a player's masteries

    :param player_obj: Player object
    :param ctx: Discord CTX
    '''
    embed = discord.Embed(
        title=f'{player_obj.name}\'s masteries',
        description=player_obj.show_masteries(),
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)