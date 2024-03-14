#!/usr/bin/python3
"""Module to manage then entire AcademiX platform"""
from flask import Flask, render_template, url_for, request
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '65979eae88d8f29fb44a573fe53f7c0a41635378'

@app.route("/", methods=['GET','POST'], strict_slashes=False)
def login():
    """method to handle logins"""
    err_msg= {"message":"Incorrect username or Password try again"}
    if request.method == 'POST':
        email = request.form.get('email')  # Get the value of the 'email' input field
        password = request.form.get('password')  # Get the value of the 'password' input field
        students = requests.get("http://127.0.0.1:6000/api/v1/students")

        if students.status_code == 200:
            # API request successful, do something with the response
            api_data = students.json()
            # Process the API response here
            for student in api_data:
                if student["email"].lower().strip() == email.lower().strip() and student["password"] == password:
                    student_info = requests.get("http://127.0.0.1:6000/api/v1/student/info/{}".format(student["id"])).json()
                    print(student_info)
                    return render_template("student_dashboard.html", info=student_info)
    
        teachers = requests.get("http://127.0.0.1:6000/api/v1/teachers")
        if teachers.status_code == 200:
            api_data = teachers.json()
            for teacher in api_data:
                if teacher["email"].lower().strip() == email.lower().strip() and teacher["password"] == password:
                    teacher_info = requests.get("http://127.0.0.1:6000/api/v1/teacher/info/{}".format(teacher["id"])).json()
                    print(teacher_info)
                    return render_template("teacher_dashboard.html", info=teacher_info)
        admins = requests.get("http://127.0.0.1:6000/api/v1/admins")


        if admins.status_code == 200:
            api_data = teachers.json()
            for admin in api_data:
                if admin["email"].lower().strip() == email.lower().strip() and admin["password"] == password:
                    admin_info = requests.get("http://127.0.0.1:6000/api/v1/admin/info/{}".format(admin["id"])).json()
                    print(admin_info)
                    return render_template("admin_dashboard.html", info=admin_info)
        return render_template("login.html", message=err_msg)
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3500, debug=True)