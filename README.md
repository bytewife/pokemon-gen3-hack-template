## Pokemon Gen 3
This is aith's template install & custom scripts for Pokemon Gen 3 romhacks using pret's pokemon decompilations. Tested on Ubuntu 20.04.   

This repo comes with:  
+ agbcc        
+ poryscript  (requires some manual changes in your chosen ROM's Makefile)  

## Usage  
Dependencies:  
+ Go Lang (for poryscript)

To install everything else, use:  
```  
./get-all.sh [pokeemerald]  
```  

## Scripts
mod-encounter.py
For all commands, use
```
cd scripts/
python3 mod-encounters.py --help
```
Example: Replace all non-Safari & non-Pyramid Pokemon with level 10~20 Poochyena and level 20-30 Rayquazas
```
cd scripts/
python3 mod-encounters.py ../pokeemerald/src/data/wild_encounters.json --choose-all-maps --delete-all-mons --format-mons --add-mons=poochyena-10-20-land_mons,Rayquaza-20-30-water_mons --save-to=../pokeemerald/src/data/wild_encounters.out.json
```