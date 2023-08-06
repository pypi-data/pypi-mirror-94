# IpsecConnection

An IPsec connection
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A descriptive name for the ipsec connection. The name must be a unique within a connectors connections.  | 
**inherit** | **bool** | Enable configuration inheritance. See inherit_config_from attribute.  | [optional] [default to False]
**inherit_from** | **str** | Allows inheriting configuration from a named config object. If any configuration in this object is Null or undefined, it will inherit from the named source that is part of the connector.  | [optional] 
**gateway_interface** | [**IpsecGatewayInterface**](IpsecGatewayInterface.md) |  | [optional] 
**config** | [**IpsecConnectionConfig**](IpsecConnectionConfig.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


