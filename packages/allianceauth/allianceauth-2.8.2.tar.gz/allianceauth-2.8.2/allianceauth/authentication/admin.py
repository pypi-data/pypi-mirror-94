from django.conf import settings

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as BaseUser, \
    Permission as BasePermission, Group
from django.db.models import Q, F
from allianceauth.services.hooks import ServicesHook
from django.db.models.signals import pre_save, post_save, pre_delete, \
    post_delete, m2m_changed
from django.db.models.functions import Lower
from django.dispatch import receiver
from django.forms import ModelForm
from django.utils.html import format_html
from django.urls import reverse
from django.utils.text import slugify

from allianceauth.authentication.models import State, get_guest_state,\
    CharacterOwnership, UserProfile, OwnershipRecord
from allianceauth.hooks import get_hooks
from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo,\
    EveAllianceInfo
from allianceauth.eveonline.tasks import update_character
from .app_settings import AUTHENTICATION_ADMIN_USERS_MAX_GROUPS, \
    AUTHENTICATION_ADMIN_USERS_MAX_CHARS

if 'allianceauth.eveonline.autogroups' in settings.INSTALLED_APPS:
    _has_auto_groups = True    
else:
    _has_auto_groups = False


def make_service_hooks_update_groups_action(service):
    """
    Make a admin action for the given service
    :param service: services.hooks.ServicesHook
    :return: fn to update services groups for the selected users
    """
    def update_service_groups(modeladmin, request, queryset):
        if hasattr(service, 'update_groups_bulk'):
            service.update_groups_bulk(queryset)
        else:
            for user in queryset:  # queryset filtering doesn't work here?
                service.update_groups(user)

    update_service_groups.__name__ = str('update_{}_groups'.format(slugify(service.name)))
    update_service_groups.short_description = "Sync groups for selected {} accounts".format(service.title)
    return update_service_groups


def make_service_hooks_sync_nickname_action(service):
    """
    Make a sync_nickname admin action for the given service
    :param service: services.hooks.ServicesHook
    :return: fn to sync nickname for the selected users
    """
    def sync_nickname(modeladmin, request, queryset):
        if hasattr(service, 'sync_nicknames_bulk'):
            service.sync_nicknames_bulk(queryset)
        else:
            for user in queryset:  # queryset filtering doesn't work here?
                service.sync_nickname(user)

    sync_nickname.__name__ = str('sync_{}_nickname'.format(slugify(service.name)))
    sync_nickname.short_description = "Sync nicknames for selected {} accounts".format(service.title)
    return sync_nickname


class QuerysetModelForm(ModelForm):
    # allows specifying FK querysets through kwarg
    def __init__(self, querysets=None, *args, **kwargs):
        querysets = querysets or {}
        super().__init__(*args, **kwargs)
        for field, qs in querysets.items():
            self.fields[field].queryset = qs


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    readonly_fields = ('state',)
    form = QuerysetModelForm
    verbose_name = ''
    verbose_name_plural = 'Profile'

    def get_formset(self, request, obj=None, **kwargs):
        # main_character field can only show current value or unclaimed alts
        # if superuser, allow selecting from any unclaimed main
        query = Q()
        if obj and obj.profile.main_character:
            query |= Q(pk=obj.profile.main_character_id)
            if request.user.is_superuser:
                query |= Q(userprofile__isnull=True)
            else:
                query |= Q(character_ownership__user=obj)
        qs = EveCharacter.objects.filter(query)
        formset = super().get_formset(request, obj=obj, **kwargs)

        def get_kwargs(self, index):
            return {'querysets': {'main_character': EveCharacter.objects.filter(query)}}
        formset.get_form_kwargs = get_kwargs
        return formset

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def user_profile_pic(obj):
    """profile pic column data for user objects

    works for both User objects and objects with `user` as FK to User
    To be used for all user based admin lists (requires CSS)
    """
    user_obj = obj.user if hasattr(obj, 'user') else obj
    if user_obj.profile.main_character:
        return format_html(
            '<img src="{}" class="img-circle">',
            user_obj.profile.main_character.portrait_url(size=32)
        )
    else:
        return None
user_profile_pic.short_description = ''


