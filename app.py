from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
#import pandas as pd

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auction.db"
db = SQLAlchemy(app)

class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bidder_number = db.Column(db.Integer, nullable=True)
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
    fName = db.Column(db.String(80), nullable=False)
    lName = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"), nullable=False)

    club = db.relationship("Club", backref=db.backref("exhibitors", lazy=True))

    def __repr__(self):
        return f"<Exhibitor {self.fName}>"
    
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ear_tag_number = db.Column(db.Integer, nullable=False)
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
    sale_price = db.Column(db.Float, nullable=False)

    animal = db.relationship("Animal", backref=db.backref("sales", lazy=True))
    buyer = db.relationship("Buyer", backref=db.backref("purchases", lazy=True))

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
        return f"<Addon {self.price}>"


@app.route("/", methods=["GET", "POST"])
def main():    
    return render_template("index.html")

@app.route("/buyerList", methods=["GET", "POST"])
def buyer_list():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["Phone"]
        address = request.form["Address"]
        bidder_number = request.form["BidderNumber"]
        buyer = Buyer(name=name, phone=phone, address=address, bidder_number=bidder_number)
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

@app.route("/buyerList/edit/<int:buyer_id>", methods=["POST", "GET"])
def edit_buyer(buyer_id):
    buyer = Buyer.query.get_or_404(buyer_id)
    if request.method == "POST":
        buyer.bidder_number = request.form["BidderNumber"]
        buyer.name = request.form["name"]
        buyer.phone = request.form["phone"]
        buyer.address = request.form["address"]
        try:
            db.session.commit()
            return redirect("/buyerList")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating buyer: {e}")
            return f"ERROR: {e}"
    else:
        return render_template("editBuyer.html", buyer=buyer)
    
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

@app.route("/clubList/edit/<int:club_id>", methods=["POST", "GET"])
def edit_club(club_id):
    club = Club.query.get_or_404(club_id)
    if request.method == "POST":
        club.name = request.form["name"]
        try:
            db.session.commit()
            return redirect("/clubList")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating club: {e}")
            return f"ERROR: {e}"
    else:
        return render_template("editClub.html", club=club)

@app.route("/exhibitorList", methods=["GET", "POST"])
def exhibitor_list():
    if request.method == "POST":
        fName = request.form["fName"]
        lName = request.form["lName"]
        address = request.form["Address"]
        club_id = request.form["club_id"]
        exhibitor = Exhibitor(fName=fName, lName=lName, address=address, club_id=club_id)
        try:
            db.session.add(exhibitor)
            db.session.commit()
            return redirect("/exhibitorList")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding exhibitor: {e}")
            return f"ERROR: {e}"
    else:
        exhibitors = Exhibitor.query.order_by(Exhibitor.fName).all()
        clubs = Club.query.order_by(Club.name).all()
        return render_template("exhibitorList.html", exhibitors=exhibitors, clubs=clubs)

@app.route("/exhibitorList/edit/<int:exhibitor_id>", methods=["POST", "GET"])
def edit_exhibitor(exhibitor_id):
    exhibitor = Exhibitor.query.get_or_404(exhibitor_id)
    if request.method == "POST":
        exhibitor.fName = request.form["fName"]
        exhibitor.lName = request.form["lName"]
        exhibitor.address = request.form["address"]
        exhibitor.club_id = request.form["club_id"]
        try:
            db.session.commit()
            return redirect("/exhibitorList")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating exhibitor: {e}")
            return f"ERROR: {e}"
    else:
        clubs = Club.query.order_by(Club.name).all()
        return render_template("editExhibitor.html", exhibitor=exhibitor, clubs=clubs)

@app.route("/animalList", methods=["GET", "POST"])
def animal_list():
    if request.method == "POST":
        ear_tag_number = request.form["Ear_Tag_No"]
        name = request.form["Name"]
        species = request.form["Species"]
        weight = request.form["Weight"]
        exhibitor_id = request.form["exhibitor_id"]
        packer = request.form["Packer"]
        kill_plant = request.form["Kill_Plant"]
        animal = Animal(ear_tag_number=ear_tag_number, name=name, species=species, weight=weight, exhibitor_id=exhibitor_id, packer=packer, kill_plant=kill_plant)
        try:
            db.session.add(animal)
            db.session.commit()
            return redirect("/animalList")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding animal: {e}")
            return f"ERROR: {e}"
    else:
        animals = Animal.query.order_by(Animal.ear_tag_number).all()
        exhibitors = Exhibitor.query.order_by(Exhibitor.fName).all()
        return render_template("animalList.html", animals=animals, exhibitors=exhibitors)

