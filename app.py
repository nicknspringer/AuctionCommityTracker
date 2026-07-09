from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from pandas import pandas as pd

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

class Exhibitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(80), nullable=False)
    lName = db.Column(db.String(80), nullable=False)
    sale_number = db.Column(db.Integer, nullable=False)
    division = db.Column(db.String(80))
    division_placing = db.Column(db.String(80))
    club = db.Column(db.String)

    def __repr__(self):
        return f"<Exhibitor {self.fName}>"

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ear_tag_number = db.Column(db.Integer, nullable=False)
    species = db.Column(db.String(80))
    weight = db.Column(db.Float, nullable=False)
    picture = db.Column(db.LargeBinary, nullable=True)
    exhibitor_id = db.Column(db.Integer, db.ForeignKey("exhibitor.id"), nullable=False)
    sale_number = db.Column(db.Integer, nullable=False)


    exhibitor = db.relationship("Exhibitor", backref=db.backref("animals", lazy=True))

    def __repr__(self):
        return f"<Animal {self.name}>"

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=False)
    buyer_id_1 = db.Column(db.Integer, db.ForeignKey("buyer.id"), nullable=False)
    buyer_id_2 = db.Column(db.Integer, db.ForeignKey("buyer.id"))
    buyer_id_3 = db.Column(db.Integer, db.ForeignKey("buyer.id"))
    buyer_id_4 = db.Column(db.Integer, db.ForeignKey("buyer.id"))
    packer = db.Column(db.String(80), nullable=True)
    kill_plant = db.Column(db.String(80), nullable=True)
    sale_price = db.Column(db.Float, nullable=False)
    is_processed = db.Column(db.Boolean, nullable=False)
    sale_number = db.Column(db.Integer)

    animal = db.relationship("Animal", backref=db.backref("sales", lazy=True))
    buyer1 = db.relationship("Buyer", foreign_keys=[buyer_id_1], backref=db.backref("buyer1", lazy=True))
    buyer2 = db.relationship("Buyer", foreign_keys=[buyer_id_2], backref=db.backref("buyer2", lazy=True))
    buyer3 = db.relationship("Buyer", foreign_keys=[buyer_id_3], backref=db.backref("buyer3", lazy=True))
    buyer4 = db.relationship("Buyer", foreign_keys=[buyer_id_4], backref=db.backref("buyer4", lazy=True))


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
        buyers = Buyer.query.order_by(Buyer.bidder_number).all()
        return render_template("buyerList.html", buyers=buyers)

@app.route("/buyerSaleList", methods=["GET"])
def buyer_sale_list():
    buyers = Buyer.query.order_by(Buyer.bidder_number).all()
    return render_template("buyerSaleList.html", buyers=buyers)

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

@app.route("/exhibitorList", methods=["GET", "POST"])
def exhibitor_list():
    if request.method == "POST":
        sale_number = request.form["sale_number"]
        fName = request.form["fName"]
        lName = request.form["lName"]
        club = request.form["club"]
        division = request.form["division"]
        division_placing = request.form["division_placing"]
        exhibitor = Exhibitor(sale_number=sale_number, fName=fName, lName=lName, club=club, division=division, division_placing=division_placing)
        try:
            db.session.add(exhibitor)
            db.session.commit()
            return redirect("/exhibitorList")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding exhibitor: {e}")
            return f"ERROR: {e}"
    else:
        exhibitors = Exhibitor.query.order_by(Exhibitor.sale_number).all()
        return render_template("exhibitorList.html", exhibitors=exhibitors)

@app.route("/exhibitorList/edit/<int:exhibitor_id>", methods=["POST", "GET"])
def edit_exhibitor(exhibitor_id):
    exhibitor = Exhibitor.query.get_or_404(exhibitor_id)
    if request.method == "POST":
        exhibitor.sale_number = request.form["sale_number"]
        exhibitor.fName = request.form["fName"]
        exhibitor.lName = request.form["lName"]
        exhibitor.division = request.form["division"]
        exhibitor.division_placing = request.form["division_placing"]
        exhibitor.club = request.form["club"]
        try:
            db.session.commit()
            return redirect("/exhibitorList")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating exhibitor: {e}")
            return f"ERROR: {e}"
    else:
        return render_template("editExhibitor.html", exhibitor=exhibitor)