def user_username(obj):
    """user column data for user objects

    works for both User objects and objects with `user` as FK to User
    To be used for all user based admin lists
    """    
    link = reverse(
        'admin:{}_{}_change'.format(
            obj._meta.app_label,
            type(obj).__name__.lower()
        ), 
        args=(obj.pk,)
    )
    user_obj = obj.user if hasattr(obj, 'user') else obj
    if user_obj.profile.main_character:
        return format_html(
            '<strong><a href="{}">{}</a></strong><br>{}',
            link, 
            user_obj.username,
            user_obj.profile.main_character.character_name
        )
    else:
        return format_html(
            '<strong><a href="{}">{}</a></strong>',
            link, 
            user_obj.username,
        )

user_username.short_description = 'user / main'
user_username.admin_order_field = 'username'


def user_main_organization(obj):
    """main organization column data for user objects

    works for both User objects and objects with `user` as FK to User
    To be used for all user based admin lists
    """
    user_obj = obj.user if hasattr(obj, 'user') else obj
    if not user_obj.profile.main_character:
        result = None
    else:        
        corporation = user_obj.profile.main_character.corporation_name
        if user_obj.profile.main_character.alliance_id:        
            result = format_html('{}<br>{}',
                corporation, 
                user_obj.profile.main_character.alliance_name
            )
        else:
            result = corporation    
    return result

user_main_organization.short_description = 'Corporation / Alliance (Main)'
user_main_organization.admin_order_field = \
    'profile__main_character__corporation_name'


class MainCorporationsFilter(admin.SimpleListFilter):
    """Custom filter to filter on corporations from mains only

    works for both User objects and objects with `user` as FK to User
    To be used for all user based admin lists
    """
    title = 'corporation'
    parameter_name = 'main_corporation_id__exact'

    def lookups(self, request, model_admin):
        qs = EveCharacter.objects\
            .exclude(userprofile=None)\
            .values('corporation_id', 'corporation_name')\
            .distinct()\
            .order_by(Lower('corporation_name'))
        return tuple(
            [(x['corporation_id'], x['corporation_name']) for x in qs]
        )

    def queryset(self, request, qs):
        if self.value() is None:
            return qs.all()
        else:    
            if qs.model == User:
                return qs\
                    .filter(profile__main_character__corporation_id=\
                        self.value())
            else:
                return qs\
                    .filter(user__profile__main_character__corporation_id=\
                        self.value())
            

class MainAllianceFilter(admin.SimpleListFilter):
    """Custom filter to filter on alliances from mains only

    works for both User objects and objects with `user` as FK to User
    To be used for all user based admin lists
    """
    title = 'alliance'
    parameter_name = 'main_alliance_id__exact'

    def lookups(self, request, model_admin):
        qs = EveCharacter.objects\
            .exclude(alliance_id=None)\
            .exclude(userprofile=None)\
            .values('alliance_id', 'alliance_name')\
            .distinct()\
            .order_by(Lower('alliance_name'))
        return tuple(
            [(x['alliance_id'], x['alliance_name']) for x in qs]
        )

    def queryset(self, request, qs):
        if self.value() is None:
            return qs.all()
        else:    
            if qs.model == User:
                return qs\
                    .filter(profile__main_character__alliance_id=self.value())                
            else:
                return qs\
                    .filter(user__profile__main_character__alliance_id=\
                        self.value())
                

def update_main_character_model(modeladmin, request, queryset):    
    tasks_count = 0
    for obj in queryset:
        if obj.profile.main_character:
            update_character.delay(obj.profile.main_character.character_id)
            tasks_count += 1

    modeladmin.message_user(
        request, 
        'Update from ESI started for {} characters'.format(tasks_count)
    )

update_main_character_model.short_description = \
    'Update main character model from ESI'


