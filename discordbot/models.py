import json
import uuid
from datetime import timedelta
from urllib.parse import urlencode

from discord import Colour, Embed
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CounterGroup(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False, null=True)
    title = models.CharField(max_length=20)
    latest_counter_id = models.PositiveIntegerField(blank=True, null=True)
    latest_counter_streak = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'<CounterGroup> {self.title}'

    def to_embed(self):
        return Embed(
            title=f'{self.title}',
            colour=Colour(0xff0074),
            description='\n'.join([x.to_message()
                                   for x in self.counters.all()])
        )


class Counter(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False, null=True)
    title = models.CharField(max_length=20)
    flavor_text = models.TextField(blank=True)
    value_description = models.TextField()
    value = models.IntegerField(default=0)
    group = models.ForeignKey(
        CounterGroup, on_delete=models.SET_NULL, blank=True, null=True, related_name='counters')

    def increment_value(self):
        self.value += 1
        self.save(update_fields=['value'])

    def decrement_value(self):
        self.value -= 1
        self.save(update_fields=['value'])

    def __str__(self):
        return f'{self.title}'

    def to_embed(self):
        return Embed(
            title=f'{self.title}',
            colour=Colour(0xff0074),
            description=f"{self.value_description}: {self.value}"
        )

    def to_message(self):
        return f"{self.value_description}: {self.value}"

    def _update_counter_group(self):
        if self.group.latest_counter_id == self.id:
            self.group.latest_counter_streak += 1
            self.group.save(update_fields=['latest_counter_streak'])
        else:
            self.group.latest_counter_id = self.id
            self.group.latest_counter_streak = 1
            self.group.save(
                update_fields=['latest_counter_id', 'latest_counter_streak'])

    def save(self, *args, **kwargs):
        if self.group:
            self._update_counter_group()
        super().save(*args, **kwargs)


