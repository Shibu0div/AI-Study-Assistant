from app import create_application 
flask_app = create_application() 

if(__name__ =="__main__"):
    flask_app.run(debug=True) 