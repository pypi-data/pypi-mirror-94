import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from allianceauth.notifications import notify

from .managers import GroupManager
from .models import GroupRequest, RequestLog


logger = logging.getLogger(__name__)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_management(request):
    logger.debug("group_management called by user %s" % request.user)
    acceptrequests = []
    leaverequests = []

    base_group_query = GroupRequest.objects.select_related('user', 'group', 'user__profile__main_character')
    if GroupManager.has_management_permission(request.user):
        # Full access
        group_requests = base_group_query.all()
    else:
        # Group specific leader
        users__groups = GroupManager.get_group_leaders_groups(request.user)
        group_requests = base_group_query.filter(group__in=users__groups)

    for grouprequest in group_requests:
        if grouprequest.leave_request:
            leaverequests.append(grouprequest)
        else:
            acceptrequests.append(grouprequest)

    logger.debug("Providing user %s with %s acceptrequests and %s leaverequests." % (
        request.user, len(acceptrequests), len(leaverequests)))

    render_items = {'acceptrequests': acceptrequests, 'leaverequests': leaverequests}

    return render(request, 'groupmanagement/index.html', context=render_items)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_membership(request):
    logger.debug("group_membership called by user %s" % request.user)
    # Get all open and closed groups
    if GroupManager.has_management_permission(request.user):
        # Full access
        groups = GroupManager.get_all_non_internal_groups()
    else:
        # Group leader specific
        groups = GroupManager.get_group_leaders_groups(request.user)

    groups = groups.exclude(authgroup__internal=True).annotate(num_members=Count('user')).order_by('name')

    render_items = {'groups': groups}

    return render(request, 'groupmanagement/groupmembership.html', context=render_items)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_membership_audit(request, group_id):
    logger.debug("group_management_audit called by user %s" % request.user)
    group = get_object_or_404(Group, id=group_id)
    try:
        # Check its a joinable group i.e. not corp or internal
        # And the user has permission to manage it
        if not GroupManager.check_internal_group(group) or not GroupManager.can_manage_group(request.user, group):
            logger.warning("User %s attempted to view the membership of group %s but permission was denied" %
                           (request.user, group_id))
            raise PermissionDenied

    except ObjectDoesNotExist:
        raise Http404("Group does not exist")
    render_items = {'group': group.name}
    entries = RequestLog.objects.filter(group=group).order_by('-date')
    render_items['entries'] = entries

    return render(request, 'groupmanagement/audit.html', context=render_items)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_membership_list(request, group_id):
    logger.debug(
        "group_membership_list called by user %s "
        "for group id %s" % (request.user, group_id)
    )
    group = get_object_or_404(Group, id=group_id)
    try:

        # Check its a joinable group i.e. not corp or internal
        # And the user has permission to manage it
        if (not GroupManager.check_internal_group(group)
            or not GroupManager.can_manage_group(request.user, group)
        ):
            logger.warning(
                "User %s attempted to view the membership of group %s "
                "but permission was denied" % (request.user, group_id)
            )
            raise PermissionDenied

    except ObjectDoesNotExist:
        raise Http404("Group does not exist")

    group_leaders = group.authgroup.group_leaders.all()
    members = list()
    for member in \
        group.user_set\
            .all()\
            .select_related('profile', 'profile__main_character')\
            .order_by('profile__main_character__character_name'):

        members.append({
            'user': member,
            'main_char': member.profile.main_character,
            'is_leader': member in group_leaders
        })

    render_items = {'group': group, 'members': members}

    return render(
        request, 'groupmanagement/groupmembers.html',
        context=render_items
    )


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_membership_remove(request, group_id, user_id):
    logger.debug("group_membership_remove called by user %s for group id %s on user id %s" %
                 (request.user, group_id, user_id))
    group = get_object_or_404(Group, id=group_id)
    try:
        # Check its a joinable group i.e. not corp or internal
        # And the user has permission to manage it
        if not GroupManager.check_internal_group(group) or not GroupManager.can_manage_group(request.user, group):
            logger.warning("User %s attempted to remove a user from group %s but permission was denied" % (request.user,
                                                                                                           group_id))
            raise PermissionDenied

        try:
            user = group.user_set.get(id=user_id)
            request_info = user.username + ":" + group.name
            log = RequestLog(request_type=None,group=group,request_info=request_info,action=1,request_actor=request.user)
            log.save()
            # Remove group from user
            user.groups.remove(group)
            logger.info("User %s removed user %s from group %s" % (request.user, user, group))
            messages.success(request, _("Removed user %(user)s from group %(group)s.") % {"user": user, "group": group})
        except ObjectDoesNotExist:
            messages.warning(request, _("User does not exist in that group"))

    except ObjectDoesNotExist:
        messages.warning(request, _("Group does not exist"))

    return redirect('groupmanagement:membership', group_id)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_accept_request(request, group_request_id):
    logger.debug("group_accept_request called by user %s for grouprequest id %s" % (request.user, group_request_id))
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        group, created = Group.objects.get_or_create(name=group_request.group.name)

        if not GroupManager.joinable_group(group_request.group, group_request.user.profile.state) or \
                not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        group_request.user.groups.add(group)
        group_request.user.save()
        log = RequestLog(request_type=group_request.leave_request,group=group,request_info=group_request.__str__(),action=1,request_actor=request.user)
        log.save()
        group_request.delete()
        logger.info("User %s accepted group request from user %s to group %s" % (
            request.user, group_request.user, group_request.group.name))
        notify(group_request.user, "Group Application Accepted", level="success",
               message="Your application to %s has been accepted." % group_request.group)
        messages.success(request,
                         _('Accepted application from %(mainchar)s to %(group)s.') % {"mainchar": group_request.main_char, "group": group_request.group})

    except PermissionDenied as p:
        logger.warning("User %s attempted to accept group join request %s but permission was denied" %
                       (request.user, group_request_id))
        raise p
    except:
        messages.error(request, _('An unhandled error occurred while processing the application from %(mainchar)s to %(group)s.') % {"mainchar": group_request.main_char, "group": group_request.group})
        logger.exception("Unhandled exception occurred while user %s attempting to accept grouprequest id %s." % (
            request.user, group_request_id))
        pass

    return redirect("groupmanagement:management")


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_reject_request(request, group_request_id):
    logger.debug("group_reject_request called by user %s for group request id %s" % (request.user, group_request_id))
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        if not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        if group_request:
            logger.info("User %s rejected group request from user %s to group %s" % (
                request.user, group_request.user, group_request.group.name))
            log = RequestLog(request_type=group_request.leave_request,group=group_request.group,request_info=group_request.__str__(),action=0,request_actor=request.user)
            log.save()
            group_request.delete()
            notify(group_request.user, "Group Application Rejected", level="danger",
                   message="Your application to %s has been rejected." % group_request.group)
            messages.success(request,
                             _('Rejected application from %(mainchar)s to %(group)s.') % {"mainchar": group_request.main_char, "group": group_request.group})

    except PermissionDenied as p:
        logger.warning("User %s attempted to reject group join request %s but permission was denied" %
                       (request.user, group_request_id))
        raise p
    except:
        messages.error(request, _('An unhandled error occurred while processing the application from %(mainchar)s to %(group)s.') % {"mainchar": group_request.main_char, "group": group_request.group})
        logger.exception("Unhandled exception occurred while user %s attempting to reject group request id %s" % (
            request.user, group_request_id))
        pass

    return redirect("groupmanagement:management")


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_leave_accept_request(request, group_request_id):
    logger.debug(
        "group_leave_accept_request called by user %s for group request id %s" % (request.user, group_request_id))
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        if not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        group, created = Group.objects.get_or_create(name=group_request.group.name)
        group_request.user.groups.remove(group)
        group_request.user.save()
        log = RequestLog(request_type=group_request.leave_request,group=group_request.group,request_info=group_request.__str__(),action=1,request_actor=request.user)
        log.save()
        group_request.delete()
        logger.info("User %s accepted group leave request from user %s to group %s" % (
            request.user, group_request.user, group_request.group.name))
        notify(group_request.user, "Group Leave Request Accepted", level="success",
               message="Your request to leave %s has been accepted." % group_request.group)
        messages.success(request,
                         _('Accepted application from %(mainchar)s to leave %(group)s.') % {"mainchar": group_request.main_char, "group": group_request.group})
    except PermissionDenied as p:
        logger.warning("User %s attempted to accept group leave request %s but permission was denied" %
                       (request.user, group_request_id))
        raise p
    except:
        messages.error(request, _('An unhandled error occurred while processing the application from %(mainchar)s to leave %(group)s.') % {
            "mainchar": group_request.main_char, "group": group_request.group})
        logger.exception("Unhandled exception occurred while user %s attempting to accept group leave request id %s" % (
            request.user, group_request_id))
        pass

    return redirect("groupmanagement:management")


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_leave_reject_request(request, group_request_id):
    logger.debug(
        "group_leave_reject_request called by user %s for group request id %s" % (request.user, group_request_id))
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        if not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        if group_request:
            log = RequestLog(request_type=group_request.leave_request,group=group_request.group,request_info=group_request.__str__(),action=0,request_actor=request.user)
            log.save()
            group_request.delete()
            logger.info("User %s rejected group leave request from user %s for group %s" % (
                request.user, group_request.user, group_request.group.name))
            notify(group_request.user, "Group Leave Request Rejected", level="danger",
                   message="Your request to leave %s has been rejected." % group_request.group)
            messages.success(request, _('Rejected application from %(mainchar)s to leave %(group)s.') % {
                "mainchar": group_request.main_char, "group": group_request.group})
    except PermissionDenied as p:
        logger.warning("User %s attempted to reject group leave request %s but permission was denied" %
                       (request.user, group_request_id))
        raise p
    except:
        messages.error(request, _('An unhandled error occurred while processing the application from %(mainchar)s to leave %(group)s.') % {
            "mainchar": group_request.main_char, "group": group_request.group})
        logger.exception("Unhandled exception occurred while user %s attempting to reject group leave request id %s" % (
            request.user, group_request_id))
        pass

    return redirect("groupmanagement:management")


