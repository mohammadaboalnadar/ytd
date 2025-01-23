import os
import yt_dlp
import time
import tkinter as tk
from tkinter import filedialog

mode = ''
params = ''

commands = {
	"144p": "bestvideo[height<=144]+bestaudio/best[height<=144]",
	"240p": "bestvideo[height<=240]+bestaudio/best[height<=240]",
	"360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
	"480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
	"720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
	"1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
	"mp3": "bestaudio/best",
}

# Check for Cookies.txt file in the same directory as this script
cookies = False
scripts_dir = os.path.dirname(os.path.realpath(__file__))
try:
	with open(os.path.join(scripts_dir, 'Cookies.txt'), 'r') as f:
		cookies = True
except FileNotFoundError:
	print("Cookies.txt not found. Cookies are needed to log in to Youtube to avoid restrictions. Please create a Cookies.txt file in the same directory as this script and add your youtube cookies to it. The cookies should be in the format of a Netscape cookie file.")
	print("Script might not work without cookies.")
	print()

print("Available modes:")
modesString = ""
for i in commands:
	modesString += i + ' | '
print(modesString[:-3])

while True:
	mode = input('Download mode: ').split()[0].lower()

	if mode not in commands:
		print('Invalid mode: ' + mode)
	else:
		break

link_or_title = input('Enter a link or title: ')
if not link_or_title.startswith('https://'):
	link_or_title = f'ytsearch:"{link_or_title}"'

# Initialize tkinter
root = tk.Tk()
root.withdraw()  # Hide the root window

# Get video name using yt-dlp
with yt_dlp.YoutubeDL() as ydl:
	info = ydl.extract_info(link_or_title, download=False)
	title = info['title']

# Prompt user to select save location
save_path = filedialog.asksaveasfilename(
	initialfile=title + ".mp4" if mode != 'mp3' else title + ".mp3",
	title="Select file",
	defaultextension=".mp4" if mode != 'mp3' else ".mp3",
	filetypes=(("MP4 files", "*.mp4"), ("MP3 files", "*.mp3"), ("All files", "*.*")),
	confirmoverwrite=True,
)
if not save_path:
	print("No save path selected. Exiting...")
	time.sleep(1)
	exit()

# Define download options
ydl_opts = {
	'cookiefile': cookies and 'Cookies.txt' or None,
	'format': commands[mode],
	'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
	'nocheckcertificate': True,
	'quiet': False,
	'verbose': True,
	'outtmpl': save_path,  # Set the output template to the selected save path
	'http_headers': {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'DNT': '1',  # Do Not Track Request Header
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'none',
		'Sec-Fetch-User': '?1',
	},
	'postprocessors': [{
		'key': 'FFmpegVideoConvertor',
		'preferedformat': 'mp4',  # Convert video to mp4
	}] if mode != 'mp3' else [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}]
}

# Download the video
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
	ydl.download([link_or_title])

print("Finished... Exiting in 10s...")
time.sleep(10)
