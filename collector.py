import os
import re
import config
from config import *
from prettytable import PrettyTable
import shutil
import sys
from datetime import datetime
import requests
import json


def log_discord(*args):
    log = ' '.join(map(str, args))
    webhook_url = DISCORD_WEBHOOK
    slack_data = {'content': "%s" % log}
    response = requests.post(webhook_url, data=json.dumps(
        slack_data), headers={'Content-Type': 'application/json'})


def is_a_series(file):
    series = file.split(".")
    for segment in series:
        if re.match("[a-z][0-9][0-9][a-z][0-9][0-9]+", segment.lower()):
            return True
    return False


def series_name(file):
    series = file.split(".")
    name = ""
    isASeries = False
    for segment in series:
        if re.match("[a-z][0-9][0-9][a-z][0-9][0-9]+", segment.lower()):
            break
        else:
            name += f"{segment.capitalize()} "
    name = name.strip()
    if not is_a_series(file):
        return None
    if TITLE_DB.get(name) != None:
        name = TITLE_DB.get(name)
    return name


def series_season(file):
    series = file.split(".")
    if is_a_series(file):
        for segment in series:
            if re.match("[a-z][0-9][0-9][a-z][0-9][0-9]+", segment.lower()):
                season = int(segment.lower().split("e")[0].replace("s", ""))
                return f"Season {season}"


def series_folder(name):
    if name != None:
        for drive in RESOURCE_DRIVE:
            my_list = os.listdir(drive)
            for item in my_list:
                if item.strip().lower() == name.strip().lower():
                    return f"{drive}\\{item}"
    return None


def choose_drive():
    drive_sizes = {}
    for drive in RESOURCE_DRIVE:
        total, used, free = shutil.disk_usage(drive)
        drive_sizes.update({drive: free})
    largest_free_space = 0
    drive = ""
    for item in drive_sizes.items():
        if item[1] > largest_free_space:
            largest_free_space = item[1]
            drive = item[0]
    return drive


def find_file(name, dirlist):
    for path in dirlist:
        if name in path:
            return path


def absoluteFilePaths(directory):
    directory_list = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            directory_list.append(os.path.abspath(os.path.join(dirpath, f)))
    return directory_list


def generate_title():
    clear()
    print("+-----------------------------------------------------------+")
    print("_________        .__  .__                 __                |")
    print("\_   ___ \  ____ |  | |  |   ____   _____/  |_  ___________ |")
    print("/    \\  \\/ /  _ \\|  | |  | _/ __ \\_/ ___\\   __\\/  _ \\_  __ \|")
    print("\\     \\___(  <_> )  |_|  |_\\  ___/\\  \\___|  | (  <_> )  | \\/|")
    print(" \\______  /\\____/|____/____/\\___  >\\___  >__|  \\____/|__|   |")
    print("        \\/                      \\/     \\/                   |")
    print("+--------------------------------------------------By Arkrus+")


def main():
    file_list = []
    # Generate inventory
    t = PrettyTable(["File", "Title", "Season", "Source Directory",
                    "Target Directory", "Season Directory Exists"])
    log_discord(f"Process Started at {datetime.now()}")
    for drive in SOURCE_DRIVE:
        dirlist = absoluteFilePaths(SOURCE_DRIVE[0])
        for path, subdirs, files in os.walk(drive):
            for name in files:
                for media in ACCEPTED_TYPES:
                    if name.endswith(media) and "sample" not in name.lower():
                        title = series_name(name)
                        season = series_season(name)
                        target_directory = series_folder(title)
                        source_directory = find_file(name, dirlist)
                        season_directory = os.path.isdir(
                            f"{target_directory}\\{season}")
                        payload = \
                            {
                                "title": title,
                                "season": season,
                                "source_directory": source_directory,
                                "target_directory": target_directory,
                                "season_directory": season_directory,
                                "filename": name
                            }
                        t.add_row([name, title, season, source_directory,
                                  target_directory, season_directory])
                        file_list.append(payload)
    # Create directory folders
    t.align = "l"
    t._max_width = {"Source Directory": 25, "Target Directory": 25}
    print(t)
    tvshows = 0
    other = 0
    for file in file_list:
        if file["title"] != None:
            tvshows += 1
        else:
            other += 1
    log_discord(f"{tvshows} TV shows Found")
    log_discord(f"{other} additional media files Found")
    if CREATE_FOLDERS:
        print("Creating directories")
        for file in file_list:
            print(json.dumps(file, indent=4))
            if file["title"] != None:
                if file["target_directory"] == None:
                    # check if share has been created
                    location = series_folder(file["title"])
                    if location == None:
                        drive = choose_drive()
                        # create folder
                        title = file["title"]
                        os.mkdir(f"{drive}\\{title}")
                    file["target_directory"] = f"{drive}\\{title}"
                    log_discord(f'{file["target_directory"]} has been created')
                if not file["season_directory"]:
                    # check season has been created
                    print(f"Target directory is {file['target_directory']}")
                    print(
                        f"With a full path of {file['target_directory']}\\{file['season']}")
                    season_directory = os.path.isdir(
                        f"{file['target_directory']}\\{file['season']}")
                    if season_directory == False:
                        os.mkdir(
                            f"{file['target_directory']}\\{file['season']}")
                        log_discord(
                            f"{file['target_directory']}\\{file['season']} has been created")
                # move file
                print(f"Moving {file['filename']}")
                shutil.move(
                    file["source_directory"], f"{file['target_directory']}\\{file['season']}\\{file['filename']}")
                print(f"{file['filename']} Moved")
            else:
                print(f"Moving {file['filename']}")
                shutil.move(file["source_directory"],
                            f"{UNSORTED_DRIVE[0]}\\{file['filename']}")
                print(f"{file['filename']} Moved")
    log_discord("Run Complete")


if __name__ == "__main__":
    generate_title()
    main()
    sys.exit(0)
