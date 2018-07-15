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
                stock.dirty = True
                if stock.down_confine < 0 or stock.up_confine < 0 or stock.down_confine > 100:
                    flash ( '限制不合规', 'warning' )
                    db.session.rollback ()
                    stock_list = []
                    for auth in auth_list:
                        stock_list.append ( Stock.query.filter_by ( stock_name=auth.stock_id ).first () )
                    return render_template ( "confine.html", username=current_user.get_id (), stock_list=stock_list,
                                             form=form )
                db.session.commit ()
                flash ( '变更成功，将在明天生效', 'success' )
            else:
                flash ( '未找到该股票', 'warning' )
            if DEBUGGING:
                flash ( form.data, 'info' )
            pass
        else:
            flash ( "您没有该权限", 'danger' )
    elif request.method == 'POST':
        flash ( '输入无效', 'warning' )
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
                            r = requests.post ( CENTER_API_URL, json=api_data, timeout=1 )
                            print ( json.dumps ( api_data ) )
                            ans = r.json ()
                            if ans.get ( 'result', None ):
                                flash ( '开启交易成功', 'success' )
                                db.session.commit ()
                            else:
                                db.session.rollback ()
                                flash ( '开启交易失败', 'danger' )
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
                            # print(api_data)
                            r = requests.post ( CENTER_API_URL, json=api_data, timeout=1 )
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
