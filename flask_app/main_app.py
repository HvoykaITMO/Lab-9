import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired
import datetime


app = Flask('Cities')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cities.db"
app.config['SECRET_KEY'] = "MegaSecretKeyYouHaveEverSeen228"
db = SQLAlchemy(app)


class Cities(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    city = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    visit_date = sqlalchemy.Column(db.DATE, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String(300), nullable=True, default='Это прекрасный город,'
                                                                                   ' у вас отличный вкус!')

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class MainForm(FlaskForm):
    city_name = StringField('Город', validators=[DataRequired()])
    visit_date = DateField('Дата посещения', validators=[DataRequired()])
    city_description = StringField('Описание')
    submit = SubmitField('Добавить')


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def main():
    form = MainForm()
    all_visits = Cities.query.all()
    return render_template('form.html', title='Гид по посещённым городам',
                           form=form, items=all_visits)


@app.route('/', methods=['POST'])
def add_user():
    city = request.form['city_name']
    date = datetime.date(*[int(el) for el in request.form['visit_date'].split('-')])
    city_description = request.form['city_description'] if request.form['city_description'].strip() != '' else None
    new_visit = Cities(city=city, visit_date=date, description=city_description)
    db.session.add(new_visit)
    db.session.commit()
    return redirect('/')


@app.route('/<int:city_id>', methods=['POST'])
def delete_user(city_id):
    city = Cities.query.get(city_id)
    if not city:
        return jsonify({"message": "City not found"}), 404
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


@app.route('/delete_all', methods=['POST'])
def delete_all():
    Cities.query.delete()
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(port=8080)
