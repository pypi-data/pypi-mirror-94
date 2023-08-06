
![publish-pypi](https://github.com/matthewashley1/Fetch_BehrTech/workflows/publish-pypi/badge.svg)

# py-behrtech

A python wrapper for BehrTech's Mythings Central REST API. Currently, supporting version 3.1.0.

## Status:

This package is a work in progress. Currently, working to get all API endpoints implemented with checks on each returned status code.

## Example:

Set up your call, which creates a connection to your gateway and request messages.

```python
from py_behrtech import Calls

call = Calls(username='gateway_username', password='password for username', server_address='gateways IP address')

messages = call.messagesGet(returnCount=10, offset=100, epEui='70B3D5C1F004112C')

print(messages.getData())
```

## Endpoints Check List:

### Azure
EndPoint | Done
:--- | :---
azurefunctionDelete | :white_check_mark:
azurefunctionFunctionIDDelete | :white_check_mark:
azurefunctionFunctionIDGet | :white_check_mark:
azurefunctionGet | :white_check_mark:
azurefunctionPost | :x:
azuremappingDelete | :white_check_mark:
azuremappingGet | :white_check_mark:
azuremappingMappingIDDelete | :white_check_mark:
azuremappingMappingIDGet | :white_check_mark:
azuremappingPost | :x:

### Base Station
EndPoint | Done
:--- | :---
systemBasestationBsEuiConfigGet | :white_check_mark:
systemBasestationBsEuiConfigPost | :x:
systemBasestationBsEuiDelete | :white_check_mark:
systemBasestationBsEuiGet | :white_check_mark:
systemBasestationBsEuiPost | :white_check_mark:

### MQTT
EndPoint | Done
:--- | :---
brokerBrokerIDDelete | :x:
brokerBrokerIDGet | :white_check_mark:
brokerBrokerIDPost | :x:
brokerDelete | :x:
brokerGet | :white_check_mark:
brokerPost | :x:
mqttmappingDelete | :x:
mqttmappingGet | :white_check_mark:
mqttmappingPost | :x:
mqttmappingMappingIDDelete | :x:
mqttmappingMappingIDGet | :white_check_mark:

### Messages
EndPoint | Done
:--- | :---
messagesDelete | :white_check_mark:
messagesGet | :white_check_mark:
messagesPost | :x:

### Nodes
EndPoint | Done
:--- | :---
nodesDelete | :x:
nodesEpEuiDelete | :x:
nodesEpEuiGet | :white_check_mark:
nodesEpEuiPost | :x:
nodesEpEuiTxdataDelete | :x:
nodesEpEuiTxdataGet | :white_check_mark:
nodesEPEuiTxdataIdDelete | :x:
nodesEpEuiTxdataIdGet | :white_check_mark:
nodesEpEuiTxdataIdPost   | :x:
nodesEpEuiTxdataPost | :x:
nodesGet | :white_check_mark:
nodesPost | :x:

### Plugin
EndPoint | Done
:--- | :---
pluginAcceptGet | :white_check_mark:
pluginAcceptPost | :x:
pluginPluginNameArbitraryPathGet | :white_check_mark:
pluginPluginNameDelete | :white_check_mark:
pluginPluginNameGet | :white_check_mark:
pluginPluginNameMappingDelete | :white_check_mark:
pluginPluginNameMappingGet | :white_check_mark:
pluginPluginNameMappingPost | :white_check_mark:
pluginPluginNameMappingEpEuiDelete | :white_check_mark:
pluginRegisterGet | :white_check_mark:

### Sensor Models
EndPoint | Done
:--- | :---
sensormodelsDelete | :white_check_mark:
sensormodelsGet | :white_check_mark:
sensormodelsPost | :x:
sensormodelsSensorTypeDelete | :white_check_mark:
sensormodelsSensorTypeGet | :white_check_mark:
sensormodelsSensorTypePost | :x:

### System
EndPoint | Done
:--- | :---
authTicketGet | :white_check_mark:
systemDatabasedumpGet | :white_check_mark:
systemDatabasedumpIdDelete | :white_check_mark:
systemDatabasedumpIdGet | :white_check_mark:
systemEulaGet | :white_check_mark:
systemGet | :white_check_mark:
wsGet | :white_check_mark:
 
### User
EndPoint | Done
:--- | :---
loginPost | :white_check_mark:
userGet | :white_check_mark:
userPost | :white_check_mark:
userUUIDDelete | :white_check_mark:
userUUIDGet | :white_check_mark:
userUUIDProfilePost | :white_check_mark:
userUUIDResetPasswordPost | :white_check_mark:
 
## PyPI
Access [PyPI](https://pypi.org/project/py-behrtech/) project.

## License

py-behrtech is released under the [MIT](https://opensource.org/licenses/MIT) license
