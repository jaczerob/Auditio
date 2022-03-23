# Auditio
Apple Music RPC interface for Discord. 

Made to run in the background of your computer and will update your presence every 5 seconds if Apple Music and Discord is running.

## How to use
```zsh
git clone https://github.com/jaczerob/Auditio.git
cd Auditio
python3 main.py
```

Recommended to make a launchctl .plist file for this program.

## Album Covers
Album covers are powered by the ngrok. Sign up for a free ngrok account and follow the steps below to add album cover support. 

Make a file called `ngrok.yaml` in the `config` folder and set it like so: 

```yaml
auth_token: xxxxx
```

Optionally, you can add other ngrok config options in the file.
