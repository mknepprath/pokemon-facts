# Pokémon Facts

A bot that tweets random Pokémon facts.

Set up:

1. `pip install Mastodon.py`.
2. Export environment variables.
3. `python3 {filename}` to run.

## Environment Variables

Environment variables can be fetched from AWS. They should be added to this repo
in a file called `.env.local`:

```bash
MASTODON_CLIENT_KEY=...
MASTODON_CLIENT_SECRET=...
MASTODON_ACCESS_TOKEN=...
```

## Publishing

### Dependencies

To deploy this app, run:

```bash
sh deploy.sh
```

## main.py

This script fetches a card from a Pokémon API and posts it.
