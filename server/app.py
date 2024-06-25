

from flask import Flask, request, jsonify

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/pets', methods=['GET', 'POST'])
def manage_pets():
    if request.method == 'POST':
        data = request.get_json()
        new_pet = Pet(name=data['name'], species=data['species'])
        db.session.add(new_pet)
        db.session.commit()
        return jsonify({'message': 'Pet added successfully'}), 201

    pets = Pet.query.all()
    return jsonify([{'id': pet.id, 'name': pet.name, 'species': pet.species} for pet in pets])

if __name__ == '__main__':
    app.run(port=5555, debug=True)
