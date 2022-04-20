from datetime import datetime
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Permission:
    """
    该类包含有权限控制参数

    Attributes
        ADDCART:添加购物车
        BUY:购买
        COMMENT:评论
        MERCHANT:商家
        MODERATE:协管（即管理用户发言）
        ADMIN:管理员权限（拥有整个系统的权限）
    """
    ADDCART = 1
    BUY = 2
    COMMENT = 4
    MERCHANT = 8
    MODERATE = 16
    ADMIN = 32


class Role(db.Model):
    """
    角色类
        有四类：
        1.匿名用户：只可浏览商品
        2.用户：可以购买商品，发表评论
        3.商家：可以管理商店，管理商品等
        4.协管员：增加管理其他用户所发表评论的权限
        5.管理员：具有所有权限，包括修改其他用户所属角色的权限
    """

    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)  # 表明是否为默认账户，即User
    permission = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role name:%r>' % self.name

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permission is None:
            self.permission = 0

    # 权限控制
    def has_permission(self, permission):
        """
        检查用户是否有permission权限
        :param permission: 需要被检查的权限
        :return: True Or False
        """
        return self.permission & permission == permission

    def add_permission(self, permission):
        """
        add permission
        :param permission:the permission going to be added
        :return: null
        """
        if not self.has_permission(permission):
            self.permission += permission

    def remove_permission(self, permission):
        """
        remove the permission
        :param permission: permission
        :return: null
        """
        if self.has_permission(permission):
            self.permission -= permission

    def reset_permission(self):
        """
        reset permission
        :return: null
        """
        self.permission = 0

    @staticmethod
    def insert_Roles():
        roles = {
            'User': [Permission.ADDCART, Permission.BUY, Permission.COMMENT],
            'Merchant': [Permission.ADDCART, Permission.COMMENT, Permission.MERCHANT],
            'Moderator': [Permission.ADDCART, Permission.COMMENT, Permission.MODERATE],
            'Administrator': [Permission.ADDCART, Permission.BUY, Permission.COMMENT, Permission.MODERATE,
                              Permission.MERCHANT, Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class Order(db.Model):
    """
    orders:关联表，用于记录用户购买商品的订单
    """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodities.id'))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # 用户id
    username = db.Column(db.String(64), unique=True, index=True)  # 用户名
    email = db.Column(db.String(64), unique=True, index=True)  # 电子邮件
    about_me = db.Column(db.Text())
    address = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())
    password_hash = db.Column(db.String(128))  # 密码hash值
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 角色id
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User name:%r>' % self.username

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permission):
        return self.role is not None and self.role.has_permission(permission)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class Commodity(db.Model):
    """
    商品类:
        id:逻辑主键
        name:名称
        price:价格
        salesVolumes:销量
        description:商品介绍
        img_src:商品图片链接
    """
    __tablename__ = 'commodities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, index=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    salesVolumes = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, default='Commodity has no description.')
    commodity_img_src = db.Column(db.String(255))
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
    orders = db.relationship('Order', backref='commodity', lazy='dynamic')
    comments = db.relationship('Comment', backref='commodity', lazy='dynamic')

    def __repr__(self):
        return '<Commodity %r>' % self.name


class Shop(db.Model):
    """
    商店：。。。
    Attribute:
        id: 逻辑主键
        name: 商店名称（不允许重名）
        intro: 简介
        shop_img_src: 商店头像图片链接
    """
    __tablename__ = 'shops'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    intro = db.Column(db.Text, default='Shop has no intro.')
    shop_img_src = db.Column(db.String(255))
    commodities = db.relationship('Commodity', backref='shop', lazy='dynamic')

    def __repr__(self):
        return '<Shop %r>' % self.name


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    disabled = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodities.id'))
