from django.contrib import admin

from discordbot.models import DiscordUser
from poeladder.models import PoeCharacter


class ProfileFilter(admin.SimpleListFilter):
    title = 'Profile'
    parameter_name = 'profile'

    def lookups(self, request, model_admin):
        profiles = (DiscordUser.objects
                    .exclude(poe_profile__isnull=True)
                    .exclude(poe_profile=''))
        print(profiles)
        return [(x.id, x.poe_profile) for x in profiles]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(profile_id=self.value())


@admin.register(PoeCharacter)
class PoeCharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'class_name', 'level', 'league')
    search_fields = ('name',)
    list_filter = ('league', ProfileFilter)
    exclude = ['gems']

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]
