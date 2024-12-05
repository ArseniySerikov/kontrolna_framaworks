from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


class TicketForm(FlaskForm):
    ticket = StringField('Enter your ticket number', validators=[
        DataRequired(),
        Length(min=6, max=6, message='Ticket number must be 6 digits.'),
        Regexp('^[0-9]*$', message='Ticket number must contain only digits.')
    ])
    submit = SubmitField('Check')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = form.ticket.data
        first_half = sum(map(int, ticket[:3]))
        second_half = sum(map(int, ticket[3:]))
        is_lucky = first_half == second_half
        return render_template('result.html', is_lucky=is_lucky)
    elif form.errors:  # Если форма не валидна
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", 'danger')  # Сообщение через flash
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
