import requests
import os
import pendulum
from dotenv import load_dotenv


def main():
    load_dotenv()  # take environment variables from .env.

    day = pendulum.today(tz="Europe/Paris").date().isoformat()

    KEY = os.getenv("KEY")

    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": KEY, "date": day, "thumbs": True}

    response = requests.get(url, params)

    if response.status_code == 200:
        data = response.json()

        # download the image
        if data.get("media_type") == "image":
            url = data.get("hdurl")
            dir_name = "/home/phil/Images/wallpapers/NASA/pic_of_the_day/"
            os.makedirs(dir_name, exist_ok=True)
            dl_command = f"wget -cq {url} --directory-prefix={dir_name}"
            os.system(dl_command)
            # set the wallpaper

            filename = url
            while "/" in filename:
                next_slash = filename.index("/")
                filename = filename[next_slash + 1 :]
            file_path = dir_name + filename
            # rename file to insert date at the beginning
            new_file_path = f"{dir_name}/{day}_{filename}"
            os.rename(file_path, new_file_path)
            # for gnome through gsettings
            # wallpaper_set_cmd = f"gsettings set org.gnome.desktop.background picture-uri file:///{new_file_path}"

            # with feh
            wallpaper_set_cmd = f"feh --bg-scale {new_file_path}"

            os.system(wallpaper_set_cmd)
            print(
                f"Day: {day}: {data.get('title')}.\n\nExplanation: {data.get('explanation')}\n\nWallpaper downloaded and set."
            )
        else:
            print(f"Day: {day}. Today's Pic of the day is a {data.get('media_type')}.")


if __name__ == "__main__":
    main()
