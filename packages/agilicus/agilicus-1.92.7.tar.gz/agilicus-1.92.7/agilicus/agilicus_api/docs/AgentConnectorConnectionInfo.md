# AgentConnectorConnectionInfo

Connection information pertaining to a Connector
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_uri** | **str** | The URI used to establish a connection to the connector. | [optional] 
**connection_location** | **str** | The location (e.g. fully qualified domain name) of the connection. While this matches the location in the &#x60;connection_uri&#x60;, it is provided separately for convenience.  | [optional] 
**connection_path** | **str** | The path of the connection. While this matches the path in the &#x60;connection_uri&#x60;, it is provided separately for convenience.  | [optional] 
**max_number_connections** | **int** | The maximum number of connections to maintain to the cluster when stable. Note that this value may be exceeded during times of reconfiguration. A value of zero means that the connection is effectively unused by this Secure Agent.  | [optional] [default to 16]
**ip_services** | [**list[ApplicationService]**](ApplicationService.md) | The list of ip services associated with this connection | [optional] 
**file_share_services** | [**list[FileShareService]**](FileShareService.md) | The list of fileshare services associated with this connection | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


