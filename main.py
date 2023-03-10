import os
import random
from time import sleep

import requests
from mastodon import Mastodon


def main():
    mastodon = Mastodon(
        api_base_url='https://mastodon.social',
        client_id=os.environ.get('MASTODON_CLIENT_KEY'),
        client_secret=os.environ.get('MASTODON_CLIENT_SECRET'),
        access_token=os.environ.get('MASTODON_ACCESS_TOKEN'),
    )

    # get total number of Pokémon
    response = requests.get(
        'https://pokeapi.co/api/v2/pokemon-species/?limit=1')
    total = response.json()["count"]

    # random number between 1 and total number of Pokémon
    page = random.randint(1, total)

    response = requests.get(
        'https://pokeapi.co/api/v2/pokemon/%s' % page)
    pokemon = response.json()

    response = requests.get(
        'https://pokeapi.co/api/v2/pokemon-species/%s' % page)
    species = response.json()

    sprites = []

    def find_sprites(d):
        for k, v in d.items():
            if isinstance(v, dict):
                find_sprites(v)
            elif isinstance(v, str):
                sprites.append(v)

    find_sprites(pokemon["sprites"])
    sprite = random.choice(sprites)

    # filter only english flavor text
    entries = species["flavor_text_entries"] = list(
        filter(lambda x: x["language"]["name"] == "en", species["flavor_text_entries"]))

    entry = ""

    # check if there are entries
    if len(entries) == 0:
        print("No entries")
    else:
        # get random flavor text
        flavor_text = random.choice(entries)
        entry = flavor_text["flavor_text"].replace("\n", " ")

    # get english name in list of names
    name = list(filter(lambda x: x["language"]["name"] == "en", species["names"]))[0]["name"]

    filename = "/tmp/temp.png"
    request = requests.get(sprite, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        alt_text = "#%s: %s" % (
            page, name)

        status = ""
        if entry != "":
            status = "#%s %s: %s" % (
                page, name, entry)
        else:
            status = "#%s %s" % (
                page, name)

        print(status)
        print(sprite)

        mastodon_media_response = mastodon.media_post(
            filename, description=alt_text)

        sleep(3)

        if mastodon_media_response.id:
            mastodon.status_post(status=status, media_ids=[
                mastodon_media_response.id])

        os.remove(filename)
    else:
        print("Unable to download image")


if __name__ == "__main__":
    main()
