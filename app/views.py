# -*- coding:utf-8 -*-
__author__ = u'Jiang Wen'
from flask import render_template, flash, request, abort, redirect, url_for, g, jsonify
from app import app, db, lm, CENTER_API_URL, DEBUGGING  # , csv_set
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import LoginForm, ChangePWDForm, ConfineForm, ChangeAuth, ChangeAccount
from flask_bootstrap import Bootstrap
from app.models import Admin, Auth, Buy, Sell, Tran, Stock, test_init
from sqlalchemy.sql import and_
from sqlalchemy import func
import json
import requests

Bootstrap ( app )


@app.before_first_request
def init_view():
    # Uncomment to recreate database every time
    db.drop_all ( bind=None )
    db.create_all ( bind=None )  # Do not recreate mysql database.
    test_init ()
    # Add login guider
    lm.login_view = url_for ( 'login' )
    # lm.login_message = "Please login"
    # lm.login_message_category = 'info'


@app.before_request
def before_request():
    g.user = current_user


@app.route ( '/' )
@app.route ( '/index.html' )
@login_required
def index():
    # flash ( 'Hello %s, you have logged in.' % current_user.get_id (), 'success' )
    auth_list = None
    user_id = current_user.get_id ()
    auth_list = Auth.query.filter_by ( admin_id=user_id )
    return render_template ( "index.html", username=current_user.get_id (), auth_list=auth_list )


@app.route ( '/change_password', methods=['GET', 'POST'] )
def change_password():
    # if request.method == 'POST':
    #     import pdb;
    #     pdb.set_trace ()
    username = str ( current_user.get_id () )
    flash ( username, 'info' )
    logout_user ()
    error = None
    form = ChangePWDForm ()
    if form.validate_on_submit ():
        try:
            user = Admin.query.filter_by ( id=form.username.data ).first ()
            if user is None:
                error = 'Invalid username'
            elif not user.check_password_hash ( form.old_password.data ):
                error = 'Invalid password'
            else:
                user.password = form.new_password.data
                db.session.commit ()
                login_user ( user=user, remember=False )
                flash ( 'Change password success', category='success' )
                return redirect ( url_for ( 'index' ) )
        except Exception as e:
            # flash ( 'login fail', 'primary' )
            flash ( e, 'danger' )

    elif request.method == 'POST':
        flash ( 'Invalid input', 'warning' )
    if error is not None:
        flash ( error, category='danger' )
    return render_template ( "change_password.html", username=username, form=form )


@app.route ( '/query' )
@login_required
def query():
    price = 'N/A'
    num = 'N/A'
    buy = []
    sell = []
    user_id = current_user.get_id ()
    stock_name = request.args.get ( 'stock_id', None )
    if Auth.query.filter ( and_ ( Auth.admin_id == user_id, Auth.stock_id == stock_name ) ).first ():
        tran = Tran.query.filter_by ( stock_name=stock_name ).order_by ( Tran.time.desc () ).first ()
        if tran:
            price = tran.trans_price
            num = db.session.query ( func.sum ( Tran.trans_stock_num ) ).filter_by ( stock_name=stock_name ).scalar ()
        else:
            if stock_name:
                flash ( '未找到该股票', 'warning' )
        buy = Buy.query.filter_by ( stock_name=stock_name ).order_by ( Buy.stock_price.desc () ).all ()
        sell = Sell.query.filter_by ( stock_name=stock_name ).order_by ( Sell.stock_price.asc () ).all ()
    elif stock_name:
        flash ( '您没有查询该股票的权限', 'danger' )
    return render_template ( "query.html", buy=buy, sell=sell, price=price, num=num )


