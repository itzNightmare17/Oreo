#!/usr/bin/env bash
# OreO - UserBot

clear
sec=5
spinner=(⣻ ⢿ ⡿ ⣟ ⣯ ⣷)
while [ $sec -gt 0 ]; do
    echo -ne "\e[33m ${spinner[sec]} Starting dependency installation in $sec seconds...\r"
    sleep 1
    sec=$(($sec - 1))
done
echo -e "\e[1;32mInstalling Dependencies ---------------------------\e[0m\n" # Don't Fix it
apt-get update
apt-get upgrade -y
pkg upgrade -y
pkg install python wget -y
#wget https://raw.githubusercontent.com/..../main/resources/session/ssgen.py   # change in update
pip uninstall telethon -y && install telethon
clear
python3 ssgen.py
