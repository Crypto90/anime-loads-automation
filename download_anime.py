from subprocess import Popen, PIPE, STDOUT
import shlex
import sys
import threading
import time
import os
import subprocess
from threading import Thread
import queue


# this is a wrapper for: https://github.com/Pfuenzle/anime-loads
# docker run --rm -it -v $PWD/config:/config pfuenzle/anime-loads add
# docker run --rm -it -v $PWD/config:/config pfuenzle/anime-loads edit
# docker run --rm -it -v $PWD/config:/config pfuenzle/anime-loads remove



#HOW TO USE:

# python3 download_anime.py "search_string" [LANGUAGE] [RESOLUTION] [FORCE_ANIME_RESULT_NUMBER] [FORCE_RELEASE_NUMBER] [DRY_RUN]

# python3 download_anime.py "search_string" german -> adds to monitoring and downloads latest german 1080p release
# python3 download_anime.py "search_string" german 1080p -> adds to monitoring and downloads latest german 1080p release
# python3 download_anime.py "search_string" german 720p -> adds to monitoring and downloads latest german 720p release

# python3 download_anime.py "search_string" japanese -> adds to monitoring and downloads latest japanese 1080p release
# python3 download_anime.py "search_string" japanese 1080p -> adds to monitoring and downloads latest japanese 1080p release
# python3 download_anime.py "search_string" japanese 720p -> adds to monitoring and downloads latest japanese 720p release

# Valid language parameters (which is required!):
# japanese or jap
# german or ger


#remove a download entry from anime-loads docker config:
# docker exec -i pfuenzle-anime-loads1 python anibot.py --configfile /config/ani.json remove

RUNNING_DOCKER_CONTAINER="pfuenzle-anime-loads1"





CRED = '\033[33m'
CEND = '\033[0m'

RELEASE_ID_TO_DOWNLOAD=0
RELEASE_SELECTED=False
GOT_FIRST_EXIT_MESSAGE=False
SEARCH_RESULTS_FOUND=False
SEARCH_RESULT_TYPE="tv"
DRY_RUN=False


def reader(pipe, queue):
    try:
        with pipe:
            for line in iter(pipe.readline, b''):
                queue.put((pipe, line))
    finally:
        queue.put(None)





