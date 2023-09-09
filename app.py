from flask import Flask, render_template, abort, request
from forms import SignupForm, LoginForm, EditPetForm
from flask import session, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

from models import User, Pet, database

team = User(full_name="Pet Rescue Team", email="team@petrescue.co", password="adminpass")
database.session.add(team)

# Create all pets
nelly = Pet(name="Nelly", age="5 weeks",
            bio="I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.")
yuki = Pet(name="Yuki", age="8 months", bio="I am a handsome gentle-cat. I like to dress up in bow ties.")
basker = Pet(name="Basker", age="1 year", bio="I love barking. But, I love my friends more.")
mrfurrkins = Pet(name="Mr. Furrkins", age="5 years", bio="Probably napping.")

# Add all pets to the session
database.session.add(nelly)
database.session.add(yuki)
database.session.add(basker)
database.session.add(mrfurrkins)

# Commit changes in the session
try:
    database.session.commit()
except Exception as e:
    print(f'Error occurred while adding pets: {e}')
    database.session.rollback()
finally:
    database.session.close()


@app.route('/home')
def home():
    """Home page"""
    pets = database.session.query(Pet).all()
    return render_template('home.html', pets=pets)


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/details/<int:pet_id>', methods=['GET', 'POST'])
def details(pet_id):
    """Details page"""

    if request.method == 'POST':
        return redirect(url_for('edit', pet_id=pet_id))

    pets = database.session.query(Pet).all()
    for pet in pets:
        if pet.ID == pet_id:
            return render_template('details.html', pet=pet)
    return abort(404, description="No Pet was Found with the given ID")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Login page"""
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            new_user = User(full_name=form.full_name.data, email=form.email.data, password=form.password.data)

            if database.session.query(User).filter_by(email=new_user.email).first():
                return render_template('signup.html',
                                       message="This email already exists in the system! Please log in instead.",
                                       form=form)

            try:
                database.session.add(new_user)
                database.session.commit()
                message = "You have successfully registered"
            except Exception as e:
                database.session.rollback()
                message = f'Error occurred while registering: {e}'
            finally:
                database.session.close()

            return render_template('signup.html', message=message)
    return render_template('signup.html', form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    message = None
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():

            email = form.email.data
            password = form.password.data

            user = database.session.query(User).filter_by(email=email, password=password).first()
            if user:
                session['user'] = user.ID
                return render_template('login.html', message="You have successfully logged in")

            return render_template('login.html',
                                   message="Wrong Credentials. Please Try Again.",
                                   form=form)
    return render_template("login.html", form=form, message=message)


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/edit/<int:pet_id>', methods=['GET', 'POST'])
def edit(pet_id):
    form = EditPetForm()
    pets = database.session.query(Pet).all()
    for pet in pets:
        if pet.ID == pet_id:

            if request.method == 'POST':

                pet.name = form.name.data
                pet.age = form.age.data
                pet.bio = form.bio.data
                try:
                    database.session.commit()
                except Exception as e:
                    database.session.rollback()
                    print(f'Error occurred while updating pet: {e}')
                return redirect(url_for('details', pet_id=pet.ID))

            return render_template('edit.html', pet=pet, form=form)
    return abort(404, description="No Pet was Found with the given ID")


@app.route('/delete/<int:pet_id>', methods=['GET', 'POST'])
def delete(pet_id):
    pets = database.session.query(Pet).all()
    for pet in pets:
        if pet.ID == pet_id:
            database.session.delete(pet)
            try:
                database.session.commit()
            except Exception as e:
                database.session.rollback()
                print(f'Error occurred while deleting pet: {e}')
            return redirect(url_for('home'))
    return abort(404, description="No Pet was Found with the given ID")


if __name__ == '__main__':
    app.run(debug=True)
