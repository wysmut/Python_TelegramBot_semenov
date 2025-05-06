from dataclasses import dataclass

from app.core.orders.constants import OrderStatusEnum
from app.core.orders.models import Product, Order, OrderedProduct
from app.infra.postgres.db import Database
from sqlalchemy import select, update, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.postgresql import insert


@dataclass
class ProductRepository:
    database: Database

    async def list_products(self) -> list[Product]:
        async with self.database.session() as session:
            result = await session.execute(select(Product))
            return result.scalars().all()

@dataclass
class OrderRepository:
    database: Database

    async def create_order(self, user_id: int) -> Order:
        async with self.database.session() as session:
            order = Order(user_id=user_id, status=OrderStatusEnum.UNLISTED)
            session.add(order)
            await session.commit()
            return order

    async def get_active_order(self, user_id: int) -> Order | None:
        async with self.database.session() as session:
            result = await session.execute(
                select(Order)
                .where(and_(
                    Order.user_id == user_id,
                    Order.status != OrderStatusEnum.DONE
                ))
                .options(joinedload(Order.products).joinedload(OrderedProduct.product))
            return result.scalars().first()

    async def add_product_to_order(self, order_id: int, product_id: int) -> None:
        async with self.database.session() as session:
            await session.execute(
                insert(OrderedProduct)
                .values(order_id=order_id, product_id=product_id, quantity=1)
                .on_conflict_do_update(
                    constraint="orders_products_pkey",
                    set_={"quantity": OrderedProduct.quantity + 1}
                ))
            await session.commit()

    async def finish_order(self, order_id: int) -> None:
        async with self.database.session() as session:
            await session.execute(
                update(Order)
                .where(Order.id == order_id)
                .values(status=OrderStatusEnum.ORDERED))
            await session.commit()

    async def complete_order(self, order_id: int) -> None:
        async with self.database.session() as session:
            await session.execute(
                update(Order)
                .where(Order.id == order_id)
                .values(status=OrderStatusEnum.DONE))
            await session.commit()
