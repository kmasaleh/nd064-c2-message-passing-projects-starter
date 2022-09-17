from modules.shared.models import Connection, Location, Person  # noqa
from modules.shared.schemas import ConnectionSchema, LocationSchema, PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from modules.connections.app.udaconnect.controllers import api as connections_api

    api.add_namespace(connections_api, path=f"/{root}")