@app.route ( '/confine', methods=['GET', 'POST'] )
@login_required
def confine():
    form = ConfineForm ()
    auth_list = None
    user_id = current_user.get_id ()
    auth_list = Auth.query.filter_by ( admin_id=user_id )
    stock_list = []
    # import pdb; pdb.set_trace()
    for auth in auth_list:
        stock_list.append ( Stock.query.filter_by ( stock_name=auth.stock_id ).first () )
    if request.method == 'POST' and form.validate_on_submit ():
        stock_name = form.stock_name.data
        if Auth.query.filter ( and_ ( Auth.admin_id == user_id, Auth.stock_id == stock_name ) ).first ():
            stock = Stock.query.filter_by ( stock_name=stock_name ).first ()
            if stock:
                stock.down_confine = form.down_confine.data
                stock.up_confine = form.up_confine.data
                if stock.down_confine < 0 or stock.up_confine < 0 or stock.down_confine > 100:
                    flash ( '限制不合规', 'warning' )
                    return render_template ( "confine.html", username=current_user.get_id (), stock_list=stock_list,
                                             form=form )
                try:
                    flash ( '请求已发送', 'success' )
                    api_data = request.values.to_dict ()
                    api_data['action'] = 'confine_change'
                    print ( json.dumps ( api_data ) )
                    r = requests.post ( CENTER_API_URL, json=api_data )
                    ans = r.json ()
                    if ans.get ( 'result', None ):
                        flash ( '变更成功', 'success' )
                        db.session.commit ()
                    else:
                        flash ( '变更失败', 'danger' )
                        db.session.rollback ()
                    if DEBUGGING:
                        flash ( r.json (), 'info' )
                except Exception as e:
                    if DEBUGGING:
                        flash ( e, 'danger' )
                        raise e
                    db.session.rollback ()
                    flash ( '中央交易系统端异常', 'danger' )
            else:
                flash ( '未找到该股票', 'warning' )
            if DEBUGGING:
                flash ( form.data, 'info' )
            pass
        else:
            flash ( "您没有该权限", 'danger' )
    return render_template ( "confine.html", username=current_user.get_id (), stock_list=stock_list, form=form )


@app.route ( '/trading', methods=['GET', 'POST'] )
@login_required
def trading():
    stock_name = request.values.get ( 'stock_id', None )
    action = request.values.get ( 'action', None )
    user_id = current_user.get_id ()
    auth_list = Auth.query.filter_by ( admin_id=user_id )
    stock_list = []
    if stock_name:
        # import pdb; pdb.set_trace()
        if Auth.query.filter ( and_ ( Auth.admin_id == user_id, Auth.stock_id == stock_name ) ).first ():
            stock = Stock.query.filter_by ( stock_name=stock_name ).first ()
            if stock:
                if action == 'start':
                    if stock.is_trading:
                        flash ( '交易本身就已开启', 'warning' )
                    else:
                        stock.is_trading = True
                        flash ( '开启请求已发送', 'success' )
                        try:
                            api_data = request.values.to_dict ()
                            r = requests.post ( CENTER_API_URL, json=api_data )
                            print ( json.dumps ( api_data ) )
                            ans = r.json ()
                            if ans.get ( 'result', None ):
                                flash ( '开启交易成功' )
                                db.session.commit ()
                            else:
                                db.session.rollback ()
                                flash ( '开启交易失败' )
                            if DEBUGGING:
                                flash ( r.json (), 'info' )
                        except Exception as e:
                            if DEBUGGING:
                                flash ( e, 'danger' )
                                raise e
                            db.session.rollback ()
                            flash ( '中央交易系统端异常', 'danger' )

                elif action == 'stop':
                    if stock.is_trading:
                        stock.is_trading = False
                        flash ( '停止请求已发送', 'success' )
                        try:
                            api_data = request.values.to_dict ()
                            r = requests.post ( CENTER_API_URL, json=api_data )
                            print ( json.dumps ( api_data ) )
                            ans = r.json ()
                            if ans.get ( 'result', None ):
                                db.session.commit ()
                                flash ( '停止交易成功', 'success' )
                            else:
                                db.session.rollback ()
                                flash ( '停止交易失败', 'danger' )
                            if DEBUGGING:
                                flash ( r.json (), 'info' )
                        except Exception as e:
                            if DEBUGGING:
                                flash ( e, 'danger' )
                                raise e
                            db.session.rollback ()
                            flash ( '中央交易系统端异常', 'danger' )
                    else:
                        flash ( '交易本身就已关闭', 'success' )
                else:
                    flash ( '仅支持开始/停止交易', 'info' )
            else:
                flash ( '未找到该股票', 'danger' )

        else:
            flash ( "您没有该权限", 'danger' )
    for auth in auth_list:
        stock_list.append ( Stock.query.filter_by ( stock_name=auth.stock_id ).first () )
    return render_template ( "trading.html", username=current_user.get_id (), stock_list=stock_list )