p = Popen(shlex.split("docker exec -i " + RUNNING_DOCKER_CONTAINER + " python anibot.py --configfile /config/ani.json add"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0)
q = queue.Queue()

Thread(target=reader, args=[p.stdout, q]).start()
Thread(target=reader, args=[p.stderr, q]).start()



if len(sys.argv) >= 7 and int(sys.argv[6]) > 0:
    DRY_RUN=True


def threadSelectRelease():
    global RELEASE_ID_TO_DOWNLOAD
    time.sleep(5)
    if len(sys.argv) >= 6 and int(sys.argv[5]) > 0:
        RELEASE_ID_TO_DOWNLOAD = int(sys.argv[5])
    if RELEASE_ID_TO_DOWNLOAD > 0:
        print("Selecting last matched result (because its the newest): " + str(RELEASE_ID_TO_DOWNLOAD))
        print("Sending input: " + str(RELEASE_ID_TO_DOWNLOAD))
        p.stdin.write((str(RELEASE_ID_TO_DOWNLOAD) + "\n").encode())
        p.stdin.flush()
        p.stdout.flush()
        sys.stdout.flush()
    else:
        print("Keine Ergebnisse")
        p.stdin.write(("exit\n").encode())
        p.stdin.flush()
        p.stdout.flush()
        sys.stdout.flush()
        p.terminate()
        sys.exit()

#ok = True
#while ok:
while p.poll() is None:
    for source, output in iter(q.get, None):
        output = str(output.decode())
        #output = p.stdout.readline().rstrip().decode()
        print(CRED + output + CEND)
        if "nach dem du suchen willst" in output and GOT_FIRST_EXIT_MESSAGE == False:
            time.sleep(3)
            print("Sending input: " + sys.argv[1])
            #p.communicate((sys.argv[1] + '\n').encode())
            p.stdin.write((sys.argv[1]+"\n").encode())
            p.stdin.flush()
            p.stdout.flush()
            sys.stdout.flush()
        
        
        if "Keine Ergebnisse" in output:
            print("Keine Ergebnisse. Exit...")
            p.stdin.write(("exit\n").encode())
            p.stdin.flush()
            p.stdout.flush()
            sys.stdout.flush()
            p.terminate()
            sys.exit()
            
            
        if "os error" in output:
            print("OS Error. Exit...")
            p.stdin.write(("exit\n").encode())
            p.stdin.flush()
            p.stdout.flush()
            sys.stdout.flush()
            p.terminate()
            sys.exit()
        
        
        if (("Exit" in output or "exit" in output) or ("nach dem du suchen willst" in output)) and GOT_FIRST_EXIT_MESSAGE == True:
            print("Finished! Exit...")
            print("Sending input: exit")
            p.stdin.write(("exit\n").encode())
            p.stdin.flush()
            p.stdout.flush()
            sys.stdout.flush()
            p.terminate()
            sys.exit()
        elif "Exit" in output or "exit" in output and GOT_FIRST_EXIT_MESSAGE == False:
            GOT_FIRST_EXIT_MESSAGE=True 
    
        if "Ergebnisse:" in output:
            SEARCH_RESULTS_FOUND=True
            
            SELECT_RESULT_ANIME_NAME="1"
            if len(sys.argv) >= 5 and int(sys.argv[4]) > 0:
                SELECT_RESULT_ANIME_NAME=str(sys.argv[4])
            
            print("Found a matching result! Selecting " + SELECT_RESULT_ANIME_NAME + ". match.")
            print("Sending input: " + SELECT_RESULT_ANIME_NAME)
            p.stdin.write((SELECT_RESULT_ANIME_NAME + "\n").encode())
            p.stdin.flush()
            p.stdout.flush()
            sys.stdout.flush()
        
        if "[1] Name:" in output and ("Episoden: 1337" in output or "1337/1337" in output):
            SEARCH_RESULT_TYPE="movie"
        
        if "Releases:" in output:
            th = threading.Thread(target=threadSelectRelease)
            th.start()
    
        RESOLUTION="1080p"
        if len(sys.argv) >= 4:
            RESOLUTION=sys.argv[3]
        
        if sys.argv[2] == "" or sys.argv[2] == "german" or sys.argv[2] == "ger":
            if ("Release ID:" in output) and (", Dub" in output and "Deutsch" in output.split(", Dub")[1].split("]")[0]) and ("Resolution: " + RESOLUTION) in output and "Du hast folgendes Release" not in output:
                RELEASE_ID_TO_DOWNLOAD=int(output.split(',')[0].split('ID: ')[1])
                print("Found german 1080p release. Set RELEASE_ID_TO_DOWNLOAD to: " + str(RELEASE_ID_TO_DOWNLOAD))
                if RELEASE_SELECTED == False:
                    RELEASE_SELECTED=True
        
        if sys.argv[2] == "japanese" or sys.argv[2] == "jap":
            if ("Release ID:" in output) and (", Dub" in output and "Japanisch" in output.split(", Dub")[1].split("]")[0]) and ("Resolution: " + RESOLUTION) in output and "Du hast folgendes Release" not in output:
                RELEASE_ID_TO_DOWNLOAD=int(output.split(',')[0].split('ID: ')[1])
                print("Found japanese 1080p release. Set RELEASE_ID_TO_DOWNLOAD to: " + str(RELEASE_ID_TO_DOWNLOAD))
                if RELEASE_SELECTED == False:
                    RELEASE_SELECTED=True
    
        if ("Das Release hat" in output and "Episode(n)" in output):
            # -- download all
            print("Sending input: #")
            p.stdin.write(("#\n").encode())
            # -- download all new, so this script can run multiple times with a same series request without downloading it multiple times
            #print("Downloading all new episodes... needs ENTER.")
            #print("Sending input: ENTER")
            #p.stdin.write(("\n").encode())
            p.stdin.flush()
            p.stdout.flush()
            sys.stdout.flush()
    
        if "Wieviel Episoden hast du bereits runtergeladen" in output and "Fehlerhafte Eingabe" in output:
            # -- download all
            print("Downloading all episodes so we need to send 0.")
            print("Sending input: 0")
            p.stdin.write(("0\n").encode())
            p.stdin.flush()
            p.stdout.flush()
            sys.stdout.flush()
        
       
        #if "dem Anime einen spezifischen Paketnamen geben" in output:
        if "Wieviel Episoden hast du bereits runtergeladen" in output and "Fehlerhafte Eingabe" not in output:
            #paket name: "search_string language resolution"
            #sending invalid character to refresh output and get new input
            print("Sending input:j")
            p.stdin.write(("j\n").encode())
            p.stdin.flush()
            p.stdout.flush()
            sys.stdout.flush()
            
            lang_for_package_name = 'NA'
            if sys.argv[2] == "japanese" or sys.argv[2] == "jap":
                lang_for_package_name = "japanese"
            elif sys.argv[2] == "" or sys.argv[2] == "german" or sys.argv[2] == "ger":
                lang_for_package_name = "german"
            print("Sending input: " + (sys.argv[1] + " " + lang_for_package_name + " " + RESOLUTION + " " + SEARCH_RESULT_TYPE))
            
            
            if DRY_RUN == True:
                print("DRY RUN aktiviert! Exit...")
                p.terminate()
                sys.exit()
            
            
            p.stdin.write((sys.argv[1] + " " + lang_for_package_name + " " + RESOLUTION + " " + SEARCH_RESULT_TYPE + "\n").encode())
            p.stdin.flush()
            p.stdout.flush()
            sys.stdout.flush()
        
        
        #if "Paketnamen:" in output:
        #if "dem Anime einen spezifischen Paketnamen geben" in output:
        #    #sending invalid character to refresh output and get new input
        #    p.stdin.write(("#\n").encode())
        #    p.stdin.flush()
        #    p.stdout.flush()
        #    sys.stdout.flush()
        #    
        #    lang_for_package_name = 'NA'
        #    if sys.argv[2] == "japanese" or sys.argv[2] == "jap":
        #        lang_for_package_name = "japanese"
        #    elif sys.argv[2] == "" or sys.argv[2] == "german" or sys.argv[2] == "ger":
        #        lang_for_package_name = "german"
        #    p.stdin.write((sys.argv[1] + " " + lang_for_package_name + " " + RESOLUTION + "\n").encode())
        #    p.stdin.flush()
        #    p.stdout.flush()
        #    sys.stdout.flush()
        
        #p.stdin.write(("").encode())
        #p.stdin.flush()
        if output == '' and p.poll() is not None:
            break
rc = p.poll()






