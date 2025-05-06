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
            query = select(Product)
            return list(await session.scalars(query))


@dataclass
class OrderRepository:
    database: Database

    async def create_order(self, user_id: int) -> int:
        async with self.database.session() as session:
            insert_stmt = insert(Order).values(user_id=user_id, status=OrderStatusEnum.unlisted)
            order_id = await session.execute(insert_stmt)
            await session.commit()
            return order_id.scalar()

    async def get_order_by_id(self, order_id: int) -> Order | None:
        async with self.database.session() as session:
            query = select(Order).where(Order.id == order_id).options(
                joinedload(Order.products).joinedload(OrderedProduct.product))
            return await session.scalar(query)

    async def get_active_order_for_user(self, user_id: int) -> Order | None:
        async with self.database.session() as session:
            select_stmt = select(Order).where(
                and_(Order.user_id == user_id,
                     Order.status.in_([OrderStatusEnum.unlisted, OrderStatusEnum.ordered]))).options(
                joinedload(Order.products).joinedload(OrderedProduct.product))
            return await session.scalar(select_stmt)

    async def add_product_to_order(self, order_id: int, product_id: int) -> None:
        async with self.database.session() as session:
            insert_stmt = insert(OrderedProduct).values(order_id=order_id, product_id=product_id, amount=1)
            upsert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=[OrderedProduct.order_id, OrderedProduct.product_id],
                set_={"amount": OrderedProduct.amount + 1})
            await session.execute(upsert_stmt)
            await session.commit()

    async def set_order_status(self, order_id: int, status: OrderStatusEnum) -> None:
        async with self.database.session() as session:
            update_stmt = update(Order).where(Order.id == order_id).values(status=status)
            await session.execute(update_stmt)
            await session.commit()
