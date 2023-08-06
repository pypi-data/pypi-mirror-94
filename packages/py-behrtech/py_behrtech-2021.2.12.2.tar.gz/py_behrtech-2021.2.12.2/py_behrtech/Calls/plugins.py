
import requests

from py_behrtech.exceptions import check_status_code


class Plugins:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def pluginAcceptGet(self) -> dict:
        """
        Gets information about accepted plugins

        :return: Information about accepted plugins
        """

        req = requests.get(url=self.server_address + f"/v2/plugin/accept", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def pluginAcceptPost(self):
        pass

    def pluginNameArbitraryPathGet(self, pluginName: str, arbitraryPath: str) -> dict:
        """
        Gets plugin provided endpoints. Every plugin provides its own endpoints

        :param pluginName: Name of the plugin to get information on
        :param arbitraryPath: URL of the endpoints to be accessed
        :return: Information on plugin provided endpoints
        """

        req = requests.get(url=self.server_address + f"/v2/plugin/{pluginName}/{arbitraryPath}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def pluginNameDelete(self, pluginName: str) -> bool:
        """
        Deletes and de-registers already accepted plugins

        :param pluginName: Name of the plugin to be deleted
        :return: Bool if plugin has been successfully deleted or not
        """

        req = requests.delete(url=self.server_address + f"/v2/plugin/{pluginName}", verify=False,
                              headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return True
        else:
            check_status_code(req=req)

    def pluginNameGet(self, pluginName: str) -> dict:
        """
        Gets information about the requested plugin by name

        :param pluginName: Name of the plugin to get information on
        :return: Information about the requested plugin by name
        """

        req = requests.get(url=self.server_address + f"/v2/plugin/{pluginName}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def pluginNameMappingGet(self, pluginName: str) -> dict:
        """
        Gets information about all mappings to a plugin by name

        :param pluginName: Name of the plugin to get information on
        :return: Information about all mappings to a plugin by name
        """

        req = requests.get(url=self.server_address + f"/v2/plugin/{pluginName}/mapping", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def pluginNameMappingDelete(self, pluginName: str, deleteAll: bool = False) -> bool:
        """
        Deletes all mappings for a plugin

        :param pluginName: Name of the plugin to delete all mappings for
        :param deleteAll: Verifies deletion of all mappings is on purpose
        :return: Bool if plugin mappings have been successfully deleted or not
        """

        req = requests.delete(url=self.server_address + f"/v2/plugin/{pluginName}/mapping?deleteAll={deleteAll}",
                              verify=False, headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return True
        else:
            check_status_code(req=req)

    def pluginNameMappingEpEuiDelete(self, pluginName: str, epEui: str) -> bool:
        """
        Deletes mapping of a node to a plugin

        :param pluginName: Name of the plugin to delete a mapping to
        :param epEui: The unique epEui of the node to delete a mapping for
        :return: Bool if plugin mapping has been successfully deleted or not
        """

        req = requests.delete(url=self.server_address + f"/v2/plugin/{pluginName}/mapping/{epEui}", verify=False,
                              headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return True
        else:
            check_status_code(req=req)

    def pluginNameMappingPost(self, pluginName: str, nodes: dict) -> dict:
        """
        Adds mapping for a node to a plugin

        :param pluginName: Name of the plugin to map a node to
        :param nodes: Nodes to me mapped to a plugin
        :return: Successfully mapped nodes
        """

        req = requests.post(url=self.server_address + f"/v2/plugin/{pluginName}/mapping", verify=False,
                            headers={"Authorization": f"Bearer {self.jwt_token}"}, json={'nodes': nodes}, timeout=3)

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def pluginRegisterGet(self) -> dict:
        """
        Gets information about registered plugins

        :return: Information about registered plugins
        """

        req = requests.get(url=self.server_address + f"/v2/plugin/register", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)
