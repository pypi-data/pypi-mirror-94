from unittest.mock import patch

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client

from allianceauth.authentication.models import CharacterOwnership, State
from allianceauth.eveonline.models import (
    EveCharacter, EveCorporationInfo, EveAllianceInfo
)

from ..admin import HasLeaderFilter, GroupAdmin, Group
from . import get_admin_change_view_url

if 'allianceauth.eveonline.autogroups' in settings.INSTALLED_APPS:
    _has_auto_groups = True
    from allianceauth.eveonline.autogroups.models import AutogroupsConfig
    from ..admin import IsAutoGroupFilter
else:
    _has_auto_groups = False


MODULE_PATH = 'allianceauth.groupmanagement.admin'


class MockRequest(object):
    
    def __init__(self, user=None):
        self.user = user


class TestGroupAdmin(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # group 1 - has leader
        cls.group_1 = Group.objects.create(name='Group 1')        
        cls.group_1.authgroup.description = 'Default Group'
        cls.group_1.authgroup.internal = False
        cls.group_1.authgroup.hidden = False
        cls.group_1.authgroup.save()

        # group 2 - no leader
        cls.group_2 = Group.objects.create(name='Group 2')
        cls.group_2.authgroup.description = 'Internal Group'
        cls.group_2.authgroup.internal = True        
        cls.group_2.authgroup.save()

        # group 3 - has leader
        cls.group_3 = Group.objects.create(name='Group 3')
        cls.group_3.authgroup.description = 'Hidden Group'
        cls.group_3.authgroup.internal = False
        cls.group_3.authgroup.hidden = True
        cls.group_3.authgroup.save()

        # group 4 - no leader
        cls.group_4 = Group.objects.create(name='Group 4')
        cls.group_4.authgroup.description = 'Open Group'
        cls.group_4.authgroup.internal = False
        cls.group_4.authgroup.hidden = False
        cls.group_4.authgroup.open = True
        cls.group_4.authgroup.save()

        # group 5 - no leader
        cls.group_5 = Group.objects.create(name='Group 5')
        cls.group_5.authgroup.description = 'Public Group'
        cls.group_5.authgroup.internal = False
        cls.group_5.authgroup.hidden = False
        cls.group_5.authgroup.public = True
        cls.group_5.authgroup.save()

        # group 6 - no leader
        cls.group_6 = Group.objects.create(name='Group 6')
        cls.group_6.authgroup.description = 'Mixed Group'
        cls.group_6.authgroup.internal = False
        cls.group_6.authgroup.hidden = True
        cls.group_6.authgroup.open = True
        cls.group_6.authgroup.public = True
        cls.group_6.authgroup.save()
        
        # user 1 - corp and alliance, normal user
        cls.character_1 = EveCharacter.objects.create(
            character_id=1001,
            character_name='Bruce Wayne',
            corporation_id=2001,
            corporation_name='Wayne Technologies',
            corporation_ticker='WT',
            alliance_id=3001,
            alliance_name='Wayne Enterprises',
            alliance_ticker='WE',
        )
        cls.character_1a = EveCharacter.objects.create(
            character_id=1002,
            character_name='Batman',
            corporation_id=2001,
            corporation_name='Wayne Technologies',
            corporation_ticker='WT',
            alliance_id=3001,
            alliance_name='Wayne Enterprises',
            alliance_ticker='WE',
        )
        alliance = EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name='Wayne Enterprises',
            alliance_ticker='WE',            
            executor_corp_id=2001
        )
        EveCorporationInfo.objects.create(
            corporation_id=2001,
            corporation_name='Wayne Technologies',
            corporation_ticker='WT',            
            member_count=42,
            alliance=alliance
        )        
        cls.user_1 = User.objects.create_user(
            cls.character_1.character_name.replace(' ', '_'),
            'abc@example.com',
            'password'
        )
        CharacterOwnership.objects.create(
            character=cls.character_1,
            owner_hash='x1' + cls.character_1.character_name,
            user=cls.user_1
        )
        CharacterOwnership.objects.create(
            character=cls.character_1a,
            owner_hash='x1' + cls.character_1a.character_name,
            user=cls.user_1
        )
        cls.user_1.profile.main_character = cls.character_1
        cls.user_1.profile.save()
        cls.user_1.groups.add(cls.group_1)
        cls.group_1.authgroup.group_leaders.add(cls.user_1)

        # user 2 - corp only, staff
        cls.character_2 = EveCharacter.objects.create(
            character_id=1003,
            character_name='Clark Kent',
            corporation_id=2002,
            corporation_name='Daily Planet',
            corporation_ticker='DP',
            alliance_id=None
        )
        EveCorporationInfo.objects.create(
            corporation_id=2002,
            corporation_name='Daily Plane',
            corporation_ticker='DP',            
            member_count=99,
            alliance=None
        )
        cls.user_2 = User.objects.create_user(
            cls.character_2.character_name.replace(' ', '_'),
            'abc@example.com',
            'password'
        )
        CharacterOwnership.objects.create(
            character=cls.character_2,
            owner_hash='x1' + cls.character_2.character_name,
            user=cls.user_2
        )
        cls.user_2.profile.main_character = cls.character_2
        cls.user_2.profile.save()
        cls.user_2.groups.add(cls.group_2)
        cls.user_2.is_staff = True
        cls.user_2.save()
        
        # user 3 - no main, no group, superuser
        cls.character_3 = EveCharacter.objects.create(
            character_id=1101,
            character_name='Lex Luthor',
            corporation_id=2101,
            corporation_name='Lex Corp',
            corporation_ticker='LC',
            alliance_id=None
        )
        EveCorporationInfo.objects.create(
            corporation_id=2101,
            corporation_name='Lex Corp',
            corporation_ticker='LC',            
            member_count=666,
            alliance=None
        )
        EveAllianceInfo.objects.create(
            alliance_id=3101,
            alliance_name='Lex World Domination',
            alliance_ticker='LWD',
            executor_corp_id=2101
        )
        cls.user_3 = User.objects.create_user(
            cls.character_3.character_name.replace(' ', '_'),
            'abc@example.com',
            'password'
        )
        CharacterOwnership.objects.create(
            character=cls.character_3,
            owner_hash='x1' + cls.character_3.character_name,
            user=cls.user_3
        )
        cls.user_3.is_superuser = True
        cls.user_3.save()
        cls.user_3.groups.add(cls.group_3)
        cls.group_3.authgroup.group_leaders.add(cls.user_3)

    def setUp(self):
        self.factory = RequestFactory()
        self.modeladmin = GroupAdmin(
            model=Group, admin_site=AdminSite()
        )

    def _create_autogroups(self):
        """create autogroups for corps and alliances"""
        if _has_auto_groups:
            autogroups_config = AutogroupsConfig(
                corp_groups=True,
                alliance_groups=True
            )
            autogroups_config.save()
            for state in State.objects.all():
                autogroups_config.states.add(state)
            autogroups_config.update_corp_group_membership(self.user_1)
    
    # column rendering

    def test_description(self):
        expected = 'Default Group'
        result = self.modeladmin._description(self.group_1)
        self.assertEqual(result, expected)

    def test_member_count(self):        
        expected = 1
        obj = self.modeladmin.get_queryset(MockRequest(user=self.user_1))\
            .get(pk=self.group_1.pk)
        result = self.modeladmin._member_count(obj)
        self.assertEqual(result, expected)

    def test_has_leader(self):        
        result = self.modeladmin.has_leader(self.group_1)
        self.assertTrue(result)

    def test_properties_1(self):
        expected = ['Default']
        result = self.modeladmin._properties(self.group_1)
        self.assertListEqual(result, expected)

    def test_properties_2(self):
        expected = ['Internal']
        result = self.modeladmin._properties(self.group_2)
        self.assertListEqual(result, expected)

    def test_properties_3(self):
        expected = ['Hidden']
        result = self.modeladmin._properties(self.group_3)
        self.assertListEqual(result, expected)

    def test_properties_4(self):
        expected = ['Open']
        result = self.modeladmin._properties(self.group_4)
        self.assertListEqual(result, expected)

    def test_properties_5(self):
        expected = ['Public']
        result = self.modeladmin._properties(self.group_5)
        self.assertListEqual(result, expected)

    def test_properties_6(self):
        expected = ['Hidden', 'Open', 'Public']
        result = self.modeladmin._properties(self.group_6)
        self.assertListEqual(result, expected)

    if _has_auto_groups:
        @patch(MODULE_PATH + '._has_auto_groups', True)
        def test_properties_7(self):
            self._create_autogroups()
            expected = ['Auto Group']
            my_group = Group.objects\
                .filter(managedcorpgroup__isnull=False)\
                .first()
            result = self.modeladmin._properties(my_group)
            self.assertListEqual(result, expected)

    # actions
   
    # filters
    
    if _has_auto_groups:
        @patch(MODULE_PATH + '._has_auto_groups', True)
        def test_filter_is_auto_group(self):
            
            class GroupAdminTest(admin.ModelAdmin): 
                list_filter = (IsAutoGroupFilter,)
                    
            self._create_autogroups()        
            my_modeladmin = GroupAdminTest(Group, AdminSite())

            # Make sure the lookups are correct
            request = self.factory.get('/')
            request.user = self.user_1
            changelist = my_modeladmin.get_changelist_instance(request)
            filters = changelist.get_filters(request)
            filterspec = filters[0][0]
            expected = [
                ('yes', 'Yes'),
                ('no', 'No'),
            ]
            self.assertEqual(filterspec.lookup_choices, expected)

            # Make sure the correct queryset is returned - no
            request = self.factory.get(
                '/', {'is_auto_group__exact': 'no'}
            )
            request.user = self.user_1
            changelist = my_modeladmin.get_changelist_instance(request)
            queryset = changelist.get_queryset(request)
            expected = [
                self.group_1,
                self.group_2,
                self.group_3,
                self.group_4,
                self.group_5,
                self.group_6
            ]
            self.assertSetEqual(set(queryset), set(expected))

            # Make sure the correct queryset is returned - yes
            request = self.factory.get(
                '/', {'is_auto_group__exact': 'yes'}
            )
            request.user = self.user_1
            changelist = my_modeladmin.get_changelist_instance(request)
            queryset = changelist.get_queryset(request)
            expected = Group.objects.exclude(
                managedalliancegroup__isnull=True, 
                managedcorpgroup__isnull=True
            )
            self.assertSetEqual(set(queryset), set(expected))
         
    def test_filter_has_leader(self):
        
        class GroupAdminTest(admin.ModelAdmin): 
            list_filter = (HasLeaderFilter,)
                
        self._create_autogroups()        
        my_modeladmin = GroupAdminTest(Group, AdminSite())

        # Make sure the lookups are correct
        request = self.factory.get('/')
        request.user = self.user_1
        changelist = my_modeladmin.get_changelist_instance(request)
        filters = changelist.get_filters(request)
        filterspec = filters[0][0]
        expected = [
            ('yes', 'Yes'),
            ('no', 'No'),
        ]
        self.assertEqual(filterspec.lookup_choices, expected)

        # Make sure the correct queryset is returned - no
        request = self.factory.get(
            '/', {'has_leader__exact': 'no'}
        )
        request.user = self.user_1
        changelist = my_modeladmin.get_changelist_instance(request)
        queryset = changelist.get_queryset(request)
        expected = Group.objects.exclude(pk__in=[
            self.group_1.pk, self.group_3.pk
        ])
        self.assertSetEqual(set(queryset), set(expected))

        # Make sure the correct queryset is returned - yes
        request = self.factory.get(
            '/', {'has_leader__exact': 'yes'}
        )
        request.user = self.user_1
        changelist = my_modeladmin.get_changelist_instance(request)
        queryset = changelist.get_queryset(request)
        expected = [
            self.group_1,            
            self.group_3
        ]
        self.assertSetEqual(set(queryset), set(expected))
    
    def test_change_view_loads_normally(self):
        User.objects.create_superuser(
            username='superuser', password='secret', email='admin@example.com'
        )
        c = Client()
        c.login(username='superuser', password='secret')                
        response = c.get(get_admin_change_view_url(self.group_1))
        self.assertEqual(response.status_code, 200)
