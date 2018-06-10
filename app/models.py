from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


# BaseModel = declarative_base ()


class Admin ( db.Model ):
    __tablename__ = "admin"
    id = db.Column ( db.Integer, primary_key=True )
    password_hash = db.Column ( db.String ( 32 ) )
    name = db.Column ( db.String ( 32 ), index=True )
    contact = db.Column ( db.String ( 32 ), index=True )

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __init__(self, id, password, name, contact):
        self.id = id
        self.password = password
        self.name = name
        self.contact = contact

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
        return '<User %r>' % self.name

#
# class Book ( db.Model ):
#     __tablename__ = "book"
#     length = 8
#     bookID = db.Column ( db.String ( 32 ), primary_key=True )
#     category = db.Column ( db.String ( 32 ) )
#     book_name = db.Column ( db.String ( 32 ) )
#     press = db.Column ( db.String ( 32 ) )
#     year = db.Column ( db.Numeric ( 4, 0 ) )
#     author = db.Column ( db.String ( 32 ) )
#     price = db.Column ( db.Numeric ( 10, 2 ) )
#     amount = db.Column ( db.Integer )
#     stock = db.Column ( db.Integer )
#
#     def __init__(self, bookID, category, book_name, press, year, author, price, amount, stock):
#         try:
#             self.bookID = str ( bookID )
#             self.category = str ( category )
#             self.book_name = str ( book_name )
#             self.press = str ( press )
#             assert int ( year ) > 0 and int ( year ) < 10000, 'year not in (0,10000)'
#             self.year = int ( year )
#             self.author = str ( author )
#             assert float ( price ) >= 0, 'Price should be non negative number'
#             self.price = float ( price )
#             assert int ( amount ) >= 0, 'Amount should be non negative integer'
#             self.amount = int ( amount )
#             assert int ( stock ) >= 0, 'Stock should be non negative integer'
#             self.stock = int ( stock )
#         except Exception as e:
#             print ( e )
#             raise e
#
#     def __repr__(self):
#         return '<Book Name %r>' % self.book_name
#
#
# class Card ( db.Model ):
#     __tablename__ = "card"
#     length = 4
#     cardID = db.Column ( db.Integer, primary_key=True )
#     name = db.Column ( db.String ( 32 ) )
#     department = db.Column ( db.String ( 32 ) )
#     category = db.Column ( db.String ( 32 ) )
#
#     def __init__(self, cardID, name, departement, category):
#         try:
#             self.cardID = int ( cardID )
#             self.name = str ( name )
#             self.department = str ( departement )
#             self.category = str ( category )
#         except Exception as e:
#             print ( e )
#             raise e
#
#
# class Borrow ( db.Model ):
#     __tablename__ = "borrow"
#     bid = db.Column ( db.Integer, primary_key=True, autoincrement=True )
#     book_id = db.Column ( db.String ( 32 ), db.ForeignKey ( "book.bookID" ) )
#     card_id = db.Column ( db.Integer, db.ForeignKey ( "card.cardID", ondelete="CASCADE" ) )
#     borrow_date = db.Column ( db.DateTime, default=datetime.datetime.now () )
#     return_date = db.Column ( db.DateTime, default=datetime.datetime.now () + datetime.timedelta ( days=15 ) )
#     returned = db.Column ( db.Boolean )
#
#     def __init__(self, book_id, card_id, return_days=15, borrow_date=datetime.datetime.now ().date (), returned=False):
#         try:
#             self.book_id = str ( book_id )
#             self.card_id = int ( card_id )
#             # self.borrow_date = datetime.datetime.strptime ( borrow_date, "%Y-%m-%d" )
#             # self.return_date = datetime.datetime.strptime ( return_date, "%Y-%m-%d" )
#             self.borrow_date = borrow_date
#             assert return_days > 0, 'Should borrow at last 1 day'
#             self.return_date = (datetime.datetime.now () + datetime.timedelta ( days=int ( return_days ) )).date ()
#             self.returned = returned
#         except Exception as e:
#             print ( e )
#             raise e
