from django.contrib import admin

from .models import AuthTS, Teamspeak3User, StateGroup
from ...admin import ServicesUserAdmin


@admin.register(Teamspeak3User)
class Teamspeak3UserAdmin(ServicesUserAdmin):    
    list_display = ServicesUserAdmin.list_display + (        
        'uid',
        'perm_key'        
    )
    search_fields = ServicesUserAdmin.search_fields + ('uid', )
    

@admin.register(AuthTS)
class AuthTSgroupAdmin(admin.ModelAdmin):
    ordering = ('auth_group__name', )
    list_select_related = True  
    
    list_display = ('auth_group', '_ts_group')
    list_filter = ('ts_group', )
    
    fields = ('auth_group', 'ts_group')
    filter_horizontal = ('ts_group',)

    def _ts_group(self, obj):
        return [x for x in obj.ts_group.all().order_by('ts_group_id')]
    
    _ts_group.short_description = 'ts groups'
    #_ts_group.admin_order_field = 'profile__state'


@admin.register(StateGroup)
class StateGroupAdmin(admin.ModelAdmin):
    list_display = ('state', 'ts_group')
    search_fields = ('state__name', 'ts_group__ts_group_name')
