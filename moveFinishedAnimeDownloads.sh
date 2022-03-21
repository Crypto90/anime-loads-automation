#!/bin/bash

#this script checks for anime content (movie/tv type) in the downloads directory
# and moves the folders if they do not show any change for more than 10 minutes.

DOWNLOADS_DIRECTORY=/volume1/Downloads/*


# Type: tv, Language: german
DESTINATION_PATH1="/volume1/video/Anime (Ger)"
PLEX_LIBRARY_ID_TO_REFRESH1=2

# Type: movie, Language: german
DESTINATION_PATH2="/volume1/video/Filme"
PLEX_LIBRARY_ID_TO_REFRESH2=2

# Type: tv, Language: japanese
DESTINATION_PATH3="/volume1/video/Anime (Jap)"
PLEX_LIBRARY_ID_TO_REFRESH3=3

# Type: movie, Language: japanese
DESTINATION_PATH4="/volume1/video/Filme (Jap)"
PLEX_LIBRARY_ID_TO_REFRESH4=25

# You also have to check and edit the DESTINATION_PATH and if you use plex the plex url and library id.

# the script checks the modified date of the files inside the tv and movie folders.
# only move files that are no more modified since X minutes
MOVE_FILES_AFTER_MODIFIED_IDLE_MINUTES=10


# on finish moving, the wget command does a plex library refresh for the target library with its section id.
# if you use it, set your plex url, token for an admin access and the above PLEX_LIBRARY_ID_TO_REFRESH section ids.
# if you don't use plex, comment out all "wget -q "$PLEX_URL..." commands.
PLEX_URL="YOUR_PLEX_URL_FOR_LIBRARY_REFRESHES"
PLEX_TOKEN="YOUR_PLEX_TOKEN_TO_REFRESH_LIBRARIES"

echo ""
echo ""
echo "### checking for 'german' and 'tv' (anime shows) ###"
for d in $DOWNLOADS_DIRECTORY ; do
	if [[ "$d" =~ .*" german 1080p tv" ]] || [[ "$d" =~ .*" german 720p tv" ]]; then
		if [[ $(find "$d" -mmin -$MOVE_FILES_AFTER_MODIFIED_IDLE_MINUTES -ls) ]] || [[ $(find "$d" -name '*.rar*') ]]; then
			echo "$d download is still processing..."
		else
			echo "$d had no more changes since $MOVE_FILES_AFTER_MODIFIED_IDLE_MINUTES minutes. Begin moving..."
			#echo "$d"
			BASE_DIR=$(basename "$d")
			BASE_DIR=${BASE_DIR//" german 1080p tv"/}
			BASE_DIR=${BASE_DIR//" german 720p tv"/}
						
			echo "moving folder: mv \"$d\" to \"$DESTINATION_PATH1/$BASE_DIR\""
			mv "$d" "$DESTINATION_PATH1/$BASE_DIR"
			mv "$d/"* "$DESTINATION_PATH1/$BASE_DIR/" && rm -rf "$d"
			
			# after moving, refresh plex library: Anime (Ger)
			wget -q "$PLEX_URL/library/sections/$PLEX_LIBRARY_ID_TO_REFRESH/refresh?X-Plex-Token=$PLEX_TOKEN" -O /dev/null
		fi
	fi
done

echo ""
echo ""
echo "### checking for 'german' and 'movie' (anime movies) ###"
for d in $DOWNLOADS_DIRECTORY ; do
	if [[ "$d" =~ .*" german 1080p movie" ]] || [[ "$d" =~ .*" german 720p movie" ]]; then
		if [[ $(find "$d" -mmin -$MOVE_FILES_AFTER_MODIFIED_IDLE_MINUTES -ls) ]] || [[ $(find "$d" -name '*.rar*') ]]; then
			echo "$d download is still processing..."
		else
			echo "$d had no more changes since $MOVE_FILES_AFTER_MODIFIED_IDLE_MINUTES minutes. Begin moving..."
			#echo "$d"
			BASE_DIR=$(basename "$d")
			BASE_DIR=${BASE_DIR//" german 1080p movie"/}
			BASE_DIR=${BASE_DIR//" german 720p movie"/}
						
			echo "moving folder: mv \"$d\" to \"$DESTINATION_PATH2/$BASE_DIR\""
			mv "$d" "$DESTINATION_PATH2/$BASE_DIR"
			mv "$d/"* "$DESTINATION_PATH2/$BASE_DIR/" && rm -rf "$d"
			
			# after moving, refresh plex library: Filme
			wget -q "$PLEX_URL/library/sections/$PLEX_LIBRARY_ID_TO_REFRESH2/refresh?X-Plex-Token=$PLEX_TOKEN" -O /dev/null
		fi
		
	fi
done


echo ""
echo ""
echo "### checking for 'japanese' and 'tv' (anime shows) ###"
for d in $DOWNLOADS_DIRECTORY ; do
	if [[ "$d" =~ .*" japanese 1080p tv" ]] || [[ "$d" =~ .*" japanese 720p tv" ]]; then
		if [[ $(find "$d" -mmin -$MOVE_FILES_AFTER_MODIFIED_IDLE_MINUTES -ls) ]] || [[ $(find "$d" -name '*.rar*') ]]; then
			echo "$d download is still processing..."
		else
			echo "$d had no more changes since $MOVE_FILES_AFTER_MODIFIED_IDLE_MINUTES minutes. Begin moving..."
			#echo "$d"
			BASE_DIR=$(basename "$d")
			BASE_DIR=${BASE_DIR//" japanese 1080p tv"/}
			BASE_DIR=${BASE_DIR//" japanese 720p tv"/}
						
			echo "moving folder: mv \"$d\" to \"$DESTINATION_PATH3/$BASE_DIR\""
			mv "$d" "$DESTINATION_PATH3/$BASE_DIR"
			mv "$d/"* "$DESTINATION_PATH3/$BASE_DIR/" && rm -rf "$d"
			
			# after moving, refresh plex library: Anime (Jap)
			wget -q "$PLEX_URL/library/sections/$PLEX_LIBRARY_ID_TO_REFRESH3/refresh?X-Plex-Token=$PLEX_TOKEN" -O /dev/null
		fi
		
	fi
done



echo ""
echo ""
echo "### checking for 'japanese' and 'movie' (anime movies) ###"
for d in $DOWNLOADS_DIRECTORY ; do
	if [[ "$d" =~ .*" japanese 1080p movie" ]] || [[ "$d" =~ .*" japanese 720p movie" ]]; then
		if [[ $(find "$d" -mmin -$MOVE_FILES_AFTER_MODIFIED_IDLE_MINUTES -ls) ]] || [[ $(find "$d" -name '*.rar*') ]]; then
			echo "$d download is still processing..."
		else
			echo "$d had no more changes since $MOVE_FILES_AFTER_MODIFIED_IDLE_MINUTES minutes. Begin moving..."
			#echo "$d"
			BASE_DIR=$(basename "$d")
			BASE_DIR=${BASE_DIR//" japanese 1080p movie"/}
			BASE_DIR=${BASE_DIR//" japanese 720p movie"/}
			
			echo "moving folder: mv \"$d\" to \"$DESTINATION_PATH4/$BASE_DIR\""
			mv "$d" "$DESTINATION_PATH4/$BASE_DIR"
			mv "$d/"* "$DESTINATION_PATH4/$BASE_DIR/" && rm -rf "$d"
			
			# after moving, refresh plex library: Filme (Jap)
			wget -q "$PLEX_URL/library/sections/$PLEX_LIBRARY_ID_TO_REFRESH4/refresh?X-Plex-Token=$PLEX_TOKEN" -O /dev/null
		fi
		
	fi
done

echo ""
echo ""
