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
            # set the wallpaper with feh

            filename = url
            while "/" in filename:
                next_slash = filename.index("/")
                filename = filename[next_slash + 1 :]
            file_path = dir_name + filename
            os.system(f"feh --bg-scale {file_path}")
            print(
                f"Day: {day}: {data.get('title')}.\nExplanation: {data.get('explanation')}.\nWallpaper downloaded."
            )
        else:
            print(f"Day: {day}. Today's Pic of the day is a {data.get('media_type')}.")


if __name__ == "__main__":
    main()
