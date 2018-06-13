# 引入Form基类
from flask_wtf import FlaskForm
# 引入Form元素父类
from wtforms import StringField, PasswordField, BooleanField, IntegerField, FloatField, SelectField, DecimalField
# 引入Form验证父类
from wtforms.validators import DataRequired, Length, NumberRange, Optional

# from flask_wtf.file import FileAllowed, FileRequired, FileField
# from app import csv_set
# from app.models import Book

__author__ = 'JiangWen'


class LoginForm ( FlaskForm ):
    username = StringField ( "username", validators=[DataRequired ()] )
    password = PasswordField ( 'passsword', validators=[DataRequired ()] )
    remember = BooleanField ( "remember", validators=[Optional ()], default=False )


class ChangePWDForm ( FlaskForm ):
    username = StringField ( "username", validators=[DataRequired ()] )
    old_password = PasswordField ( 'passsword', validators=[DataRequired ()] )
    new_password = PasswordField ( 'passsword', validators=[DataRequired ()] )


class ConfineForm ( FlaskForm ):
    stock_name = StringField ( "stock_name", validators=[DataRequired ()] )
    down_confine = DecimalField ( "down_confine", validators=[DataRequired ()] )
    up_confine = DecimalField ( "up_confine", validators=[DataRequired ()] )


class ChangeAuth ( FlaskForm ):
    admin_id = StringField ( "admin_id", validators=[DataRequired ()] )
    stock_name = StringField ( "stock_name", validators=[DataRequired ()] )
    # action = StringField ( "action", validators=[DataRequired ()])
    action = SelectField ( "action", validators=[DataRequired ()],
                           choices=[("add", 'add'), ("delete", "delete")] )


class ChangeAccount ( FlaskForm ):
    admin_id = StringField ( "admin_id", validators=[DataRequired ()] )
    password = StringField ( "password", validators=[Optional ()] )
    is_root = BooleanField ( "is_root", validators=[Optional ()], default=False )
    action = SelectField ( "action", validators=[DataRequired ()],
                           choices=[("add", 'add'), ("delete", "delete"), ("update", "update")] )

# class CheckInForm ( FlaskForm ):
#     bookID = StringField ( "bookID", validators=[DataRequired ()] )
#     category = StringField ( "category", validators=[DataRequired ()] )
#     book_name = StringField ( "book_name", validators=[DataRequired ()] )
#     press = StringField ( "press", validators=[DataRequired ()] )
#     year = IntegerField ( "year", validators=[DataRequired (), NumberRange ( 0, 10000 )] )
#     author = StringField ( "author", validators=[DataRequired ()] )
#     price = FloatField ( "price", validators=[DataRequired (), NumberRange ()] )
#     stock = IntegerField ( "stock", validators=[DataRequired (), NumberRange ( min=0 )] )
#
#
# class FileForm ( FlaskForm ):
#     csv = FileField ( "csv", validators=[FileAllowed ( csv_set, 'Incorrect file format' ), FileRequired ()] )
#
#
# class SearchForm ( FlaskForm ):
#     bookID = StringField ( "bookID", validators=[Optional ()] )
#     category = StringField ( "category", validators=[Optional ()] )
#     book_name = StringField ( "book_name", validators=[Optional ()] )
#     press = StringField ( "press", validators=[Optional ()] )
#     year_from = IntegerField ( "year_from", validators=[Optional ()] )
#     year_to = IntegerField ( "year_to", validators=[Optional ()] )
#     author = StringField ( "author", validators=[Optional ()] )
#     price_from = FloatField ( "price_from", validators=[Optional ()] )
#     price_to = FloatField ( "price_to", validators=[Optional ()] )
#     stock = IntegerField ( "stock", validators=[Optional ()] )
#     order_by = SelectField ( "order_by", validators=[Optional ()],
#                              choices=[("book_name", 'book_name'), ("category", "category"), ("bookID", "bookID"),
#                                       ("press", "press"), ("year", "year"), ("author", "author"), ("price", "price"),
#                                       ("stock", "stock"), ("amount", "amount")] )
#     # order_by = StringField ( "order_by" )
#
#
# class BorrowForm ( FlaskForm ):
#     cardID = IntegerField ( "cardID", validators=[DataRequired ()] )
#     bookID = StringField ( "bookID", validators=[Optional ()] )
#     days = IntegerField ( "days", validators=[Optional (), NumberRange ( 1, 10000 )] )
#
#
# class ReturnForm ( FlaskForm ):
#     cardID = IntegerField ( "cardID", validators=[DataRequired ()] )
#     bookID = StringField ( "bookID", validators=[Optional ()] )
#
#
# class NewCardForm ( FlaskForm ):
#     cardID = IntegerField ( "cardID", validators=[DataRequired ()] )
#     name = StringField ( "name", validators=[DataRequired ()] )
#     department = StringField ( "department", validators=[DataRequired ()] )
#     category = SelectField ( "category",
#                              choices=[("student", "student"), ("teacher", "teacher"), ("else", "else")] )
#
#
# class DeleteCardForm ( FlaskForm ):
#     cardID = IntegerField ( "cardID", validators=[DataRequired ()] )
#
#
# order_object = {"book_name": Book.book_name, "category": Book.category, "bookID": Book.bookID,
#                 "press": Book.press, "year": Book.year, "author": Book.author, "price": Book.price,
#                 "stock": Book.stock, "amount": Book.amount}
