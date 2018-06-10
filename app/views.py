# -*- coding:utf-8 -*-
__author__ = u'Jiang Wen'
from flask import render_template, flash, request, abort, redirect, url_for, g
from app import app, db, lm #, csv_set
from flask_login import login_user, login_required, logout_user, current_user
# from app.forms import LoginForm, CheckInForm, FileForm, SearchForm, order_object, NewCardForm, DeleteCardForm, \
#     BorrowForm, ReturnForm
from flask_bootstrap import Bootstrap
from app.models import Admin #, Book, Card, Borrow
from sqlalchemy.sql import and_
import csv

Bootstrap ( app )


@app.before_first_request
def init_view():
    # Uncomment to recreate database every time
    db.drop_all ()
    db.create_all ()
    admins = [Admin ( 0, 'a', 'a.name', 'admin@example.com' ), Admin ( 1, 'b', 'b.name', 'bdmin@example.com' )]
    for admin in admins:
        if Admin.query.get ( admin.id ) is None:
            db.session.add ( admin )
    db.session.commit ()
    # Add login guider
    lm.login_view = url_for ( 'login' )
    lm.login_message = "Please login"
    lm.login_message_category = 'info'


@app.before_request
def before_request():
    g.user = current_user


@app.route ( '/' )
@app.route ( '/index.html' )
def index():
    return render_template ( "dashboard.html" )

