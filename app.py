import datetime
import os
from typing import List
from flask import Flask, redirect, send_from_directory, url_for
from Controller import accountController, employeeController, memberController
from Controller import adminController
from Controller.adminController import admin_bp
from Controller.memberController import member_bp
from Controller.accountController import account_bp
from Controller.employeeController import employee_bp



def main():
    app = Flask(__name__, template_folder='View', static_url_path='/css', static_folder='View/css')
    app.register_blueprint(admin_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(employee_bp)
    app.secret_key = "secret_code"

    @app.route('/css/<path:filename>')
    def custom_css(filename):
        return send_from_directory(os.path.join('view', 'css'), filename)
    
    @app.route('/View/<path:filename>')
    def custom_view_static(filename):
        return send_from_directory('view', filename)

    @app.route("/")
    def index():
        return redirect(url_for('login_route'))
    
    @app.route("/login", methods=['GET', 'POST'])
    def login_route():
        return accountController.show_login()
    
    @app.route("/register", methods=['GET','POST'])
    def register_route():
        return accountController.show_register()
    
    app.add_url_rule('/logout', 'logout', accountController.logout)
    app.run(debug=True)

if __name__ == '__main__':
    # adminController.addNewShowing(1, datetime.datetime(2025,7,12,10,0,0), datetime.datetime(2025,7,12,10,0,0), 1)
    main()