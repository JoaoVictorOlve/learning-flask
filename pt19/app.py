from flask import Flask, make_response, jsonify, request, render_template

app = Flask(__name__)

stock = {
    "fruit" : {
        "apple": 30,
        "banana": 45,
        "cherry": 1000
    }
}

# GET
# POST
# PUT
# PATCH
# DELETE

@app.route("/get-text", methods=["GET"])
def get_text():
    return "some text"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/qs")
def qs():

    if request.args:
        req = request.args
        return " ".join(f"{k}: {v} " for k, v in req.items())

    return "No query"

@app.route("/stock")
def get_stock():

    res = make_response(jsonify(stock), 200)

    return res

@app.route("/stock/<collection>")
def get_collection(collection):

    """ Returns the collection from stock """

    if collection in stock:
        res = make_response(jsonify(stock[collection]), 200)
        return res
    
    res = res = make_response(jsonify({"error" : "Item not found"}), 400)

    return res

# Get a collection member

@app.route("/stock/<collection>/<member>")
def get_member(collection, member):

    """ Returns the qty of the member """

    if collection in stock:
        member = stock[collection].get(member)
        if member:
            res = make_response(jsonify(member), 200)
            return res
        
        res = make_response(jsonify({"error": "Unknown member"}), 400)
        return res

    res = res = make_response(jsonify({"error": "Collection not found"}), 400)
    return res

#POST - Create a collection
@app.route("/stock/<collection>", methods=["POST"])
def create_collection(collection):

    """ Create a new collection if it doesn't exist """

    req = request.get_json()

    if collection in stock:
        res = make_response(jsonify({"error": "Collection already exists"}), 400)
        return res
    
    stock.update({collection: req})

    res = make_response(jsonify({"message": "Collection created"}), 200)
    return res

#PUT a collection

@app.route("/stock/<collection>", methods=["PUT"])
def put_collection(collection):

    """
    Replace or creates a collection. Expected body: {"member": qty}
    """

    req = request.get_json()

    stock[collection] = req

    res = make_response(jsonify({"message": "Collection replaced"}), 200)
    return res

#PATCH a collection
@app.route("/stock/<collection>", methods=["PATCH"])
def patch_collection(collection):

    """
    Updates or creates a collection. Expected body: {"member": qty}
    """

    req = request.get_json()

    if collection in stock:
        for k, v in req.items():
            stock[collection][k] = v
        
        res = make_response(jsonify({"message": "Collection updated"}), 200)
        return res
    
    stock[collection] = req

    res = make_response(jsonify({"message": "Collection created"}), 200)
    return res

#DELETE - Deletes a collection

@app.route("/stock/<collection>", methods=["DELETE"])
def delete_collection(collection):

    """ If the collection exists, delete it """

    if collection in stock:
        del stock[collection]
        res = make_response(jsonify({}), 204)
        return res
    
    res = make_response(jsonify({"error": "Collection not found"}), 400)
    return res

#DELETE - Deletes a collection member

@app.route("/stock/<collection>/<member>", methods=["DELETE"])
def delete_member(collection, member):
    
    """ If the collection exists and the member exists, delete it """

    if collection in stock:
        if member in stock[collection]:
            del stock[collection][member]
            res = make_response(jsonify({}), 204) # Action enacted
            return res
        
        res = make_response(jsonify({"error": "member not found"}), 400)
        return res
    
    res = make_response(jsonify({"error": "collection not found"}), 400)
    return res