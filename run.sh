#!/bin/zsh

source /home/phil/.zshrc
export DISPLAY=:0.0

pyenv activate nasa_api
python /home/phil/code/nasa_api/download_and_set_wallpaper.py
