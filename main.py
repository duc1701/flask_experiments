from flask import Flask, render_template, request, flash
from wtforms import Form, BooleanField, TextField, IntegerField, Field
from wtforms import widgets

app = Flask(__name__)
app.debug = True

class EmailInput(widgets.Input):
    """
    Renders an input with type "email".
    """
    input_type = 'email'

class EmailField(TextField):
    """
    Represents an ``<input type="email">``.
    """
    widget = EmailInput()

class NumberInput(widgets.Input):
    """
    Renders an input with type "number".
    """
    input_type = 'number'

    def __init__(self, step=None):
        self.step = step

    def __call__(self, field, **kwargs):
        if self.step is not None:
            kwargs.setdefault('step', self.step)
        return super(NumberInput, self).__call__(field, **kwargs)

class NumberField(IntegerField):
    """
    Represents an ``<input type="number">``.
    """
    widget = NumberInput(step='1')

class RangeInput(widgets.Input):
    """
    Renders an input with type "range".
    """
    input_type = 'range'

    def __init__(self, step=None, min=None, max=None):
        self.step = step
        self.min = min
        self.max = max

    def __call__(self, field, **kwargs):
        if self.step is not None:
            kwargs.setdefault('step', self.step)
        if self.min is not None:
            kwargs.setdefault('min', self.min)
        if self.max is not None:
            kwargs.setdefault('max', self.max)
        return super(RangeInput, self).__call__(field, **kwargs)

class IntegerRangeField(IntegerField):
    """
    Represents an ``<input type="range">``.
    """
    widget = RangeInput(step='1', min='0', max='100')
    section_text = None

def make_form():
    class AssessmentForm(Form):
        pass

    # DEBUG
    assessment = [
        ('text', 'First Name'),
        ('text', 'Last Name'),
        ('email', 'Email Address'),
        ('number', 'Years Teaching'),
        ('sum', 'Some question text', ('Apples', 'Oranges')),
    ]

    labels = {}
    for (i, a) in enumerate(assessment):
        field = None
        if a[0] == 'text':
            field = TextField(a[1])
        if a[0] == 'email':
            field = EmailField(a[1])
        if a[0] == 'number':
            field = NumberField(a[1])

        if field != None:
            field_name = 'field_' + str(i)
            setattr(AssessmentForm, field_name, field)

        if a[0] == 'sum':
            for (j, r) in enumerate(a[2]):
                field = IntegerRangeField(r, default='0')
                setattr(AssessmentForm, 'range_' + str(i) + '_' + str(j), field)

                if j ==0:
                    field.section_text = a[1]

    return AssessmentForm(request.form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = make_form()

    if request.method == 'POST' and form.validate():
        flash(form.first_name.data)
        flash(form.last_name.data)
        flash(form.email.data)
        flash(form.years_teaching.data)
        #return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
