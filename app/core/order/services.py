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
    order_repository: OrderRepository
    product_repository: ProductRepository

    async def create_order(self, user_id: int) -> Order:
        if await self.order_repository.get_active_order(user_id):
            raise ActiveOrderExists()
        return await self.order_repository.create_order(user_id)

    async def get_active_order(self, user_id: int) -> Order | None:
        return await self.order_repository.get_active_order(user_id)

    async def add_product_to_order(self, order_id: int, product_id: int) -> None:
        await self.order_repository.add_product_to_order(order_id, product_id)

    async def finish_order(self, order_id: int) -> None:
        await self.order_repository.finish_order(order_id)

    async def complete_order(self, order_id: int) -> None:
        await self.order_repository.complete_order(order_id)
