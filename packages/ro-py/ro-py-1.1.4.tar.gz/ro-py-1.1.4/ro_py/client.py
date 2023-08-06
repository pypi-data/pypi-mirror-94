"""

This file houses functions and classes that represent the core Roblox web client.

"""

from ro_py.games import Game
from ro_py.groups import Group
from ro_py.assets import Asset
from ro_py.badges import Badge
from ro_py.chat import ChatWrapper
from ro_py.events import EventTypes
from ro_py.trades import TradesWrapper
from ro_py.users import PartialUser
from ro_py.utilities.requests import Requests
from ro_py.accountsettings import AccountSettings
from ro_py.utilities.cache import Cache, CacheType
from ro_py.notifications import NotificationReceiver
from ro_py.accountinformation import AccountInformation
from ro_py.utilities.errors import UserDoesNotExistError, InvalidPlaceIDError
from ro_py.captcha import UnsolvedLoginCaptcha
import asyncio


class ClientSharedObject:
    """
    This object is shared across most instances and classes for a particular client.
    """
    def __init__(self, client):
        self.client = client
        """Client (parent) of this object."""
        self.cache = Cache()
        """Cache object to keep objects that don't need to be recreated."""
        self.requests = Requests()
        """Reqests object for all web requests."""
        self.evtloop = asyncio.new_event_loop()
        """Event loop for certain things."""


