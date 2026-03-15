from injector import Module, provider, singleton

from apps.orders.services import OrderService


class AppModule(Module):
    @singleton
    @provider
    def provide_order_service(self) -> OrderService:
        return OrderService()