class UserAdmin(BaseUserAdmin):
    """Extending Django's UserAdmin model
    
    Behavior of groups and characters columns can be configured via settings

    """

    class Media:
        css = {
            "all": ("authentication/css/admin.css",)
        }
         
    class RealGroupsFilter(admin.SimpleListFilter):
        """Custom filter to get groups w/o Autogroups"""
        title = 'group'
        parameter_name = 'group_id__exact'

        def lookups(self, request, model_admin):
            qs = Group.objects.all().order_by(Lower('name'))
            if _has_auto_groups:
                qs = qs\
                    .filter(managedalliancegroup__isnull=True)\
                    .filter(managedcorpgroup__isnull=True)                
            return tuple([(x.pk, x.name) for x in qs])

        def queryset(self, request, queryset):
            if self.value() is None:
                return queryset.all()
            else:    
                return queryset.filter(groups__pk=self.value())

    def get_actions(self, request):
        actions = super(BaseUserAdmin, self).get_actions(request)

        actions[update_main_character_model.__name__] = (
            update_main_character_model, 
            update_main_character_model.__name__, 
            update_main_character_model.short_description
        )

        for hook in get_hooks('services_hook'):
            svc = hook()
            # Check update_groups is redefined/overloaded
            if svc.update_groups.__module__ != ServicesHook.update_groups.__module__:
                action = make_service_hooks_update_groups_action(svc)
                actions[action.__name__] = (
                    action, 
                    action.__name__,
                    action.short_description
                )
            
            # Create sync nickname action if service implements it
            if svc.sync_nickname.__module__ != ServicesHook.sync_nickname.__module__:
                action = make_service_hooks_sync_nickname_action(svc)
                actions[action.__name__] = (
                    action, action.__name__, 
                    action.short_description
                )
        return actions

    def _list_2_html_w_tooltips(self, my_items: list, max_items: int) -> str:    
        """converts list of strings into HTML with cutoff and tooltip"""
        items_truncated_str = ', '.join(my_items[:max_items])
        if not my_items:
            result = None
        elif len(my_items) <= max_items:
            result = items_truncated_str
        else:
            items_truncated_str += ', (...)'
            items_all_str = ', '.join(my_items)
            result = format_html(
                '<span data-tooltip="{}" class="tooltip">{}</span>',
                items_all_str,
                items_truncated_str
            )
        return result
    
    inlines = BaseUserAdmin.inlines + [UserProfileInline]

    ordering = ('username', )
    list_select_related = True
    show_full_result_count = True 
    
    list_display = (
        user_profile_pic,
        user_username, 
        '_state', 
        '_groups',
        user_main_organization,
        '_characters',
        'is_active',
        'date_joined',
        '_role'
    )    
    list_display_links = None

    list_filter = ( 
        'profile__state',
        RealGroupsFilter,        
        MainCorporationsFilter,        
        MainAllianceFilter,
        'is_active',
        'date_joined',
        'is_staff',
        'is_superuser'
    )
    search_fields = (
        'username', 
        'character_ownerships__character__character_name'
    )
    
    def _characters(self, obj):
        my_characters = [
            x.character.character_name 
            for x in CharacterOwnership.objects\
                .filter(user=obj)\
                .order_by('character__character_name')\
                .select_related()
        ]
        return self._list_2_html_w_tooltips(
            my_characters, 
            AUTHENTICATION_ADMIN_USERS_MAX_CHARS
        )
          
    _characters.short_description = 'characters'
    

    def _state(self, obj):
        return obj.profile.state.name
    
    _state.short_description = 'state'
    _state.admin_order_field = 'profile__state'

    def _groups(self, obj):
        if not _has_auto_groups:
            my_groups = [x.name for x in obj.groups.order_by('name')]
        else:
            my_groups = [
                x.name for x in obj.groups\
                    .filter(managedalliancegroup__isnull=True)\
                    .filter(managedcorpgroup__isnull=True)\
                    .order_by('name')
            ]
        
        return self._list_2_html_w_tooltips(
            my_groups, 
            AUTHENTICATION_ADMIN_USERS_MAX_GROUPS
        )
       
    _groups.short_description = 'groups'

    def _role(self, obj):
        if obj.is_superuser:
            role = 'Superuser'
        elif obj.is_staff:
            role = 'Staff'
        else:
            role = 'User'        
        return role
    
    _role.short_description = 'role'
    
    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('auth.change_user')

    def has_add_permission(self, request, obj=None):
        return request.user.has_perm('auth.add_user')

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('auth.delete_user')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """overriding this formfield to have sorted lists in the form"""
        if db_field.name == "groups":
            kwargs["queryset"] = Group.objects.all().order_by(Lower('name'))
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):    
    list_select_related = True
    list_display = ('name', 'priority', '_user_count')
    
    def _user_count(self, obj):
        return obj.userprofile_set.all().count()
    _user_count.short_description = 'Users'

    fieldsets = (
        (None, {
            'fields': ('name', 'permissions', 'priority'),
        }),
        ('Membership', {
            'fields': (
                'public', 
                'member_characters', 
                'member_corporations', 
                'member_alliances'
            ),
        })
    )
    filter_horizontal = [
        'member_characters', 
        'member_corporations', 
        'member_alliances', 
        'permissions'
    ]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """overriding this formfield to have sorted lists in the form"""
        if db_field.name == "member_characters":
            kwargs["queryset"] = EveCharacter.objects.all()\
                .order_by(Lower('character_name'))
        elif db_field.name == "member_corporations":
            kwargs["queryset"] = EveCorporationInfo.objects.all()\
                .order_by(Lower('corporation_name'))
        elif db_field.name == "member_alliances":
            kwargs["queryset"] = EveAllianceInfo.objects.all()\
                .order_by(Lower('alliance_name'))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if obj == get_guest_state():
            return False
        return super(StateAdmin, self).has_delete_permission(request, obj=obj)

    def get_fieldsets(self, request, obj=None):
        if obj == get_guest_state():
            return (
                (None, {
                    'fields': ('permissions', 'priority'),
                }),
            )
        return super(StateAdmin, self).get_fieldsets(request, obj=obj)
    

class BaseOwnershipAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("authentication/css/admin.css",)
        }
     
    list_select_related = True
    list_display = (
        user_profile_pic,
        user_username,
        user_main_organization,
        'character',
    )
    search_fields = (
        'user__username', 
        'character__character_name', 
        'character__corporation_name', 
        'character__alliance_name'
    )
    list_filter = (                 
        MainCorporationsFilter,        
        MainAllianceFilter,
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.pk:
            return 'owner_hash', 'character'
        return tuple()


@admin.register(OwnershipRecord)
class OwnershipRecordAdmin(BaseOwnershipAdmin):
    list_display = BaseOwnershipAdmin.list_display + ('created',)


@admin.register(CharacterOwnership)
class CharacterOwnershipAdmin(BaseOwnershipAdmin):
    def has_add_permission(self, request):
        return False


class PermissionAdmin(admin.ModelAdmin):
    actions = None
    readonly_fields = [field.name for field in BasePermission._meta.fields]
    list_display = ('admin_name', 'name', 'codename', 'content_type')
    list_filter = ('content_type__app_label',)

    @staticmethod
    def admin_name(obj):
        return str(obj)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        # can see list but not edit it
        return not obj


# Hack to allow registration of django.contrib.auth models in our authentication app
class User(BaseUser):
    class Meta:
        proxy = True
        verbose_name = BaseUser._meta.verbose_name
        verbose_name_plural = BaseUser._meta.verbose_name_plural


class Permission(BasePermission):
    class Meta:
        proxy = True
        verbose_name = BasePermission._meta.verbose_name
        verbose_name_plural = BasePermission._meta.verbose_name_plural


try:
    admin.site.unregister(BaseUser)
finally:
    admin.site.register(User, UserAdmin)
    admin.site.register(Permission, PermissionAdmin)


@receiver(pre_save, sender=User)
def redirect_pre_save(sender, signal=None, *args, **kwargs):
    pre_save.send(BaseUser, *args, **kwargs)


@receiver(post_save, sender=User)
def redirect_post_save(sender, signal=None, *args, **kwargs):
    post_save.send(BaseUser, *args, **kwargs)


@receiver(pre_delete, sender=User)
def redirect_pre_delete(sender, signal=None, *args, **kwargs):
    pre_delete.send(BaseUser, *args, **kwargs)


@receiver(post_delete, sender=User)
def redirect_post_delete(sender, signal=None, *args, **kwargs):
    post_delete.send(BaseUser, *args, **kwargs)


@receiver(m2m_changed, sender=User.groups.through)
def redirect_m2m_changed_groups(sender, signal=None, *args, **kwargs):
    m2m_changed.send(BaseUser, *args, **kwargs)


@receiver(m2m_changed, sender=User.user_permissions.through)
def redirect_m2m_changed_permissions(sender, signal=None, *args, **kwargs):
    m2m_changed.send(BaseUser, *args, **kwargs)
