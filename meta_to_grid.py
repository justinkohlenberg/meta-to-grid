#! /usr/bin/python3

from pyquery import PyQuery
import pandas as pd
from shutil import copyfile
import json, datetime, requests, argparse

parser = argparse.ArgumentParser(description="Retrieves immortal level meta stats, parses them into your dota hero grid config file")
parser.add_argument("--cfg_file", "-f", help="Path to your hero_grid_config.json, if not used uses default file configured in script")
parser.add_argument("--hero_count", "-c", nargs="+", type=int, help="1 or more amounts of heroes to put in the hero grid, for example -c 15 25 to generate both lists")
parser.add_argument("--output_cfg", "-o", help="Write the output config file to specified file, if not used writes to [--cfg_file|-f]")

args = parser.parse_args()

#path to YOUR dota 2 remote cfg grid file - UPDATE THIS FOR YOUR SITUATION !
if not args.cfg_file:
    CFG_PATH = r"C:\Program Files (x86)\Steam\userdata\63878762\570\remote\cfg\hero_grid_config.json"
else:
    CFG_PATH = args.cfg_file

#how many heroes per category
if not args.hero_count:
    TOP_NR = [15]
else:
    TOP_NR = args.hero_count

#change this value if you don't want to override the default grid cfg file, but want the output in a different file
if not args.output_cfg:
    CFG_OUTPUT_PATH = CFG_PATH
else:
    CFG_OUTPUT_PATH = args.output_cfg

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

update_date_string = "Last updated on "
#end data dump

def is_date_section(name):
    return name.startswith(update_date_string) or name == "Courtesy of spectral.gg"

#Create a backup of the hero grid file in the same folder
copyfile(CFG_PATH, CFG_PATH+".bck")

update_date = datetime.datetime.now().strftime("%d-%m-%Y")

#don't touch these
hero_meta_data_r = requests.get("https://stats.spectral.gg/lrg2/api/?mod=metadata&gets=heroes&pretty")
if hero_meta_data_r.status_code != 200:
    print("Issue retrieving hero meta data, status code {status}".format(status=hero_meta_data_r.status_code))
    exit()
hero_meta_data = hero_meta_data_r.json()

roles = ['Core Safelane', 'Core Midlane', 'Core Offlane', 'Support Safelane', 'Support Offlane']

d = PyQuery(url="https://stats.spectral.gg/lrg2/?league=imm_ranked_meta_last_7&mod=heroes-positions",
                                headers={'user-agent': 'pyquery'})

tag = d('#module-heroes-positions-overview')

dfs = pd.read_html(tag.html())

data = None

with open(CFG_PATH, 'r') as json_file:
    data = json.load(json_file)
    
    for count in TOP_NR:
        print(count)
        try:
            grid = next(item for item in data['configs'] if item["config_name"] == "Spectral Meta Top {nr}".format(nr = count))
        except StopIteration:
            data['configs'].append(default_grid)
            grid = data['configs'][-1]
            grid["config_name"] = "Spectral Meta Top {nr}".format(nr = count)

        for role in roles:
            # print(role)
            dfs[0].sort_values(by=[(role, 'Rank')], inplace=True, ascending=False)
            heroes_top = (dfs[0][('Unnamed: 1_level_0', 'Hero')].head(count))
            grid_section = next(item for item in grid["categories"] if item["category_name"] == role)
            grid_section['hero_ids'] = []
            for hero in heroes_top:
                print(hero)
                hero_id = next(item for item in hero_meta_data["result"]["heroes"].keys() if hero_meta_data["result"]["heroes"][str(item)]["name"] == hero)
                grid_section['hero_ids'].append(hero_id)
            print(grid_section)

        date_section = next(item for item in grid["categories"] if is_date_section(item["category_name"]))
        if date_section is not None:
            #fill date section
            date_section["category_name"] = update_date_string + update_date
        

if data:
    with open(CFG_OUTPUT_PATH, 'w') as json_file:
        json.dump(data, json_file)