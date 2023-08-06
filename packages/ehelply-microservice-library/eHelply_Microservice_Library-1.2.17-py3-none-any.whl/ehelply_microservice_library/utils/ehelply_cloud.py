from ehelply_python_sdk.services.access.auth_rules import AuthRule
from ehelply_python_sdk.services.access.sdk import AuthModel


def ehelply_cloud_access(
        auth: AuthModel,
        node: str,
        service_target: str,
        exception_if_unauthorized=True
) -> bool:
    return AuthRule(
        auth,
        AuthRule(auth).participant_has_node_on_target(
            node=node,
            target_identifier=service_target,
            partition="ehelply-resources"
        ),
        AuthRule(auth).participant_has_node_on_target(
            node=node,
            target_identifier=auth.project_uuid,
            partition="ehelply-cloud"
        ).customentity_has_node_on_target(
            node=node,
            target_identifier=service_target,
            partition="ehelply-cloud",
            entity_identifier=auth.project_uuid
        ),
        exception_if_unauthorized=exception_if_unauthorized
    ).verify()
