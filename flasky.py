import click
from flask_migrate import Migrate
from app import db, create_app
from app.models import User, Role, Shop, Order, Commodity

app = create_app('development')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Commodity=Commodity, Shop=Shop, Order=Order)


# 自定义命令来测试model类方法是否正确
@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
