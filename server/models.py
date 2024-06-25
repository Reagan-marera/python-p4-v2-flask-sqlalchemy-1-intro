from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


metadata = MetaData()

db = SQLAlchemy(app, metadata=metadata)


class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Pet {self.name}>'

with app.app_context():
    db.create_all()


@app.route('/add_pet', methods=['POST'])
def add_pet():
    data = request.get_json()
    name = data.get('name')
    species = data.get('species')
    if not name or not species:
        return jsonify({'error': 'Name and species are required'}), 400

    new_pet = Pet(name=name, species=species)
    db.session.add(new_pet)
    db.session.commit()
    return jsonify({'message': 'Pet added successfully', 'pet': {'id': new_pet.id, 'name': new_pet.name, 'species': new_pet.species}}), 201

@app.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    return jsonify([{'id': pet.id, 'name': pet.name, 'species': pet.species} for pet in pets])


@app.route('/pet/<int:id>', methods=['GET'])
def get_pet(id):
    pet = Pet.query.get(id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    return jsonify({'id': pet.id, 'name': pet.name, 'species': pet.species})

if __name__ == '__main__':
    app.run(debug=True)