@app.route("/animalList/edit/<int:animal_id>", methods=["POST", "GET"])
def edit_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    if request.method == "POST":
        animal.ear_tag_number = request.form["Ear_Tag_No"]
        animal.name = request.form["name"]
        animal.species = request.form["species"]
        animal.weight = request.form["weight"]
        animal.exhibitor_id = request.form["exhibitor_id"]
        animal.packer = request.form["packer"]
        animal.kill_plant = request.form["kill_plant"]
        try:
            db.session.commit()
            return redirect("/animalList")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating animal: {e}")
            return f"ERROR: {e}"
    else:
        exhibitors = Exhibitor.query.order_by(Exhibitor.fName).all()
        return render_template("editAnimal.html", animal=animal, exhibitors=exhibitors)

@app.route("/saleList", methods=["GET", "POST"])
def sale_list():
    if request.method == "POST":
        animal_id = request.form["animal_id"]
        buyer_id = request.form["buyer_id"]
        sale_price = request.form["price"]
        sale = Sale(animal_id=animal_id, buyer_id=buyer_id, sale_price=sale_price)
        try:
            db.session.add(sale)
            db.session.commit()
            return redirect("/saleList")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding sale: {e}")
            return f"ERROR: {e}"
    else:
        sales = Sale.query.order_by(Sale.id).all()
        animals = Animal.query.order_by(Animal.ear_tag_number).all()
        buyers = Buyer.query.order_by(Buyer.name).all()
        exhibitors = Exhibitor.query.order_by(Exhibitor.fName).all()
        return render_template("saleList.html", sales=sales, animals=animals, buyers=buyers, exhibitors=exhibitors)

@app.route("/saleList/edit/<int:sale_id>", methods=["POST", "GET"])
def edit_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    if request.method == "POST":
        sale.animal_id = request.form["animal_id"]
        sale.buyer_id = request.form["buyer_id"]
        sale.sale_price = request.form["price"]
        try:
            db.session.commit()
            return redirect("/saleList")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating sale: {e}")
            return f"ERROR: {e}"
    else:
        animals = Animal.query.order_by(Animal.ear_tag_number).all()
        buyers = Buyer.query.order_by(Buyer.name).all()
        exhibitors = Exhibitor.query.order_by(Exhibitor.fName).all()
        return render_template("editSale.html", sale=sale, animals=animals, buyers=buyers, exhibitors=exhibitors)

@app.route("/addonList", methods=["GET", "POST"])
def addon_list():
    if request.method == "POST":
        buyer_id = request.form["buyer_id"]
        exhibitor_id = request.form["exhibitor_id"]
        price = request.form["Price"]
        addon = Addon(buyer_id=buyer_id, exhibitor_id=exhibitor_id, price=price)
        try:
            db.session.add(addon)
            db.session.commit()
            return redirect("/addonList")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding addon: {e}")
            return f"ERROR: {e}"
    else:
        addons = Addon.query.order_by(Addon.id).all()
        buyers = Buyer.query.order_by(Buyer.name).all()
        exhibitors = Exhibitor.query.order_by(Exhibitor.fName).all()
        return render_template("addonList.html", addons=addons, buyers=buyers, exhibitors=exhibitors)

@app.route("/addonList/edit/<int:addon_id>", methods=["POST", "GET"])
def edit_addon(addon_id):
    addon = Addon.query.get_or_404(addon_id)
    if request.method == "POST":
        addon.buyer_id = request.form["buyer_id"]
        addon.exhibitor_id = request.form["exhibitor_id"]
        addon.price = request.form["Price"]
        try:
            db.session.commit()
            return redirect("/addonList")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating addon: {e}")
            return f"ERROR: {e}"
    else:
        buyers = Buyer.query.order_by(Buyer.name).all()
        exhibitors = Exhibitor.query.order_by(Exhibitor.fName).all()
        return render_template("editAddon.html", addon=addon, buyers=buyers, exhibitors=exhibitors)

"""@app.route("/importData/<file_type>", methods=["POST", "GET"])
def import_data(file_type):
    if request.method == "POST":
        if "file" not in request.files:
            return "No file selected"

        file = request.files["file"]
        if file.filename == "":
            return "No file selected"

        if file and file.filename.endswith(".csv"):
            spreadsheet_dataframe = pd.read_csv(file)
            spreadsheet_dict = spreadsheet_dataframe.to_dict(orient="records")

            if file_type == "buyer":
                # Process buyer CSV file here
                for row in spreadsheet_dict:
                    name = row.get("Name", "")
                    bidder_number = row.get("no", "")
                    address = row.get("address", "")
                    city = row.get("city", "")
                    state = row.get("state", "")
                    zip_code = row.get("zip", "")

                    address_full = f"{address}, {city}, {state} {zip_code}"
                    buyer = Buyer(name=name, bidder_number=bidder_number, address=address_full)
                    try:
                        db.session.add(buyer)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error adding buyer from CSV: {e}")
                        return redirect ("/importData")
                pass
            else:
                # Process exhibitor CSV file here
                pass

        return redirect("/importData")
    else:
        return render_template("importData.html")"""


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)