import requests

from py_behrtech.exceptions import check_status_code
from py_behrtech.Calls.functions import buildParameter


class Azure:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def azureFunctionDelete(self, deleteAll: bool = False) -> dict:
        """
        Deletes all Azure functions from the Service Center. Iterates over all existing functions, if a function still
        has mappings referred to it, the task will stop, resulting in some functions being deleted and some not.
        No guarantee can be given if all functions without mappings are actually deleted.

        :param deleteAll: Verifies deletion of all Azure functions is on purpose
        :return: Number of Azure functions deleted
        """

        req = requests.delete(url=self.server_address + f"/v2/azurefunction?deleteAll={deleteAll}", verify=False,
                              headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def azureFunctionIdDelete(self, functionId: str) -> bool:
        """
        Delete a single Azure function from the Service Center.

        :param functionId: Unique Azure function ID
        :return: Bool if Azure function has been successfully deleted or not
        """

        req = requests.delete(url=self.server_address + f"/v2/azurefunction/{functionId}", verify=False,
                              headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return True
        else:
            check_status_code(req=req)

    def azureFunctionIdGet(self, functionId: str) -> dict:
        """
        Gets information about the requested Azure function

        :param functionId: Unique Azure function ID
        :return: Detailed information about the requested Azure function
        """

        req = requests.get(url=self.server_address + f"/v2/azurefunction/{functionId}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def azureFunctionGet(self, returnCount: int = '', offset: int = '') -> dict:
        """
        Gets information about all Azure functions

        :param returnCount: The amount of Azure functions to be requested. -1 is ALL
        :param offset: The Azure functions count to start the Azure function data request from
        :return: Detailed information about the requested Azure functions
        """

        req = requests.get(url=self.server_address + f"/v2/azurefunction" + buildParameter(params=vars()), verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def azureMappingDelete(self, deleteAll: bool = False) -> dict:
        """
        Deletes all Azure mappings from the Service Center.

        :param deleteAll: Verifies deletion of all Azure mappings is on purpose
        :return: Number of Azure mappings deleted
        """

        req = requests.delete(url=self.server_address + f"/v2/azuremapping?deleteAll={deleteAll}", verify=False,
                              headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def azureMappingGet(self, returnCount: int = '', offset: int = '', azureFunctionID: str = '') -> dict:
        """
        Gets information about the requested Azure mappings

        :param returnCount: The amount of Azure mappings to be requested. -1 is ALL
        :param offset: The Azure mapping count to start the Azure mapping data request from
        :param azureFunctionID: Unique Azure function ID
        :return: Detailed information about the requested Azure mappings
        """

        req = requests.get(url=self.server_address + f"/v2/azuremapping" + buildParameter(params=vars()), verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def azureMappingIdDelete(self, mappingId: str) -> bool:
        """
        Delete a single Azure mapping from the Service Center.

        :param mappingId: Unique Azure mapping ID
        :return: Bool if Azure mapping has been successfully deleted or not
        """

        req = requests.delete(url=self.server_address + f"/v2/azuremapping/{mappingId}", verify=False,
                              headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return True
        else:
            check_status_code(req=req)

    def azureMappingIdGet(self, mappingId: str) -> dict:
        """
        Gets information about the requested Azure mapping

        :param mappingId: Unique Azure mapping ID
        :return: Detailed information about the requested Azure mapping
        """

        req = requests.get(url=self.server_address + f"/v2/azuremapping/{mappingId}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)
