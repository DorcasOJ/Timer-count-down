import click
from app import app
from flask.cli import with_appcontext
from app import db


@click.command(name = 'create_tables')
#@app.cli.command('create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    print('Database created')