@login_required
def groups_view(request):
    logger.debug("groups_view called by user %s" % request.user)

    groups_qs = GroupManager.get_joinable_groups_for_user(
        request.user, include_hidden=False
    )
    groups_qs = groups_qs.order_by('name')
    groups = []
    for group in groups_qs:
        group_request = GroupRequest.objects\
            .filter(user=request.user)\
            .filter(group=group)
        groups.append({
            'group': group,
            'request': group_request[0] if group_request else None
        })

    context = {'groups': groups}
    return render(request, 'groupmanagement/groups.html', context=context)


@login_required
def group_request_add(request, group_id):
    logger.debug("group_request_add called by user %s for group id %s" % (request.user, group_id))
    group = Group.objects.get(id=group_id)
    state = request.user.profile.state
    if not GroupManager.joinable_group(group, state):
        logger.warning("User %s attempted to join group id %s but it is not a joinable group" %
                       (request.user, group_id))
        messages.warning(request, _("You cannot join that group"))
        return redirect('groupmanagement:groups')
    if group in request.user.groups.all():
        # User is already a member of this group.
        logger.warning("User %s attempted to join group id %s but they are already a member." %
                       (request.user, group_id))
        messages.warning(request, _("You are already a member of that group."))
        return redirect('groupmanagement:groups')
    if not request.user.has_perm('groupmanagement.request_groups') and not group.authgroup.public:
        # Does not have the required permission, trying to join a non-public group
        logger.warning("User %s attempted to join group id %s but it is not a public group" %
                       (request.user, group_id))
        messages.warning(request, _("You cannot join that group"))
        return redirect('groupmanagement:groups')
    if group.authgroup.open:
        logger.info("%s joining %s as is an open group" % (request.user, group))
        request.user.groups.add(group)
        request_info = request.user.username + ":" + group.name
        log = RequestLog(request_type=False, group=group, request_info=request_info, action=1, request_actor=request.user)
        log.save()
        return redirect("groupmanagement:groups")
    req = GroupRequest.objects.filter(user=request.user, group=group)
    if len(req) > 0:
        logger.info("%s attempted to join %s but already has an open application" % (request.user, group))
        messages.warning(request, _("You already have a pending application for that group."))
        return redirect("groupmanagement:groups")
    grouprequest = GroupRequest()
    grouprequest.status = _('Pending')
    grouprequest.group = group
    grouprequest.user = request.user
    grouprequest.leave_request = False
    grouprequest.save()
    logger.info("Created group request for user %s to group %s" % (request.user, Group.objects.get(id=group_id)))
    messages.success(request, _('Applied to group %(group)s.') % {"group": group})
    return redirect("groupmanagement:groups")


