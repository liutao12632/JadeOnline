from flask import render_template, flash, url_for
from flask_login import login_required
from werkzeug.utils import redirect

from . import main
from .forms import CommodityForm, editCommodityForm
from .. import db
from ..decorators import admin_required
from ..models import User, Commodity


@main.route('/', methods=['GET', 'POST'])
def index():
    commodities = Commodity.query.all()
    return render_template('index.html', commodities=commodities)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)


@main.route('/registerCommodity', methods=['GET', 'POST'])
@login_required
@admin_required
def registerCommodity():
    form = CommodityForm()
    if form.validate_on_submit():
        commodity = Commodity(name=form.name.data,
                              price=form.price.data,
                              description=form.about_commodity.data,
                              commodity_img_src=form.img_src.data
                              )
        db.session.add(commodity)
        db.session.commit()
        flash('商品已完成注册!')
        return redirect(url_for('main.commodity', id=commodity.id))
    return render_template('commodity/registerCommodity.html', form=form)


@main.route('/editCommodity/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editCommodity(id):
    commodity = Commodity.query.get_or_404(id)
    form = editCommodityForm()
    if form.validate_on_submit():
        commodity.name = form.name.data
        commodity.price = form.price.data
        commodity.description = form.about_commodity.data
        commodity.commodity_img_src = form.img_src.data
        db.session.add(commodity)
        db.session.commit()
        return redirect(url_for('main.commodity', id=commodity.id))
    form.name.data = commodity.name
    form.price.data = commodity.price
    form.about_commodity.data = commodity.description
    form.img_src.data = commodity.commodity_img_src
    return render_template('commodity/editCommodity.html', form=form)


@main.route('/commodity/<int:id>')
def commodity(id):
    commodity = Commodity.query.get_or_404(id)
    return render_template("commodity/commodity.html", commodity=commodity)
