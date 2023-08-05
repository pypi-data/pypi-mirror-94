"""Controls Jiachang Cover devices.
"""
from .account import JcDevice


class JcCover(JcDevice):
    def __init__(self, JcDirector):
        """Creates a Jiachang cover object.

        Parameters:
            `JcDirector` - A `jcapi.director.JcDirector` object that corresponds to the Jiachang Director that the cover is connected to.

            `item_id` - The Jiachang item ID of the cover.
        Cover varis:
            {
            "type": "cl1",
            "attr": {
                "ID": "116",
                "DEVID": "82",
                "NAME": "窗帘",
                "SYSNAME": "cl1",
                "ICON": null,
                "YYBM": null,
                "INUSE": "1",
                "CANDEL": "0",
                "ISR": "1",
                "ISS": "0",
                "ISC": "1",
                "ATTRINT": "10"
            },
            "value": 10,
            "other": {
                "0": "关",
                "10": "开",
                "min": 0,
                "max": 10
            },
            "detail": false,
            "phydev": "1"
        }
        """
        self.director = JcDirector

    async def get_level(self):
        """Returns the level of a curtain as an int 0-10.属性值：0为关，10为开，101为停
        Will cause an error if called on a tcq. Use `getState()` instead.
        """
        value = await self.director.get_item_variable_value(self._device_id, var_name=None, dev_type="cl1")
        return int(value * 10)

    async def get_state(self):
        """Returns the state of a tcq as a boolean (True=on, False=off).0开，1停，2关
        """
        value = await self.director.get_item_variable_value(self._device_id, var_name=None, dev_type="cl")
        if value == "2":
            return False
        else:
            return True

    async def set_level(self, level):
        """Sets the cover level of a dimmer or turns on/off a cover.
        Any `level > 0` will turn on a cover, and `level = 0` will turn off a cover.

        Parameters:
            `level` - (int) 0-100
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self._device_id,
            "rsargs[1]": level
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)

    async def open_cover(self):
        """turns on a cover.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self._device_id,
            "rsargs[1]": 10
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)

    async def close_cover(self):
        """turns off a cover.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self._device_id,
            "rsargs[1]": 0
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)

    async def stop_cover(self):
        """turns off a cover.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self._device_id,
            "rsargs[1]": 101
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)