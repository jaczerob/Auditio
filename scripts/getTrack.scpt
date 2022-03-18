tell application "Music"
	if player state is playing then
		set tName to name of current track
		set tArtist to artist of current track
		set tPosition to player position div 1
		set tDuration to (duration of current track) div 1
		set tAlbum to album of current track
		return {trackName:tName, trackArtist:tArtist, trackPosition:tPosition, trackDuration:tDuration, trackAlbum:tAlbum}
	else
		return none
	end if
end tell