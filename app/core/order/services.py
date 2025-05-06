from dataclasses import dataclass

from app.core.orders.constants import OrderStatusEnum
from app.core.orders.exceptions import ActiveOrderExists
from app.core.orders.models import Order, Product
from app.core.orders.repositories import OrderRepository, ProductRepository


@dataclass
class ProductService:
    repository: ProductRepository

    async def list_products(self) -> list[Product]:
        return await self.repository.list_products()


@dataclass
class OrderService:
    repository: OrderRepository

    async def create_order(self, user_id: int) -> int:
        if await self.get_active_order_for_user(user_id):
            raise ActiveOrderExists()
        return await self.repository.create_order(user_id)

    async def get_order_by_id(self, order_id: int) -> Order | None:
        return await self.repository.get_order_by_id(order_id)

    async def get_active_order_for_user(self, user_id: int) -> Order | None:
        return await self.repository.get_active_order_for_user(user_id)

    async def add_product_to_order(self, order_id: int, product_id: int) -> None:
        return await self.repository.add_product_to_order(order_id, product_id)

    async def send_order_to_waiters(self, order_id: int) -> None:
        return await self.repository.set_order_status(order_id, OrderStatusEnum.ordered)

    async def mark_order_done(self, order_id: int) -> None:
        return await self.repository.set_order_status(order_id, OrderStatusEnum.done)
