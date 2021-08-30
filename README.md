# meta-to-grid

Retrieves high rank (immortal) dota pub meta information, parses it into dota supported hero grid config files.
Meta information provided by Spectral.gg

# Usage 
Run the python script while supplying the following argument:
  --cfg_file | -f : The hero grid config file to read as a starting point. Generally this should point to this file: [Steam install path]/userdata/[your_user_id]/570/remote/cfg/hero_grid_config.json
  
Optional arguments:
  --hero_count | -c : Determines the amount of heroes to put in the grid, takes the top X heroes based on ranking (pickrate+winrate)
  --output_cfg | -o : Write the output config file to the specified file, instead of the default. (default = --cfg_file)
  
# Behaviour
If your --cfg_file does not contain a meta-to-grid section yet, it will be added. A seperate grid is added for each different --hero_count you use.
That means you can run the script with -c 25 and -c 15, and you will end up with two seperate grids

If the --cfg_file does contain a meta-to-grid section, it will be updated with the new heroes.

Feel free to move the sections in the grids around, resize them. As long as you keep the names the same the script will update them and keep your layout

# Automating
If you are on windows, you can create a shortcut to the script (with arguments added to the shortcut target) and put it in "shell:startup". 
The script will now run when you start your computer
