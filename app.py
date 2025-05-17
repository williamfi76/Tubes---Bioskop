from flask import Flask
from Controller import accountController
from Model.genre import Genre

def main():
    # app = Flask(__name__, template_folder="View", static_url_path='/css', static_folder='View/css')
    # app.run(debug="True")
    movieGenre = Genre.ACTION
    print(Genre.ACTION.value)

if __name__ == '__main__':
    main()