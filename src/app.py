
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")
       
jackson_family.add_member(
    { "first_name" : "John",
     "age":33,
     "lucky_numbers": [7, 13, 22] })           
                
jackson_family.add_member(
    { "first_name" : "jane",
     "age":35,
     "lucky_numbers": [10, 14, 3] }) 

jackson_family.add_member(
    { "first_name" : "Jimmy",
     "age":5,
     "lucky_numbers": [1] }) 






@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
     return jsonify(member), 200
    return jsonify({"msg": "Miembro no encontrado"}), 404


@app.route('/members/', methods=['POST'])
def add_new_menber():
   new_menber = request.json
   if not new_menber:
      return jsonify({"msg" : "error al añadir un miembro"}), 400
   jackson_family.add_member(new_menber)
   return jsonify({"msg":"Miembro añadido"}), 200



@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_sigle_members(member_id):
 deleted = jackson_family.delete_member(member_id)
 if deleted :
      return jsonify({"done": True}), 200
 return jsonify({"msg:" "no se puede borrar"}), 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
