# Generated by Django 5.0.6 on 2024-05-24 06:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
        ('decks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='deck_cards',
        ),
        migrations.CreateModel(
            name='DeckCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.card')),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decks.deck')),
            ],
        ),
    ]
