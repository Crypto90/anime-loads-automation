# anime-loads-automation
In dieser Repo finden sich allerlei nützliche Scripts um die Verwendung von https://github.com/Pfuenzle/anime-loads komplett zu automatisieren.

Ich selbst lasse das Projekt von @Pfuenzle mitsamt all meiner Scripte in einem Docker Container auf einer Synology DS415+ laufen.

Die Scripte unterteilen sich auf folgende Aufgaben:

# download_anime.py:
Ein Wrapper Script welches den ADD Befehl von https://github.com/Pfuenzle/anime-loads ansteuert und geforderte Eingaben automatisiert, um automatisch einen Titel nach gewünschter Sprache und Qualität auszuwählen.


Nutzung:

```python3 download_anime.py "search_string" [LANGUAGE] [RESOLUTION] [FORCE_ANIME_RESULT_NUMBER] [FORCE_RELEASE_NUMBER] [DRY_RUN]```

Zwingend benötigt:

"search_string" = Sucht nach dem Titel auf anime-loads.org

[LANGUAGE] = german, ger, japanese oder jap

[RESOLUTION] = 1080p oder 720p


Optional:

[FORCE_ANIME_RESULT_NUMBER] = 2 (um z.B. den 2. Ergebnisse Treffer für einen Anime Filme oder Serien Titel auszuwählen). 0: deaktiviert.

[FORCE_RELEASE_NUMBER] = 2 (um z.B. den 2. Release Treffer für einen zuvor gewählten Titel auszuwählen). 0: deaktiviert.

[DRY_RUN] = Der ADD Prozess läuft voll durch, alle Ausgaben und Inputs sind sichtbar. Gefundene Anime Titel Ergebnisse und Releases können eingesehen werden in der Ausgabe, jedoch wird KEIN DOWNLOAD ausgeführt. Das Script bricht vor dem Download ab!

