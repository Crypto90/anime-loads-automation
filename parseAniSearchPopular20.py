try:
    from urllib.request import Request, urlopen  # Python 3
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import Request, urlopen  # Python 2
    from urllib2 import HTTPError
import re
from subprocess import Popen, PIPE, STDOUT
import shlex
import os.path
import os, time, shutil
import urllib.parse
import json


# this script searches top 20 popular anime tv and movie entries and sends it to download_anime.py
# for downloading it from anime-loads.org

# URL to parse:
# https://www.anisearch.de/anime/popular?char=all&syncro=de&view=2&limit=20&hentai=no



OVERSEER_API_KEY = "YOUR_OVERSEERR_API_KEY_HERE"
OVERSEER_URL = "YOUR_OVERSEERR_URL_HERE"


one_day_ago = time.time() - (7 * 86400)
no_releases_log_file = "no_releases_found_log.txt"
if os.stat(no_releases_log_file).st_ctime <= one_day_ago:
    if os.path.isfile(path):
        try:
            print("Deleted", no_releases_log_file, "because creation date is older than 24 hours.")
            os.remove(no_releases_log_file)
        except:
            print("Could not remove file:", no_releases_log_file)


def execAnimeLoadsSearch(result_title):
    #check first if title is already in downloading_and_monitoring.txt file, if true return
    if not os.path.isfile('downloading_and_monitoring.txt'):
        open('downloading_and_monitoring.txt', 'a').close()
    if not os.path.isfile('no_releases_found_log.txt'):
        open('no_releases_found_log.txt', 'a').close()
    
    if os.path.isfile('downloading_and_monitoring.txt'):
        with open('downloading_and_monitoring.txt') as myfile:
            if result_title in myfile.read():
                print("\"" + result_title + "\" already exists in downloading_and_monitoring.txt... Skipping...\n")
                return
        with open('no_releases_found_log.txt') as myfile:
            if result_title in myfile.read():
                print("\"" + result_title + "\" already exists in no_releases_found_log.txt... it will get cleared every 24 hours. Skipping...\n")
                return
        print("Running: python3 download_anime.py \"" + result_title + "\" german 1080p\n")
        p = Popen(shlex.split("python3 download_anime.py \"" + result_title + "\" german 1080p"), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        while True:
            output = p.stdout.readline().rstrip().decode()
            print(output)
            
            if "Finished" in output:
                with open("downloading_and_monitoring.txt", "a+") as text_file:
                    text_file.write("%s [GERMAN]\n" % result_title)
                break
            if "Keine Ergebnisse" in output:
                print("Could not find \"" + result_title + "\" german 1080p -- searching for japanese version...\n")
                with open("no_releases_found_log.txt", "a+") as text_file:
                    text_file.write("Could not find \"%s\" german 1080p\n" % result_title)
                
                print("Running: python3 download_anime.py \"" + result_title + "\" japanese 1080p\n")
                p2 = Popen(shlex.split("python3 download_anime.py \"" + result_title + "\" japanese 1080p"), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                while True:
                    output2 = p2.stdout.readline().rstrip().decode()
                    print(output2)
                    
                    if "Finished" in output2:
                        with open("downloading_and_monitoring.txt", "a+") as text_file:
                            text_file.write("%s [JAPANESE]\n" % result_title)
                        break
                    if "Keine Ergebnisse" in output2:
                        print("Could not find \"" + result_title + "\" japanese 1080p -- Skipping title\n")
                        with open("no_releases_found_log.txt", "a+") as text_file:
                            text_file.write("Could not find \"%s\" japanese 1080p\n" % result_title)
                        break
                        
                    if output2 == '' and p2.poll() is not None:
                        break
                rc2 = p2.poll()
                break
            
            if output == '' and p.poll() is not None:
                break
        rc = p.poll()


req = Request('https://www.anisearch.de/anime/popular?char=all&syncro=de&view=2&limit=20&hentai=no', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req)
sourceCode = webpage.read().decode()

# <a href="anime/15983,the-worlds-finest-assassin-gets-reincarnated-in-another-world-as-an-aristocrat" class="rbox-2-1-15983" lang="de">The World’s Finest Assassin Gets Reincarnated in Another World as an Aristocrat</a>
# we check for lines containing: 
# '<a href='
# 'class="rbox-'
# 'lang="de"'



animeLinksTextOnlyArray = re.findall(r'<a[^>]*lang="de"*>(.+?)</a>', sourceCode)
#animeLinksTypeArray = re.findall(r'<td[^>]*>(Film|TV-Serie),', sourceCode)

print("===============================================================")
print("Top 20 anime results in popular on anisearch.de:              =")
print("===============================================================")
print(animeLinksTextOnlyArray)
print("===============================================================")
for animeTitle in animeLinksTextOnlyArray:
    #print (animeTitle)
    animeTitle = re.sub(r"[^a-zA-Z0-9]+", ' ', animeTitle)
    
    #we have to check if the title is already marked as available/downloaded on overseerr:
    safe_animeTitle = urllib.parse.quote(animeTitle, safe='')
    req = Request(OVERSEER_URL + '/api/v1/search?query=' + safe_animeTitle + '&page=1&language=de')
    req.add_header('X-Api-Key', OVERSEER_API_KEY)
    jsonDataSearch = json.loads(urlopen(req).read().decode())
    
    if len(jsonDataSearch['results']) > 0:
        for result in jsonDataSearch['results']:
            if "mediaInfo" in result and "plexUrl" in result['mediaInfo']:
                print('Title "' + animeTitle + '" already exists on plex: ' + str(result['mediaInfo']['plexUrl']) + " - Skipping ...")
                continue
    else:
        #no results from overseerr, so we can start the download
        print("Searching for \"" + animeTitle + "\" on anime-loads.org ...\n")
        execAnimeLoadsSearch(animeTitle)


            



    
    
    
    
    
    
    
    