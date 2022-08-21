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
                     '`!equip [item_index]` - Equip an item from your inventory\n' \
                     '`!spells` - See a list with all of your spells\n' \
                     '`!aptitudes` - Show your current aptitudes\n' \
                     '`!aptitudes [aptitude] [points]` - Spend points on upgrading aptitudes\n' \
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