class Client:
    """
    Represents an authenticated Roblox client.

    Parameters
    ----------
    token : str
        Authentication token. You can take this from the .ROBLOSECURITY cookie in your browser.
    """

    def __init__(self, token: str = None):
        self.cso = ClientSharedObject(self)
        """ClientSharedObject. Passed to each new object to share information."""
        self.requests = self.cso.requests
        """See self.cso.requests"""
        self.accountinformation = None
        """AccountInformation object. Only available for authenticated clients."""
        self.accountsettings = None
        """AccountSettings object. Only available for authenticated clients."""
        self.chat = None
        """ChatWrapper object. Only available for authenticated clients."""
        self.trade = None
        """TradesWrapper object. Only available for authenticated clients."""
        self.notifications = None
        """NotificationReceiver object. Only available for authenticated clients."""
        self.events = EventTypes
        """Types of events used for binding events to a function."""

        if token:
            self.token_login(token)

    def token_login(self, token):
        """
        Authenticates the client with a ROBLOSECURITY token.

        Parameters
        ----------
        token : str
            .ROBLOSECURITY token to authenticate with.
        """
        self.requests.session.cookies[".ROBLOSECURITY"] = token
        self.accountinformation = AccountInformation(self.cso)
        self.accountsettings = AccountSettings(self.cso)
        self.chat = ChatWrapper(self.cso)
        self.trade = TradesWrapper(self.cso, self.get_self)
        self.notifications = NotificationReceiver(self.cso)

    async def user_login(self, username, password, token=None):
        """
        Authenticates the client with a username and password.

        Parameters
        ----------
        username : str
            Username to log in with.
        password : str
            Password to log in with.
        token : str, optional
            If you have already solved the captcha, pass it here.

        Returns
        -------
        ro_py.captcha.UnsolvedCaptcha or request
        """
        if token:
            login_req = self.requests.back_post(
                url="https://auth.roblox.com/v2/login",
                json={
                    "ctype": "Username",
                    "cvalue": username,
                    "password": password,
                    "captchaToken": token,
                    "captchaProvider": "PROVIDER_ARKOSE_LABS"
                }
            )
            return login_req
        else:
            login_req = await self.requests.post(
                url="https://auth.roblox.com/v2/login",
                json={
                    "ctype": "Username",
                    "cvalue": username,
                    "password": password
                },
                quickreturn=True
            )
            if login_req.status_code == 200:
                # If we're here, no captcha is required and we're already logged in, so we can return.
                return
            elif login_req.status_code == 403:
                # A captcha is required, so we need to return the captcha to solve.
                field_data = login_req.json()["errors"][0]["fieldData"]
                captcha_req = await self.requests.post(
                    url="https://roblox-api.arkoselabs.com/fc/gt2/public_key/476068BF-9607-4799-B53D-966BE98E2B81",
                    headers={
                        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
                    },
                    data=f"public_key=476068BF-9607-4799-B53D-966BE98E2B81&data[blob]={field_data}"
                )
                captcha_json = captcha_req.json()
                return UnsolvedLoginCaptcha(captcha_json, "476068BF-9607-4799-B53D-966BE98E2B81")

    async def get_self(self):
        self_req = await self.requests.get(
            url="https://roblox.com/my/profile"
        )
        data = self_req.json()
        return PartialUser(self.cso, data['UserId'], data['Username'])

    async def get_user(self, user_id, expand=True):
        """
        Gets a Roblox user.

        Parameters
        ----------
        user_id
            ID of the user to generate the object from.
        expand : bool
            Whether to automatically expand the data returned by the endpoint into Users.s
        """
        user = self.cso.cache.get(CacheType.Users, user_id)
        if not user:
            user = PartialUser(self.cso, user_id)
            if expand:
                expanded = await user.expand()
                self.cso.cache.set(CacheType.Users, user_id, expanded)
                return expanded
        return user

    async def get_user_by_username(self, user_name: str, exclude_banned_users: bool = False, expand=True):
        """
        Gets a Roblox user by their username..

        Parameters
        ----------
        user_name : str
            Name of the user to generate the object from.
        exclude_banned_users : bool
            Whether to exclude banned users in the request.
        expand : bool
            Whether to automatically expand the data returned by the endpoint into Users.
        """
        username_req = await self.requests.post(
            url="https://users.roblox.com/v1/usernames/users",
            data={
                "usernames": [
                    user_name
                ],
                "excludeBannedUsers": exclude_banned_users
            }
        )
        username_data = username_req.json()
        if len(username_data["data"]) > 0:
            user_id = username_req.json()["data"][0]["id"]  # TODO: make this a partialuser
            return await self.get_user(user_id, expand=expand)
        else:
            raise UserDoesNotExistError

    async def get_group(self, group_id):
        """
        Gets a Roblox group.

        Parameters
        ----------
        group_id
            ID of the group to generate the object from.
        """
        group = self.cso.cache.get(CacheType.Groups, group_id)
        if not group:
            group = Group(self.cso, group_id)
            self.cso.cache.set(CacheType.Groups, group_id, group)
            await group.update()
        return group

    async def get_game_by_universe_id(self, universe_id):
        """
        Gets a Roblox game.

        Parameters
        ----------
        universe_id
            ID of the game to generate the object from.
        """
        game = self.cso.cache.get(CacheType.Games, universe_id)
        if not game:
            game = Game(self.cso, universe_id)
            self.cso.cache.set(CacheType.Games, universe_id, game)
            await game.update()
        return game

    async def get_game_by_place_id(self, place_id):
        """
        Gets a Roblox game by one of it's place's Plaece IDs.

        Parameters
        ----------
        place_id
            ID of the place to generate the object from.
        """
        place_req = await self.requests.get(
            url="https://games.roblox.com/v1/games/multiget-place-details",
            params={
                "placeIds": place_id
            }
        )
        place_data = place_req.json()

        try:
            place_details = place_data[0]
        except IndexError:
            raise InvalidPlaceIDError("Invalid place ID.")

        universe_id = place_details["universeId"]

        return await self.get_game_by_universe_id(universe_id)

    async def get_asset(self, asset_id):
        """
        Gets a Roblox asset.

        Parameters
        ----------
        asset_id
            ID of the asset to generate the object from.
        """
        asset = self.cso.cache.get(CacheType.Assets, asset_id)
        if not asset:
            asset = Asset(self.cso, asset_id)
            self.cso.cache.set(CacheType.Assets, asset_id, asset)
            await asset.update()
        return asset

    async def get_badge(self, badge_id):
        """
        Gets a Roblox badge.

        Parameters
        ----------
        badge_id
            ID of the badge to generate the object from.
        """
        badge = self.cso.cache.get(CacheType.Assets, badge_id)
        if not badge:
            badge = Badge(self.cso, badge_id)
            self.cso.cache.set(CacheType.Assets, badge_id, badge)
            await badge.update()
        return badge

    async def get_friend_requests(self):
        friend_req = await self.requests.get(
            url="https://friends.roblox.com/v1/user/friend-requests/count"
        )
        return friend_req.json()["count"]
