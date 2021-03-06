from core.models import Tag
from core.models import Topic
from core.models import Info, Feedback, ArticleDetails, ArticleHeader
from core.models import ReadOnlyAdminFields
from django.contrib.auth.models import User
from django import forms
from core.actions import export_as_csv_action

from django.contrib import admin



class ArticleDetailsInlineAdmin(admin.TabularInline):
    model      = ArticleDetails
    extra      = 0
    can_delete = True
    fields     = ['current', 'slug','summary','mod_date']

class ArticleForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField( queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta: 
         model = ArticleHeader

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        if self.instance:
            tags = Tag.objects.all()
            self.fields['tags'].queryset = tags

class ArticleHeaderAdmin(admin.ModelAdmin):
    inlines = [ArticleDetailsInlineAdmin,]
    list_display = ('name','topic','order')
    list_filter = ('topic',)
    list_editable = ['order']
    search_fields = ['name']
    form = ArticleForm

    class Media:
        js = ( 'js/jquery.min.js', 'js/jquery-ui.min.js', 'js/admin-list-reorder.js', 'js/admin-current-article.js')

class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ('articledetails',)
    search_fields = ['suggestion']
    list_display = ('name', 'articledetails','user', 'email', 'suggestion')
    

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ('short_name','name','order')
    list_editable = ['order']

    class Media:
        js = ( 'js/jquery.min.js', 'js/jquery-ui.min.js', 'js/admin-list-reorder.js', )

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ('name','short_name','order')
    list_editable = ['order']

    class Media:
        js = ( 'js/jquery.min.js', 'js/jquery-ui.min.js', 'js/admin-list-reorder.js', )

class InfoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ('name',)

    class Media:
        js = ( 'js/jquery.min.js', 'js/jquery-ui.min.js', 'js/admin-list-reorder.js', )

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username' ,'first_name', 'last_name', 'is_staff', 'is_active')
    list_editable = ['is_staff', 'is_active']
    list_filter = ('is_staff', 'is_active')
    search_fields = ['email', 'username' ,'first_name', 'last_name']

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def get_actions(self, request):
       actions = super(UserAdmin, self).get_actions(request)
       try:
           del actions['delete_selected']
       except KeyError:
           pass
       return actions
    
admin.site.register(ArticleHeader, ArticleHeaderAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
