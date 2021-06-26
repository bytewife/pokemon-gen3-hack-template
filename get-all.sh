#!/bin/bash
## For Ubuntu only
set -x # display output

GAME=${1:-pokeemerald}    

## Necessary packages
sudo apt install build-essential binutils-arm-none-eabi git libpng-dev

## Get decompiled game
# git clone https://github.com/pret/pokeemerald

## Get agbcc (compiler)
# git clone https://github.com/pret/agbcc
# agbcc/./build.sh
# agbcc/./install.sh ./$GAME

## Get Debug packages
sudo apt install gdebi-core


## Attach PoryScript to rom decomp
# cp -r ./poryscript ./$GAME/tools/
cd poryscript
go build
cp poryscript ../$GAME/tools/poryscript/
cd ..
poryscript/./install.sh ./$GAME

### You will also need to follow the poryscript 
### Makefile changes manually.
