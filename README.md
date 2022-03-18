# Apple Music RPC
Apple Music RPC interface for Discord. 

Made to run in the background of your computer and will update your presence every 5 seconds if Apple Music and Discord is running.

![Example image](https://media.discordapp.net/attachments/714581563022770218/932011802018082826/unknown.png)

## How to use
```zsh
git clone https://github.com/thewallacems/apple-music-rpc.git
cd apple-music-rpc
python3 main.py
```

Recommended to make a launchctl .plist file for this program.

## Album Covers
Album covers are powered by the cloudinary API which is free for anyone to use. Sign up at https://cloudinary.com/ for a free account and follow the steps below to set it up.

1. In your `config.yaml` file set album_cover to true.
2. Make a file called `cloudinary.yaml` and set it like so: 

```yaml
cloud_name: cloudname
api_key: 'api_key'
api_secret: api_secret
```

`api_key` **MUST** be wrapped in apostrophes!
