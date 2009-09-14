from django import forms
from django.db import models
from django.conf import settings
from trustedhtml.classes import Html
from trustedhtml.signals import rule_done, rule_exception
from pages.models import Page, Content
from photologue.models import Gallery

class Log(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField()
    source = models.TextField()
    result = models.TextField()
    sender = models.CharField(max_length=100)
    rule = models.TextField()

def log(sender, rule, value, source, **kwargs):
    Log.objects.create(valid='exception' not in kwargs, source=source,
        result=value, sender=unicode(sender), rule=unicode(rule.__dict__))
    return value

if getattr(settings, 'TRUSTEDHTML_ENABLE_LOG', False):
    rule_done.connect(log, sender=Html)