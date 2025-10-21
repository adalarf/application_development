from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db import User, Address, session_factory, Order, OrderItem, Product


def get_users_with_addresses():
    # добавил дополнительные selectinload для вывода информации из других таблиц
    query = select(User).options(selectinload(User.addresses),
                                 selectinload(User.orders).selectinload(Order.items)
                                 .selectinload(OrderItem.product))

    with session_factory() as session:
        users = session.execute(query).scalars().all()

    return users


users = get_users_with_addresses()
for u in users:
    print(f"{u.username} <{u.email}>")
    for addr in u.addresses:
        print(f"  - {addr.street}, {addr.city}, {addr.country}")
    
    for order in u.orders:
        print(f"Заказ #{str(order.id)}")
        
        print("Продукты в заказе:")
        for item in order.items:
            print(item.product.name)
