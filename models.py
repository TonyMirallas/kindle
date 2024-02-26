from kindle import db
import json
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    # TODO: This method is an infinite loop
    @password.setter
    def password(self, plain_password):
        self.password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)

    def __repr__(self):
        return '<User %r>' % self.username

class KindleHighlight(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=False, nullable=True)
    author = db.Column(db.String(255), unique=False, nullable=True)
    highlight = db.Column(db.Text, unique=True, nullable=False)
    date = db.Column(db.String(80), unique=False, nullable=True)
    
    def __repr__(self):
        return '<KindleHighlight %r>' % self.highlight
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __str__(self):
        # return election as json
        return self.highlight
    
    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(255), unique=True, nullable=False)
    highlight_id = db.Column(db.Integer, db.ForeignKey('kindle_highlight.id'), nullable=False)
    
    def __repr__(self):
        return '<Tags %r>' % self.tag
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __str__(self):
        # return election as json
        return self.tag
    
    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)