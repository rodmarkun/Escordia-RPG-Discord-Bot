import emojis

help_text = f'{emojis.STAR_EMOJI} **General** {emojis.STAR_EMOJI}\n' \
                     '`!help` - Display all commands\n' \
                     '`!start` - Create a player in Escordia RPG\n' \
                     '`!players` - Show all players of Escordia RPG\n' \
                     f'{emojis.CHARACTER_EMOJI} **Character** {emojis.CHARACTER_EMOJI}\n' \
                     '`!profile` - Check your current profile and stats\n' \
                     '`!profile [player name]` - Show profile of a certain player\n' \
                     '`!rest` - Fully recover your HP and MP. Has a 30min cooldown.\n' \
                     '`!inn` - Fully recover your HP and MP, for a reasonable price.\n' \
                     '`!inventory` - Show all items from your inventory\n' \
                     '`!spells` - See a list with all of your spells\n' \
                     '`!aptitudes` - Show your current aptitudes\n' \
                     '`!masteries` - Show your current mastery with each type of weapon\n' \
                     f'{emojis.COIN_EMOJI} **Economy** {emojis.COIN_EMOJI}\n' \
                     '`!shop` - Buy items from the store\n' \
                     '`!sell [item_index] [quantity]` - Sell items from your inventory at 50% its price value\n' \
                     f'{emojis.DAGGER_EMOJI} **Combat** {emojis.DAGGER_EMOJI}\n' \
                     '`!area` - Show info about your current area \n' \
                     '`!fight` - Fight against a monster in your area\n' \
                     '`!dungeon` - Show all dungeons in this area\n' \
                     '`!boss` - Fight against the boss of this area\n' \
                     '`!attack` - Perform a normal attack against your opponent\n' \
                     '`!spells [number]` - Cast a certain spell\n'

tutorial_1 = f'**Tutorial** \n' \
             f'Welcome to Escordia RPG, adventurer!\n' \
             f'\n' \
             f'**Basics**\n' \
             f'The bot prefix is `!`. All commands start with this prefix\n' \
             f'To start playing you first need to create a character using `!start`\n' \
             f'\n' \
             f'**Progression**\n' \
             f'You can start fighting enemies in your area by typing `!fight`. By slaying enemies you will be awarded ' \
             f'with XP, money, and some loot. You can also get some basic equipment from the `!shop`.\n\n' \
             f'If you find yourself with low HP or MP you can `!rest` for free every 30 minutes or go to the `!inn` and ' \
             f'recover all your HP and MP for a small fee.\n\n' \
             f'Once you feel strong and determined, you can challenge a `!dungeon`, in which you will fight monsters ' \
             f'and find high-quality gear. \n\n' \
             f'The world is divided in various areas (`!area` to see them all). To advance to the next area, you will ' \
             f'need to defeat the `!boss` of the previous area. Before fighting a boss, you should be well-equiped ' \
             f'and with a decent level. The `!shop` contents change depending the area you are at.\n\n' \
             f'Whenever you level up, you will be awarded with an aptitude point. Check `!aptitudes` and assign your ' \
             f'hard-earned points to become stronger!\n\n' \
             f'Everything else is explained in the `!help` command. Hope you have a great time in Escordia!'