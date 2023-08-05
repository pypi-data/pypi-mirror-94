"""Abode cloud push events."""
import collections
import logging

from .account import JcAccount
from .error_handling import JcException
from .error_handling import *
import jcapi.socketio as sio
import json
import collections

_LOGGER = logging.getLogger(__name__)


class JcEventController():
    """Class for subscribing to abode events."""

    def __init__(self, JcAccount, url, token=None):
        """Init event subscription class."""
        self._jc_account = JcAccount
        self._thread = None
        self._running = False
        self._connected = False

        # Setup callback dicts
        self._connection_status_callbacks = collections.defaultdict(list)
        self._device_callbacks = collections.defaultdict(list)

        # Setup SocketIO
        self._socketio = sio.SocketIO(url=f"ws://{url}", token=token)

        # Setup SocketIO Callbacks
        self._socketio.on(sio.STARTED, self._on_socket_started)
        self._socketio.on(sio.CONNECTED, self._on_socket_connected)
        self._socketio.on(sio.DISCONNECTED, self._on_socket_disconnected)
        self._socketio.on(sio.DEVICE_UPDATE_EVENT, self._on_device_update)

    def start(self):
        """Start a thread to handle Abode SocketIO notifications."""
        self._socketio.start()

    def stop(self):
        """Tell the subscription thread to terminate - will block."""
        self._socketio.stop()

    def add_connection_status_callback(self, unique_id, callback):
        """Register callback for Abode server connection status."""
        if not unique_id:
            return False

        _LOGGER.debug(
            "Subscribing to Abode connection updates for: %s", unique_id)

        self._connection_status_callbacks[unique_id].append((callback))

        return True

    def remove_connection_status_callback(self, unique_id):
        """Unregister connection status callbacks."""
        if not unique_id:
            return False

        _LOGGER.debug(
            "Unsubscribing from Abode connection updates for : %s", unique_id)

        self._connection_status_callbacks[unique_id].clear()

        return True

    @property
    def connected(self):
        """Get the Abode connection status."""
        return self._connected

    @property
    def socketio(self):
        """Get the SocketIO instance."""
        return self._socketio

    def _on_socket_started(self):
        """Socket IO startup callback."""
        # pylint: disable=W0212
        cookies = self._jc_account._get_session().cookies.get_dict()
        cookie_string = "; ".join(
            [str(x) + "=" + str(y) for x, y in cookies.items()])

        self._socketio.set_cookie(cookie_string)

    def _on_socket_connected(self):
        """Socket IO connected callback."""
        self._connected = True

        try:
            self._jc_account.fetch_devices()
        # pylint: disable=W0703
        except Exception as exc:
            _LOGGER.warning("Captured exception during Abode refresh: %s", exc)
        finally:
            # Callbacks should still execute even if refresh fails (Abode
            # server issues) so that the entity availability in Home Assistant
            # is updated since we are in fact connected to the web socket.
            for callbacks in self._connection_status_callbacks.items():
                for callback in callbacks[1]:
                    _execute_callback(callback)

    def _on_socket_disconnected(self):
        """Socket IO disconnected callback."""
        self._connected = False

        for callbacks in self._connection_status_callbacks.items():
            # Check if list is not empty.
            # Applicable when remove_all_device_callbacks
            # is called before _on_socket_disconnected.
            if callbacks[1]:
                for callback in callbacks[1]:
                    _execute_callback(callback)

    def _on_device_update(self, devid):
        """Device callback from Abode SocketIO server."""
        if isinstance(devid, (tuple, list)):
            devid = devid[0]
        #
        # if devid is None:
        #     _LOGGER.warning("Device update with no device id.")
        #     return
        #
        # _LOGGER.debug("Device update event for device ID: %s", devid)
        #
        # device = self._jc_account.get_device(devid, True)
        #
        # if not device:
        #     _LOGGER.debug("Got device update for unknown device: %s", devid)
        #     return
        #
        # for callback in self._device_callbacks.get(device.device_id, ()):
        #     _execute_callback(callback, device)


def _execute_callback(callback, *args, **kwargs):
    # Callback with some data, capturing any exceptions to prevent chaos
    try:
        callback(*args, **kwargs)
    # pylint: disable=W0703
    except Exception as exc:
        _LOGGER.warning("Captured exception during callback: %s", exc)

