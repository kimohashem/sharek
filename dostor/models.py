from django.db import models
from django.utils import timezone
from datetime import datetime
from markitup.fields import MarkupField
from django.core import exceptions
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30, default='')
    slug = models.SlugField(max_length=50, unique=True, help_text="created from name")
    #photo = models.ImageField(upload_to="dostor/static/photos/", blank=True)
    summary = MarkupField(blank=True, default='')

    def __unicode__(self):
        #return u'%s - %s' % (self.topic.name, self.name)
        return self.name

    def get_absolute_url(self):
        return "/%s" % (self.slug)
    
    def get_articles(self):
        return Article.objects.filter(tag_id= self.id)
        
    class Meta:
       ordering = ["name"]
       
class Article(models.Model):
    tags = models.ManyToManyField(Tag)
    name = models.CharField(max_length=40)
    slug 	 = models.SlugField(max_length=40, unique=True, help_text="created from name")
    summary = MarkupField(blank=True, default='')

    def feedback_count(self):
        return len(Feedback.objects.filter(article_id = self.id))

    def get_votes(self):
        return Rating.objects.filter(article_id= self.id)

    def clean(self):
        if len(self.name) >= 40:
            raise exceptions.ValidationError('Too many characters ...')
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/" % (self.slug)

    class Meta:
       ordering = ["name"] 

class Feedback(models.Model):
    article = models.ForeignKey(Article)
    name = models.CharField(max_length=200)
    email = models.SlugField(default='')
    suggestion = MarkupField(default='')
    date = models.DateTimeField(default=timezone.make_aware(datetime.now(),timezone.get_default_timezone()).astimezone(timezone.utc))
    order = models.IntegerField(default=0)
    user = models.CharField(max_length=200,default='')

class Rating(models.Model):
    article = models.ForeignKey(Article)
    feedback = models.ForeignKey(Feedback)
    user = models.CharField(max_length=200,default='')
    vote = models.BooleanField()