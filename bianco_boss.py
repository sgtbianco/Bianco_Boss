#!python
import random

# Requirements for this boss:
# Species clause for medium/hard
# User must have 6 level 100 Pokemon


def pass_species_clause():
    for p1 in user.pokes[:5]:
        for p2 in user.team:
            if p1.name == p2.name and p1.id != p2.id:
                return False
    return True


# Awards 1 random item from tier_rewards list based on
# difficulty and extra reward based on win streak
def give_reward(difficulty):
    # list of rewards
    tier_rewards = [
        ["Flame Orb", "Toxic Orb", "Marill"],
        ["Life Orb", "Master Ball", "Scyther"],
        ["Torchic", "Treecko", "Mudkip"]]

    # 3 win streak rewards
    win_streak_rewards = ["Rotom", "Timburr", "Larvesta"]

    # adds weight to random chance
    tier = [0, 1, 2]
    tier_weights = [
        [.85, .1, .05],
        [.80, .1, .1],
        [.6, .25, .15]
    ]
    # reward Pokedollars
    if difficulty == 0:
        pokedollars_reward = random.randint(5000, 10000)
    elif difficulty == 1:
        pokedollars_reward = random.randint(12000, 18000)
    else:
        pokedollars_reward = random.randint(20000, 30000)

    user.money += pokedollars_reward
    user.say(f"You received {pokedollars_reward} Pokedollars!")

    coin_reward = difficulty * 2  # reward pve coins based on difficulty
    user.vars.PvECoinsBalance = str(int(user.vars.PvECoinsBalance) + coin_reward)
    if coin_reward > 0:
        user.say(f"You received {coin_reward} PvE Coins!")

    rand_tier = random.choices(tier, tier_weights[difficulty], k=1)  # returns a list
    rand_reward = random.choice(tier_rewards[rand_tier[0]])
    if rand_reward in ["Flame Orb", "Toxic Orb", "Life Orb", "Master Ball"]:  # can I check if something "is Item"
        user.items[rand_reward] += 1
        user.say(f"You received a {rand_reward}!")
    else:  # give pokemon reward
        p = Pokemon(rand_reward, 20)
        user.pokes.add(p)
        user.say(f"You received a {rand_reward}.")

    # checks user win streak and gives reward
    if user.vars.Bianco_Boss_Consec_Wins == 3:
        user.vars.Bianco_Boss_Consec_Wins = 0
        streak_reward = random.choice(win_streak_rewards)
        streak_poke = Pokemon(streak_reward, 20)
        user.say("Bianco: Wow, you've beaten me three times now!")
        user.pause()
        user.pokes.add(streak_poke)
        user.say("Bianco: Take this as a special reward!")
        user.say(f"You received a {streak_poke}.")


# Sets ivs, evs, and items to npc team depending on difficulty
def set_difficulty(difficulty):
    if difficulty > 0:
        npc.team[0].item, npc.team[1].item, npc.team[2].item, npc.team[3].item, npc.team[4].item, npc.team[5].item = \
            ("Life Orb", "Leftovers", "Air Balloon", "Choice Band", "Life Orb", "Scizorite")
    if difficulty == 1:
        for p in npc.team:
            p.ev_atk, p.ev_def, p.ev_spd, p.ev_spdef, p.ev_spatk, p.ev_hp = (252, 252, 252, 252, 252, 252)
    if difficulty == 2:
        for p in npc.team:
            p.ev_atk, p.ev_def, p.ev_spd, p.ev_spdef, p.ev_spatk, p.ev_hp = (400, 400, 400, 400, 400, 400)
            p.iv_atk, p.iv_def, p.iv_spd, p.iv_spdef, p.iv_spatk, p.iv_hp = (31, 31, 31, 31, 31, 31)


# boss team
poke_list = ["Jynx", "Volcarona", "Excadrill", "Weavile", "Clefable", "Scizor"]
nature_list = [Nature.Timid, Nature.Modest, Nature.Jolly, Nature.Jolly, Nature.Modest, Nature.Adamant]
ability_list = ["Dry Skin", "Flame Body", "Mold Breaker", "Pressure", "Magic Guard", "Technician"]
move_list = [("Lovely Kiss", "Ice Beam", "Psychic", "Nasty Plot"),
             ("Fiery Dance", "Quiver Dance", "Giga Drain", "Bug Buzz"),
             ("Swords Dance", "Earthquake", "Iron Head", "Rock Tomb"),
             ("Icicle Crash", "Ice Shard", "Low Kick", "Poison Jab"),
             ("Moonblast", "Ice Beam", "Flamethrower", "Focus Blast"),
             ("Swords Dance", "Bullet Punch", "Bug Bite", "Roost")]

for poke, nature, ability, skills in zip(poke_list, nature_list, ability_list, move_list):
    p = Pokemon(poke, 100)
    p.nature = nature
    p.ability = ability
    p.skills = skills
    npc.team.append(p)


if not user.vars.Bianco_Boss:
    user.vars.Bianco_Boss_Consec_Wins = 0
    user.vars.Bianco_Boss = True

if not user.vars.Bianco_Boss_cooldown:  # check boss cooldown
    choice1 = user.select("Bianco: Looking for a fight?", ["I want to battle!", "Check consecutive wins"])
    if choice1[0] == 0:
        if not all(p.level >= 100 for p in user.team):  # checks user's pokemon levels
            user.say("Bianco: Sorry, come back when your Pokemon are stronger.")
        else:
            choice2 = user.select("Alright. How badly do you want to lose?", ["Easy", "Medium", "Hard"])
            set_difficulty(choice2[0])  # set boss difficulty
            team_length = 0
            for i in user.team:  # there is probably a better way to check team length
                team_length += 1
            if team_length < 6:
                user.say("Bianco: Sorry, come back when you have 6 Pokemon.")
            elif choice2[0] > 0 and not pass_species_clause():  # species clause check for medium/hard
                user.say("Bianco: Yawn... Try bringing a more creative team.")
            else:
                user.pause()
                user.vars.set("Bianco_Boss_cooldown", True, timedelta(days=12))  # 12 day cooldown for boss
                check_no_item = choice2[0] == 2
                if user.battle(npc, no_items=check_no_item, no_exp=True, no_teleport=True) == 1:  # start the battle, returns 1 on battle success
                    if choice2[0] > 0:  # medium/hard mode
                        user.vars.Bianco_Boss_Consec_Wins += 1
                    user.say("Bianco: Congrats... I guess.")
                    user.say("Bianco: Here is your reward.")
                    user.pause()
                    give_reward(choice2[0])  # give user rewards
                else:
                    user.say("Bianco: Try again when you're stronger!")
                    user.vars.Bianco_Boss_Consec_Wins = 0
    else:
        if user.vars.Bianco_Boss_Consec_Wins == 1:
            user.say(f"You have {user.vars.Bianco_Boss_Consec_Wins} consecutive win.")
        else:
            user.say(f"You have {user.vars.Bianco_Boss_Consec_Wins} consecutive wins.")
else:
    choice3 = user.select("Bianco: Looking for a fight?", ["Check cooldown", "Check consecutive wins"])
    if choice3[0] == 0:
        user.say(f"Come back in {user.expire.Bianco_Boss_cooldown}")
    else:
        if user.vars.Bianco_Boss_Consec_Wins == 1:
            user.say(f"You have {user.vars.Bianco_Boss_Consec_Wins} consecutive win.")
        else:
            user.say(f"You have {user.vars.Bianco_Boss_Consec_Wins} consecutive wins.")
