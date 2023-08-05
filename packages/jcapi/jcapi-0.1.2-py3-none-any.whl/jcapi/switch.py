"""Controls Jiachang Switch devices.
"""


class JcSwitch:
    def __init__(self, JcDirector, item_id):
        """Creates a Jiachang Switch object.

        Parameters:
            `JcDirector` - A `jcapi.director.JcDirector` object that corresponds to the Jiachang Director that the switch is connected to.

            `item_id` - The Jiachang item ID of the switch.
        Switch varis:
            {
            "type": "switch",
            "attr": {
                "ID": "106",
                "DEVID": "76",
                "NAME": "2015",
                "SYSNAME": "kg",
                "ICON": "3k3",
                "YYBM": null,
                "INUSE": "1",
                "CANDEL": "0",
                "ISR": "1",
                "ISS": "0",
                "ISC": "1",
                "ATTRINT": "0"
            },
            "value": 0,
            "other": null,
            "detail": true,
            "phydev": "1"
        }
        """
        self.director = JcDirector
        self.item_id = item_id

    async def get_state(self):
        """Returns the power state of a dimmer or switch as a boolean (True=on, False=off).
        """
        value = await self.director.get_item_variable_value(self.item_id, var_name=None, dev_type="switch")
        if str(value) == "0":
            return False
        else:
            return True

    async def turn_on(self):
        """turns on a switch.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self.item_id,
            "rsargs[m]": "1",
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)

    async def turn_off(self):
        """turns off a switch.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self.item_id,
            "rsargs[m]": "0",
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)