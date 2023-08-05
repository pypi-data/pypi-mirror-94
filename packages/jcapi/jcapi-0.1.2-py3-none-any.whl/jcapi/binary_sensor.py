"""a Jiachang Sensor devices.
"""


class JcB_sensor:
    def __init__(self, JcDirector, item_id):
        """Creates a Jiachang Sensor object.

        Parameters:
            `JcDirector` - A `jcapi.director.JcDirector` object that corresponds to the Jiachang Director that the sensor is connected to.
            `item_id` - The Jiachang item ID of the sensor.
        Sensor varis:
            {
            "type": "alarm",
            "attr": {
                "ID": "302",
                "DEVID": "1058",
                "NAME": "水浸",
                "SYSNAME": "gj",
                "ICON": "mc",
                "INUSE": "1",
                "CANDEL": "0",
                "ISR": "1",
                "ISS": "1",
                "ISC": "1",
                "ATTRINT": "0",
                "YYBM": null
            },
            "value": 0,
            "other": {
                "info": [
                    "正常",
                    "告警"
                ],
                "action": 0,
                "alarm": "bu"
            },
            "detail": true,
            "phydev": "1"
        }
        """
        self.director = JcDirector
        self.item_id = item_id

    async def get_state(self):
        """Returns the power state of a dimmer or sensor as a boolean (True=on, False=off).
        """
        value = await self.director.get_item_variable_value(self.item_id, var_name=None, dev_type="sensor")
        if str(value) == "0":
            return False
        else:
            return True
