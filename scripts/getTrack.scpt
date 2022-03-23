tell application "Music"
	if player state is playing then
		set tRawData to (get raw data of artwork 1 of current track)
		set tName to name of current track
		set tArtist to artist of current track
		set tPosition to player position div 1
		set tDuration to (duration of current track) div 1
		set tAlbum to album of current track
	else
		return none
	end if
end tell

tell application "Finder"
	set currentPath to container of (((path to me as text) & "::") as alias) as string
end tell

set newPath to ((currentPath as text) & "share:albumcover.jpg") as text
tell me to set fileRef to (open for access newPath with write permission)
write tRawData to fileRef starting at 0
tell me to close access fileRef

return {trackName:tName, trackArtist:tArtist, trackPosition:tPosition, trackDuration:tDuration, trackAlbum:tAlbum}