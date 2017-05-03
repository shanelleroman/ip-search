from server import *

document = Document(name='Reading_Response', text=)

post = Post(title = request.form('title'), content = request.form['content'])
        db.session.add(post)
        db.session.commit()

        id= db.Column(db.Integer, primary_key=True)
    name = db.Column((db.String(30)))
    #text = db.Column(db.String(100))
    text = db.Column((db.Text()))
document = Document()