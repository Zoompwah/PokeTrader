import requests, json
from django.core.management.base import BaseCommand
from collection.models import Card

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        res = requests.get("https://api.pokemontcg.io/v2/cards?q=nationalPokedexNumbers:[1 TO 151]")
        data = json.loads(res.text)
        cards = data.get('data')

        for card in cards:
            try:
                Card.objects.get(name=card.get('name', ''))
            except Card.DoesNotExist:
                abilities = []
                abilities_json = card.get('abilities', [])
                for ability in abilities_json:
                    abilities.append(ability.get('name', ''))

                attacks = []
                attacks_json = card.get('attacks', [])
                for attack in attacks_json:
                    attacks.append(attack.get('name', ''))

                weaknesses = []
                weaknesses_json = card.get('weaknesses', [])
                for weakness in weaknesses_json:
                    weaknesses.append(weakness.get('type', ''))

                Card.objects.get_or_create(
                    name = card.get('name', ''),
                    card_image = card.get('images', '').get('small', ''),
                    types = card.get('types', ''),
                    abilities = json.dumps(abilities),
                    attacks = json.dumps(attacks),
                    weaknesses = json.dumps(weaknesses),
                )

