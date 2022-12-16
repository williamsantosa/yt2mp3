# yt2mp3

Downloads youtube videos to mp3 format with additional options to change metadata.

# YouToo

Program that downloads YouTube videos for the purpose of quick and easy media acquisition.

## Setup

Ensure that you have Python v3.10.5+. If python is outdated or not installed on your system, follow these steps for [Windows](https://www.python.org/downloads/) and for [Unix](https://docs.python.org/3/using/unix.html) respectively. 

Afterward, install the dependencies via using `pip` or another Python package installer (Check dependencies in `pyproject.toml`). Alternatively, run the program via the Poetry package manager.

## Usage

```
Usage:
  python yt2mp3.py [options] [LINKS ...]

positional arguments:
  LINKS             YouTube links to download and convert to mp3

options:
  -h, --help        show this help message and exit
```

## Debugging

For best results, enclose links using the string literal, e.g.
```
python yt2mp3.py 'https://youtu.be/kffacxfA7G4' 'https://youtu.be/dQw4w9WgXcQ'
```
or 
```
python yt2mp3.py "https://youtu.be/kffacxfA7G4" "https://youtu.be/dQw4w9WgXcQ"
```
