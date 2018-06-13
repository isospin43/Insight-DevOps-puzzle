import datetime
import os

from flask import Flask, render_template, redirect, url_for
from forms import ItemForm
from models import Items
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


#form = ItemForm()
#item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())

@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

# directory to data /var/lib/postgresql/data

@app.route("/success")
def success():
    #self.item=item
    results = []
 
    qry = db_session.query(Items.name,Items.quantity,Items.description,Items.date_added)
    results = qry.all()

    return str(results)
    #return render_template('results.html', table=list(results))
    #return tuple(models.Items.name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
