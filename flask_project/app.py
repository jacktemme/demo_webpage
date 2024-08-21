from flask import Flask, jsonify
from pymongo import MongoClient
import config
from bson import ObjectId

app = Flask(__name__)

def serialize_doc(doc):
    """Convert MongoDB ObjectId fields to string and prepare document for JSON serialization."""
    if isinstance(doc, dict):
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
            elif isinstance(value, dict):
                serialize_doc(value)
            elif isinstance(value, list):
                doc[key] = [serialize_doc(item) if isinstance(item, dict) else item for item in value]
    return doc

# Initialize MongoDB client
client = MongoClient(config.MONGO_URI)
db = client.get_default_database()
establishments = db.establishments

@app.route('/')
def index():
    try:
        establishment = establishments.find_one()
    
        return jsonify(serialize_doc(establishment))
    except Exception as e:
        app.logger.error(f"Error querying the database: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run()