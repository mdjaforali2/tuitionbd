from django.contrib import admin
from .models import Comment, Postfile, Contact, Post
from django.utils.html import format_html

from django.utils import timezone

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin


admin.site.site_title = 'TuitionBD Admin Panel'
admin.site.index_title = 'TuitionBD Admin Panel'
# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment

class PostfileInline(admin.TabularInline):
    model = Postfile

class PostAdmin(admin.ModelAdmin):
    # fields = ('user', 'title')
    # exclude = ('user', 'title')
    # readonly_fields = ('slug',)
    list_display = ('user', 'title', 'created_at', 'salary', 'created_since')
    list_filter = ('user',)
    search_fields = ('details', 'user__username',)
    list_editable = ('salary',)
    list_display_links = ('title',)
    actions = ('change_salary_3000',)
    inlines = [
        CommentInline,
        PostfileInline
    ]

    # def title_html_display(self, obj):
    #     return format_html(
    #         f'<span style="font-size: 20px; color:blue;"> {obj.title}</span>'
    #     )
    
    
    def created_since(self, Post):
        diff = timezone.now() - Post.created_at
        return diff.days



    def change_salary_3000(self, request, queryset):
        count = queryset.update(salary=3000.0)
        self.message_user(request, '{} posts updated'.format(count))
    change_salary_3000.short_description = 'Change Salary'

class DistrictAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
        

admin.site.register(Contact)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Postfile)

