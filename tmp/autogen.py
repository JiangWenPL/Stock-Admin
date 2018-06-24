# coding: utf-8
from sqlalchemy import Column, DECIMAL, Enum, ForeignKey, INTEGER, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Buy(Base):
    __tablename__ = 'buy'

    buy_no = Column(INTEGER(11), primary_key=True)
    stock_name = Column(String(40))
    stock_price = Column(DECIMAL(7, 2))
    stock_num = Column(INTEGER(11))
    time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    state = Column(Enum('1', '2', '3'))
    price = Column(DECIMAL(7, 2))
    complete_num = Column(INTEGER(11))


class Sell(Base):
    __tablename__ = 'sell'

    sell_no = Column(INTEGER(11), primary_key=True)
    stock_name = Column(String(40))
    stock_price = Column(DECIMAL(7, 2))
    stock_num = Column(INTEGER(11))
    time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    state = Column(Enum('1', '2', '3'))
    price = Column(DECIMAL(7, 2))
    complete_num = Column(INTEGER(11))


class Tran(Base):
    __tablename__ = 'tran'

    trans_no = Column(INTEGER(11), primary_key=True)
    stock_name = Column(String(40))
    trans_price = Column(DECIMAL(7, 2))
    trans_stock_num = Column(INTEGER(11))
    time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    sell_no = Column(ForeignKey('sell.sell_no'), index=True)
    buy_no = Column(ForeignKey('buy.buy_no'), index=True)

    buy = relationship('Buy')
    sell = relationship('Sell')
