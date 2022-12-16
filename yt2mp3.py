import os
import sys
import logging as lg
import shutil
import eyed3
from moviepy.editor import *
from pytube import YouTube
from pytube.contrib.playlist import Playlist


def mp4_to_mp3(mp4, mp3):
  """
  Converts mp4 file to mp3 file
  :param mp4: mp4 path (input)
  :param mp3: mp3 path (output)
  """
  mp4_without_frames = AudioFileClip(mp4)     
  mp4_without_frames.write_audiofile(mp3)     
  mp4_without_frames.close() # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")

def downloadYouTube(link, outputPath=''):
  """
  Downloads YouTube playlist or video
  :param link: link of YouTube playlist/video
  :param outputPath: output path of the video
  """

  # Create dictionary of links
  link = link.strip()
  if "https://www.youtube.com/playlist?list=" in link:
    download_list = Playlist(link).video_urls
  elif "https://www.youtube.com/watch?v=" in link or "https://youtu.be/" in link:
    download_list = [link]
  else:
    lg.error(f'Invalid YouTube link: {link}')
    return False

  # Create output path
  outputPath = outputPath.strip()
  if len(outputPath) == 0 or not os.path.isdir(outputPath):
    lg.error(f'Invalid output path: {outputPath}')
    return False

  # Download each link within the download list
  for download_link in download_list:
    lg.info(f"Beginning download for {download_link}...")

    try:
      yt = YouTube(download_link)
    except:
      lg.error(f'Could not create YouTube object with link: {download_link}. Check link and internet connection.')

    # Order by bitrate (audio)
    streams = yt.streams.order_by('abr')
    stream = yt.streams.get_by_itag(int(streams[-1].itag))
  
    # Download file
    try:
      stream.download(outputPath)
    except:
      lg.error(f'Error occurred when downloading {download_link}.')
      return

    lg.info(f"Finished download for {download_link}.")

def help():
  return (
"""
Usage:
  python yt2mp3.py [options] [LINKS ...]

positional arguments:
  LINKS             YouTube links to download and convert to mp3

options:
  -h, --help        show this help message and exit
"""
)

def main():
  # Check command line
  if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
    print(help())
    return

  # Create directories
  if not os.path.exists('./tmp/'):
    os.mkdir('./tmp/')
  if not os.path.exists('./mp3/'):
    os.mkdir('./mp3/')

  # Download each link supplied
  args = sys.argv[1:]
  for arg in args:
    downloadYouTube(arg, './tmp/')
  
  # For each file in temp, process to mp3 file and place in mp3 directory
  files = os.listdir('./tmp/')
  for file in files:
    mp4 = os.path.join('./tmp/', file)
    mp3 = os.path.join('./mp3/', file[:file.find('.mp4')] + '.mp3')
    mp4_to_mp3(mp4, mp3)

  # Delete temporary folder
  try:
    lg.info('Deleting ./tmp/ folder...')
    shutil.rmtree('./tmp/')
    lg.info('Deleted ./tmp/ folder succesfully.')
  except:
    lg.error('Error occurred while trying to delete ./tmp/ folder...')

  # Check if they want to edit the file
  response = ''
  while response != 'y' and response != 'n':
    response = input('Would you like to edit your files?: ')
    response = response.strip()[0].lower()
  
  # Finished file editing
  if response != 'y':
    return
  
  # Edit the files
  files = os.listdir('./mp3/')
  for file in files:
    # Ask to edit or not
    response = ''
    while response != 'y' and response != 'n':
      response = input(f'Would you like to edit {file}?: ')
      response = response.strip()[0].lower()
    if response != 'y':
      continue

    # Edit the file
    lg.info(f'Editing "{file}..."')
    path = os.path.join('./mp3/', file)
    mp3file = eyed3.load(path)

    filename = input('File Name: ')
    if len(filename) > 0:
      mp3file.rename(filename)

    title = input('Title: ')
    if len(title) > 0:
      mp3file.tag.title = title

    artist = input('Artist: ')
    if len(artist) > 0:
      mp3file.tag.artist = artist

    album = input('Album: ')
    if len(album) > 0:
      mp3file.tag.album = album

    mp3file.tag.save()

if __name__=="__main__":
  lg.basicConfig(format='%(levelname)s: %(message)s', level=lg.INFO)
  main()