#! /usr/bin/python3

from pyquery import PyQuery
import pandas as pd
import json
from shutil import copyfile
import datetime
import requests

#path to YOUR dota 2 remote cfg grid file - UPDATE THIS FOR YOUR SITUATION !
CFG_PATH = r"C:\Program Files (x86)\Steam\userdata\63878762\570\remote\cfg\hero_grid_config.json"

#how many heroes per category
TOP_NR = 15
#change this value if you don't want to override the default grid cfg file, but want the output in a different file
CFG_OUTPUT_PATH = r"C:\Users\jkohlenberg\Desktop\meta-to-grid\test.json"

#data dump
default_grid = {
    "config_name": "Spectral Meta Top X",
    "categories": [
        {
            "category_name": "Core Safelane",
            "x_position": 0.0,
            "y_position": 0.0,
            "width": 640.434875,
            "height": 175.434799,
            "hero_ids": [
            ]
        },
        {
            "category_name": "Core Midlane",
            "x_position": 0.0,
            "y_position": 204.968948,
            "width": 641.739197,
            "height": 171.98764,
            "hero_ids": [
            ]
        },
        {
            "category_name": "Core Offlane",
            "x_position": 4.565218,
            "y_position": 390.652222,
            "width": 638.478333,
            "height": 157.173935,
            "hero_ids": [
            ]
        },
        {
            "category_name": "Support Safelane",
            "x_position": 649.565308,
            "y_position": 146.739151,
            "width": 509.34787,
            "height": 159.782623,
            "hero_ids": [
            ]
        },
        {
            "category_name": "Support Offlane",
            "x_position": 652.17395,
            "y_position": 346.304382,
            "width": 443.478302,
            "height": 202.826111,
            "hero_ids": [
            ]
        },
        {
            "category_name": "Last updated on ",
            "x_position": 656.739197,
            "y_position": 7.826088,
            "width": 300.0,
            "height": 100.0,
            "hero_ids": []
        }
    ]
}

