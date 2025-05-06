from app.core.orders.models import Product, Order
from app.core.users.models import User
from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.is_waiter]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name]


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.user_id, Order.status]
