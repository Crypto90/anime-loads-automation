# anime-loads-automation
In dieser Repo finden sich allerlei nützliche Scripts um die Verwendung von https://github.com/Pfuenzle/anime-loads komplett zu automatisieren.

Ich selbst lasse das Projekt von @Pfuenzle mitsamt all meiner Scripte in einem Docker Container auf einer Synology DS415+ laufen.

Die Scripte unterteilen sich auf folgende Aufgaben:

# download_anime.py:
Ein Wrapper Script welches den ADD Befehl von https://github.com/Pfuenzle/anime-loads ansteuert und geforderte Eingaben automatisiert, um automatisch einen Titel nach gewünschter Sprache und Qualität auszuwählen.


Einrichtung:

Editiere ```download_anime.py```und setze den Namen des laufenden Docker Conainers für https://github.com/Pfuenzle/anime-loads:

RUNNING_DOCKER_CONTAINER="pfuenzle-anime-loads1"



Nutzung:

```python3 download_anime.py "search_string" [LANGUAGE] [RESOLUTION] [FORCE_ANIME_RESULT_NUMBER] [FORCE_RELEASE_NUMBER] [DRY_RUN]```


Zwingend benötigt:

```"search_string"``` = Sucht nach dem Titel auf anime-loads.org

```[LANGUAGE]``` = ```german```, ```ger```, ```japanese``` oder ```jap```

Standard RESOLUTION wird immer 1080p ausgewählt.


Optional:

```[RESOLUTION]``` = ```1080p``` (standard) oder ```720p```

```[FORCE_ANIME_RESULT_NUMBER]``` = ```2``` (um z.B. den 2. Ergebnisse Treffer für einen Anime Filme oder Serien Titel auszuwählen). ```0```: deaktiviert.

```[FORCE_RELEASE_NUMBER]``` = ```2``` (um z.B. den 2. Release Treffer für einen zuvor gewählten Titel auszuwählen). ```0```: deaktiviert.

```[DRY_RUN]``` = ```1```: Der ADD Prozess läuft voll durch, alle Ausgaben und Inputs sind sichtbar. Gefundene Anime Titel Ergebnisse und Releases können eingesehen werden in der Ausgabe, jedoch wird KEIN DOWNLOAD ausgeführt. Das Script bricht vor dem Download ab! ```0```: deaktiviert.



Die Reihenfolge der Parameter ist wichtig und deren Anzahl! Will man für ```[FORCE_ANIME_RESULT_NUMBER]``` die ```1``` setzen, muss der vorherige Parameter ```[RESOLUTION]``` auch angegeben werden, z.B. ```1080p```.



Beispiel:

Dry run ohne Download, Sprache Deutsch, 1080p, automatisch 1. Ergebnis Titel und 1. Release wählen:

```python3 download_anime.py "search_string" german 1080p 0 0 1```

Download, Sprache Japanisch, 720p, 2. Ergebnis für Titel und 4. Release wählen:

```python3 download_anime.py "search_string" japanese 720p 2 4 0```

Download, Sprache Deutsch, 1080p, automatisch 1. Ergebnis Titel und 1. Release wählen:

```python3 download_anime.py "search_string" german```

```python3 download_anime.py "search_string" ger```



# parseOverseerrRequestsAnimeMoviesAndSeries.py:
Falls https://github.com/sct/overseerr für Requests genutzt wird, kann dieses Script die noch offenen (und genehmigten) Requests von der Overseerr API abfragen und diese Requests auf (Genre=Animation und Originalsprache=Japanisch) oder (Keyword=anime) filten. Die gefundenen Titel werden dann versucht mittels ```download_anime.py``` zuerst in 1080p german und falls nicht gefunden in 1080p Japanisch gesucht und geladen.


Einrichtung:

Editiere ```parseOverseerrRequestsAnimeMoviesAndSeries.py``` und passe die Overseerr Angaben an:

```OVERSEER_API_KEY = "YOUR_OVERSEERR_API_KEY_HERE"```

```OVERSEER_URL = "YOUR_OVERSEERR_URL_HERE"```


Nutzung:

```python3 parseOverseerrRequestsAnimeMoviesAndSeries.py```

Dieses Script erstellt folgende Logs:

```downloading_and_monitoring.txt```: Für jeden erfolgreich durch ```download_anime.py``` hinzugefügten Titel wird ein Eintrag hinterlegt, der ein weiteres Hinzufügen des selben Titels verhindert.


# parseAniSearchPopular20.py:
Durchsucht anisearch.de um die "popular top 20" Deutschen Anime Titel zu parsen. Die gefundenen Titel werden mit https://github.com/sct/overseerr abgeglichen, ob dort selbiger Titel vefügbar ist und ob die mediaInfo einen gesetzen Wert für "plexUrl" hat. Falls nicht, wird die Anfrage an ```download_anime.py``` geleitet. Existiert bereits ein Eintrag in Overseerr mit gesetzer "PlexURL", wird die Anfrage übersprungen.

Einrichtung:

Editiere ```parseAniSearchPopular20.py```und passe den Overseer API KEY und URL an:

```OVERSEER_API_KEY = "YOUR_OVERSEERR_API_KEY_HERE"```

```OVERSEER_URL = "YOUR_OVERSEERR_URL_HERE"


Nutzung:

```python3 parseAniSearchPopular20.py````


# moveFinishedAnimeDownloads.sh:
Dieses Script untersucht den darin gesetzten Download Ordner Pfad auf fertige downloads.

Ein Download Ordner hat immer das Format: ```TITEL LANGUAGE RESOLUTION TYPE```, z.B.:

```Toller Anime Film Name german 1080p movie```

oder

```Toller Anime Serien Name german 1080p tv```

Durch dieses Format ist es möglich, die fertigen Downloads geziehlt zu einem gewünschten Pfad zu verschieben (Pfade in der moveFinishedAnimeDownloads.sh editieren!).

