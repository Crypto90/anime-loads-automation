try:
    from urllib.request import Request, urlopen  # Python 3
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import Request, urlopen  # Python 2
    from urllib2 import HTTPError
import json
from subprocess import Popen, PIPE, STDOUT
import shlex
import re
import os.path
import os, time, shutil



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
            if "Exit" in output:
                p.terminate()
            if "Finished" in output:
                with open("downloading_and_monitoring.txt", "a+") as text_file:
                    text_file.write("%s [GERMAN]\n" % result_title)
                break
                p.terminate()
            if "Keine Ergebnisse" in output:
                print("Could not find \"" + result_title + "\" german 1080p -- searching for japanese version...\n")
                with open("no_releases_found_log.txt", "a+") as text_file:
                    text_file.write("Could not find \"%s\" german 1080p\n" % result_title)
                p.terminate()
                print("Running: python3 download_anime.py \"" + result_title + "\" japanese 1080p\n")
                p2 = Popen(shlex.split("python3 download_anime.py \"" + result_title + "\" japanese 1080p"), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                while True:
                    output2 = p2.stdout.readline().rstrip().decode()
                    print(output2)
                    if "Exit" in output2:
                        p2.terminate()
                    if "Finished" in output2:
                        with open("downloading_and_monitoring.txt", "a+") as text_file:
                            text_file.write("%s [JAPANESE]\n" % result_title)
                        break
                        p2.terminate()
                    if "Keine Ergebnisse" in output2:
                        print("Could not find \"" + result_title + "\" japanese 1080p -- Skipping title\n")
                        with open("no_releases_found_log.txt", "a+") as text_file:
                            text_file.write("Could not find \"%s\" japanese 1080p\n" % result_title)
                        break
                        p2.terminate()
                    if output2 == '' and p2.poll() is not None:
                        break
                rc2 = p2.poll()
                break
            
            if output == '' and p.poll() is not None:
                break
        rc = p.poll()


# first get all unavailable requests, get their id and type (tv or movie), then get the tv or movie details and check for "Animation".
req = Request(OVERSEER_URL + '/api/v1/request?take=100000&filter=unavailable&sort=added')
req.add_header('X-Api-Key', OVERSEER_API_KEY)
jsonDataAll = json.loads(urlopen(req).read().decode())
RESULT_COUNTER=0

print("Found", len(jsonDataAll['results']), "open requests which now gets filtered for anime only...")

for result in reversed(jsonDataAll['results']):
    # we now have all unavailable requests, now we need to check if its in genre animation for type tv and movie
    #print("id:", result['id'], 'type:', result['type'], 'created:', result['createdAt'])
    
    result_id = result['id']
    result_type = result['type']
    result_created = result['createdAt']
    result_requested_by = result['requestedBy']['displayName']
    
    result_media_id = result['media']['id']
    
    result_media_tmdbId = result['media']['tmdbId']
    result_media_tvdbId = result['media']['tvdbId']
    result_media_imdbId = result['media']['imdbId']
    
    result_media_serviceId = result['media']['serviceId']
    
    result_media_service_id_to_use = 0;
    if result_media_serviceId == 0:
        result_media_service_id_to_use = result_media_tmdbId
    elif result_media_serviceId == 1:
        result_media_service_id_to_use = result_media_tvdbId
    elif result_media_serviceId == 1:
        result_media_service_id_to_use = result_media_imdbId
    
    
    try:
        singleReq = Request(OVERSEER_URL + '/api/v1/' + result_type + '/' + str(result_media_service_id_to_use) + '?language=en')
        singleReq.add_header('X-Api-Key', OVERSEER_API_KEY)
        resultSingle = json.loads(urlopen(singleReq).read().decode())
        
        result_title = ''
        if result_type == 'movie':
            result_title = resultSingle['title']
        else:
            result_title = resultSingle['name'] 
        result_status = resultSingle['status']#status has to be 'Released'
        result_keywords = ''
        if "keywords" in resultSingle:
            result_keywords = resultSingle['keywords']
        result_genres = ''
        if "genres" in resultSingle:
            result_genres = resultSingle['genres']
        
        result_original_language = resultSingle['originalLanguage']
        
        result_keywords_string = json.dumps(result_keywords)
        result_genres_string = json.dumps(result_genres)
        #print(result_genres_string)
        if ("anime" in result_keywords_string or "Anime" in result_keywords_string) or ("ja" in result_original_language and "Animation" in result_genres_string):
            RESULT_COUNTER=RESULT_COUNTER+1
            print("#"+str(RESULT_COUNTER), "title:", result_title, 'type:', result_type, 'status:', result_status, 'created:', result_created, 'Requester:', result_requested_by, "id:", result_id,"media_id:", result_media_id, "tmdbId:", result_media_tmdbId, "tvdbId:", result_media_tvdbId, "imdbId:", result_media_imdbId, "serviceId:", result_media_serviceId)
            
            result_title = re.sub(r"[^a-zA-Z0-9]+", ' ', result_title)
            print("Searching for \"" + result_title + "\" on anime-loads.org ...\n")
            execAnimeLoadsSearch(result_title)
            
            
            
    except HTTPError as err:
        if err.code == 404:
               continue
        else:
            raise
    
    
    
    
    
    
    