@login_required
def group_request_leave(request, group_id):
    logger.debug("group_request_leave called by user %s for group id %s" % (request.user, group_id))
    group = Group.objects.get(id=group_id)
    if not GroupManager.check_internal_group(group):
        logger.warning("User %s attempted to leave group id %s but it is not a joinable group" %
                       (request.user, group_id))
        messages.warning(request, _("You cannot leave that group"))
        return redirect('groupmanagement:groups')
    if group not in request.user.groups.all():
        logger.debug("User %s attempted to leave group id %s but they are not a member" %
                     (request.user, group_id))
        messages.warning(request, _("You are not a member of that group"))
        return redirect('groupmanagement:groups')
    if group.authgroup.open:
        logger.info("%s leaving %s as is an open group" % (request.user, group))
        request_info = request.user.username + ":" + group.name
        log = RequestLog(request_type=True, group=group, request_info=request_info, action=1, request_actor=request.user)
        log.save()
        request.user.groups.remove(group)
        return redirect("groupmanagement:groups")
    req = GroupRequest.objects.filter(user=request.user, group=group)
    if len(req) > 0:
        logger.info("%s attempted to leave %s but already has an pending leave request." % (request.user, group))
        messages.warning(request, _("You already have a pending leave request for that group."))
        return redirect("groupmanagement:groups")
    if getattr(settings, 'AUTO_LEAVE', False):
        logger.info("%s leaving joinable group %s due to auto_leave" % (request.user, group))
        request_info = request.user.username + ":" + group.name
        log = RequestLog(request_type=True, group=group, request_info=request_info, action=1, request_actor=request.user)
        log.save()
        request.user.groups.remove(group)
        return redirect('groupmanagement:groups')
    grouprequest = GroupRequest()
    grouprequest.status = _('Pending')
    grouprequest.group = group
    grouprequest.user = request.user
    grouprequest.leave_request = True
    grouprequest.save()
    logger.info("Created group leave request for user %s to group %s" % (request.user, Group.objects.get(id=group_id)))
    messages.success(request, _('Applied to leave group %(group)s.') % {"group": group})
    return redirect("groupmanagement:groups")
