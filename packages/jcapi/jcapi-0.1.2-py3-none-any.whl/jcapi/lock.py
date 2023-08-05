"""Controls Jiachang lock devices."""
import json


class JcLock:
    def __init__(self, JcDirector, item_id):
        """Creates a Jiachang lock object.

        Parameters:
            `JcDirector` - A `jcapi.director.JcDirector` object that corresponds to the Jiachang Director that the lock is connected to.

            `item_id` - The Jiachang item ID of the switch.
        Switch varis:
            {
            "type": "ms",
            "attr": {
                "ID": "168",
                "DEVID": "461",
                "NAME": "门锁",
                "SYSNAME": "ms",
                "ICON": "ms",
                "INUSE": "1",
                "CANDEL": "0",
                "ISR": "1",
                "ISS": "0",
                "ISC": "0",
                "ATTRINT": "0",
                "YYBM": null
            },
            "value": 2,

        """
        self.director = JcDirector
        self.item_id = item_id

    async def get_state(self):
        """Returns the lock state of a lock as a boolean (True=locked, False=open).
        """
        value = await self.director.get_item_variable_value(self.item_id, var_name=None, dev_type="lock")
        if str(value) == "2":
            return True
        else:
            return False

    async def async_get_record(self):
        """get the name of last changed by user.
        """
        res = await self.director.get_item_info(self.item_id)
        records=json.loads(res)["detail"]["ksrecord"]
        name = sorted(records.items())[-1][1][0]["text"]
        return name

    async def async_unlock(self):
        """unlock a lock.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self.item_id,
            "rsargs[1][m]": "0",
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)

    async def async_lock(self):
        """lock a lock.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self.item_id,
            "rsargs[1][m]": "1",
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)