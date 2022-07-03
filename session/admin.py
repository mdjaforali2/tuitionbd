from django.contrib import admin
from .models import UserProfile, TuitionProfile, Division, District, Upazilla, Qualification


from import_export.admin import ImportExportModelAdmin
from django.contrib import admin


class DivisionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...

class DistrictAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        list_display = ('name', 'id')
        search_fields = ('name', 'id')

class UpazillaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        list_display = ('name', 'id')
        search_fields = ('name', 'id')

# class UnionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#         ...



# Register your models here.        
admin.site.register(Division, DivisionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Upazilla, UpazillaAdmin)
# admin.site.register(Union, UnionAdmin)
admin.site.register(UserProfile)
admin.site.register(TuitionProfile)
admin.site.register(Qualification)