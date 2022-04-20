from flask_wtf import FlaskForm

# name = db.Column(db.String(64), unique=False, index=True, nullable=False)
# price = db.Column(db.Float, nullable=False)
# description = db.Column(db.Text, default='Commodity has no description.')
# commodity_img_src = db.Column(db.String(255))
# shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
# orders = db.relationship('Order', backref='commodity', lazy='dynamic')
# comments = db.relationship('Comment', backref='commodity', lazy='dynamic')
from wtforms import StringField, TextAreaField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, Regexp


class CommodityForm(FlaskForm):
    name = StringField('商品名', validators=[DataRequired(), Length(1, 64)])
    about_commodity = TextAreaField('商品介绍')
    price = FloatField('价格', validators=[DataRequired()])
    img_src = StringField('图片地址')
    submit = SubmitField('添加商品')


class editCommodityForm(FlaskForm):
    name = StringField('商品名', validators=[DataRequired(), Length(1, 64)])
    about_commodity = TextAreaField('商品介绍')
    price = FloatField('价格', validators=[DataRequired()])
    img_src = StringField('图片地址')
    submit = SubmitField('修改商品')