heroes= [
    {
        "name": "antimage",
        "id": 1,
        "localized_name": "Anti-Mage"
    },
    {
        "name": "axe",
        "id": 2,
        "localized_name": "Axe"
    },
    {
        "name": "bane",
        "id": 3,
        "localized_name": "Bane"
    },
    {
        "name": "bloodseeker",
        "id": 4,
        "localized_name": "Bloodseeker"
    },
    {
        "name": "crystal_maiden",
        "id": 5,
        "localized_name": "Crystal Maiden"
    },
    {
        "name": "drow_ranger",
        "id": 6,
        "localized_name": "Drow Ranger"
    },
    {
        "name": "earthshaker",
        "id": 7,
        "localized_name": "Earthshaker"
    },
    {
        "name": "juggernaut",
        "id": 8,
        "localized_name": "Juggernaut"
    },
    {
        "name": "mirana",
        "id": 9,
        "localized_name": "Mirana"
    },
    {
        "name": "nevermore",
        "id": 11,
        "localized_name": "Shadow Fiend"
    },
    {
        "name": "morphling",
        "id": 10,
        "localized_name": "Morphling"
    },
    {
        "name": "phantom_lancer",
        "id": 12,
        "localized_name": "Phantom Lancer"
    },
    {
        "name": "puck",
        "id": 13,
        "localized_name": "Puck"
    },
    {
        "name": "pudge",
        "id": 14,
        "localized_name": "Pudge"
    },
    {
        "name": "razor",
        "id": 15,
        "localized_name": "Razor"
    },
    {
        "name": "sand_king",
        "id": 16,
        "localized_name": "Sand King"
    },
    {
        "name": "storm_spirit",
        "id": 17,
        "localized_name": "Storm Spirit"
    },
    {
        "name": "sven",
        "id": 18,
        "localized_name": "Sven"
    },
    {
        "name": "tiny",
        "id": 19,
        "localized_name": "Tiny"
    },
    {
        "name": "vengefulspirit",
        "id": 20,
        "localized_name": "Vengeful Spirit"
    },
    {
        "name": "windrunner",
        "id": 21,
        "localized_name": "Windranger"
    },
    {
        "name": "zuus",
        "id": 22,
        "localized_name": "Zeus"
    },
    {
        "name": "kunkka",
        "id": 23,
        "localized_name": "Kunkka"
    },
    {
        "name": "lina",
        "id": 25,
        "localized_name": "Lina"
    },
    {
        "name": "lich",
        "id": 31,
        "localized_name": "Lich"
    },
    {
        "name": "lion",
        "id": 26,
        "localized_name": "Lion"
    },
    {
        "name": "shadow_shaman",
        "id": 27,
        "localized_name": "Shadow Shaman"
    },
    {
        "name": "slardar",
        "id": 28,
        "localized_name": "Slardar"
    },
    {
        "name": "tidehunter",
        "id": 29,
        "localized_name": "Tidehunter"
    },
    {
        "name": "witch_doctor",
        "id": 30,
        "localized_name": "Witch Doctor"
    },
    {
        "name": "riki",
        "id": 32,
        "localized_name": "Riki"
    },
    {
        "name": "enigma",
        "id": 33,
        "localized_name": "Enigma"
    },
    {
        "name": "tinker",
        "id": 34,
        "localized_name": "Tinker"
    },
    {
        "name": "sniper",
        "id": 35,
        "localized_name": "Sniper"
    },
    {
        "name": "necrolyte",
        "id": 36,
        "localized_name": "Necrophos"
    },
    {
        "name": "warlock",
        "id": 37,
        "localized_name": "Warlock"
    },
    {
        "name": "beastmaster",
        "id": 38,
        "localized_name": "Beastmaster"
    },
    {
        "name": "queenofpain",
        "id": 39,
        "localized_name": "Queen of Pain"
    },
    {
        "name": "venomancer",
        "id": 40,
        "localized_name": "Venomancer"
    },
    {
        "name": "faceless_void",
        "id": 41,
        "localized_name": "Faceless Void"
    },
    {
        "name": "wraith_king",
        "id": 42,
        "localized_name": "Wraith King"
    },
    {
        "name": "death_prophet",
        "id": 43,
        "localized_name": "Death Prophet"
    },
    {
        "name": "phantom_assassin",
        "id": 44,
        "localized_name": "Phantom Assassin"
    },
    {
        "name": "pugna",
        "id": 45,
        "localized_name": "Pugna"
    },
    {
        "name": "templar_assassin",
        "id": 46,
        "localized_name": "Templar Assassin"
    },
    {
        "name": "viper",
        "id": 47,
        "localized_name": "Viper"
    },
    {
        "name": "luna",
        "id": 48,
        "localized_name": "Luna"
    },
    {
        "name": "dragon_knight",
        "id": 49,
        "localized_name": "Dragon Knight"
    },
    {
        "name": "dazzle",
        "id": 50,
        "localized_name": "Dazzle"
    },
    {
        "name": "rattletrap",
        "id": 51,
        "localized_name": "Clockwerk"
    },
    {
        "name": "leshrac",
        "id": 52,
        "localized_name": "Leshrac"
    },
    {
        "name": "furion",
        "id": 53,
        "localized_name": "Nature's Prophet"
    },
    {
        "name": "life_stealer",
        "id": 54,
        "localized_name": "Lifestealer"
    },
    {
        "name": "dark_seer",
        "id": 55,
        "localized_name": "Dark Seer"
    },
    {
        "name": "clinkz",
        "id": 56,
        "localized_name": "Clinkz"
    },
    {
        "name": "omniknight",
        "id": 57,
        "localized_name": "Omniknight"
    },
    {
        "name": "enchantress",
        "id": 58,
        "localized_name": "Enchantress"
    },
    {
        "name": "huskar",
        "id": 59,
        "localized_name": "Huskar"
    },
    {
        "name": "night_stalker",
        "id": 60,
        "localized_name": "Night Stalker"
    },
    {
        "name": "broodmother",
        "id": 61,
        "localized_name": "Broodmother"
    },
    {
        "name": "bounty_hunter",
        "id": 62,
        "localized_name": "Bounty Hunter"
    },
    {
        "name": "weaver",
        "id": 63,
        "localized_name": "Weaver"
    },
    {
        "name": "jakiro",
        "id": 64,
        "localized_name": "Jakiro"
    },
    {
        "name": "batrider",
        "id": 65,
        "localized_name": "Batrider"
    },
    {
        "name": "chen",
        "id": 66,
        "localized_name": "Chen"
    },
    {
        "name": "spectre",
        "id": 67,
        "localized_name": "Spectre"
    },
    {
        "name": "doom_bringer",
        "id": 69,
        "localized_name": "Doom"
    },
    {
        "name": "ancient_apparition",
        "id": 68,
        "localized_name": "Ancient Apparition"
    },
    {
        "name": "ursa",
        "id": 70,
        "localized_name": "Ursa"
    },
    {
        "name": "spirit_breaker",
        "id": 71,
        "localized_name": "Spirit Breaker"
    },
    {
        "name": "gyrocopter",
        "id": 72,
        "localized_name": "Gyrocopter"
    },
    {
        "name": "alchemist",
        "id": 73,
        "localized_name": "Alchemist"
    },
    {
        "name": "invoker",
        "id": 74,
        "localized_name": "Invoker"
    },
    {
        "name": "silencer",
        "id": 75,
        "localized_name": "Silencer"
    },
    {
        "name": "obsidian_destroyer",
        "id": 76,
        "localized_name": "Outworld Destroyer"
    },
    {
        "name": "lycan",
        "id": 77,
        "localized_name": "Lycan"
    },
    {
        "name": "brewmaster",
        "id": 78,
        "localized_name": "Brewmaster"
    },
    {
        "name": "shadow_demon",
        "id": 79,
        "localized_name": "Shadow Demon"
    },
    {
        "name": "lone_druid",
        "id": 80,
        "localized_name": "Lone Druid"
    },
    {
        "name": "chaos_knight",
        "id": 81,
        "localized_name": "Chaos Knight"
    },
    {
        "name": "meepo",
        "id": 82,
        "localized_name": "Meepo"
    },
    {
        "name": "treant",
        "id": 83,
        "localized_name": "Treant Protector"
    },
    {
        "name": "ogre_magi",
        "id": 84,
        "localized_name": "Ogre Magi"
    },
    {
        "name": "undying",
        "id": 85,
        "localized_name": "Undying"
    },
    {
        "name": "rubick",
        "id": 86,
        "localized_name": "Rubick"
    },
    {
        "name": "disruptor",
        "id": 87,
        "localized_name": "Disruptor"
    },
    {
        "name": "nyx_assassin",
        "id": 88,
        "localized_name": "Nyx Assassin"
    },
    {
        "name": "naga_siren",
        "id": 89,
        "localized_name": "Naga Siren"
    },
    {
        "name": "keeper_of_the_light",
        "id": 90,
        "localized_name": "Keeper of the Light"
    },
    {
        "name": "wisp",
        "id": 91,
        "localized_name": "Io"
    },
    {
        "name": "visage",
        "id": 92,
        "localized_name": "Visage"
    },
    {
        "name": "slark",
        "id": 93,
        "localized_name": "Slark"
    },
    {
        "name": "medusa",
        "id": 94,
        "localized_name": "Medusa"
    },
    {
        "name": "troll_warlord",
        "id": 95,
        "localized_name": "Troll Warlord"
    },
    {
        "name": "centaur",
        "id": 96,
        "localized_name": "Centaur Warrunner"
    },
    {
        "name": "magnataur",
        "id": 97,
        "localized_name": "Magnus"
    },
    {
        "name": "shredder",
        "id": 98,
        "localized_name": "Timbersaw"
    },
    {
        "name": "bristleback",
        "id": 99,
        "localized_name": "Bristleback"
    },
    {
        "name": "tusk",
        "id": 100,
        "localized_name": "Tusk"
    },
    {
        "name": "skywrath_mage",
        "id": 101,
        "localized_name": "Skywrath Mage"
    },
    {
        "name": "abaddon",
        "id": 102,
        "localized_name": "Abaddon"
    },
    {
        "name": "elder_titan",
        "id": 103,
        "localized_name": "Elder Titan"
    },
    {
        "name": "legion_commander",
        "id": 104,
        "localized_name": "Legion Commander"
    },
    {
        "name": "ember_spirit",
        "id": 106,
        "localized_name": "Ember Spirit"
    },
    {
        "name": "earth_spirit",
        "id": 107,
        "localized_name": "Earth Spirit"
    },
    {
        "name": "abyssal_underlord",
        "id": 108,
        "localized_name": "Underlord"
    },
    {
        "name": "terrorblade",
        "id": 109,
        "localized_name": "Terrorblade"
    },
    {
        "name": "phoenix",
        "id": 110,
        "localized_name": "Phoenix"
    },
    {
        "name": "techies",
        "id": 105,
        "localized_name": "Techies"
    },
    {
        "name": "oracle",
        "id": 111,
        "localized_name": "Oracle"
    },
    {
        "name": "winter_wyvern",
        "id": 112,
        "localized_name": "Winter Wyvern"
    },
    {
        "name": "arc_warden",
        "id": 113,
        "localized_name": "Arc Warden"
    },
    {
        "name":"monkey_king",
        "id": 114,
        "localized_name": "Monkey King",
    },
    {
        "name":	"dark_willow",
        "id":	119,
        "localized_name":	"Dark Willow"
    },
    {
        "name": "pangolier",
        "id": 120,
        "localized_name": "Pangolier",
    },
    {
        "name": "grimstroke",
        "id": 121,
        "localized_name": "Grimstroke"
    },
    {
        "name": "hoodwink",
        "id": 123,
        "localized_name": "Hoodwink"
    },
    {
        "name": "void_spirit",
        "id": 126,
        "localized_name": "Void Spirit"
    },
    {
        "name": "snapfire",
        "id": 128,
        "localized_name": "Snapfire"
    },
    {
            "name": "mars",
        "id": 129,
        "localized_name": "Mars"
    },
    {
        "name": "dawnbreaker",
        "id": 135,
        "localized_name": "Dawnbreaker"
    }
]

