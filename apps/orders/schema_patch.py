from injector import Injector
from rest_framework.schemas import generators

from apps.orders.app_module import AppModule

_injector = Injector([AppModule()])

_original_create_view = generators.BaseSchemaGenerator.create_view


def patched_create_view(self, callback, method, request=None):
    view_cls = callback.cls

    import inspect

    sig = inspect.signature(view_cls.__init__)
    params = list(sig.parameters.keys())

    if "order_service" not in params:
        return _original_create_view(self, callback, method, request)

    initkwargs = getattr(callback, "initkwargs", {}).copy()

    view = _injector.get(view_cls)

    for key, value in initkwargs.items():
        setattr(view, key, value)

    if not hasattr(view, "action_map"):
        view.action_map = initkwargs.get(
            "action_map",
            {
                "get": "list",
                "post": "create",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
        )

    view.action = view.action_map.get(method.lower())
    view.basename = initkwargs.get(
        "basename", view_cls.__name__.lower().replace("viewset", "")
    )

    if request is not None:
        view.request = request
    view.args = ()
    view.kwargs = {}
    view.format_kwarg = None

    return view


generators.BaseSchemaGenerator.create_view = patched_create_view
