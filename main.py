import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import json

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True)

    # def __str__(self):
    #     return f'{self.id} | {self.name}'


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=180), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")

    # def __str__(self):
    #     return f'{self.id} | {self.title} | {self.id_publisher}'


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True)

    # def __str__(self):
    #     return f'{self.id} | {self.name}'


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)

    book = relationship(Book, backref="book_stock")
    shop = relationship(Shop, backref="shop_stock")

    # def __str__(self):
    #     return f'{self.id} | {self.count} | {self.id_book} | {self.id_shop}'


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    stock = relationship(Stock, backref="Sale")

    # def __str__(self):
    #     return f'{self.id} | {self.price} | {self.date_sale} | {self.count} | {self.id_stock}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


DSN = 'postgresql://postgres:Catrin.Sin.13@localhost:5432/HomeworkORM'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json') as f:
    json_data = json.load(f)

for record in json_data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

publisher_name = input('Введите идентификатор издателя: ')
session.commit()

for c in session.query(Publisher.name, Book.title, Shop.name, Sale.price, Sale.date_sale).join(Book).join(Stock).join(Shop).join(Sale).filter(Publisher.id == publisher_name).all():
    print(f'{c.title} | {c.name} | {c.price} | {c.date_sale}')


session.close()
