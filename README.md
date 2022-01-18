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