#
# @app.route ( '/check_in', methods=['GET', 'POST'] )
# @login_required
# def check_in():
#     single_form = CheckInForm ()
#     group_form = FileForm ()
#     if request.method == 'POST' and request.form['kinds'] == 'single':
#         if single_form.validate_on_submit ():
#             try:
#                 cur_book = Book ( bookID=single_form.bookID.data, category=single_form.category.data,
#                                   book_name=single_form.book_name.data,
#                                   press=single_form.press.data, year=single_form.year.data,
#                                   author=single_form.author.data,
#                                   price=single_form.price.data, amount=single_form.stock.data,
#                                   stock=single_form.stock.data )
#                 db_book = Book.query.filter_by ( bookID=cur_book.bookID ).first ()
#                 if db_book:
#                     db_book.stock += cur_book.stock
#                     db_book.amount += cur_book.stock
#                 else:
#                     db.session.add ( cur_book )
#                 db.session.commit ()
#                 flash ( 'Check in book success', 'success' )
#             except Exception as e:
#                 flash ( 'Check in fail', 'warning' )
#                 # flash ( e, 'danger' )
#         elif request.method == 'POST':
#             flash ( 'Invalid input', 'warning' )
#     elif request.method == 'POST' and request.form['kinds'] == 'group':
#         if group_form.validate_on_submit ():
#             try:
#                 csv_name = csv_set.save ( request.files['csv'] )
#                 flash ( 'Upload file success', 'info' )
#                 books = []
#                 with open ( app.config['UPLOADED_CSV_DEST'] + '/' + csv_name ) as csv_file:
#                     reader = csv.reader ( csv_file )
#                     for line in reader:
#                         assert len ( line ) == Book.length, "Not match col size"
#                         books.append (
#                             Book ( bookID=line[0].strip (), category=line[1].strip (), book_name=line[2].strip (),
#                                    press=line[3].strip (), year=line[4].strip (),
#                                    author=line[5].strip (), price=line[6].strip (), amount=line[7].strip (),
#                                    stock=line[7].strip () ) )
#                     for cur_book in books:
#                         db_book = Book.query.filter_by ( bookID=cur_book.bookID ).first ()
#                         if db_book:
#                             db_book.stock += cur_book.stock
#                             db_book.amount += cur_book.stock
#                         else:
#                             db.session.add ( cur_book )
#                     db.session.commit ()
#             except Exception as e:
#                 flash ( 'Batch check in fail', 'warning' )
#                 # flash ( e, 'danger' )
#                 # raise e
#             else:
#                 flash ( 'Success load into database', 'success' )
#         elif request.method == 'POST':
#             flash ( 'Invalid file', 'warning' )
#
#     return render_template ( "check_in.html", single_form=single_form, group_form=group_form )
#
#
# @app.route ( '/login', methods=['GET', 'POST'] )
# def login():
#     error = None
#     if g.user is not None and g.user.is_authenticated:
#         return redirect ( url_for ( 'index' ) )
#     form = LoginForm ()
#     if form.validate_on_submit ():
#         try:
#             user = Admin.query.filter_by ( id=form.username.data ).first ()
#             if user is None:
#                 error = 'Invalid username'
#             elif not user.check_password_hash ( form.password.data ):
#                 error = 'Invalid password'
#             else:
#                 login_user ( user=user, remember=form.remember.data )
#                 flash ( 'You were logged in', category='success' )
#                 return redirect ( url_for ( 'index' ) )
#         except Exception as e:
#             flash ( 'login fail', 'primary' )
#             # flash ( e, 'danger' )
#
#     elif request.method == 'POST':
#         flash ( 'Invalid input', 'warning' )
#     if error is not None:
#         flash ( error, category='danger' )
#     return render_template ( 'login.html', form=form, error=error )
#
#
# @app.route ( '/search', methods=['GET', 'POST'] )
# def search():
#     form = SearchForm ()
#     result = []
#     pagination = None
#     query_string = request.query_string
#     try:
#         # if request.form.to_dict () and form.validate_on_submit ():
#         # flash ( request.query_string, 'info' )
#         if request.query_string:
#             # if request.method == 'GET' and form.validate ():
#             # flash ( 'get it', 'info' )
#             # raise ArithmeticError
#             rules = []
#             if request.args.to_dict ().get ( 'bookID', '' ):
#                 rules.append ( Book.bookID == str ( request.args.to_dict ().get ( 'bookID', '' ) ) )
#             if request.args.to_dict ().get ( 'category', '' ):
#                 rules.append ( Book.category == str ( request.args.to_dict ().get ( 'category', '' ) ) )
#             if request.args.to_dict ().get ( 'author', '' ):
#                 rules.append ( Book.author == str ( request.args.to_dict ().get ( 'author', '' ) ) )
#             if request.args.to_dict ().get ( 'price_from', '' ):
#                 rules.append ( Book.price >= float ( request.args.to_dict ().get ( 'price_from', '' ) ) )
#             if request.args.to_dict ().get ( 'price_to', '' ):
#                 rules.append ( Book.price <= float ( request.args.to_dict ().get ( 'price_to', '' ) ) )
#             if request.args.to_dict ().get ( 'year_from', '' ):
#                 rules.append ( Book.year >= int ( request.args.to_dict ().get ( 'year_from', '' ) ) )
#             if request.args.to_dict ().get ( 'year_to', '' ):
#                 rules.append ( Book.year <= int ( request.args.to_dict ().get ( 'year_to', '' ) ) )
#             if request.args.to_dict ().get ( 'book_name', '' ):
#                 rules.append ( Book.book_name == str ( request.args.to_dict ().get ( 'book_name', '' ) ) )
#             if request.args.to_dict ().get ( 'press', '' ):
#                 rules.append ( Book.press == str ( request.args.to_dict ().get ( 'press', '' ) ) )
#             page = request.args.get ( 'page', 1, type=int )
#             # result = Book.query.filter ( and_ ( *rules ) ).order_by ( order_object[form.order_by.data] ).all ()
#             pagination = Book.query.filter ( and_ ( *rules ) ).order_by (
#                 order_object[request.args.to_dict ().get ( 'order_by', 'book_name' )] ).paginate (
#                 page, per_page=10,
#                 error_out=False
#             )
#             # pagination = Posts.query.order_by ( Posts.timestamp.desc () )
#             result = pagination.items
#             # raise ArithmeticError
#         elif request.query_string:
#             flash ( "Invalid search", 'warning' )
#     except Exception as e:
#         flash ( 'Search error', 'primary' )
#         # flash ( e, 'danger' )
#         # raise e
#     if request.query_string and str ( request.query_string ).split ( "\'" )[1]:
#         # flash ( str ( request.query_string ).split ( '\'' ), 'info' )
#         return render_template ( 'search.html', form=form, result=result, pagination=pagination, cur_url='search',
#                                  frag='&' + str ( request.query_string ).split ( "\'" )[1] )
#     else:
#         return render_template ( 'search.html', form=form, result=result, pagination=pagination, cur_url='search',
#                                  frag='' )
#
#
# @app.route ( '/borrow', methods=['GET', 'POST'] )
# @login_required
# def borrow():
#     form = BorrowForm ()
#     last_id = None
#     results = []
#     try:
#         if request.method == 'POST' and form.validate_on_submit ():
#             card_id = form.cardID.data
#             if Card.query.filter_by ( cardID=card_id ).first ():
#                 last_id = card_id
#                 if form.bookID.data:
#                     cur_book = Book.query.filter_by ( bookID=form.bookID.data ).first ()
#                     if cur_book:
#                         if cur_book.stock > 0:
#                             cur_book.stock -= 1
#                             cur_borrow = Borrow ( cur_book.bookID, card_id, form.days.data )
#                             db.session.add ( cur_borrow )
#                             db.session.commit ()
#                             flash ( "Borrow success", 'success' )
#                         else:
#                             newest_borrow = Borrow.query.filter_by ( book_id=cur_book.bookID ).order_by (
#                                 Borrow.return_date ).first ()
#                             flash ( 'No book in stock', category='info' )
#                             if newest_borrow:
#                                 flash (
#                                     'The book will be returned in ' + newest_borrow.return_date.strftime ( "%Y-%m-%d" ),
#                                     category='info' )
#                     else:
#                         flash ( 'Book ID not exist', category='info' )
#                 records = Borrow.query.filter_by ( card_id=card_id ).all ()
#                 for record in records:
#                     results.append ( Book.query.filter_by ( bookID=record.book_id ).first () )
#             else:
#                 flash ( 'Card not exist', 'warning' )
#         elif request.method == 'POST':
#             flash ( "Invalid input", 'warning' )
#     except Exception as e:
#         flash ( 'Borrow fail', 'warning' )
#         # flash ( e, 'danger' )
#         # raise e
#     return render_template ( 'borrow.html', form=form, last_id=last_id, result=results )
#
#
# @app.route ( '/return_book', methods=['GET', 'POST'] )
# @login_required
# def return_book():
#     form = ReturnForm ()
#     last_id = None
#     results = []
#     try:
#         if request.method == 'POST' and form.validate_on_submit ():
#             card_id = form.cardID.data
#             if Card.query.filter_by ( cardID=card_id ).first ():
#                 last_id = card_id
#                 if form.bookID.data:
#                     cur_borrow = Borrow.query.filter (
#                         and_ ( Borrow.book_id == form.bookID.data, Borrow.card_id == card_id ) ).first ()
#                     if cur_borrow:
#                         cur_book = Book.query.filter_by ( bookID=cur_borrow.book_id ).first ()
#                         cur_book.stock += 1
#                         db.session.delete ( cur_borrow )
#                         db.session.commit ()
#                         flash ( 'Return book success', 'success' )
#                     else:
#                         flash ( 'Book have not been borrowed', category='info' )
#                 records = Borrow.query.filter_by ( card_id=card_id ).all ()
#                 for record in records:
#                     results.append ( Book.query.filter_by ( bookID=record.book_id ).first () )
#             else:
#                 flash ( 'Card not exist', 'warning' )
#         elif request.method == 'POST':
#             flash ( "Invalid input", 'warning' )
#     except Exception as e:
#         # flash ( e, 'danger' )
#         # raise e
#         flash ( 'Return book error', 'warning' )
#     return render_template ( 'return_book.html', form=form, last_id=last_id, result=results )
#
#
# @app.route ( '/card', methods=['GET', 'POST'] )
# @login_required
# def card():
#     new_card = NewCardForm ()
#     delete_card = DeleteCardForm ()
#     try:
#         if request.method == 'POST' and request.form['kinds'] == 'new':
#             if new_card.validate_on_submit ():
#                 cur_card = Card ( cardID=new_card.cardID.data, name=new_card.name.data,
#                                   departement=new_card.department.data, category=new_card.category.data )
#                 if Card.query.filter_by ( cardID=cur_card.cardID ).first ():
#                     flash ( 'Duplicate card id', 'danger' )
#                 else:
#                     db.session.add ( cur_card )
#                     db.session.commit ()
#                     flash ( 'Add card success', 'success' )
#             elif request.method == 'POST':
#                 flash ( 'Invalid input', 'warning' )
#         elif request.method == 'POST' and request.form['kinds'] == 'delete':
#             if delete_card.validate_on_submit ():
#                 cur_cardID = delete_card.cardID.data
#                 cur_card = Card.query.filter_by ( cardID=cur_cardID ).first ()
#                 if cur_card:
#                     record = Borrow.query.filter_by ( card_id=cur_card.cardID ).first ()
#                     if record:
#                         flash ( 'The book borrowed by this card has not been returned', 'danger' )
#                     else:
#                         db.session.delete ( cur_card )
#                         db.session.commit ()
#                         flash ( 'Delete card success', 'success' )
#                 else:
#                     flash ( 'Card not exist', 'danger' )
#             elif request.method == 'POST':
#                 flash ( 'Invalid input', 'warning' )
#         cards = Card.query.all ()
#     except Exception as e:
#         # flash ( e, 'danger' )
#         raise e
#         flash ( 'Card operation fail', 'warning' )
#     return render_template ( 'card.html', new_card=new_card, delete_card=delete_card, cards=cards )
#
#
# @app.route ( '/about' )
# def about():
#     return render_template ( 'about.html' )
#
#
@app.route ( '/logout/' )
@login_required
def logout():
    logout_user ()  # 登出用户
    flash ( "Logout successful", category='success' )
    return redirect ( url_for ( 'index' ) )


@lm.user_loader
def load_user(id):
    return Admin.query.get ( int ( id ) )
@app.route ( '/login', methods=['GET', 'POST'] )
def login():
    """
    error = None
    if g.user is not None and g.user.is_authenticated:
        return redirect ( url_for ( 'index' ) )
    form = LoginForm ()
    if form.validate_on_submit ():
        try:
            user = Admin.query.filter_by ( id=form.username.data ).first ()
            if user is None:
                error = 'Invalid username'
            elif not user.check_password_hash ( form.password.data ):
                error = 'Invalid password'
            else:
                login_user ( user=user, remember=form.remember.data )
                flash ( 'You were logged in', category='success' )
                return redirect ( url_for ( 'index' ) )
        except Exception as e:
            flash ( 'login fail', 'primary' )
            # flash ( e, 'danger' )

    elif request.method == 'POST':
        flash ( 'Invalid input', 'warning' )
    if error is not None:
        flash ( error, category='danger' )
    """
    return render_template ( 'login.html', form=form, error=error )