@app.route ( '/logout' )
@login_required
def logout():
    logout_user ()  # 登出用户
    flash ( "Logout successful", category='success' )
    return redirect ( url_for ( 'index' ) )


@lm.user_loader
def load_user(id):
    return Admin.query.get ( id )


@app.route ( '/login', methods=['GET', 'POST'] )
def login():
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
                return redirect ( url_for ( 'index' ) )
        except Exception as e:
            # flash ( 'login fail', 'primary' )
            flash ( e, 'danger' )

    elif request.method == 'POST':
        flash ( 'Invalid input', 'warning' )
    if error is not None:
        flash ( error, category='danger' )
    return render_template ( 'login.html', form=form, error=error )


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


@app.route ( '/tutorial' )
@login_required
def tutorial():
    user_id = current_user.get_id ()
    auth_list = Auth.query.filter_by ( admin_id=user_id )
    return render_template ( "tutorial.html", username=current_user.get_id (), auth_list=auth_list )


@app.route ( '/auth', methods=['GET', 'POST'] )
@login_required
def auth_set():
    form = ChangeAuth ()
    if not current_user.is_root:
        flash ( '您没有超级用户权限', 'danger' )
        return redirect ( '/index.html' )
    # import pdb; pdb.set_trace()
    if form.validate_on_submit ():
        stock_name = form.stock_name.data
        admin_id = form.admin_id.data
        if form.action.data == 'add':
            if Auth.query.filter ( and_ ( Auth.admin_id == admin_id, Auth.stock_id == stock_name ) ).first ():
                flash ( '用户本身就有该权限', 'warning' )
            else:
                db.session.add ( Auth ( admin_id, stock_name ) )
                db.session.commit ()
        elif form.action.data == 'delete':
            auth = Auth.query.filter ( and_ ( Auth.admin_id == admin_id, Auth.stock_id == stock_name ) ).first ()
            if auth:
                db.session.delete ( auth )
                db.session.commit ()
            else:
                flash ( '用户本身就没有该权限', 'warning' )
    user_id = current_user.get_id ()
    auth_list = Auth.query.all ()
    return render_template ( "auth.html", username=user_id, auth_list=auth_list, form=form )


@app.route ( '/account', methods=['GET', 'POST'] )
@login_required
def account():
    form = ChangeAccount ()
    if not current_user.is_root:
        flash ( '您没有超级用户权限', 'danger' )
        return redirect ( '/index.html' )
    if form.validate_on_submit ():
        if form.action.data == 'add':
            if Admin.query.filter_by ( id=form.admin_id.data ).first ():
                flash ( '添加失败，管理员已存在', 'warning' )
            elif not form.password.data:
                flash ( '请设置密码', 'warning' )
            else:
                admin = Admin ( form.admin_id.data, form.password.data, form.is_root.data )
                db.session.add ( admin )
                db.session.commit ()
                flash ( '添加成功', 'success' )
        elif form.action.data == 'update':
            admin = Admin.query.filter_by ( id=form.admin_id.data ).first ()
            if admin:
                if form.password.data:
                    admin.password = form.password.data
                if form.is_root.data:
                    admin.is_root = form.is_root.data
                db.session.commit ()
                flash ( '修改成功', 'success' )
            else:
                flash ( '管理员不存在', 'warning' )
        elif form.action.data == 'delete':
            admin = Admin.query.filter_by ( id=form.admin_id.data ).first ()
            if admin:
                db.session.delete ( admin )
                db.session.commit ()
                flash ( '删除成功', 'success' )
            else:
                flash ( '管理员不存在', 'warning' )
    user_id = current_user.get_id ()
    auth_list = Admin.query.all ()
    return render_template ( "account.html", username=user_id, auth_list=auth_list, form=form )


@app.route ( '/api', methods=['GET', 'POST'] )
def api():
    api_return = {'result': False}
    # return json.dumps ( api_return )
    return '{"result": true}'
