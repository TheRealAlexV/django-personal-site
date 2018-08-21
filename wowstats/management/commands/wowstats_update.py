import json
import logging
import os
import traceback
from time import sleep

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from VertigoProject.settings import WOW_KEY
from wowstats.models import (PVPBracket, WOWAccount, WOWCharacter, WOWSettings,
                             WOWStatSnapshot)

REGIONS = ['eu', 'us', 'kr', 'sea', 'tw']
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    handlers=[
        logging.FileHandler('logs/wowstats_update.log'),
        logging.StreamHandler()
    ])


class Command(BaseCommand):
    help = 'Manages WOWAccount creation and WOWCharacter updates'

    def create_bracket(self, bracket: dict) -> PVPBracket:
        p = PVPBracket.objects.create(
            slug=bracket['slug'],
            rating=bracket['rating'],
            weekly_played=bracket['weeklyPlayed'],
            weekly_won=bracket['weeklyWon'],
            weekly_lost=bracket['weeklyLost'],
            season_played=bracket['seasonPlayed'],
            season_won=bracket['seasonWon'],
            season_lost=bracket['seasonLost'])
        return p

    def get_api_url(self, region):
        return 'https://{}.api.battle.net/'.format(region)

    def get_user_info(self, token):
        return 'account/user?access_token={}'.format(token)

    def get_characters_info(self, token):
        return 'wow/user/characters?access_token={}'.format(token)

    def get_characer_info(self, key=None):
        return "wow/character/{0}/{1}?fields=pvp&locale=en_GB&apikey={2}"

    def update_snapshots(self, account):
        link = "wow/character/{0}/{1}?fields=pvp&locale=en_GB&apikey={2}"
        characters = WOWCharacter.objects.filter(account=account)
        user = account.user
        for character in characters:
            if character.track:
                url = self.get_api_url(account.region) + link.format(
                    character.realm, character.name, WOW_KEY)
                sleep(0.5)
                data = json.loads(requests.get(url).text)
                if data.get('status', None) or not data:
                    logging.error("Can't load player %s", character.id)
                    character.is_pvp = False
                    character.save()
                else:
                    try:
                        character.is_pvp = True
                        character.faction = data.get('faction', None)
                        character.save()
                        pvp_brackets = data['pvp']['brackets']
                        # Load settings
                        qs = (WOWSettings.objects.filter(user=user)
                              .values('track_2v2', 'track_3v3', 'track_rbg'))
                        settings = {k: v for k, v in qs[0].items()}
                        W = WOWStatSnapshot(character=character,
                                            honorable_kills=data['totalHonorableKills'])
                        if settings['track_2v2']:
                            W.arena_2v2 = self.create_bracket(
                                pvp_brackets['ARENA_BRACKET_2v2'])
                        if settings['track_3v3']:
                            W.arena_3v3 = self.create_bracket(
                                pvp_brackets['ARENA_BRACKET_3v3'])
                        if settings['track_rbg']:
                            W.arena_rbg = self.create_bracket(
                                pvp_brackets['ARENA_BRACKET_RBG'])
                        W.save()
                    except:
                        logging.error(data)
                        traceback.print_exc()

    def update_character(self, data):
        character = WOWCharacter.objects.get(
            name=data['name'], realm=data['realm'])
        character.battlegroup = data['battlegroup']
        character.class_id = data['class']
        character.race = data['race']
        character.level = data['level']
        character.gender = data['gender']
        character.achievement_points = data['achievementPoints']
        character.thumbnail = data['thumbnail']
        character.last_modified = data['lastModified']
        character.guild = data.get('guild', None)
        if data.get('spec', None):
            character.spec = data['spec'].get('name', None)
        character.save(update_fields=[
            'battlegroup', 'class_id', 'race', 'last_modified', 'spec',
            'gender', 'achievement_points', 'thumbnail', 'guild', 'level'])

    def update_characters(self, account, session):
        """Creates or updates characters"""
        # Get dict {(name, realm): last_modified} of current characters
        qs = account.wowcharacter_set.values('name', 'realm', 'last_modified')
        saved = {(x['name'], x['realm']): x['last_modified'] for x in qs}
        r = session.get(self.get_api_url(account.region) +
                        self.get_characters_info(account.token))
        data = json.loads(r.text)
        objs = []
        for c in data['characters']:
            # (name, realm) is always unique
            if not (c['name'], c['realm']) in saved:
                logging.info("Creating new character")
                new = (WOWCharacter(
                    account=account,
                    name=c['name'],
                    realm=c['realm'],
                    level=c['level'],
                    battlegroup=c['battlegroup'],
                    class_id=c['class'],
                    race=c['race'],
                    gender=c['gender'],
                    achievement_points=c['achievementPoints'],
                    thumbnail=c['thumbnail'],
                    last_modified=c['lastModified'],
                    guild=c.get('guild', None)))
                if c.get('spec', None):
                    new.spec = c['spec'].get('name', None)
                objs.append(new)
            elif c['lastModified'] != saved[(c['name'], c['realm'])]:
                logging.info('Character info changed!')
                self.update_character(c)
        if objs:
            WOWCharacter.objects.bulk_create(objs)
        self.update_snapshots(account)

    def create_new_account(self, options, user, session):
        """Creates new WOWAccount instance"""
        region = options['region'] if options['region'] in REGIONS else 'eu'
        api_link = self.get_api_url(region)
        try:
            url = api_link + self.get_user_info(options['token'])
            data = json.loads(session.get(url).text)
            logging.debug(data)
            if not data.get('code', None):
                # Create new account
                new_account = WOWAccount.objects.create(
                    user=user,
                    btag=data['battletag'],
                    bnet_id=data['id'],
                    token=options['token'],
                    region=region)
                self.update_characters(new_account, session)

        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def update_token(self, user, options):
        user.wowaccount.token = options['token']
        user.wowaccount.register_date = now()
        user.wowaccount.save(update_fields=['token', 'register_date'])

    def add_arguments(self, parser):
        parser.add_argument('--id', action='store', dest='id', type=int)
        parser.add_argument('--token', action='store', dest='token')
        parser.add_argument('--region', action='store', dest='region')

    def handle(self, *args, **options):
        with requests.Session() as session:
            options['skip_checks'] = True

            if options.get('id', None) and options.get('token', None):
                user = User.objects.get(id=options['id'])
                if not hasattr(user, 'wowaccount'):
                    print('Creating new WOWAccount...')
                    self.create_new_account(options, user, session)
                else:
                    print('Refreshing token...')
                    self.update_token(user, options)
            else:
                qs = WOWAccount.objects.all().prefetch_related('wowcharacter_set')
                for account in qs:
                    self.update_characters(account, session)