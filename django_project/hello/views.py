# stressdetector/views.py
# import os
import mysql.connector
import mysql.connector as sql
from django.views.decorators.csrf import csrf_protect
from .forms import SignupForm
# from .forms import UserForm
from .models import User 
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

# import joblib
from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template





@csrf_protect
# Import regex library for pattern matching

# Define the view for the index page
def signup(request):
    if request.method == "POST":
        us = request.POST.get('username')
        em = request.POST.get('email')
        ps = request.POST.get('password')
        cpass = request.POST.get('cpassword')

        errors = {}

        # Validation for matching passwords
        if ps != cpass:
            errors['cpassword_error'] = "Passwords do not match!"
            print("Passwords do not match")  # Debugging line

        conn = None
        cursor = None

        try:
            # Database connection
            conn = sql.connect(
                host="127.0.0.1",
                user="root",
                password="1234",
                database="humanstress"
            )
            cursor = conn.cursor()

            # Check for duplicate username or email
            query = "SELECT COUNT(*) FROM signup WHERE username = %s OR email = %s"
            cursor.execute(query, (us, em))
            if cursor.fetchone()[0] > 0:
                errors['duplicate_error'] = "Username or email already exists!"
                print("Account already exists")  # Debugging line
                return render(request, 'signup.html', {'errors': errors})

            # If no errors, insert new user
            if not errors:
                comm = "INSERT INTO signup (username, email, password, cpassword) VALUES (%s, %s, %s, %s)"
                cursor.execute(comm, (us, em, ps, cpass))
                conn.commit()

                messages.success(request, "Account created successfully!")
                print("Redirecting to login...")  # Debugging line
                return redirect('login')

        except sql.Error as e:
            print(f"Database error: {e}")  # Debugging line
            messages.error(request, f"Error: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # Render the signup page with errors if any
    return render(request, 'signup.html')



from django.contrib.auth.decorators import login_required


@csrf_protect
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
 
        conn = None
        cursor = None
 
        try:
            # Connect to the MySQL database
            conn = sql.connect(host="127.0.0.1", user="root", password="1234", database="humanstress")
            cursor = conn.cursor()
 
            # Check if user exists with the provided username and password
            query = "SELECT * FROM signup WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
 
            if user:
                # Successful login; redirect to a dashboard or home page
                messages.success(request,"✅ Successfully logged in!")
                return redirect('dataentry')  # Replace 'home' with the actual home view name
            else:
                # Invalid login
                messages.error(request,"❌Invalid username or password.")
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'error_message': error_message})
 
        except sql.Error as e:
            error_message = f"An error occurred: {e}"
            return render(request, 'login.html', {'error_message': error_message})
 
        finally:
            # Close the cursor and connection only if they were created
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
 
    # Render the login page if the method is not POST
    return render(request, 'login.html')


 
  


        



# Data Entry View (Only accessible to logged-in users)
@login_required
def dataentry(request):
    return render(request, 'dataentry.html')  # Use 'hello/dataentry.html' as per your file structure
 # Use 'hello/dataentry.html' as per your file structure


# Result View (only accessible to logged-in users)
@login_required
def result(request):
    return render(request, 'result.html')  # Ensure the correct path to `result.html` in `hello/templates`
