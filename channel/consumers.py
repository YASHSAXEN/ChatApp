from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
# from channels.db import database_sync_to_async
import json
from channel.models import ChatMessages, Groupname
from datetime import datetime

class MyWebsocketConsumer(WebsocketConsumer):
    el = ''
    def connect(self):
        self.accept()
        self.groupname = self.scope['url_route']['kwargs']['groupname']
        async_to_sync(self.channel_layer.group_add)(self.groupname,self.channel_name)
        group = Groupname.objects.get(group=self.groupname)
        member = group.member
        if member == '':
            member = [str(self.scope['user'])]
            group.member = str(member)
            group.member_count = len(member)
            group.save()
            user_data = {'user':str(self.scope['user']),'status':'new','ct':len(member)}
            user_data_json = json.dumps(user_data)
            async_to_sync(self.channel_layer.group_send)(
                    self.groupname,
                    {
                        'type':'chat.message', # event
                        'text':user_data_json
                    })
        else:
            member = eval(member)
            if str(self.scope['user']) not in member:
                member.append(str(self.scope['user']))
                group.member = str(member)
                group.member_count = len(member)
                group.save()
                if MyWebsocketConsumer.el != str(self.scope['user']):
                    user_data = {'user':str(self.scope['user']),'status':'new','ct':len(member)}
                    user_data_json = json.dumps(user_data)
                    async_to_sync(self.channel_layer.group_send)(
                            self.groupname,
                            {
                                'type':'chat.message', # event
                                'text':user_data_json
                                })
                else:
                    user_data = {'ct':len(member),'status':'change'}
                    user_data_json = json.dumps(user_data)
                    async_to_sync(self.channel_layer.group_send)(
                        self.groupname,
                        {
                            'type':'chat.message', # event
                            'text':user_data_json,
                        })
                    
    def receive(self, text_data=None, bytes_data=None):
        if text_data == 'close':
            self.close(1000)
        elif text_data == 'private_false':
            group = Groupname.objects.get(group=self.groupname)
            group.private = True
            group.save()
            user_data = {'status':'private',"value":'true'}
            user_data_json = json.dumps(user_data)
            async_to_sync(self.channel_layer.group_send)(
                self.groupname,
                {
                    'type':'chat.message', # event
                    'text':user_data_json,
                })
        elif text_data == 'public_true':
            group = Groupname.objects.get(group=self.groupname)
            group.private = False
            group.save()
            user_data = {'status':'private',"value":'false'}
            user_data_json = json.dumps(user_data)
            async_to_sync(self.channel_layer.group_send)(
                self.groupname,
                {
                    'type':'chat.message', # event
                    'text':user_data_json,
                })
        else:
            message_data = {'user':str(self.scope['user']),"message":text_data,'status':'message'}
            group = Groupname.objects.filter(group=self.groupname)[0]
            user = ChatMessages(user=str(self.scope['user']),message=text_data,groupname=group)
            user.save()
            # Get the current time
            now = datetime.now()
            # Format the time in 12-hour format with AM/PM
            formatted_time = now.strftime("%I:%M %p").lower()
            # Convert AM/PM to lowercase with periods
            formatted_time = formatted_time.replace("am", "a.m.").replace("pm", "p.m.")
            message_data['time'] = formatted_time
            message_data_json = json.dumps(message_data)
            async_to_sync(self.channel_layer.group_send)(
                self.groupname,
                {
                    'type':'chat.message', # event
                    'text':message_data_json
                })
        
    # every event has an handler function, if the event name is help.event then its handler name is help_event(), and every handler must conatin two arguments i.e self and event.
    def chat_message(self,event):
        self.send(text_data=event['text'])

    def disconnect(self, code):
        group = Groupname.objects.get(group=self.groupname)
        member = eval(group.member)
        index = member.index(str(self.scope['user']))
        MyWebsocketConsumer.el = member.pop(index)
        group.member = str(member)
        group.member_count = len(member)
        if len(member) == 0:
            group.last_active = datetime.now()
        group.save()
        if code == 1000:
            user_data = {'user':str(self.scope['user']),'status':'close','ct':len(member)}
            user_data_json = json.dumps(user_data)
            async_to_sync(self.channel_layer.group_send)(
                self.groupname,
                {
                    'type':'chat.message', # event
                    'text':user_data_json,
                })
        if code == 1001:
            user_data = {'ct':len(member),'status':'change'}
            user_data_json = json.dumps(user_data)
            async_to_sync(self.channel_layer.group_send)(
                self.groupname,
                {
                    'type':'chat.message', # event
                    'text':user_data_json,
                })
        async_to_sync(self.channel_layer.group_discard)(self.groupname, self.channel_name)
        StopConsumer()