update_date_string = "Last updated on "
#end data dump

def is_date_section(name):
    return name.startswith(update_date_string) or name == "Courtesy of spectral.gg"

#Create a backup of the hero grid file in the same folder
copyfile(CFG_PATH, CFG_PATH+".bck")

update_date = datetime.datetime.now().strftime("%d-%m-%Y")

#don't touch these
roles = ['Core Safelane', 'Core Midlane', 'Core Offlane', 'Support Safelane', 'Support Offlane']

d = PyQuery(url="https://stats.spectral.gg/lrg2/?league=imm_ranked_meta_last_7&mod=heroes-positions",
                                headers={'user-agent': 'pyquery'})

tag = d('#module-heroes-positions-overview')

dfs = pd.read_html(tag.html())

data = None

with open(CFG_PATH, 'r') as json_file:
    data = json.load(json_file)
    try:
        grid = next(item for item in data['configs'] if item["config_name"] == "Spectral Meta Top {nr}".format(nr = TOP_NR))
    except StopIteration:
        data['configs'].append(default_grid)
        grid = data['configs'][-1]
        grid["config_name"] = "Spectral Meta Top {nr}".format(nr = TOP_NR)

    for role in roles:
        # print(role)
        dfs[0].sort_values(by=[(role, 'Rank')], inplace=True, ascending=False)
        heroes_top = (dfs[0][('Unnamed: 1_level_0', 'Hero')].head(TOP_NR))
        grid_section = next(item for item in grid["categories"] if item["category_name"] == role)
        grid_section['hero_ids'] = []
        for hero in heroes_top:
            print(hero)
            hero_id = next(item for item in heroes if item["localized_name"] == hero)['id']
            grid_section['hero_ids'].append(hero_id)
        print(grid_section)

    date_section = next(item for item in grid["categories"] if is_date_section(item["category_name"]))
    if date_section is not None:
        #fill date section
        date_section["category_name"] = update_date_string + update_date
        

with open(CFG_OUTPUT_PATH, 'w') as json_file:
        json.dump(data, json_file)