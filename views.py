from flask import jsonify, render_template
from . import app
from . import db
from .models import KindleHighlight, Tag
from . import functions
import pandas as pd
from sqlalchemy.exc import IntegrityError


@app.route("/")
def home():

    kindleHighlight = KindleHighlight.query.all()

    return render_template("home.html", kindleHighlight=kindleHighlight)

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