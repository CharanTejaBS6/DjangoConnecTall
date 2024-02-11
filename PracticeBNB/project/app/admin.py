from django.contrib import admin
from app.models import Event, Registration , Comment , RaisedHand

# Register your models here.
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Comment)
admin.site.register(RaisedHand)

