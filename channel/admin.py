from django.contrib import admin
from channel.models import ChatMessages, Groupname
# Register your models here.

@admin.register(ChatMessages)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id','user','message','groupname','file']

@admin.register(Groupname)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ['id','group','member_count','member']