"""Authenticates with the Jiachang API, retrieves account and registered
controller info, and retrieves a bearer token for connecting to a Jiachang Director.
"""
import random
import aiohttp
import async_timeout
import asyncio
import json
import logging
import datetime

from aiohttp import client_exceptions
from .director import JcDirector
from homeassistant.helpers import aiohttp_client
from .error_handling import checkResponseForError, BadCredentials, NotFound, Unauthorized
from .const import AUTHENTICATION_ENDPOINT, GET_CONTROLLERS_ENDPOINT
from .event_controller import JcEventController

_LOGGER = logging.getLogger(__name__)


class JcAccount:
    manufacturer = "JC Corp"

    def __init__(
            self, hass, username, password, hic_id, session: aiohttp.ClientSession = None, get_devices=False,
    ):
        """Creates a Jiachang account object.

        Parameters:
            `username` - Jiachang account username.

            `password` - Jiachang account password.

            `session` - (Optional) Allows the use of an `aiohttp.ClientSession` object for all network requests. This session will not be closed by the library.
            If not provided, the library will open and close its own `ClientSession`s as needed.
        """
        self._hass = hass
        self._username = username
        self._password = password
        self._id = hic_id
        self.hub_token = None
        self.account_token = None
        self.session = session
        self.devices = None
        self.online = True
        self.offline_list = []
        self.host = None
        self.wss = None
        self._event_controller = JcEventController(self, url=self.wss, token=self.hub_token)
        if get_devices:
            asyncio.run(self.fetch_devices())

    @property
    def hub_id(self):
        """ID for dummy hub."""
        return self._id

    @property
    def events(self):
        """Get the event controller."""
        return self._event_controller

    # async def test_connection(self):
    #     """Test connectivity to the Dummy hub is OK."""
    #     await asyncio.sleep(1)
    #     return True

    async def __send_account_auth_request(self):
        """Used internally to retrieve an account bearer token. Returns the entire
        JSON response from the Jiachang auth API.
        """
        data_dictionary = {
            "rs": "login",
            "rsargs[0]": self._username,
            "rsargs[1]": self._password
        }

        if self.session is None:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.post(
                            AUTHENTICATION_ENDPOINT, data=data_dictionary
                    ) as resp:
                        await checkResponseForError(await resp.text())
                        return await resp.text()
        else:
            with async_timeout.timeout(10):
                async with self.session.post(
                        AUTHENTICATION_ENDPOINT, data=data_dictionary
                ) as resp:
                    await checkResponseForError(await resp.text())
                    return await resp.text()

    async def __get_director_control_url(self, uri, token):
        """Used internally to send GET requests to the Jiachang API,
        authenticated with the account bearer token. Returns the entire JSON
        response from the Jiachang auth API.

        Parameters:
            `uri` - Full URI to send GET request to.
        """
        dataDictionary = {
            "rs": "getdturl"
        }
        # _LOGGER.info("token is %s", self.account_bearer_token)
        try:
            url = uri + "?hictoken=" + token

        except AttributeError:
            msg = "The account bearer token is missing - was your username/password correct? "
            _LOGGER.error(msg)
            raise
        # _LOGGER.info(url)
        if self.session is None:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.post(url, data=dataDictionary) as resp:
                        await checkResponseForError(await resp.text())
                        return await resp.text()
        else:
            with async_timeout.timeout(10):
                async with self.session.post(url, data=dataDictionary) as resp:
                    # await checkResponseForError(await resp.text())
                    # _LOGGER.info(await resp.text())
                    return await resp.text()

    async def __get_controller_token(self, controller_id):
        """get specified controller token. 获取网关的token
        Parameters:
            `controller_id`: ID of the controller. See `getAccountControllers()` for details.
        """
        try:
            url = AUTHENTICATION_ENDPOINT + "?hictoken=" + self.account_token
        except AttributeError:
            msg = "The account bearer token is missing - was your username/password correct? "
            _LOGGER.error(msg)
            raise
        json_dict = {
            "rs": "changeHIC",
            "rsargs[]": controller_id
        }
        if self.session is None:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.post(
                            url,
                            data=json_dict,
                    ) as resp:
                        await checkResponseForError(await resp.text())
                        return await resp.text()
        else:
            with async_timeout.timeout(10):
                async with self.session.post(
                        url,
                        data=json_dict,
                ) as resp:
                    await checkResponseForError(await resp.text())
                    return await resp.text()

    async def get_account_token(self):
        """Gets an account bearer token for making Jiachang online API requests.
        Returns:
            {
                "login":true,
                "info":"1189120558-1589091143-3386663-d2d60108e2-accad487b8",
                "nohic":false,
                "iswebsocket":true,
                "domain":"c.jia.mn"
            }
        """
        data = await self.__send_account_auth_request()
        json_dict = json.loads(data)
        try:
            self.account_token = json_dict["info"]
            # return self.account_token
        except KeyError:
            msg = "Did not recieve an account bearer token. Is your username/password correct? "
            _LOGGER.error(msg + data)
            raise

    async def get_controller_url(self, token):
        """Returns a dictionary of the information for all controllers registered to an account.
        get server address.获取接口请求地址

        Returns:
            ```
            {
                "a": "http://c.jia.mn/App/a",
                "b": "http://182.61.44.102:8381/App/b",
                "c": "http://c.jia.mn/App/c",
                "s": "182.61.44.102:8385",
                "wss": "182.61.44.102:8418",
                "fromdev": "mainapp",
                "on": true
            }
            ```
        """
        data = await self.__get_director_control_url(GET_CONTROLLERS_ENDPOINT, token)
        json_dict = json.loads(data)
        # _LOGGER.info(json_dict["b"])# print(jsonDictionary["b"])
        return json_dict["b"], json_dict["s"]

    async def get_director_token(self, controller_id):
        """Returns a dictionary with a director bearer token for making Jiachang Director API requests, and its expiry time (generally 86400 seconds after current time)
        returns:
            "1189120558-1589243259-560371073-9a35aa5e49-bdb97068cf"

        Parameters:
            `controller_id`: Common name of the controller. See `getAccountControllers()` for details.
        """
        data = await self.__get_controller_token(controller_id)
        token = json.loads(data)
        token_expiration = datetime.datetime.now() + datetime.timedelta(
            seconds=7776000
        )
        # print(f"{token} and {token_expiration}")
        return {
            "token": token,
            "token_expiration": token_expiration,
        }

    async def fetch_devices(self):
        try:
            await self.get_account_token()
            # Get bearer token to communicate with controller locally
            self.hub_token = (
                await self.get_director_token(self.hub_id)
            )["token"]
            # Get controller name
            self.host, self.wss = await self.get_controller_url(self.hub_token)
        except (Unauthorized, NotFound):
            msg = "Did not recieve an account bearer token. Is your username/password correct? "
            _LOGGER.error(msg)
            raise

        director_session = aiohttp_client.async_get_clientsession(
            self.hass, verify_ssl=False
        )
        director = JcDirector(
            self.host, self.hub_token, director_session
        )
        result = await director.get_all_item_info()
        if not result:
            raise NotFound
        self.offline_list = result.json()["offline"]
        self._event_controller.start()
        dev_list = []
        for device in (result.json()["page"]).values():
            dev_list.append(JcDevice(device, self))
        self.devices = dev_list

    # def update_device(self, device_json):
    #     return JcDevice(device_json, self)
    #
    # def get_device(self, device_id, refresh=False):
    #     """Get a single device."""
    #     if self.devices is None:
    #         self.fetch_devices()
    #         refresh = False
    #
    #     device = self.devices.get(device_id)
    #
    #     if device and refresh:
    #         device.refresh()
    #
    #     return device


