from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, sessionmaker
from uuid import UUID, uuid4
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id: Mapped [UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now) 
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    addresses = relationship("Address", back_populates="user")
    orders = relationship("Order", back_populates="user")


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False) 
    street: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False) 
    state: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column(nullable=False)
    is_primary: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now) 
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="addresses")


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    address_id: Mapped[UUID] = mapped_column(ForeignKey('addresses.id'), nullable=False)
    user = relationship("User", back_populates="orders")
    address = relationship("Address")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    order_id: Mapped[UUID] = mapped_column(ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey('products.id'), nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


connect_url = "postgresql+psycopg2://postgres:12345@localhost:5432/test_db"

engine = create_engine(
    connect_url,
    echo=True
)

session_factory = sessionmaker(engine)

# with session_factory() as session:
    # сначала я создал пользователей и адресы

    # user1 = User(username="John Doe", email="jdoe@example.com")
    # user1.addresses = [
    #     Address(street="1 Main St", city="New York", state="NY", zip_code="12345", country="USA"),
    # ]

    # user2 = User(username="John Eod", email="joed@example.com")
    # user2.addresses = [
    #     Address(street="22 Oak Ave", city="Los Angeles", state="CA", zip_code="12345", country="USA"),
    # ]

    # user3 = User(username="Alex Test", email="atest@example.com")
    # user3.addresses = [
    #     Address(street="100 Elm St", city="Chicago", state="IL", zip_code="12345", country="USA"),
    # ]

    # user4 = User(username="Jessica Doe", email="jessdoe@example.com")
    # user4.addresses = [
    #     Address(street="9 Pine Rd", city="Miami", state="FL", zip_code="12345", country="USA"),
    # ]

    # user5 = User(username="Bob Doe", email="bobdoe@example.com")
    # user5.addresses = [
    #     Address(street="500 Market St", city="San Francisco", state="CA", zip_code="12345", country="USA"),
    # ]

    # # session.add(user)
    # session.add_all([user1, user2, user3, user4, user5])


    # затем остальные таблицы (Product, Order и OrderItem)


    # products = [
    #     Product(name="Computer"), Product(name="Laptop"), Product(name="Smartphone"),
    #     Product(name="Test product"), Product(name="Test product 2")
    # ]
    # session.add_all(products)
    # session.commit()

    # users = session.query(User).all()
    # products = session.query(Product).all()
    # addresses = session.query(Address).all()
    
    # orders = []
    # order_items = []
    
    # for i in range(5):
    #     order = Order(
    #         user_id=users[i].id,
    #         address_id=addresses[i].id,
    #     )
    #     session.add(order)
    #     orders.append(order)
    
    # session.flush()

    # for i in range(5):
    #     order_item = OrderItem(
    #         order_id=orders[i].id,
    #         product_id=products[i].id,
    #     )
    #     session.add(order_item)
    #     order_items.append(order_item)
        
    
    # session.add_all(orders)
    # session.add_all(order_items)
    # session.commit()
