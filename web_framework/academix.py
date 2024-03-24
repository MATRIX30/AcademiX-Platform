#!/usr/bin/python3
"""Module to manage then entire AcademiX platform"""
from flask import Flask, render_template, url_for, request, redirect, jsonify, flash, get_flashed_messages
import requests
import os
api_addresse = os.getenv('ACADEMIX_API_HOST')
api_port = os.getenv('ACADEMIX_API_PORT')
fact_api_key = os.getenv('NINJA_API_KEY')

app = Flask(__name__)
# app.config['SECRET_KEY'] = '65979eae88d8f29fb44a573fe53f7c0a41635378'
app.secret_key = '65979eae88d8f29fb44a573fe53f7c0a41635378'


@app.route("/", methods=['GET','POST'], strict_slashes=False)
def login():
    """method to handle logins"""
    err_msg= {"message":"Incorrect username or Password try again"}
    
    
    
    if request.method == 'POST':
        email = request.form.get('email')  # Get the value of the 'email' input field
        password = request.form.get('password')  # Get the value of the 'password' input field
        students = requests.get("http://{}:{}/api/v1/students".format(api_addresse, api_port))

        if students.status_code == 200:
            # API request successful, do something with the response
            api_data = students.json()
            # Process the API response here
            for student in api_data:
                if student["email"].lower().strip() == email.lower().strip() and student["password"] == password:
                    student_info = requests.get("http://{}:{}/api/v1/student/info/{}".format(api_addresse, api_port, student["id"])).json()
                    
                    # get facts from facts api to display on dashboard 
                    limit = 3
                    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
                    try:
                        response = requests.get(api_url, headers={'X-Api-Key': fact_api_key })
                        if response.status_code == requests.codes.ok:
                            facts = response.json()
                    except:
                        facts=[{"fact":"No facts availalbe ..."}]
                    
                    return render_template("student_dashboard.html", info=student_info, facts=facts)
    
        teachers = requests.get("http://{}:{}/api/v1/teachers".format(api_addresse, api_port))
        if teachers.status_code == 200:
            api_data = teachers.json()
            for teacher in api_data:
                if teacher["email"].lower().strip() == email.lower().strip() and teacher["password"] == password:
                    teacher_info = requests.get("http://{}:{}/api/v1/teacher/info/{}".format(api_addresse, api_port, teacher["id"])).json()
                    return render_template("teacher_dashboard.html", info=teacher_info)
        admins = requests.get("http://{}:{}/api/v1/admins".format(api_addresse, api_port))


        if admins.status_code == 200:
            api_data = teachers.json()
            for admin in api_data:
                if admin["email"].lower().strip() == email.lower().strip() and admin["password"] == password:
                    admin_info = requests.get("http://{}:{}/api/v1/admin/info/{}".format(api_addresse, api_port, admin["id"])).json()
                    
                    return render_template("admin_dashboard.html", info=admin_info)
        return render_template("login.html", msg="wrong credentials!")
    return render_template("login.html")


# @app.route('/course/<course_id>', methods=['GET'], strict_slashes=False)
# def course(course_id):
#     """method to handle display of course information"""
#     return {"message":404}

@app.route('/results', methods=['GET'], strict_slashes=False)
def student_result():
    """
    method to handle student results
    """
    # Get the value of the 'student_id' parameter from the query string
    student_id = request.args.get('student_id')
    
    course_info = requests.get("http://{}:{}/api/v1/student/results/{}".format(api_addresse, api_port, student_id)).json()
    print(course_info)
    student_info = requests.get("http://{}:{}/api/v1/student/info/{}".format(api_addresse, api_port, student_id)).json()
    
    summary = {}
    first_term_total=0
    overall_average=0
    for course in course_info:
        first_term_total += course["first_term"][2] * course["coeff"]
    # Do something with the student_id, for example, return it
    overall_average = first_term_total/(len(course_info)*20)
    return render_template("student_result.html", info=student_info, courses=course_info, i=1, total=first_term_total,overall_average=overall_average)


@app.route('/student_profile/<student_id>', methods=['GET'], strict_slashes=False)
def student_profile(student_id):
    """method to manage profile display"""
    student_info = requests.get("http://{}:{}/api/v1/student/info/{}".format(api_addresse, api_port, student_id)).json()
    return render_template("student_profile.html", info=student_info)


@app.route('/course/<course_id>', methods=['GET'], strict_slashes=False)
def fill_course_marks(course_id):
    """method to fill course evaluation by teacher"""
    course_info = requests.get("http://{}:{}/api/v1/course/{}".format(api_addresse, api_port, course_id)).json()
    messages = get_flashed_messages() 
    students = requests.get("http://{}:{}/api/v1/course/results/{}".format(api_addresse, api_port, course_id)).json()
    return render_template("course_evaluation.html",course=course_info, students=students, message=messages)


@app.route('/save_course_results', methods=['POST'], strict_slashes=False)
def save_course_results():
    """display course results"""
    # save the data and redirect to fill_course_marks function
    
    first_seq_marks = request.form.getlist('first_seq[]')
    second_seq_marks = request.form.getlist('second_seq[]')
    course_id = request.form.getlist('course_id[]')
    student_id = request.form.getlist("student_id[]")
    term = request.form.get("term")
    """ print("-----------------------")
    print(term)
    print(first_seq_marks)
    print(second_seq_marks)
    print(course_id)
    print(student_id) """
    # URL of the endpoint
    result_update_url = "http://{}:{}/api/v1/student_course".format(api_addresse, api_port)

    results = zip(course_id,student_id,first_seq_marks,second_seq_marks)
    
    
    
    for i in results:
        result_data = {}
        result_data["course_id"] = i[0]
        result_data["student_id"] = i[1]
        result_data["first_mark"] = i[2]
        result_data["second_mark"] = i[3]
        result_data["term"] = term
        print(i)
        print(result_data)
        # Sending POST request with JSON data
        response = requests.post(result_update_url, json=result_data)
        # Checking the response
        print(response.status_code)
        if response.status_code == 201:
            msg = "Saved successfully!" 
        else:
              msg = "Operation Unsuccessful!" 
    flash(msg, category="success")
    return redirect(url_for('fill_course_marks', course_id=result_data["course_id"]))
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3500, debug=True)
    