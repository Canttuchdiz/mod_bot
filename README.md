# Lily Bot

Lily Bot is a Discord Bot dedicated to moderation.

## Installation

Get the repository from [github](https://github.com/) to install this bot.
```bash
git clone https://github.com/Canttuchdiz/lily_bot.git
```

Make a .env file as another project file:
```
token = (your token)
```

Build and run the bot by running:
```bash
docker compose up -d --build
```

Every once and awhile run:
```bash
docker system prune -a
```

## Usage

The built in ``/ban``, ``/kick``, and ``/timeout`` are logged as an infraction,
as well as the bot's ``/warn``. The list of commands show up when you do ``/``.

## Notes

In any text channel, the owner must run ``!sync`` the first time you run
your bot.

For any configuration use the ``config.py`` file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
