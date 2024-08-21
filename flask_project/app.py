from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

# Initialize Flask application
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Reflect Database into ORM classes
Base = automap_base()

with app.app_context():
    # Prepare the Base with the engine
    Base.prepare(autoload_with=db.engine)
    # Access the table class within the context
    tables = Base.classes.keys()
    Age = Base.classes.age  

for table in tables:
    print(table)
    
@app.route('/')
def homepage():

    return ('Welcome to an API on bird banding data')

@app.route('/data')
def get_data():
    try:
        # Query the database using Flask-SQLAlchemy's session
        results = db.session.query(Age).all() 
        
        # Convert the query results into a list of dictionaries
        data = [{'code': item.age_code, 'description': item.age_description} for item in results]  
        
        # Return the data as JSON
        return jsonify({'data': data})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()