from modules.api.app.udaconnect.models import Connection, Location, Person  # noqa
from modules.api.app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from modules.api.app.udaconnect.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")
