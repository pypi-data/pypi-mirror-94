# AgentConnectorStats

Statistics periodically collected from a running AgentConnector. These statistics may be used to understand how the AgentConnector is performing, diagnose issues, and so on. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**system** | [**AgentConnectorSystemStats**](AgentConnectorSystemStats.md) |  | 
**metadata** | [**AgentConnectorStatsMetadata**](AgentConnectorStatsMetadata.md) |  | 
**transport** | [**AgentConnectorTransportStats**](AgentConnectorTransportStats.md) |  | 
**shares** | [**AgentConnectorShareStats**](AgentConnectorShareStats.md) |  | [optional] 
**overall_status** | **str** | The summary status of the AgentConnector. - A &#x60;good&#x60; status means that no action is neccessary on this AgentConnector - A &#x60;warn&#x60; status means that there is an issue that should be dealt with   Examples include connections restarting frequently. - A &#x60;down&#x60; status indicates that there is a service accessibility problem   that should be dealt with as soon as possible. This could mean that there is a   problem with the AgentConnector&#39;s configuration, or the platform. - A &#x60;stale&#x60; status indicates that although there may not be anything wrong,   we haven&#39;t been able to update the status recently. This may indicate   a communications issue between Agilicus and the AgentConnector.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


