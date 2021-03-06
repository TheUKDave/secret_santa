from django.contrib import admin

from .models import Person, SantaList


admin.site.register(Person)


class SantaListAdmin(admin.ModelAdmin):

    list_display = ['name', 'organiser_email']
    ordering = ['name']
    readonly_fields = ['slug', 'secure_hash_signup', 'secure_hash_review']


admin.site.register(SantaList, SantaListAdmin)
