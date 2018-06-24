# coding: utf-8
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import json
import datetime
# from sqlalchemy import CHAR, Column, DECIMAL, ForeignKey, INTEGER, String, TIMESTAMP, text
# from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_


# Base = declarative_base ()
# metadata = Base.metadata


# BaseModel = declarative_base ()


class Admin ( db.Model ):
    __tablename__ = "admin"
    id = db.Column ( db.String ( 32 ), primary_key=True )
    password_hash = db.Column ( db.String ( 32 ) )
    is_root = db.Column ( db.Boolean, default=False )

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __init__(self, id, password, is_root=False):
        self.id = id
        self.password = password
        self.is_root = is_root
        if id == 'Alice':
            self.is_root = True

    @property
    def password(self):
        raise AttributeError ( "Password unaccessible" )

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash ( password )

    def check_password_hash(self, password):
        return check_password_hash ( self.password_hash, password )

    # For debug
    def __repr__(self):
        return '<User %r>' % self.id


class Auth ( db.Model ):
    __tablename__ = "auth"
    auth_id = db.Column ( db.Integer, primary_key=True, autoincrement=True )
    stock_id = db.Column ( db.String ( 32 ), db.ForeignKey ( 'stock.stock_name', ondelete='CASCADE' ), index=True )
    admin_id = db.Column ( db.String ( 32 ), db.ForeignKey ( 'admin.id', ondelete='CASCADE' ) )

    def __init__(self, admin_id, stock_id):
        self.stock_id = stock_id
        self.admin_id = admin_id

    # For debug
    def __repr__(self):
        return '<auth_id %r: %r %r>' % (self.auth_id, self.stock_id, self.admin_id)


class Stock ( db.Model ):
    __tablename__ = "stock"
    stock_inner_id = db.Column ( db.Integer, primary_key=True, autoincrement=True )
    stock_name = db.Column ( db.String ( 40 ), index=True )
    is_trading = db.Column ( db.Boolean, default=True )
    up_confine = db.Column ( db.DECIMAL ( 7, 2 ), default=10 )
    down_confine = db.Column ( db.DECIMAL ( 7, 2 ), default=10 )

    def __init__(self, stock_name):
        self.stock_name = stock_name

    # For debug
    def __repr__(self):
        return '<stock: %r: %r %r %r %r>' % (
            self.stock_inner_id, self.stock_name, self.is_trading, self.down_confine, self.up_confine)


class Buy ( db.Model ):
    __bind_key__ = 'stock'
    __tablename__ = 'buy'
    buy_no = db.Column ( db.INTEGER, primary_key=True )
    stock_name = db.Column ( db.String ( 40 ) )
    stock_price = db.Column ( db.DECIMAL ( 7, 2 ) )
    stock_num = db.Column ( db.INTEGER )
    time = db.Column ( db.TIMESTAMP, server_default=db.text ( "CURRENT_TIMESTAMP" ) )
    state = db.Column ( db.Enum ( '1', '2', '3' ) )
    price = db.Column ( db.DECIMAL ( 7, 2 ) )
    complete_num = db.Column ( db.INTEGER )

    def __init__(self, stock_name, stock_price, stock_num):
        self.stock_name = stock_name
        self.stock_price = stock_price
        self.stock_num = stock_num
        # self.time = time


class Sell ( db.Model ):
    __bind_key__ = 'stock'
    __tablename__ = 'sell'
    sell_no = db.Column ( db.INTEGER, primary_key=True )
    stock_name = db.Column ( db.String ( 40 ) )
    stock_price = db.Column ( db.DECIMAL ( 7, 2 ) )
    stock_num = db.Column ( db.INTEGER )
    time = db.Column ( db.TIMESTAMP, server_default=db.text ( "CURRENT_TIMESTAMP" ) )
    state = db.Column ( db.Enum ( '1', '2', '3' ) )
    price = db.Column ( db.DECIMAL ( 7, 2 ) )
    complete_num = db.Column ( db.INTEGER )

    def __init__(self, stock_name, stock_price, stock_num):
        self.stock_name = stock_name
        self.stock_price = stock_price
        self.stock_num = stock_num
        # self.time = time


class Tran ( db.Model ):
    __bind_key__ = 'stock'
    __tablename__ = 'tran'
    trans_no = db.Column ( db.INTEGER, primary_key=True )
    stock_name = db.Column ( db.String ( 40 ) )
    trans_price = db.Column ( db.DECIMAL ( 7, 2 ) )
    trans_stock_num = db.Column ( db.INTEGER )
    time = db.Column ( db.TIMESTAMP, server_default=db.text ( "CURRENT_TIMESTAMP" ) )
    sell_no = db.Column ( db.ForeignKey ( 'sell.sell_no' ), index=True )
    buy_no = db.Column ( db.ForeignKey ( 'buy.buy_no' ), index=True )

    buy = db.relationship ( 'Buy' )
    sell = db.relationship ( 'Sell' )

    def __init__(self, stock_name, trans_price, trans_stock_num):
        self.stock_name = stock_name
        self.trans_stock_num = trans_stock_num
        self.trans_price = trans_price


def test_init():
    with open ( 'tmp/db_init.json' ) as f:
        db_dict = json.load ( f )
        for admin in db_dict['admin']:
            if Admin.query.get ( admin[0] ) is None:
                db.session.add ( Admin ( admin[0], admin[1] ) )
        for auth in db_dict['auth']:
            db.session.add ( Auth ( auth[0], auth[1] ) )
        for sell in db_dict['sell']:
            db.session.add ( Sell ( sell[0], sell[1], sell[2] ) )
        for buy in db_dict['buy']:
            db.session.add ( Buy ( buy[0], buy[1], buy[2] ) )
        for tran in db_dict['tran']:
            db.session.add ( Tran ( tran[0], tran[1], tran[1] ) )
        for stock in db_dict['stock']:
            db.session.add ( Stock ( stock[0] ) )
        db.session.commit ()
        # admins = [Admin ( 0, 'a' ), Admin ( 1, 'b' )]
        # for admin in admins:
        #     if Admin.query.get ( admin.id ) is None:
        #         db.session.add ( admin )
        # auths = [Auth ( "0", "HK_TENCENT" ), Auth ( "0", "APPLE" ), Auth ( "1", "BMW" )]
        # for auth in auths:
        #     if Auth.query.filter ( and_ ( auth.admin_id == Auth.admin_id, auth.stock_id == Auth.stock_id ) ) is None:
        #         db.session.add ( auth )
        # buys = [Buy ( "HK_TENCENT", 10.2, 100 ), Buy ( "APPLE", 1.2, 24 ), Buy ( "APPLE", 1.2, 24 ),
        #         Buy ( "BMW", 1.2, 24 )]
        # db.session.add_all ( buys )
        # sells = [Sell ( "HK_TENCENT", 10.2, 100 ), Sell ( "APPLE", 1.2, 24 ),
        #          Sell ( "APPLE", 1.2, 24 )]
        # db.session.add_all ( sells )
        # trans = [Tran ( "APPLE", 0.11, 1 ), Tran ( "BMW", 1.63, 120 )]
        # db.session.add_all ( trans )
        # db.session.commit ()