@app.route("/animalList", methods=["GET", "POST"])
def animal_list():
    if request.method == "POST":
        ear_tag_number = request.form["Ear_Tag_No"]
        species = request.form["Species"]
        weight = request.form["Weight"]
        exhibitor_id = request.form["exhibitor_id"]
        animal = Animal(ear_tag_number=ear_tag_number, species=species, weight=weight, exhibitor_id=exhibitor_id)
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
        animal.species = request.form["species"]
        animal.weight = request.form["weight"]
        animal.exhibitor_id = request.form["exhibitor_id"]
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
        # Add sale to database
        animal_id = request.form["animal_id"]
        buyer_id_1 = request.form["buyer_id_1"]
        buyer_id_2 = request.form["buyer_id_2"]
        buyer_id_3 = request.form["buyer_id_3"]
        buyer_id_4 = request.form["buyer_id_4"]
        sale_price = request.form["price"]
        packer = request.form["packer"]
        kill_plant = request.form["kill_plant"]
        is_processed = False
        sale = Sale(animal_id=animal_id, buyer_id_1=buyer_id_1, buyer_id_2=buyer_id_2, buyer_id_3=buyer_id_3, buyer_id_4=buyer_id_4, sale_price=sale_price, packer=packer, kill_plant=kill_plant, is_processed=is_processed)
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
        buyers = Buyer.query.order_by(Buyer.bidder_number).all()
        exhibitors = Exhibitor.query.order_by(Exhibitor.sale_number).all()
        return render_template("saleList.html", sales=sales, animals=animals, buyers=buyers, exhibitors=exhibitors)

@app.route("/saleList/edit/<int:sale_id>", methods=["POST", "GET"])
def edit_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    if request.method == "POST":
        sale.animal_id = request.form["animal_id"]
        sale.buyer_id_1 = request.form["buyer_id_1"]
        sale.buyer_id_2 = request.form["buyer_id_2"]
        sale.buyer_id_3 = request.form["buyer_id_3"]
        sale.buyer_id_4 = request.form["buyer_id_4"]
        sale.sale_price = request.form["price"]
        sale.packer = request.form["packer"]
        sale.kill_plant = request.form["kill_plant"]
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

@app.route("/importData", methods=["GET"])
def import_data_menu():
    return render_template("importData.html")

def get_species(club_name):
    species = ["swine", "chicken", "rabbit", "turkey", "beef", "sheep", "goat"]
    for animal in species:
        if animal.lower() in club_name.lower():
            return animal
    return "none"

@app.route("/importData/<file_type>", methods=["POST", "GET"])
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
                    name = row.get("name", "")
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
                return spreadsheet_dict
            elif file_type == "exhibitor":
                #return spreadsheet_dict# Process exhibitor CSV file here
                for row in spreadsheet_dict:
                    saleOrder = row.get("Sale Order", "")
                    lName = row.get("Last Name", "")
                    fName = row.get("First Name", "")
                    tagNumber = row.get("Tag ID", "")
                    club_name = row.get("Club", "")
                    saleWeight = row.get("Sale Weight", "")
                    division = row.get("Division", "")
                    divisionPlacing = row.get("Division Placing")
                    species = get_species(division)
                    #return f"{species}"
                    try:
                        exhibitor = Exhibitor(fName=fName, lName=lName, sale_number=saleOrder, division=division, division_placing=divisionPlacing, club=club_name)
                        db.session.add(exhibitor)
                        db.session.commit()
                        animal = Animal(ear_tag_number=tagNumber, weight=saleWeight, exhibitor_id=exhibitor.id, species=species, sale_number=saleOrder)
                        db.session.add(animal)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error adding exhibitor from CSV: {e}")
                        return f"Error adding exhibitor from CSV: {e}"
                pass
                return redirect("/importData")
            else:
                # Process exhibitor CSV file here
                return f"woop"

        return redirect("/importData")
    else:
        return render_template("importData.html")

@app.route("/saleInvoice", methods=["GET"])
def sale_invoice():
    sales = Sale.query.order_by(Sale.is_processed, Sale.sale_number)
    return render_template("saleInvoices.html", sales=sales)

@app.route("/invoice/<int:sale_id>", methods=["POST", "GET"])
def invoice(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    if request.method == "POST":
        pass
    else:
        animal = Animal.query.get_or_404(sale.animal_id)
        exhibitor = Exhibitor.query.get_or_404(animal.exhibitor_id)
        buyer1 = Buyer.query.get(sale.buyer_id_1)
        buyer2 = Buyer.query.get(sale.buyer_id_2)
        buyer3 = Buyer.query.get(sale.buyer_id_3)
        buyer4 = Buyer.query.get(sale.buyer_id_4)
        return render_template("invoice.html", sale=sale, animal=animal, exhibitor=exhibitor, buyer1=buyer1, buyer2=buyer2, buyer3=buyer3, buyer4=buyer4)

@app.route("/block/<int:sale_number>")
def block_screen(sale_number):
    #exhibitor = select(Exhibitor).where(Exhibitor.sale_number == sale_number)
    #animal = select(Animal).where(Animal.sale_number == exhibitor.sale_number)
    exhibitors = Exhibitor.query.order_by(Exhibitor.sale_number).all()
    exhibitor = exhibitors[sale_number-1]
    animals = Animal.query.order_by(Animal.sale_number).all()
    animal = animals[sale_number-1]
    buyers = Buyer.query.order_by(Buyer.bidder_number).all()
    return render_template("block.html", exhibitor=exhibitor, animal=animal, buyers=buyers)

@app.route("/Invoice")
def display_invoice():
    return render_template("invoice_test.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False, host="0.0.0.0", port="5000")