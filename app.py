from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auction.db"
db = SQLAlchemy(app)

class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"<Buyer {self.name}>"
    
class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Club {self.name}>"

class Exhibitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"), nullable=False)

    club = db.relationship("Club", backref=db.backref("exhibitors", lazy=True))

    def __repr__(self):
        return f"<Exhibitor {self.name}>"
    
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ear_tag_number = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    picture = db.Column(db.LargeBinary, nullable=True)
    packer = db.Column(db.String(80), nullable=True)
    kill_plant = db.Column(db.String(80), nullable=True)
    exhibitor_id = db.Column(db.Integer, db.ForeignKey("exhibitor.id"), nullable=False)
    

    exhibitor = db.relationship("Exhibitor", backref=db.backref("animals", lazy=True))

    def __repr__(self):
        return f"<Animal {self.name}>"
    
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyer.id"), nullable=False)
    exhibitor_id = db.Column(db.Integer, db.ForeignKey("exhibitor.id"), nullable=False)
    sale_price = db.Column(db.Float, nullable=False)

    animal = db.relationship("Animal", backref=db.backref("sales", lazy=True))
    buyer = db.relationship("Buyer", backref=db.backref("purchases", lazy=True))
    exhibitor = db.relationship("Exhibitor", backref=db.backref("sales", lazy=True))

    def __repr__(self):
        return f"<Sale {self.animal.name} to {self.buyer.name} for ${self.sale_price}/lb>"
    
class Addon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyer.id"), nullable=False)
    exhibitor_id = db.Column(db.Integer, db.ForeignKey("exhibitor.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)

    buyer = db.relationship("Buyer", backref=db.backref("addons", lazy=True))
    exhibitor = db.relationship("Exhibitor", backref=db.backref("addons", lazy=True))

    def __repr__(self):
        return f"<Addon {self.name}>"


@app.route("/", methods=["GET", "POST"])
def main():    
    return render_template("index.html")

@app.route("/buyerList", methods=["GET", "POST"])
def buyer_list():
    if request.method == "POST":
        name = request.form["Name"]
        phone = request.form["Phone"]
        address = request.form["Address"]
        buyer = Buyer(name=name, phone=phone, address=address)
        try:
            db.session.add(buyer)
            db.session.commit()
            return redirect("/buyerList")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding buyer: {e}")
            return f"ERROR: {e}"
    else:
        buyers = Buyer.query.order_by(Buyer.name).all()
        return render_template("buyerList.html", buyers=buyers)

@app.route("/clubList", methods=["GET", "POST"])
def club_list():
    if request.method == "POST":
        name = request.form["Name"]
        club = Club(name=name)
        try:
            db.session.add(club)
            db.session.commit()
            return redirect("/clubList")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding club: {e}")
            return f"ERROR: {e}"
    else:
        clubs = Club.query.order_by(Club.name).all()
        return render_template("clubList.html", clubs=clubs)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)