import requests

from py_behrtech.exceptions import check_status_code
from py_behrtech.Calls.functions import buildParameter
from py_behrtech.Parsers.modelParser import ModelParser


class Models:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def sensorModelsDelete(self, deleteAll: bool = False) -> dict:
        """
        Deletes all sensor Models

        :param deleteAll: Verifies deletion of all sensor models is on purpose
        :return: Information on deleted sensor models
        """

        req = requests.delete(url=self.server_address + f"/v2/sensormodels?deleteAll={deleteAll}", verify=False,
                              headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def sensorModelsGet(self, returnCount: int = '', offset: int = '') -> ModelParser:
        """
        Gets information on all registered node models

        :param returnCount: The amount of node models to be requested. (-1 for all)
        :param offset: Node model amount to start the request from
        :return: Parser object of configured node models
        """

        req = requests.get(url=self.server_address + f"/v2/sensormodels" + buildParameter(params=vars()), verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return ModelParser(req=req)
        else:
            check_status_code(req=req)

    def sensorModelsPost(self):
        pass

    def sensorModelsSensorTypeDelete(self, sensorType: str) -> bool:
        """
        Deletes the requested sensor model

        :param sensorType: Unique sensor model type
        :return: Bool if sensor model was deleted or not
        """

        req = requests.delete(url=self.server_address + f"/v2/sensormodels/{sensorType}", verify=False,
                              headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return True
        else:
            check_status_code(req=req, messages={404: f"Sensor Model with {sensorType} not found"})

    def sensorModelsSensorTypeGet(self, sensorType: str) -> ModelParser:
        """
        Gets information on a registered node model

        :param sensorType: Unique identifier of the node model to be requested
        :return: Parser object of configured node model
        """

        req = requests.get(url=self.server_address + f"/v2/sensormodels/{sensorType}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return ModelParser(req=req)
        else:
            check_status_code(req=req)

    def sensorModelsSensorTypePost(self):
        pass