class WFAlert(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    created_at = models.DateTimeField(
        auto_now_add=True, blank=False, null=False)
    announced = models.BooleanField(default=False)
    content = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = 'Warframe Alert'
        verbose_name_plural = 'Warframe Alerts'
        db_table = 'discord_alerts'

    def __str__(self):
        return self.content


class WFSettingsMeta(models.base.ModelBase):
    alerts = {
        'orokin_reactor_bp': _('Orokin Reactor'),
        'orokin_catalyst_bp': _('Orokin Catalyst'),
        'forma_bp': _('Forma'),
        'exilus_ap': _('Exilus Adapter'),
        'fieldron': _('Fieldron'),
        'mutagen_mass': _('Mutagen Mass'),
        'mutalist_nav': _('Mutalist Alad V Nav Coordinate'),
        'detonite_injector': _('Detonite Injector'),
        'snipetron': _('Snipetron Vandal'),
        'twin_vipers': _('Twin Vipers Wraith'),
        'latron': _('Latron Wraith'),
        'strun': _('Strun Wraith'),
        'dera': _('Dera Vandal'),
        'karak': _('Karak Wraith'),
    }

    def __new__(cls, name, bases, attrs, **kwargs):
        for field, label in cls.alerts.items():
            attrs[field] = models.BooleanField(default=False, verbose_name=label)
        return super(WFSettingsMeta, cls).__new__(cls, name, bases, attrs, **kwargs)


class WFSettings(models.Model, metaclass=WFSettingsMeta):
    class Meta:
        db_table = 'discord_wf_settings'


class Brawl(models.Model):
    name = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    victim = models.TextField(blank=True, null=True)
    tool = models.TextField(blank=True, null=True)
    action2 = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'discord_brawl'


class Gachi(models.Model):
    pid = models.IntegerField(blank=True, null=True, default=0)
    url = models.URLField(unique=True, blank=True, null=True)

    class Meta:
        db_table = 'discord_gachi'

    def __str__(self):
        return self.url


class DiscordPicture(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    pid = models.IntegerField(db_column='pID', default=0)
    url = models.URLField(unique=True)
    date = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'discord_pictures'


class DiscordLink(models.Model):
    key = models.CharField(unique=True, blank=False, null=True, max_length=20)
    url = models.URLField()

    class Meta:
        verbose_name_plural = 'Discord Links'
        db_table = 'discord_links'

    def __str__(self):
        return self.url


class DiscordSettings(models.Model):
    key = models.CharField(unique=True, blank=False, null=True, max_length=20)
    value = models.CharField(blank=False, null=True, max_length=50)

    class Meta:
        verbose_name_plural = 'Discord Settings'
        db_table = 'discord_settings'

    def __str__(self):
        return self.value


class DiscordUser(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    wf_settings = models.OneToOneField(
        WFSettings, on_delete=models.CASCADE, blank=True, null=True)
    token = models.CharField(unique=True, blank=True, null=True, max_length=20)

    id = models.IntegerField(
        "Discord ID",
        unique=True,
        blank=True,
        null=False,
        primary_key=True,
        help_text='Required. 18 characters, digits only.',
        validators=[RegexValidator(r'^\d{1,18}$')])

    display_name = models.TextField(
        "Username",
        max_length=40,
        help_text="Current discord display name")

    steam_id = models.CharField(
        "Steam ID",
        blank=True,
        null=False,
        default='',
        max_length=17,
        validators=[RegexValidator(r'^\d{1,17}$')],
        help_text="17 characters, digits only.")

    blizzard_id = models.TextField(
        "Blizzard Tag",
        blank=True,
        null=False,
        default='',
        help_text="Example: Username-0000")

    poe_profile = models.TextField(
        "PoE Account",
        blank=True,
        null=False,
        default='')

    admin = models.BooleanField(
        default=False,
        blank=False,
        null=False,
        help_text="User can execute @admin commands")
    mod_group = models.BooleanField(
        "Moderator",
        default=False,
        blank=False,
        null=False,
        help_text="User can execute @mod commands")
    avatar_url = models.URLField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Discord Users'
        db_table = 'discord_users'
        permissions = [
            ("can_update_ladder", "Can start ladder update"),
            ("can_add_wisdoms", "Can add wisdoms"),
        ]

    def __str__(self):
        return self.display_name


class Wisdom(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    pid = models.IntegerField(db_column='pID', default=0)
    text = models.TextField(unique=True)
    author = models.ForeignKey(
        DiscordUser, on_delete=models.CASCADE, verbose_name="discord user")
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        db_table = 'discord_wisdoms'

    def __str__(self):
        return truncatechars(self.text, 50)


class MixEvent(models.Model):
    # TODO: Webpage with mix statistics
    user = models.ForeignKey(
        DiscordUser, on_delete=models.CASCADE, related_name='mix_events')
    created_at = models.DateTimeField(auto_now_add=True)
    wisdom = models.ForeignKey(Wisdom, on_delete=models.CASCADE)

    def __str__(self):
        return "<MixEvent: {}>".format(self.created_at)


class MarkovText(models.Model):
    text = models.TextField()
    last_update = models.DateTimeField(blank=True, null=True, auto_now=False)
    key = models.CharField(max_length=200, help_text='Unique identifier', unique=True)

    def __str__(self):
        return f'<Markov Text Object: {self.key}>'


class CoronaReportManager(models.Manager):
    def previous_report(self, instance_id):
        try:
            return (self.get_queryset()
                    .filter(timestamp__gte=timezone.now() - timedelta(days=1))
                    .exclude(id=instance_id)
                    .last())
        except (IndexError, ValueError):
            return None


class CoronaReport(models.Model):
    REPORT_FIELDS = ['confirmed', 'recovered', 'deaths']
    API_URL = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/'
    API_ROOT = 'rest/services/ncov_cases/FeatureServer/1/query?'

    confirmed = models.IntegerField()
    recovered = models.IntegerField()
    deaths = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    objects = CoronaReportManager()

    class Meta:
        ordering = ('-timestamp',)

    @classmethod
    def get_api_url(cls):
        return cls.API_URL + cls.API_ROOT + cls.query_data()

    @classmethod
    def query_data(cls):
        return urlencode({
            'outStatistics': [{
                "statisticType": "sum",
                "onStatisticField": field.capitalize(),
                "outStatisticFieldName": field} for field in cls.REPORT_FIELDS],
            'f': 'pjson'
        })

    @property
    def header(self):
        return (f'**Corona report from '
                f'{self.timestamp.strftime("%Y-%m-%d %H-%M-%S")}**\n')

    @property
    def default_report(self) -> Embed:
        report_fields = [f'Total {field.capitalize()}: {getattr(self, field)}'
                         for field in self.REPORT_FIELDS]
        return Embed(
            title=self.header,
            colour=Colour(0xff0074),
            description='\n'.join(report_fields),
        )

    @classmethod
    def generate_embed_report(cls, instance=None, other=None) -> Embed:
        """Calculates difference with previous report, either automatically
        or by sending previous report manually

        Args:
            instance (CoronaReport, optional): First instance of CoronaReport
            other (CoronaReport, optional): Another instance of CoronaReport
            Defaults to None.
        Returns:
            Formatted message for Discord chat
        """
        if not instance:
            instance = cls.objects.first()
            if not instance:
                return 'Not enough data gathered. Please try again in 15 minutes'

        if not other:
            other = cls.objects.previous_report(instance.id)
            # If no previous report was found - send normal message
            if not other:
                return instance.default_report

        if not isinstance(other, CoronaReport):
            raise Exception(
                f'Can not calculate difference between {instance} '
                f'and {other}'
            )
        if other.timestamp >= instance.timestamp:
            raise Exception(
                f'Instance timestamp should be greater than {other} timestamp'
            )

        report_strings = []
        for field in cls.REPORT_FIELDS:
            field_string = ''
            old_value = getattr(other, field)
            new_value = getattr(instance, field)
            diff = new_value - old_value
            field_string += f'Total {field.capitalize()}: {new_value}'
            if diff != 0:
                field_string += f' ({"+" if diff > 0 else "-"}{diff})'
            report_strings.append(field_string)
        footer = f'Compared to report from {other.timestamp.strftime("%Y-%m-%d %H-%M-%S")}'
        embed = Embed(
            title=instance.header,
            colour=Colour(0xff0074),
            description='\n'.join(report_strings),
            footer=footer
        )
        embed.set_footer(text=footer)
        return embed

    def to_embed(self):
        return Embed(
            title=f'{self.title}',
            colour=Colour(0xff0074),
            description='\n'.join([x.to_message()
                                   for x in self.counters.all()])
        )

    def __str__(self):
        return f'Corona Report: {self.timestamp.strftime("%Y-%m-%d %H-%M-%S")}'


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'discorduser'):
        instance.discorduser.save()


def create_discord_token():
    return uuid.uuid4().hex[:20].upper()
