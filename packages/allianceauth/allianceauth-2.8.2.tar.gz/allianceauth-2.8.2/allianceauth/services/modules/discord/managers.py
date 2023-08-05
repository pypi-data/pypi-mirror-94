import logging
from urllib.parse import urlencode

from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.timezone import now

from allianceauth.services.hooks import NameFormatter

from . import __title__
from .app_settings import (
    DISCORD_APP_ID,
    DISCORD_APP_SECRET,
    DISCORD_BOT_TOKEN,
    DISCORD_CALLBACK_URL,
    DISCORD_GUILD_ID,    
    DISCORD_SYNC_NAMES
)
from .discord_client import DiscordClient
from .discord_client.exceptions import DiscordClientException, DiscordApiBackoff
from .discord_client.helpers import match_or_create_roles_from_names
from .utils import LoggerAddTag


logger = LoggerAddTag(logging.getLogger(__name__), __title__)


class DiscordUserManager(models.Manager):
    """Manager for DiscordUser"""

    # full server admin
    BOT_PERMISSIONS = 0x00000008

    # get user ID, accept invite
    SCOPES = [
        'identify',
        'guilds.join',
    ]

    def add_user(
        self, 
        user: User, 
        authorization_code: str, 
        is_rate_limited: bool = True
    ) -> bool:
        """adds a new Discord user

        Params:
        - user: Auth user to join
        - authorization_code: authorization code returns from oauth
        - is_rate_limited: When False will disable default rate limiting (use with care)
        
        Returns: True on success, else False or raises exception
        """
        try:        
            nickname = self.user_formatted_nick(user) if DISCORD_SYNC_NAMES else None
            group_names = self.user_group_names(user)
            access_token = self._exchange_auth_code_for_token(authorization_code)
            user_client = DiscordClient(access_token, is_rate_limited=is_rate_limited)
            discord_user = user_client.current_user()
            user_id = discord_user['id']
            bot_client = self._bot_client(is_rate_limited=is_rate_limited)
                
            if group_names:                
                role_ids = match_or_create_roles_from_names(
                    client=bot_client, 
                    guild_id=DISCORD_GUILD_ID, 
                    role_names=group_names
                ).ids()
            else:
                role_ids = None
                        
            created = bot_client.add_guild_member(
                guild_id=DISCORD_GUILD_ID, 
                user_id=user_id,
                access_token=access_token,
                role_ids=role_ids,
                nick=nickname
            )
            if created is not False:
                if created is None:
                    logger.debug(
                        "User %s with Discord ID %s is already a member.",
                        user,
                        user_id,
                    )
                self.update_or_create(
                    user=user, 
                    defaults={
                        'uid': user_id, 
                        'username': discord_user['username'][:32], 
                        'discriminator': discord_user['discriminator'][:4],
                        'activated': now()
                    }
                )
                logger.info(
                    "Added user %s with Discord ID %s to Discord server", user, user_id
                )
                return True

            else:
                logger.warning(
                    "Failed to add user %s with Discord ID %s to Discord server",
                    user,
                    user_id,
                )
                return False

        except (HTTPError, ConnectionError, DiscordApiBackoff) as ex:
            logger.exception(
                'Failed to add user %s to Discord server: %s', user, ex
            )
            return False

    @staticmethod
    def user_formatted_nick(user: User) -> str:
        """returns the name of the given users main character with name formatting
        or None if user has no main
        """
        from .auth_hooks import DiscordService
        
        if user.profile.main_character:
            return NameFormatter(DiscordService(), user).format_name()
        else:
            return None

    @staticmethod
    def user_group_names(user: User, state_name: str = None) -> list:
        """returns list of group names plus state the given user is a member of"""
        if not state_name:
            state_name = user.profile.state.name
        group_names = (
            [group.name for group in user.groups.all()] + [state_name]
        )
        logger.debug(
            "Group names for roles updates of user %s are: %s", user, group_names
        )
        return group_names
    
    def user_has_account(self, user: User) -> bool:
        """Returns True if the user has an Discord account, else False
        
        only checks locally, does not hit the API
        """
        if not isinstance(user, User):
            return False
        return self.filter(user=user).select_related('user').exists()

    @classmethod
    def generate_bot_add_url(cls) -> str:
        params = urlencode({
            'client_id': DISCORD_APP_ID,
            'scope': 'bot',
            'permissions': str(cls.BOT_PERMISSIONS)

        })
        return f'{DiscordClient.OAUTH_BASE_URL}?{params}'        

    @classmethod
    def generate_oauth_redirect_url(cls) -> str:
        oauth = OAuth2Session(
            DISCORD_APP_ID, redirect_uri=DISCORD_CALLBACK_URL, scope=cls.SCOPES
        )
        url, state = oauth.authorization_url(DiscordClient.OAUTH_BASE_URL)
        return url

    @staticmethod
    def _exchange_auth_code_for_token(authorization_code: str) -> str:
        oauth = OAuth2Session(DISCORD_APP_ID, redirect_uri=DISCORD_CALLBACK_URL)
        token = oauth.fetch_token(
            DiscordClient.OAUTH_TOKEN_URL, 
            client_secret=DISCORD_APP_SECRET, 
            code=authorization_code
        )
        logger.debug("Received token from OAuth")
        return token['access_token']
    
    @classmethod
    def server_name(cls, use_cache: bool = True) -> str:
        """returns the name of the current Discord server 
        or an empty string if the name could not be retrieved

        Params:
        - use_cache: When set False will force an API call to get the server name
        """
        try:
            server_name = cls._bot_client().guild_name(
                guild_id=DISCORD_GUILD_ID, use_cache=use_cache
            )
        except (HTTPError, DiscordClientException):
            server_name = ""
        except Exception:
            logger.warning(
                "Unexpected error when trying to retrieve the server name from Discord", 
                exc_info=True
            )
            server_name = ""

        return server_name

    @classmethod
    def group_to_role(cls, group: Group) -> dict:
        """returns the Discord role matching the given Django group by name
        or an empty dict() if no matching role exist
        """
        return cls._bot_client().match_role_from_name(
            guild_id=DISCORD_GUILD_ID, role_name=group.name
        )

    @staticmethod
    def _bot_client(is_rate_limited: bool = True) -> DiscordClient:
        """returns a bot client for access to the Discord API"""
        return DiscordClient(DISCORD_BOT_TOKEN, is_rate_limited=is_rate_limited)
