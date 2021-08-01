from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from casting_agency.app import app
from casting_agency.models import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()