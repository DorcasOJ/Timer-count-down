from app.app import *
from app.command import create_tables

app.cli.add_command(create_tables)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)