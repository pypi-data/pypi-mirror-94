import datetime
import agilicus

import dateutil.tz

from . import context
from .input_helpers import get_org_from_input_or_ctx
from agilicus import input_helpers


def query(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    kwargs["org_id"] = org_id
    query_results = apiclient.connectors_api.list_connector(**kwargs)
    return query_results


def query_agents(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    kwargs["org_id"] = org_id
    query_results = apiclient.connectors_api.list_agent_connector(**kwargs)
    return query_results


def add_agent(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    spec = agilicus.AgentConnectorSpec(org_id=org_id, **kwargs)
    connector = agilicus.AgentConnector(spec=spec)
    return apiclient.connectors_api.create_agent_connector(connector)


def get_agent(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    return apiclient.connectors_api.get_agent_connector(
        connector_id, org_id=org_id, **kwargs
    )


def delete_agent(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    return apiclient.connectors_api.delete_agent_connector(
        connector_id, org_id=org_id, **kwargs
    )


def get_agent_info(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    return apiclient.connectors_api.get_agent_info(connector_id, org_id=org_id, **kwargs)


def replace_agent(
    ctx,
    connector_id,
    connection_uri=None,
    max_number_connections=None,
    name=None,
    service_account_required=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    connector = apiclient.connectors_api.get_agent_connector(
        connector_id, org_id=org_id, **kwargs
    )

    if connection_uri:
        connector.spec.connection_uri = connection_uri

    if max_number_connections:
        connector.spec.max_number_connections = max_number_connections

    if name:
        connector.spec.name = name

    if service_account_required is not None:
        connector.spec.service_account_required = service_account_required

    return apiclient.connectors_api.replace_agent_connector(
        connector_id, agent_connector=connector
    )


def set_agent_connector_stats(ctx, connector_id, org_id, overall_status, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    system_objs = input_helpers.get_objects_by_location("system", kwargs)
    system = agilicus.AgentConnectorSystemStats(
        agent_connector_org_id=org_id, agent_connector_id=connector_id, **system_objs
    )
    transport_objs = input_helpers.get_objects_by_location("transport", kwargs)
    transport = agilicus.AgentConnectorTransportStats(**transport_objs)
    now = datetime.datetime.utcnow().replace(tzinfo=dateutil.tz.tzutc())
    metadata = agilicus.AgentConnectorStatsMetadata(collection_time=now)

    stats = agilicus.AgentConnectorStats(
        metadata=metadata,
        overall_status=overall_status,
        system=system,
        transport=transport,
    )

    return apiclient.connectors_api.create_agent_stats(connector_id, stats)


def get_agent_connector_stats(ctx, connector_id, org_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    return apiclient.connectors_api.get_agent_stats(
        connector_id, org_id=org_id, **kwargs
    )