class JcDevice:
    """Dummy roller (device for HA) for Hello World example."""

    def __init__(self, device_json, hub):
        """Init dummy roller."""
        self._json_state = device_json
        attrs = device_json.get("attr", None)
        self._attr = attrs
        self._device_id = attrs.get("ID")
        self.name = attrs.get("NAME")
        self._type = attrs.get("SYSNAME")
        self._type_tag = attrs.get("ICON")
        self.generic_type = device_json.get("type", None)
        self.value = device_json.get("value")
        self.hub = hub
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
        # Some static information about this device
        self.firmware_version = "0.0.{}".format(random.randint(1, 9))
        self.model = "Test Device"

    @property
    def idx(self):
        """Return ID for roller."""
        return self._device_id

    # async def set_position(self, position):
    #     """
    #     Set dummy cover to the given position.
    #
    #     State is announced a random number of seconds later.
    #     """
    #     self._target_position = position
    #
    #     # Update the moving status, and broadcast the update
    #     self.moving = position - 50
    #     await self.publish_updates()
    #
    #     self._loop.create_task(self.delayed_update())

    # async def delayed_update(self):
    #     """Publish updates, with a random delay to emulate interaction with device."""
    #     await asyncio.sleep(random.randint(1, 10))
    #     self.moving = 0
    #     await self.publish_updates()

    def register_callback(self, callback):
        """Register callback, called when Roller changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback):
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    # In a real implementation, this library would call it's call backs when it was
    # notified of any state changeds for the relevant device.
    async def publish_updates(self):
        """Schedule call all registered callbacks."""
        self._current_position = self._target_position
        for callback in self._callbacks:
            callback()

    @property
    def online(self):
        """Roller is online."""
        # False if offline.
        return self._device_id not in self.hub.offline_list
