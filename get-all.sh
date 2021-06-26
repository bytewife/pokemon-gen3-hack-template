#!/bin/bash
## For Ubuntu only

## Get decompiled game
git clone https://github.com/pret/pokeemerald

## Get agbcc (compiler)
git clone https://github.com/pret/agbcc
cd agbcc
./build.sh
./install.sh ../pokeemerald

## Necessary packages
sudo apt install build-essential binutils-arm-none-eabi git libpng-dev

## Debug
sudo apt install gdebi-core
