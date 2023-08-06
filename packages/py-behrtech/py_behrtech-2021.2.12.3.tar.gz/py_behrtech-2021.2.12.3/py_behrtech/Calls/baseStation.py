import requests
import enum

from py_behrtech.exceptions import check_status_code


class BaseStation:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def systemBaseStationBsEuiConfigGet(self, bsEui: str) -> dict:
        """
        Gets base station configuration overview information for the requested base station

        :param bsEui: Unique bsEui of the requested base station
        :return: Base station configuration overview information
        """

        req = requests.get(url=self.server_address + f"/v2/system/basestation/{bsEui}/config", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    # def systemBaseStationBsEuiConfigPost(self, bsEui: str, profile: enum.Enum) -> dict:
    #     """
    #     Set the profile of the requested base station
    #
    #     :param bsEui: Unique bsEui of the requested base station
    #     :param profile: The defined profile of the base station
    #     :return: Base station configuration overview information
    #     """
    #
    #     req = requests.post(url=self.server_address + f"/v2/system/basestation/{bsEui}/config", verify=False,
    #                         headers={"Authorization": f"Bearer {self.jwt_token}"},
    #                         json={'profile': profile}, timeout=3)
    #
    #     if req.status_code == 200:
    #         return req.json()
    #     else:
    #         check_status_code(req=req)

    def systemBaseStationBsEuiDelete(self, bsEui: str) -> bool:
        """
        Deletes the requested base station from Mythings Central. This cancels the connection to the core. Normally,
        the core reconnects right after. This can be used to reset the bssci session with the core and the saved
        meta data.

        :param bsEui: Unique bsEui of the requested base station
        :return: Bool if the requested base station was deleted or not
        """

        req = requests.delete(url=self.server_address + f"/v2/system/basestation/{bsEui}", verify=False,
                              headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return True
        else:
            check_status_code(req=req)

    def systemBaseStationBsEuiGet(self, bsEui: str) -> dict:
        """
        Gets system status information for the requested base station

        :param bsEui: Unique bsEui of the requested base station
        :return: System status information for the requested base station
        """

        req = requests.get(url=self.server_address + f"/v2/system/basestation/{bsEui}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def systemBaseStationBsEuiPost(self, bsEui: str, **kwargs) -> bool:
        """
        Adds meta data to a existing base station

        :param bsEui: Unique bsEui of the requested base station
        :keyword name: Unique Name of your new base station
        :keyword info: Information about this base station. Example: (what its for or who is responsible)
        :keyword location: Details on the location of the base station
        :return: Bool if meta data was successfully added to the requested base station or not
        """

        allowed = ['name', 'info', 'location']
        body = {x: kwargs[x] for x in kwargs if x in allowed and kwargs[x] is not None}

        req = requests.post(url=self.server_address + f"/v2/system/basestation/{bsEui}", verify=False,
                            headers={"Authorization": f"Bearer {self.jwt_token}"}, json=body, timeout=3)

        if req.status_code == 200:
            return True
        else:
            check_status_code(req=req)
