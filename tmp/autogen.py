# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Enum, ForeignKey, INTEGER, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Message(Base):
    __tablename__ = 'message'

    stock_name = Column(String(40), primary_key=True)
    stock_id = Column(CHAR(30))
    stock_price = Column(DECIMAL(7, 2))
    continue_trans = Column(TINYINT(1), server_default=text("'1'"))


class Buy(Base):
    __tablename__ = 'buy'

    buy_no = Column(INTEGER(11), primary_key=True)
    stock_id = Column(CHAR(10))
    stock_name = Column(ForeignKey('message.stock_name'), index=True)
    stock_price = Column(DECIMAL(7, 2))
    stock_num = Column(INTEGER(11))
    time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    state = Column(Enum('1', '2', '3'))
    price = Column(DECIMAL(7, 2))
    complete_num = Column(INTEGER(11))
    user_id = Column(INTEGER(11))

    message = relationship('Message')


class Sell(Base):
    __tablename__ = 'sell'

    sell_no = Column(INTEGER(11), primary_key=True)
    stock_id = Column(CHAR(10))
    stock_name = Column(ForeignKey('message.stock_name'), index=True)
    stock_price = Column(DECIMAL(7, 2))
    stock_num = Column(INTEGER(11))
    time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    state = Column(Enum('1', '2', '3'))
    price = Column(DECIMAL(7, 2))
    complete_num = Column(INTEGER(11))
    user_id = Column(INTEGER(11))

    message = relationship('Message')


class Tran(Base):
    __tablename__ = 'tran'

    trans_no = Column(INTEGER(11), primary_key=True)
    stock_id = Column(CHAR(10))
    stock_name = Column(ForeignKey('message.stock_name'), index=True)
    trans_price = Column(DECIMAL(7, 2))
    trans_stock_num = Column(INTEGER(11))
    time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    sell_no = Column(ForeignKey('sell.sell_no'), index=True)
    buy_no = Column(ForeignKey('buy.buy_no'), index=True)

    buy = relationship('Buy')
    sell = relationship('Sell')
    message = relationship('Message')
