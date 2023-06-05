import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

def add_data():
    with open('fixtures/tests_data.json', 'r') as file:
        data = json.load(file)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

### ВАРИАНТ №1!

# def get_info_about_sale(publisher_input):
#     info_sale = session.query(
#         Publisher,
#         Book,
#         Stock,
#         Shop,
#         Sale
#         ).select_from(Sale
#         ).join(Stock
#         ).join(Shop
#         ).join(Book
#         ).join(Publisher)
#     if publisher_input.isdigit() == True:
#         info_sale = info_sale.filter(Publisher.id == publisher_input)
#     else:
#         info_sale = info_sale.filter(Publisher.name == publisher_input)
#     for publisher, book, stock, shop, sale in info_sale.all():
#         print(f'| {book.title: <40} | {shop.name: <9} | {sale.price: <5} | {sale.date_sale.strftime("%d-%m-%Y")} |')

### ВАРИАНТ №2!

def get_info_about_sale(publisher_input):
    info_sale = session.query(
        Publisher,
        Book,
        Stock,
        Shop,
        Sale
        ).filter(Publisher.id == Book.id_publisher
        ).filter(Book.id == Stock.id_book
        ).filter(Stock.id_shop == Shop.id
        ).filter(Sale.id_stock == Stock.id)
    if publisher_input.isdigit() == True:
        info_sale = info_sale.filter(Publisher.id == publisher_input)
    else:
        info_sale = info_sale.filter(Publisher.name == publisher_input)
    for publisher, book, stock, shop, sale in info_sale.all():
        print(f'| {book.title: <40} | {shop.name: <9} | {sale.price: <5} | {sale.date_sale.strftime("%d-%m-%Y")} |')

if __name__ == '__main__':
    with open('info.txt') as file_info:
        info = file_info.read().split(', ')

    login = info[0]
    password = info[1]
    name_db = info[2]

    DSN = f'postgresql://{login}:{password}@localhost:5432/{name_db}'
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    publisher_input = input('Введите фамилию или ID писателя: ')
    get_info_about_sale(publisher_input)

    session.close
