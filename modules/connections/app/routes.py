def register_routes(api, app, root="api"):
    from modules.connections.app.udaconnect import register_routes as attach_udaconnect

    # Add routes
    attach_udaconnect(api, app)
