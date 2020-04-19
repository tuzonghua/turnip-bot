# turnip-bot
A simple Discord bot for the Turnip Stonks server

## Prerequisites
The bot uses the discord.py API to interact with 
Discord. It also uses the dotenv package to better
manage secrets.

Create a Python 3 virtual environment:

```
$ virtualenv -p python3 ~/path/to/venv/turnip-bot/
```

Activate the new environment:

```
$ source ~/path/to/venv/turnip-bot/bin/activate
```

Install the required PyPI packages

```
$ pip install -r requirements.txt
```

## Setting all the secrets
The code uses the dotenv package. First move `sample.env`
to a dotfile `.env` in the same directory. Then edit the
file with all the relevant secrets (guild ID, channel IDs,
etc.).
 