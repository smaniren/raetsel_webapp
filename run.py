from clueful import app, db
from livereload import Server

if __name__ == '__main__':
    db.create_all()
    app.run()
    
    """ server = Server(app.wsgi_app)
    server.serve() """