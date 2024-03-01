from flask import jsonify, render_template, request
from . import app
from . import db
from .models import User, KindleHighlight, Tag
from . import functions
import pandas as pd
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required


@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if username is None or password is None:
        return create_response(None, 400, 'error', 'username and password are required')
    if User.query.filter_by(username=username).first() is not None:
        return create_response(None, 400, 'error', 'username already exists')
    
    user = User(username=username)
    user.password = password
    db.session.add(user)
    db.session.commit()
    return create_response(None, 201, 'success', 'user created')

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if username is None or password is None:
        return create_response(None, 400, 'error', 'username and password are required')
    
    # get user with username query
    user = User.query.filter_by(username=username).first()
    
    # check password
    if user is None or not user.check_password(password):
        return create_response(None, 401, 'error', 'invalid username or password')
    
    access_token = create_access_token(identity=username)
    
    return create_response(access_token, 200, 'success', 'user logged in')

@app.route("/")
@jwt_required()
def home():

    kindleHighlight = KindleHighlight.query.all()

    return render_template("home.html", kindleHighlight=kindleHighlight)

@app.route("/api/test")
@jwt_required()
def test():

    return "test"

@app.route("/kindle-scraping/")
def kindle_scraping():
    
    data = []
    
    data = functions.get_books()
    df = pd.DataFrame(data, columns=['author', 'title', 'highlights_count', 'highlight'])
    # insert data into database
    for index, row in df.iterrows():
        kindleHighlight = KindleHighlight(author=row['author'], title=row['title'], highlight=row['highlight'])
        
        try:
            db.session.merge(kindleHighlight)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError: {e}")
            continue
        except Exception as e:
            db.session.rollback()
            print(e)
        continue       
    
    return data

# API

def create_response(data, status_code=200, status='success', message=''):
    response = {
        'status': status,
        'data': data,
        'message': message
    }
    return jsonify(response), status_code

@app.route("/api/get-highlights")
@jwt_required()
def get_highlights():
    
    kindleHighlights = KindleHighlight.query.all()
    # make kindleHighlights to json
    kindleHighlights = [kindleHighlight.as_dict() for kindleHighlight in kindleHighlights]
    return create_response(kindleHighlights)

@app.route("/api/get-highlight/<int:id>")
def get_highlight(id):
    
    kindleHighlight = KindleHighlight.query.get(id)
    # make kindleHighlights to json
    kindleHighlight = kindleHighlight.as_dict()
    return create_response(kindleHighlight)

# api call to add tag to highlight
@app.route("/api/add-tag/<int:id>/<string:tag>")
def add_tag(id, tag):
    
    tag = tag.lower()
    
    # get Tag by tag
    tag = Tag.query.filter_by(tag=tag).first()
    highlight = KindleHighlight.query.get(id)
    
    if highlight is None:
        return create_response(None, 404, 'error', 'Highlight not found')
    # if tag does not exist create it
    if tag is None:
        tag = Tag(tag=tag, highlight_id=id)
        db.session.add(tag)
        db.session.commit()
        return tag.as_dict()    
    
    kindleHighlight = KindleHighlight.query.get(id)
    # make kindleHighlights to json
    kindleHighlight = kindleHighlight.as_dict()
    return create_response(kindleHighlight)