# tvshow-organizer

A python script that organizes tv show media from one location to another. That outputs data to Discord. (Windows Only, untested on MacOS etc.)

## Initial Setup :

You will need to initialize a `config.py` in the same folder as this script with the following :
```
SOURCE_DRIVE = ['A:']
UNSORTED_DRIVE = ['B:']
RESOURCE_DRIVE = ['C:', 'D:', 'E:', 'F:']
ACCEPTED_TYPES = [".mkv",".avi",".mp4"]
CREATE_FOLDERS = True
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/your/discord/webhook/here"
TITLE_DB= \
    {
        "BAD NAME": "Good Name"
    }
```
Here is a breakdown of what each variable does (NOTE: In my example I use drives you can use a path instead "a:\path\with\stuff"): 

`SOURCE_DRIVE` 
The source drive from which you will be reading all the files/folders 

`UNSORTED_DRIVE`
A location to dump unknown content

`RESOURCE_DRIVE`
A location where you would order all your files,

`ACCEPTED_TYPES`
The source filetypes

`CREATE_FOLDERS`
Dialog whether to create folders and move files, if you just want to see the contents of a directory just set to False

`DISCORD_WEBHOOK` 
Discord webhook to send data as a notification to a specific discord channel

`TITLE_DB`
Files dont always read as they should, and sometimes theyll have the date attached ie : The Flash 2014, to remedy this, this is kind of like a "database" of what it would read and what you would rather it be "The Flash".


### Usage

First, make sure to install the `requirements.txt` :

`pip install -r requirements.txt`

Then create the `config.py` as above written above

From the CLI run

`python collector.py`
