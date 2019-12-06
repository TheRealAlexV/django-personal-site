from django.contrib import admin

from poeladder.models import PoeCharacter


@admin.register(PoeCharacter)
class PoeCharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'class_name', 'level', 'league')
    search_fields = ('name',)
    list_filter = ('league',)
    exclude = ['gems']

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]
