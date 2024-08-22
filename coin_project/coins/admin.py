from django.contrib import admin
from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_pic']

@admin.register(Continent)
class ContinentsAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Country)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'material',
        'box',
        'circulation',
        'owner',
        'status',
        ]
    list_filter = [
        'box',
    ]

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'recipient', 'is_read', 'created']
