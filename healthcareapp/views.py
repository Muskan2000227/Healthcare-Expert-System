from django.shortcuts import render,redirect
from healthcareapp.models import *
from django.conf import settings
from django.core.mail import send_mail
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#Plotly -graph_objects ,express
import plotly.graph_objects as go
import plotly.express as px
import itertools
import statsmodels.api as sm

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import joblib
import seaborn as sns
from newsapi import NewsApiClient
from django.contrib.auth import login as auth_login, logout as auth_logout
from social_django.models import UserSocialAuth
import os
# Create your views here.


def login(request):
    if request.method=="POST":
        e=request.POST.get('email')
        p=request.POST.get('passw')
        user=register_model.objects.filter(email=e,passw=p)
        if len(user)>0:
            request.session['email']=e
            return redirect("/dash")
        else:
            return render(request,'login.html',{'msg':"Invalid email"})
    else:
        return render(request,'login.html')
    



def logingoogle(request):
    if request.method == "POST":
        e = request.POST.get('email')
        p = request.POST.get('passw')

        # Check if the user exists in the database
        try:
            user = register_model.objects.get(email=e)
            if user.passw == p:
                # Set session key if the credentials match
                request.session['email'] = e
                return redirect("/dash")  # Redirect to dashboard
            else:
                return render(request, 'logingoogle.html', {'msg': "Incorrect password"})
        except register_model.DoesNotExist:
            return render(request, 'logingooogle.html', {'msg': "User does not exist"})
    else:
        return render(request, 'logingoogle.html')
    
# Google login view
def google_login(request):
    return redirect('social:begin', backend='google-oauth2')   



def logout(request):
    auth_logout(request)  # Clears the session for both Google and regular logins
    return redirect('index')

# def logout(request):
#     if not request.session.has_key('email'):
#         return redirect('login')
    
#     del request.session['email']
#     return redirect('login')


def signup(request):
    if request.method=="POST":
        n=request.POST.get('username')
        e=request.POST.get('email')
        p=request.POST.get('pass')
        cp=request.POST.get('cpass')
        if p==cp:
            if register_model.objects.filter(email=e).exists():
                return render(request,'signup.html',{'err':"Email aready exists"})
            else:
                otp=random.randrange(100000,999999)
                subject="One Time Passwprd"
                message="Your OTP is "+str(otp)
                email_from=settings.EMAIL_HOST_USER
                recipient_list=[e]
                send_mail(subject,message,email_from,recipient_list)
                msg="Your OTP has been sent to your respective gmail account"
                return render(request,'signup1.html',{'msg':msg,'name':n,"email":e,'password':p,'org_otp':otp})
        else:    
            return render(request,'signup.html',{'err':"Password and confirm pass doesn't match"})
    else:
        return render(request,'signup.html')
        

def check_otp(request):
    if request.method=="POST":
        n=request.POST.get('username')
        e=request.POST.get('email')
        p=request.POST.get('passw')
        org=request.POST.get('o_otp')
        enter=request.POST.get("e_otp")
        if org==enter:
            x=register_model()
            x.username=n
            x.email=e
            x.passw=p
            x.save()
            return render(request,'thankureg.html')
        else:
            return render(request,'signup1.html',{'name':n,"email":e,'password':p,'org_otp':org,'err':"OTP doesn't match"})
    else:
        return render(request,'signup.html')    


def fpass(request):
    if(request.method=="POST"):
        e=request.POST.get('email')
        user=register_model.objects.filter(email=e)
        if len(user)>0:
            pw=user[0].passw
            subject="Password"
            message="Welcome! ,Your password is "+str(pw)
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[e]
            send_mail(subject,message,email_from,recipient_list)
            msg="Your password has been sent to your respective gmail account"
            return render(request,'Forgotpassword.html',{'msg':msg})
        else:
            rest="This email id is not registered"
            return render(request,'Forgotpassword.html',{'err':rest})
    else:    
        return render(request,'Forgotpassword.html')

def index(request):
    blogs = Blogs.objects.all()[:3]  
    return render(request,'index.html',{'blogs':blogs})

def contactus(request):
    if request.method=="POST":
        x=contact_model()
        x.name=request.POST.get('Name')
        x.email=request.POST.get('Email')
        x.message=request.POST.get('textarea')
        x.save()
        return render(request,'thanku.html')
    else:    
        return render(request,'contactus.html')
    


def base(request):
    return render(request,'base.html')

def thanku(request):
    return render(request,'thanku.html')

def thankureg(request):
    return render(request,'thankureg.html')

def sidebar(request):
    
    return render(request,'sidebar.html')




# Without google
# def Userprofile(request):
#     if not (request.session.has_key('email')):
#         return redirect('login')  # Redirect to login if not authenticated
#     user=register_model.objects.get(email=request.session['email'])
#     return render(request,'userprofile.html',{'user':user})


# with google
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from .models import register_model

def Userprofile(request):
    user_data = None
    
    if request.user.is_authenticated:
        try:
            # Check if user exists in UserSocialAuth
            user_social = UserSocialAuth.objects.get(user=request.user, provider='google-oauth2')
        except UserSocialAuth.DoesNotExist:
            return redirect('logingoogle')  # Redirect if not authenticated via Google
        
        # Get or create the user in register_model
        user, created = register_model.objects.get_or_create(
            email=request.user.email,
            defaults={'username': request.user.username}
        )
        
        # Prepare user data
        user_data = {
            'username': user.username,
            'email': user.email,
            'phone_no': user.phone_no,
            'Address': user.Address,
            'pincode_no': user.pincode_no,
            'date_of_birth': user.date_of_birth,
            'Bio': user.Bio,
            'image_ed': user.image_ed,
        }

    elif 'email' in request.session:  # Session-based authentication
        try:
            user = register_model.objects.get(email=request.session['email'])
            user_data = {
                'username': user.username,
                'email': user.email,
                'phone_no': user.phone_no,
                'Address': user.Address,
                'pincode_no': user.pincode_no,
                'date_of_birth': user.date_of_birth,
                'Bio': user.Bio,
                'image_ed': user.image_ed,
            }
        except register_model.DoesNotExist:
            return redirect('register')  # Redirect if user not found
    else:
        return redirect('logingoogle')  # Redirect if not authenticated

    return render(request, 'userprofile.html', {'user': user_data})


def error(request):
    return render(request, 'error.html')


# Without google
# def chngepass(request): 
    

#         if request.method=="POST":
#             user=register_model.objects.get(email=request.session['email'])
#             op=request.POST.get('opass')
#             n=request.POST.get('npass')
#             c=request.POST.get('cpass')
#             # user=register_model.objects.filter(passw=op)
#             if user.passw==op:
#                 if(n==c):
#                   user.passw=n
#                   user.save()
#                 else:
#                     err="Password & Confirm Password doesn't match"
#                     return render(request,'changepassword.html',{'err':err}) 
#             else:
#                 err='Invalid Password'  
#                 return render(request,'changepassword.html',{'err':err}) 
            
#             return render(request,'changepassword.html',{'msg':"Password changed successfully"})
#         return render(request,'changepassword.html')
        
# With google
def chngepass(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated and 'email' not in request.session:
        return redirect('logingoogle')  # Redirect to the login page

    # Check if the user logged in via Google
    if request.user.is_authenticated:
        if UserSocialAuth.objects.filter(user=request.user, provider='google-oauth2').exists():
            return render(request, 'error.html', {'message': 'Password change is not available for Google login users.'})

    if request.method == 'POST':
        try:
            # Get user based on session email
            email = request.session.get('email') if 'email' in request.session else request.user.email
            re = register_model.objects.get(email=email)

            op = request.POST.get('opass')
            n = request.POST.get('npass')
            c = request.POST.get('cpass')

            if n == c:
                if op == re.passw:
                    re.passw = n
                    re.save()
                    res = "Password Changed"
                    return render(request, 'changepassword.html', {'msg': res})
                else:
                    res = "Invalid current Password"
                    return render(request, 'changepassword.html', {'err': res})
            else:
                res = "Confirm password and new password don't match"
                return render(request, 'changepassword.html', {'err': res})
        except register_model.DoesNotExist:
            return redirect('logingoogle')  # Redirect if the user is not found
    else:
        return render(request, 'changepassword.html')    


#without google
# def edprf(request):
#    if not (request.session.has_key('email')):
#         return redirect('login')  # Redirect to login if not authenticated
#    user=register_model.objects.get(email=request.session['email'])
#    if request.method=="POST":
#         user.username=request.POST.get('usernam')
#         user.phone_no=request.POST.get('phone')
#         user. Address=request.POST.get('address')
#         user.pincode_no=request.POST.get('pincode')
#         user.date_of_birth=request.POST.get('dob')
#         user.Bio=request.POST.get('about')
#         if 'fs' in request.FILES:
#                 user.image_ed=request.FILES['fs']
#         user.save()
#         return redirect('/uprofile')

#    return render(request,'editprf.html',{'user':user})



from django.shortcuts import render, redirect
from .models import register_model  # Assuming register_model is your custom model
#with google
def edprf(request):
    
    
    # If the user is authenticated via Google, use request.user
    if request.user.is_authenticated:
        user = register_model.objects.get(email=request.user.email)
    else:
        # If the user is authenticated via session, use the email from the session
        user = register_model.objects.get(email=request.session['email'])

    # Handle profile update if the request method is POST
    if request.method == "POST":
        # Update the user's fields from the POST data
        user.username = request.POST.get('usernam')
        user.phone_no = request.POST.get('phone')
        user.Address = request.POST.get('address')
        user.pincode_no = request.POST.get('pincode')
        user.date_of_birth = request.POST.get('dob')
        user.Bio = request.POST.get('about')

        # If a new profile image is uploaded, save it
        if 'fs' in request.FILES:
            user.image_ed = request.FILES['fs']

        # Save the updated user data
        user.save()

        # Redirect to the user profile page after saving the changes
        return redirect('/uprofile')

    # Render the edit profile page with the user's current data
    return render(request, 'editprf.html', {'user': user})



# def logout(request):
#     if not request.session.has_key('email'):
#         return redirect('login')
    
#     del request.session['email']
#     return redirect('login')



    
def sidebar1(request):
    if not (request.user.is_authenticated or request.session.has_key('email')):
        return redirect('login') 
    return render(request,'sidebar1.html') 




def calculators(request):
    return render(request,'calculators.html')







# Bmi

import io
import base64
import matplotlib.pyplot as plt
from django.shortcuts import render
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch

def bmi(request):
   
    if request.method == "POST":
        weight = float(request.POST.get('wht'))
        feet = int(request.POST.get('feet'))
        inches = int(request.POST.get('inches'))

        def calculate_bmi(weight, height_in_meters):
            bmi = weight / (height_in_meters ** 2)
            return round(bmi, 2)

        def bmi_category(bmi):
            if bmi < 18.5:
                return "Underweight"
            elif 18.5 <= bmi <= 24.99:
                return "Normal weight"
            elif 25 <= bmi < 29.9:
                return "Overweight"
            else:
                return "Obese"

        def convert_to_meters(feet, inches):
            total_inches = (feet * 12) + inches
            height_in_meters = total_inches * 0.0254
            return height_in_meters

        # Convert height to meters
        height_in_meters = convert_to_meters(feet, inches)

        # Calculate BMI
        bmi = calculate_bmi(weight, height_in_meters)
        category = bmi_category(bmi)

        # Generate a color-coded vertical BMI graph with a highlighted legend
        categories = ["Underweight", "Normal weight", "Overweight", "Obese"]
        ranges = [18.5, 24.9, 29.9, 40]  # Adjusted ranges for better visual representation

        # Assign colors based on the category
        colors = ['#87CEEB', '#98FB98', '#FFA07A', '#FA8072']  # Lighter and softer colors
        bmi_color = None

        if bmi < 18.5:
            bmi_color = '#87CEEB'  # Color for Underweight
        elif 18.5 <= bmi <= 24.99:
            bmi_color = '#98FB98'  # Color for Normal weight
        elif 25 <= bmi < 29.9:
            bmi_color = '#FFA07A'  # Color for Overweight
        else:
            bmi_color = '#FA8072'  # Color for Obese

        # Adjusted graph size
        fig, ax = plt.subplots(figsize=(6, 5))  # Reduced from (8, 6) to (6, 4)
        
        # Set the background of the figure and axes to be transparent
        fig.patch.set_facecolor('none')
        ax.patch.set_facecolor('none')

        # Plot the category bars with a smaller width
        bar_width = 0.5  # Adjust this value to control the width of the bars
        bars = ax.bar(categories, ranges, color=colors, edgecolor='black', width=bar_width)
        # Plot the user's BMI bar
        user_bmi_bar = ax.bar('Your BMI', bmi, color=bmi_color, edgecolor='black', width=bar_width)

        # Annotate each bar with its range value
        for bar, range_value in zip(bars, ranges):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f"{height:.1f}", ha='center', va='bottom', fontsize=10)

        # Annotate the user's BMI bar
        ax.text('Your BMI', bmi + 0.5, f"{bmi:.2f}", ha='center', va='bottom', fontsize=12, fontweight='bold', color='blue')

        # Customizing the plot
        ax.set_ylabel('BMI Value')
        ax.set_title('BMI Categories and Your BMI')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # Creating a custom legend with a smaller font size
        legend_elements = [
            Patch(color=colors[0], label="Underweight (<18.5)"),
            Patch(color=colors[1], label="Normal weight (18.5 - 24.9)"),
            Patch(color=colors[2], label="Overweight (25 - 29.9)"),
            Patch(color=colors[3], label="Obese (≥30)"),
            Patch(facecolor='lightblue', edgecolor='black', label=f"Your BMI: {bmi}", linestyle='--')  # Highlighted background for user's BMI
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize='small')  # Set the fontsize to 'small'

        plt.tight_layout()

        # Save the graph to a buffer with transparency
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', transparent=True)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # Encode the image to base64 string
        graph = base64.b64encode(image_png).decode('utf-8')

        # Pass the results to the template
        context = {
            'bmi': bmi,
            'category': category,
            'graph': graph,
            'weight': weight,
            'inches': inches,
            'feet': feet
        }
        return render(request, 'bmi_result.html', context)

    return render(request, 'bmi.html')




#Bmr
import io
import numpy as np
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render

def calculate_bmr1(gender, weight, height_cm, age):
    if gender.lower() == 'male':
        bmr = 88.36 + (13.4 * weight) + (4.8 * height_cm) - (5.7 * age)
    elif gender.lower() == 'female':
        bmr = 447.6 + (9.2 * weight) + (3.1 * height_cm) - (4.3 * age)
    else:
        return None  # Return None for invalid gender
    return round(bmr, 2)

def convert_to_cm(feet, inches):
    total_inches = (feet * 12) + inches
    height_cm = total_inches * 2.54
    return height_cm

def bmr_chart(request):
    # Get parameters from GET request with defaults
    gender = request.GET.get('gender', 'male')
    weight = float(request.GET.get('weight', 70))
    height_feet = int(request.GET.get('feet', 5))
    height_inches = int(request.GET.get('inches', 6))
    age = int(request.GET.get('age', 25))

    height_cm = convert_to_cm(height_feet, height_inches)
    bmr = calculate_bmr1(gender, weight, height_cm, age)
    
    if bmr is None:
        return HttpResponse("Invalid gender input. Please enter 'male' or 'female'.", status=400)

    # Create detailed graph
    fig, ax = plt.subplots(figsize=(6, 5))  # Smaller size
    ages = np.arange(10, 101, 5)  # Ages from 10 to 100 in steps of 5
    bmr_values = [calculate_bmr1(gender, weight, height_cm, a) for a in ages]
    
    ax.plot(ages, bmr_values, marker='o', linestyle='-', color='b', label='BMR')
    ax.set_xlabel('Age (years)')
    ax.set_ylabel('BMR (calories/day)')
    ax.grid(True)
    ax.legend()

    # Add a vertical line for the current age
    ax.axvline(age, color='r', linestyle='--', label=f'Current Age: {age}')
    ax.annotate(f'Current Age\nBMR: {bmr}', xy=(age, bmr), xytext=(age + 5, bmr + 100),
                arrowprops=dict(facecolor='black', shrink=0.05))

    # Remove background
    plt.gcf().patch.set_visible(False)
    ax.patch.set_visible(False)

    # Save the graph to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    buffer.seek(0)
    plt.close(fig)

    return HttpResponse(buffer, content_type='image/png')

def bmr(request):
    
    if request.method == 'POST':
        gender = request.POST.get('gender')
        weight = request.POST.get('weight')
        feet = request.POST.get('feet')
        inches = request.POST.get('inches')
        age=int(request.POST.get('age'))

        # Debugging prints
        print(f"Gender: {gender}, Weight: {weight}, Feet: {feet}, Inches: {inches}, Age: {age}")


        # Check if any required field is missing or empty
        if not all([gender, weight, age, feet, inches]):
            return HttpResponse("Please fill in all required fields.", status=400)

        try:
            weight = float(weight)
            age = int(age)
            feet = int(feet)
            inches = int(inches)
        except ValueError:
            return HttpResponse("Invalid input data. Please check the data format.", status=400)

        height_cm = convert_to_cm(feet, inches)
        bmr = calculate_bmr1(gender, weight, height_cm, age) 

        if bmr is None:
            return HttpResponse("Invalid gender input. Please enter 'male' or 'female'.", status=400)

        context = {
            'gender': gender,
            'weight': weight,
            'feet': feet,
            'inches': inches,
            'age': int(age),
            'bmr': bmr,
            'bmr_chart_url': f'/bmr_chart?gender={gender}&weight={weight}&feet={feet}&inches={inches}&age={age}'
        }
        return render(request, 'bmr_result.html', context)

    return render(request, 'bmr.html')



# Calorie Intake Calculator
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render, redirect
from django.http import HttpResponse

def calculate_bmr2(gender, weight, height_feet, height_inches, age):
    total_inches = (height_feet * 12) + height_inches
    height_cm = total_inches * 2.54
    
    if gender.lower() == 'male':
        bmr = 88.36 + (13.4 * weight) + (4.8 * height_cm) - (5.7 * age)
    elif gender.lower() == 'female':
        bmr = 447.6 + (9.2 * weight) + (3.1 * height_cm) - (4.3 * age)
    else:
        return None  # For invalid gender
    return bmr

def calculate_daily_calories(bmr, activity_level):
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'extra active': 1.9
    }
    multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
    return round(bmr * multiplier, 2)

def create_calories_plot(bmr, activity_levels):
    calorie_values = [calculate_daily_calories(bmr, lvl) for lvl in activity_levels]

    fig, ax = plt.subplots(figsize=(6, 4))  # Smaller size
    bars = ax.bar(activity_levels, calorie_values, color=['#4CAF50', '#8BC34A', '#CDDC39', '#FFEB3B', '#FFC107'])
    
    # Add labels and grid
    ax.set_xlabel('Activity Level', fontsize=10)
    ax.set_ylabel('Calories Needed', fontsize=10)
    ax.set_title('Daily Calorie Needs Based on Activity Level', fontsize=12)
    ax.set_ylim(0, max(calorie_values) + 300)  # Adjust y-limit

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right', fontsize=8)
    
    # Add grid lines
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    
    # Remove background and spines
    fig.patch.set_visible(False)
    ax.patch.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 5, f'{height}', ha='center', va='bottom', fontsize=8, color='black')

    # Save plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
    buf.seek(0)
    
    # Encode as base64 string
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return img_str

def calorie_intake(request):
   
    if request.method == 'POST':
        # Retrieve form values
        gender = request.POST.get('gender')
        weight = float(request.POST.get('weight'))
        feet = int(request.POST.get('feet'))
        inches = int(request.POST.get('inches'))
        age = int(request.POST.get('age'))
        level = request.POST.get('level')

        # Check if any required field is missing or empty
        if not all([gender, weight, age, feet, inches, level]):
            return HttpResponse("Please fill in all required fields.", status=400)

        # Convert values to appropriate types
        try:
            weight = float(weight)
            age = int(age)
            level = str(level)
            feet = int(feet)
            inches = int(inches)
        except (ValueError, TypeError):
            return HttpResponse("Invalid input data. Please check the data format.", status=400)

        # Calculate BMR and daily calorie intake
        bmr = calculate_bmr2(gender, weight, feet, inches, age)
        if bmr is None:
            return HttpResponse("Invalid gender specified.", status=400)
        
        daily_calories = calculate_daily_calories(bmr, level)
        
        # Generate plot
        activity_levels = ['sedentary', 'lightly active', 'moderately active', 'very active', 'extra active']
        plot_img = create_calories_plot(bmr, activity_levels)

        # Render the template with the result and plot
        context = {
            'gender': gender,
            'weight': weight,
            'age': age,
            'feet': feet,
            'inches': inches,
            'level': level,
            'bmr': bmr,
            'daily_calories': daily_calories,
            'graph': plot_img,
        }
        return render(request, 'calorieintakeres.html', context)

    # If not POST request, render the form
    return render(request, 'calorieintake.html')



# Ideal Body Weight
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render, redirect
import io
import urllib, base64

def ideal_weight(height_meters):
    min_bmi = 18.5
    max_bmi = 24.9
    
    min_weight = min_bmi * (height_meters ** 2)
    max_weight = max_bmi * (height_meters ** 2)
    
    print(f"Computed Min Weight: {min_weight}, Max Weight: {max_weight}")  # Debug line
    return round(min_weight, 2), round(max_weight, 2)


def convert_to_meters1(feet, inches):
    total_inches = (feet * 12) + inches
    return total_inches * 0.0254

def ideal_body_weight(request):
    if not (request.user.is_authenticated or 'email' in request.session):
        return redirect('login')  # Redirect to login if the user is not authenticated
    if request.method == 'POST':
        try:
            feet = int(request.POST.get('feet'))
            inches = int(request.POST.get('inches'))
            
            height_meters = convert_to_meters1(feet, inches)
            min_weight, max_weight = ideal_weight(height_meters)
            
            print(f"Min Weight: {min_weight}, Max Weight: {max_weight}")  # Debug line

            # Generate the pie chart
            labels = ['Min Weight', 'Max Weight']
            sizes = [min_weight, max_weight]
            colors = ['#00A6D4', '#F0C300']  # Custom slice colors
            explode = (0.05, 0)  # Explode the first slice (Min Weight)

            plt.figure(figsize=(6, 4), facecolor='none')

            # Plot the pie chart
            wedges, texts, autotexts = plt.pie(
                sizes,
                labels=labels,
                colors=colors,
                explode=explode,
                autopct=lambda p: '{:.1f}%'.format(p * sum(sizes) / 100),  # Adjusted format
                shadow=True,
                startangle=120,
                textprops={'color': 'black', 'fontsize': 14},  # Label color set to black
            )

            # Manually set the color of the percentage text to white
            for autotext in autotexts:
                autotext.set_color('white')

            plt.title('Ideal Weight Distribution', fontsize=16, color='darkblue')  # Title color and size

            # Save the plot to a BytesIO object
            buf = io.BytesIO()
            plt.savefig(buf, format='png', transparent=True)
            buf.seek(0)
            string = base64.b64encode(buf.read()).decode('utf-8')
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            buf.close()

            context = {
                'feet': feet,
                'inches': inches,
                'min_weight': min_weight,
                'max_weight': max_weight,
                'graph': uri
            }
            return render(request, 'idealbodyres.html', context)
        except (ValueError, TypeError) as e:
            return HttpResponse(f"Invalid input data. Error: {str(e)}", status=400)
    
    return render(request, 'idealbody.html')





# Hydration calculator
from django.shortcuts import render
from django.http import HttpResponse

def calculate_water_intake(weight_kg, activity_level, climate):
    base_intake = 30  # milliliters per kilogram of body weight

    activity_adjustment = {
        'sedentary': 1.0,
        'lightly active': 1.2,
        'moderately active': 1.4,
        'very active': 1.6,
        'extra active': 1.8
    }

    climate_adjustment = {
        'cool': 1.0,
        'moderate': 1.1,
        'hot': 1.2
    }

    water_intake_ml = weight_kg * base_intake

    activity_multiplier = activity_adjustment.get(activity_level.lower(), 1.0)
    climate_multiplier = climate_adjustment.get(climate.lower(), 1.0)

    water_intake_ml *= activity_multiplier * climate_multiplier

    return round(water_intake_ml / 1000, 2)  # Convert milliliters to liters

def hydration(request):
   
    if request.method == 'POST':
        try:
            weight_kg = float(request.POST.get('weight'))
            activity_level = request.POST.get('level')
            climate = request.POST.get('climate')

            daily_water_intake = calculate_water_intake(weight_kg, activity_level, climate)

            context = {
                'daily_water_intake': daily_water_intake,
                'weight': weight_kg,
                'activity_level': activity_level,
                'climate': climate
            }
            return render(request, 'hydrationres.html', context)
        except (ValueError, TypeError):
            return HttpResponse("Invalid input data. Please check the data format.", status=400)

    return render(request, 'hydration.html')


#Blood Pressure



from django.shortcuts import render
from django.http import HttpResponse

def classify_blood_pressure_by_symptoms(headaches, dizziness, nosebleeds, shortness_of_breath, chest_pain, blurred_vision, fatigue,fainting,nausea,shakiness):
    # Initialize classification
    classification = "Normal"
    
    # Symptoms indicating high blood pressure
    high_blood_pressure_symptoms = [headaches, dizziness, nosebleeds, shortness_of_breath, chest_pain, blurred_vision, fatigue]
    if any(high_blood_pressure_symptoms):
        classification = "High Blood Pressure (Hypertension)"
    
    # Symptoms indicating low blood pressure
    low_blood_pressure_symptoms = [dizziness, fainting, blurred_vision, nausea, fatigue, shakiness]
    if all(low_blood_pressure_symptoms):
        classification = "Low Blood Pressure (Hypotension)"
    
    return classification

def blood_pressure(request):
    
    if request.method == 'POST':
        # Retrieve form values
        headaches = request.POST.get('headaches') == 'on'
        dizziness = request.POST.get('dizziness') == 'on'
        nosebleeds = request.POST.get('nosebleeds') == 'on'
        shortness_of_breath = request.POST.get('shortness_of_breath') == 'on'
        chest_pain = request.POST.get('chest_pain') == 'on'
        blurred_vision = request.POST.get('blurred_vision') == 'on'
        fatigue = request.POST.get('fatigue') == 'on'
        fainting = request.POST.get('fainting') == 'on'
        nausea = request.POST.get('nausea') == 'on'
        shakiness = request.POST.get('shakiness') == 'on'

        # Classify blood pressure based on symptoms
        classification = classify_blood_pressure_by_symptoms(
            headaches, dizziness, nosebleeds, shortness_of_breath, chest_pain, blurred_vision, fatigue,fainting,nausea,
            shakiness
        )

        context = {
            'classification': classification
        }
        return render(request, 'bloodpressres.html', context)

    return render(request, 'bloodpress.html')


# Diabetes
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render, redirect
import io
import urllib, base64

def diabetes_risk(age, bmi, family_history, physical_activity):
    risk_score = 0

    if age >= 45:
        risk_score += 1
    if age >= 65:
        risk_score += 2

    if bmi >= 25:
        risk_score += 2
    if bmi >= 30:
        risk_score += 3

    if family_history.lower() == 'yes':
        risk_score += 2

    if physical_activity.lower() == 'no':
        risk_score += 2

    if risk_score <= 3:
        return "Low risk"
    elif 4 <= risk_score <= 6:
        return "Moderate risk"
    else:
        return "High risk"

def diabetes(request):
    
    if request.method == 'POST':
        try:
            age = int(request.POST.get('age'))
            bmi = float(request.POST.get('bmi'))
            family_history = request.POST.get('fhistory')
            physical_activity = request.POST.get('level')

            risk = diabetes_risk(age, bmi, family_history, physical_activity)

            # Create a bar chart with smaller bars and reduced graph size
            risk_labels = ['Low Risk', 'Moderate Risk', 'High Risk']
            risk_counts = [
                1 if risk == 'Low risk' else 0,
                1 if risk == 'Moderate risk' else 0,
                1 if risk == 'High risk' else 0
            ]

            plt.figure(figsize=(6, 4), facecolor='white')  # Reduced figure size
            bars = plt.bar(risk_labels, risk_counts, color=['#4CAF50', '#FFC107', '#F44336'], edgecolor='black', width=0.3)  # Narrower bars

            plt.xlabel('Risk Level', fontsize=12, color='black')
            plt.ylabel('Count', fontsize=12, color='black')
            plt.title('Diabetes Risk Level', fontsize=16, color='black')

            # Add a legend
            plt.legend(['Risk Level'], loc='upper right', fontsize=10)

            # Add value labels on bars
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, int(yval), ha='center', va='bottom', fontsize=10, color='black')

            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png', transparent=True)
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            buf.close()

            context = {
                'risk': risk,
                'graph': uri
            }
            return render(request, 'diabetesres.html', context)
        except (ValueError, TypeError):
            return HttpResponse("Invalid input data. Please check the data format.", status=400)

    return render(request, 'diabetes.html')







def anxiety(request):
    
    if request.method=="POST":
        ans1=int(request.POST.get("q1"))
        ans2=int(request.POST.get("q2"))
        ans3=int(request.POST.get("q3"))
        ans4=int(request.POST.get("q4"))
        ans5=int(request.POST.get("q5"))
        ans6=int(request.POST.get("q6"))
        ans7=int(request.POST.get("q7"))
        result=ans1+ans2+ans3+ans4+ans5+ans6+ans7
        print(result)
        if result>=0 and result<=9:
            head="Low to mild anxiety severity range"
            msg = """Your score falls into the low to mild range, which means you're doing well. It's great to see that you're managing your mental health effectively. To continue maintaining your well-being, you might find some useful tips, such as practicing mindfulness, staying active, connecting with loved ones, and ensuring you have a balanced routine. Remember, taking care of your mental health is an ongoing process, and these small steps can help you stay on track."""
            color="#008000"
        elif result>=10 and result<=14:
            head="Medium anxiety severity range"  
            msg = """Your score falls into the moderate range, which indicates that you may be experiencing moderate anxiety. This level of anxiety might lead to occasional feelings of worry, restlessness, or difficulty in focusing. While it's not overwhelming, it’s important to pay attention to these signs and take proactive steps to manage them. Consider practicing relaxation techniques, maintaining a healthy lifestyle, or speaking with a mental health professional if needed. Taking care of your mental health is essential for overall well-being."""
            color="#FFA500"
        elif result>=15 and result<=21:
            head="High anxiety severity range"  
            msg = """Your score falls into the high range, which indicates that you may be experiencing a high level of anxiety. This can manifest in various ways, such as constant worry, difficulty in concentrating, physical symptoms like increased heart rate or shortness of breath, and a general feeling of unease. It's important to acknowledge these feelings and consider seeking support from a mental health professional who can help you manage and reduce your anxiety. Remember, taking steps towards your mental well-being is a positive and crucial move."""
            color="#FF0000"
        return render(request,'anxietyres.html',{'head':head,'msg':msg,'color':color})
    else:
        return render(request,'anxietytest.html')


def depression(request):
    
    if request.method=="POST":
        ans1=int(request.POST.get("q1"))
        ans2=int(request.POST.get("q2"))
        ans3=int(request.POST.get("q3"))
        ans4=int(request.POST.get("q4"))
        ans5=int(request.POST.get("q5"))
        ans6=int(request.POST.get("q6"))
        ans7=int(request.POST.get("q7"))
        ans8=int(request.POST.get("q8"))
        ans9=int(request.POST.get("q9"))
        result=ans1+ans2+ans3+ans4+ans5+ans6+ans7+ans8+ans9
        print(result)
        if result>=0 and result<=9:
            head="Low to mild depression severity range"
            msg = """Your score falls into the low to mild range, which means you're doing well. It's great to see that you're managing your mental health effectively. To continue maintaining your well-being, you might find some useful tips, such as practicing mindfulness, staying active, connecting with loved ones, and ensuring you have a balanced routine. Remember, taking care of your mental health is an ongoing process, and these small steps can help you stay on track."""
            color="#008000"
        elif result>=10 and result<=17:
            head="Medium depression severity range"  
            msg = """Your score falls into the moderate range, which indicates that you may be experiencing moderate depression. This level of depression might lead to occasional feelings of sadness, lack of interest, or difficulty in focusing. While it's not overwhelming, it’s important to pay attention to these signs and take proactive steps to manage them. Consider practicing relaxation techniques, maintaining a healthy lifestyle, or speaking with a mental health professional if needed. Taking care of your mental health is essential for overall well-being."""
            color="#FFA500"
        elif result>=15 and result<=27:
            head="High depression severity range"  
            msg = """Your score falls into the high range, which indicates that you may be experiencing a high level of depression. This can manifest in various ways, such as persistent sadness, loss of interest in activities, difficulty concentrating, and a general feeling of hopelessness. It's important to acknowledge these feelings and consider seeking support from a mental health professional who can help you manage and reduce your depression. Remember, taking steps towards your mental well-being is a positive and crucial move ."""
            color="#FF0000"
        return render(request,'depressionres.html',{'head':head,'msg':msg,'color':color})
    else:
        return render(request,'depressiontest.html')    

def drugs(request):
    
     drugs_data=drug_model.objects.all()
     drugs = drug_model.objects.order_by('?')[:15]
     return render(request,'drug.html',{'data':drugs_data,'show':drugs}) 


def supplements(request):
    
    suppl_data=supplement_model.objects.all()
    return render(request,'supplements.html',{'data':suppl_data})

from django.shortcuts import render, get_object_or_404
from healthcareapp.models import drug_model
from healthcareapp.models import supplement_model

def drugshow(request,id):
   
    # Retrieve the drug by its ID
    drug = get_object_or_404(drug_model, id=id)
    context = {'drug': drug}
    return render(request, 'drugshow.html', context)

def supplementshow(request,id):
   
    # Retrieve the drug by its ID
    suppl = get_object_or_404(supplement_model, id=id)
    
    context = {'drug': suppl}
    return render(request, 'supplementshow.html', context)
   
from healthcareapp.models import BodyPart   
from healthcareapp.models import Symptom , Disease 
def body(request):
    bodyparts=BodyPart.objects.all()
    
    return render(request,'body.html',{'bodyparts':bodyparts})

def symptom(request,id):
     bodypartid= get_object_or_404(BodyPart, id=id)
     symptoms=Symptom.objects.filter(body_part=bodypartid)
     return render(request,'symptoms.html',{'symptoms':symptoms,'bodypartid': bodypartid.id})


from django.db.models import Count
def disease_view(request):
    if request.method=="POST":
        selected_symptoms=request.POST.getlist("symptoms")
        if selected_symptoms:
            symptoms=Symptom.objects.filter(pk__in=selected_symptoms)
            diseases=Disease.objects.filter(symptoms__in=symptoms).distinct()
            
           
            return render(request,"disease.html",{"symptoms":symptoms,"diseases":diseases})
    else:
        return render(request,'disease.html')
    

def diseaseanalysis(request):
    return render(request,'diseaseanalysis.html')

def diabkidanalysis(request):
    return render(request,'diabkidanalysis.html')

def neurologanalysis(request):
    return render(request,'neurologanalysis.html')

def digestiveanalysis(request):
    return render(request,'digestiveanalysis.html')

def respiratoryanalysis(request):
    return render(request,'respiratoryanalysis.html')


# Reading Dataset
def readburden():
    data=pd.read_csv("burden-of-disease-by-cause.csv")
    data.rename(columns={'DALYs (Disability-Adjusted Life Years) - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Cardiovascular disease',
                     'DALYs (Disability-Adjusted Life Years) - Diabetes and kidney diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Diabetes and kidney diseases',
                     'DALYs (Disability-Adjusted Life Years) - Mental disorders - Sex: Both - Age: All Ages (Number)':'Burden of Mental disorders',
                     'DALYs (Disability-Adjusted Life Years) - Digestive diseases - Sex: Both - Age: All Ages (Number)':'Burden of Digestive diseases',
                     'DALYs (Disability-Adjusted Life Years) - Chronic respiratory diseases - Sex: Both - Age: All Ages (Number)':'Burden of Chronic respiratory diseases',
                     'DALYs (Disability-Adjusted Life Years) - Neurological disorders - Sex: Both - Age: All Ages (Number)':'Burden of Neurological disorders'}, inplace=True)
    return data


# Cardivascular disease
def cardio1(request):
    data = pd.read_csv("burden-of-disease-by-cause.csv")
    data.rename(columns={
        'DALYs (Disability-Adjusted Life Years) - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Cardiovascular disease',
        'DALYs (Disability-Adjusted Life Years) - Diabetes and kidney diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Diabetes and kidney diseases',
        'DALYs (Disability-Adjusted Life Years) - Mental disorders - Sex: Both - Age: All Ages (Number)': 'Burden of Mental disorders',
        'DALYs (Disability-Adjusted Life Years) - Digestive diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Digestive diseases',
        'DALYs (Disability-Adjusted Life Years) - Chronic respiratory diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Chronic respiratory diseases',
        'DALYs (Disability-Adjusted Life Years) - Neurological disorders - Sex: Both - Age: All Ages (Number)': 'Burden of Neurological disorders'}, inplace=True)
    
    entity = data["Entity"].drop_duplicates().tolist()
    
    if request.method == "POST":
        n = request.POST.get('country')
        df = data[data["Entity"] == n]
        
        # Creating the line graph for Cardiovascular disease burden
        fig = px.line(df, x="Year", y="Burden of Cardiovascular disease", markers=True,
                      title=f"Burden of Cardiovascular diseases in {n}",
                      labels={"Entity": "Country", "Cardiovascular diseases": "Total DALYs"})
        
        fig.update_traces(line_color='rgba(0, 0, 255, 0.5)')
        fig.update_layout(
            xaxis_title="Year", 
            yaxis_title="Cardiovascular diseases Burden",
            plot_bgcolor='rgba(245, 245, 220, 0)', 
            title_font_size=20,
            title_x=0.5, 
            height=500, 
            # width=800,
            yaxis=dict(showgrid=True, gridcolor='LightGray'),
            font=dict(family="Arial", size=14),
            hoverlabel=dict(font_size=14, font_color="white")
        )
        graph = fig.to_html()
        return render(request, 'cardio1.html', {'graph': graph, 'entity': entity})
    
    else:
        return render(request, 'cardio1.html', {'entity': entity})

def cardio2(request):
    data=pd.read_csv("burden-of-disease-by-cause.csv")
    data.rename(columns={'DALYs (Disability-Adjusted Life Years) - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Cardiovascular disease',
                     'DALYs (Disability-Adjusted Life Years) - Diabetes and kidney diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Diabetes and kidney diseases',
                     'DALYs (Disability-Adjusted Life Years) - Mental disorders - Sex: Both - Age: All Ages (Number)':'Burden of Mental disorders',
                     'DALYs (Disability-Adjusted Life Years) - Digestive diseases - Sex: Both - Age: All Ages (Number)':'Burden of Digestive diseases',
                     'DALYs (Disability-Adjusted Life Years) - Chronic respiratory diseases - Sex: Both - Age: All Ages (Number)':'Burden of Chronic respiratory diseases',
                     'DALYs (Disability-Adjusted Life Years) - Neurological disorders - Sex: Both - Age: All Ages (Number)':'Burden of Neurological disorders'}, inplace=True)
    print(data)
    n=data["Year"].drop_duplicates().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        print(year)
        print(data)
        df=data[(data["Year"]==year) & (data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]
        print(df)
        # top 10 Countries with highest Cardiovascular diseases
        df=df.nlargest(10,"Burden of Cardiovascular disease")
        fig=px.bar(df,x="Entity",y="Burden of Cardiovascular disease",
                    title=f"Top 10 Countries with Highest Cardiovascular Diseases in {year}")
        fig.update_layout(yaxis_title="Cardiovascular Disease", xaxis_title="Countries", plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
                paper_bgcolor='rgba(242, 240, 239, 0)',hoverlabel=dict(font_size=14,font_color="white"),height=500)
        graph=fig.to_html()
        return render(request,'cardio2.html',{'graph':graph,'n':n})
    return render(request,'cardio2.html',{'n':n})    

def cardio3(request):
    data=pd.read_csv("burden-of-disease-by-cause.csv")
    data.rename(columns={'DALYs (Disability-Adjusted Life Years) - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Cardiovascular disease',
                     'DALYs (Disability-Adjusted Life Years) - Diabetes and kidney diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Diabetes and kidney diseases',
                     'DALYs (Disability-Adjusted Life Years) - Mental disorders - Sex: Both - Age: All Ages (Number)':'Burden of Mental disorders',
                     'DALYs (Disability-Adjusted Life Years) - Digestive diseases - Sex: Both - Age: All Ages (Number)':'Burden of Digestive diseases',
                     'DALYs (Disability-Adjusted Life Years) - Chronic respiratory diseases - Sex: Both - Age: All Ages (Number)':'Burden of Chronic respiratory diseases',
                     'DALYs (Disability-Adjusted Life Years) - Neurological disorders - Sex: Both - Age: All Ages (Number)':'Burden of Neurological disorders'}, inplace=True)
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=request.POST.get('year')
        df = data.query(f"Year == {year}")

     # Create the choropleth map
        fig = go.Figure(data=go.Choropleth(
        locations = df['Code'],
        z = df['Burden of Cardiovascular disease'],
        text = df['Entity'],
        colorscale = 'pinkyl',
        # autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        # title = 'Cardiovascular Disease Burden',
        ))
        fig.update_layout(
                title_text='Burden of Cardiovascular Disease by Country',  # Add your title here
            title_x=0.5,
             title_y=0.92, 
             title_font=dict(
                size=25,  # Set the font size
                color='darkblue'  # Change the color of the title
            ),
                height=630,  # Set the height as desired
            )
        
        graph=fig.to_html()
        return render(request,'cardio3.html',{'graph':graph,'nyear':nyear})
    return render(request,'cardio3.html',{'nyear':nyear})

def cardio4(request):
    data=pd.read_csv("burden-of-disease-by-cause.csv")
    data.rename(columns={'DALYs (Disability-Adjusted Life Years) - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Cardiovascular disease',
                     'DALYs (Disability-Adjusted Life Years) - Diabetes and kidney diseases - Sex: Both - Age: All Ages (Number)': 'Burden of Diabetes and kidney diseases',
                     'DALYs (Disability-Adjusted Life Years) - Mental disorders - Sex: Both - Age: All Ages (Number)':'Burden of Mental disorders',
                     'DALYs (Disability-Adjusted Life Years) - Digestive diseases - Sex: Both - Age: All Ages (Number)':'Burden of Digestive diseases',
                     'DALYs (Disability-Adjusted Life Years) - Chronic respiratory diseases - Sex: Both - Age: All Ages (Number)':'Burden of Chronic respiratory diseases',
                     'DALYs (Disability-Adjusted Life Years) - Neurological disorders - Sex: Both - Age: All Ages (Number)':'Burden of Neurological disorders'}, inplace=True)
    
    nyear = data["Year"].drop_duplicates().to_list()

    if request.method == "POST":
        start_year = int(request.POST.get('start_year'))
        end_year = int(request.POST.get('end_year'))

        # Server-side validation
        if start_year >= end_year:
            error_message = "Start year cannot be greater than or equal to End year."
            return render(request, 'cardio4.html', {'year1': nyear, 'year2': nyear, 'error': error_message})

        df_filtered = data[(data["Year"] >= start_year) &
                           (data["Year"] <= end_year) &
                           (data["Code"].notnull()) &
                           (~data["Entity"].isin(["World", "G20"]))]

        df_grouped = df_filtered.groupby("Entity", as_index=False).agg({
            "Burden of Cardiovascular disease": "sum"
        })

        df_top10 = df_grouped.sort_values(by="Burden of Cardiovascular disease", ascending=False).head(10)

        # Pie chart
        fig = px.pie(df_top10,
                     values="Burden of Cardiovascular disease",
                     names="Entity",
                     title=f"Top 10 Countries by DALYs (Cardiovascular Diseases) from {start_year} to {end_year}",
                     color="Entity",
                     color_discrete_sequence=px.colors.sequential.Plasma)
        fig.update_layout(height=600,title_x=0.5,title_font=dict(
                size=18,  # Set the font size
                color='darkblue'  # Change the color of the title
            ),)

        fig.update_traces(textinfo='percent+label')
        graph = fig.to_html()

        return render(request, 'cardio4.html', {'graph': graph, 'year1': nyear, 'year2': nyear})

    return render(request, 'cardio4.html', {'year1': nyear, 'year2': nyear})

def cardio5(request):
    data=readburden()
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=int(request.POST.get("year"))
        df=data[(data["Year"]==year) & (data["Code"].isnull()) & (~data["Entity"].isin(["World","G20"]))]
        fig=px.bar(df,x="Entity",y="Burden of Cardiovascular disease",color="Entity")
        fig.update_layout(xaxis_title="Region",yaxis_title="Burden of Cardiovascular disease",hoverlabel=dict(font_size=14,font_color="white"),
                            plot_bgcolor='rgba(242, 240, 239, 0)',height=630)
        graph=fig.to_html()
        return render(request, 'cardio5.html',{'graph':graph,'nyear':nyear})
    return render(request,'cardio5.html',{'nyear':nyear})

def cardio6(request):
    data=readburden()
    entity=data["Entity"].drop_duplicates().to_list()
    if request.method=="POST":
        countries=request.POST.getlist('country[]')
        # Filter the data for the specified countries
        df = data[data["Entity"].isin(countries)]

        # Get the minimum and maximum years in the dataset
        min_year = df['Year'].min()
        max_year = 2019

        # Create a scatter plot with lines
        fig = px.scatter(df,
                        x="Year",
                        y="Burden of Cardiovascular disease",
                        color="Entity",  # Different colors for each country
                        title="Comparison of DALYs for Cardiovascular Diseases Over Time",
                        labels={
                            "Entity": "Country",
                            "Year": "Year",
                            "DALYs (Disability-Adjusted Life Years) - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)": "Total DALYs"
                        })

        # Add lines between points
        fig.update_traces(mode='lines+markers', marker=dict(size=5), line_shape='linear')

        # Add the range slider
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Total DALYs",
            title_x=0.5,  # Center the title
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            paper_bgcolor='rgba(0, 0, 0, 0)'
              ,height=450  ,
            xaxis=dict(
                range=[min_year, max_year],  # Set the range based on the available data
                rangeslider=dict(visible=True),  # Enable range slider
                type="linear"
            ),hoverlabel=dict(font_size=14,font_color="white")
        )
        graph=fig.to_html()
        return render(request,'cardio6.html',{'graph':graph,'entity':entity})

    return render(request,'cardio6.html',{'entity':entity})

def cardio7(request):
        data=readburden()
        filtered_data = data[(data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]

        # Step 2: Group the data by Year and Entity to get the total burden per country
        country_burden = filtered_data.groupby(['Year', 'Entity'], as_index=False).agg({'Burden of Cardiovascular disease': 'sum'})

        # Step 3: Calculate the total burden for each year
        total_burden_per_year = country_burden.groupby('Year', as_index=False).agg({'Burden of Cardiovascular disease': 'sum'})
        total_burden_per_year.rename(columns={'Burden of Cardiovascular disease': 'TotalBurden'}, inplace=True)

        # Step 4: Merge to get the total burden alongside each country's burden
        merged_df = pd.merge(country_burden, total_burden_per_year, on='Year')

        # Step 5: Calculate the percentage contribution
        merged_df['PercentageContribution'] = (merged_df['Burden of Cardiovascular disease'] / merged_df['TotalBurden']) * 100

        # Step 6: Get the top 20 countries by total burden
        top_countries = merged_df.groupby('Entity')['Burden of Cardiovascular disease'].sum().nlargest(20).index
        top_20_data = merged_df[merged_df['Entity'].isin(top_countries)]

        # Step 7: Create the sunburst chart
        fig = px.sunburst(
            top_20_data,
            path=['Year', 'Entity'],
            values='PercentageContribution',
            title='Percentage Contribution of Cardiovascular Disease Burden by Top 20 Countries per Year',
            labels={
                'PercentageContribution': 'Percentage Contribution (%)',
                'labels':'Year'

            },

        )

        fig.update_traces(
            hovertemplate='<b>Year:</b> %{label}<br>Percentage Contribution:</b> %{value:.2f}%<extra></extra>',
            insidetextorientation='radial'
        )
        # Update layout for better visual appeal
        fig.update_layout(
            title_x=0.5,  # Center the title
            width=1000,   # Set the desired width
        height=670    # Set the desired height
        ,plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
            paper_bgcolor='rgba(0,0,0,0)',
            title_font=dict(
                    size=20,  # Set the font size
                    color='darkblue'  # Change the color of the title
                )
    )
        graph=fig.to_html()
        return render(request,'cardio7.html',{'graph':graph})


#Diabetic Kidney Disease
def diab1(request):
        data=readburden()
        entity = data["Entity"].drop_duplicates().tolist()
    
        if request.method == "POST":
            n = request.POST.get('country')
            df = data[data["Entity"] == n]

            # Create an area chart
            fig = px.area(
                df,
                x="Year",
                y="Burden of Diabetes and kidney diseases",
                title=f"Burden of Diabetes and Kidney Diseases in {n}",
                markers=True  # Adding markers for each data point
            )

            # Updating trace and layout for better aesthetics
            fig.update_traces(
                line_color='rgba(0, 0, 255, 0.7)',  # A more opaque line color
                fillcolor='rgba(0, 0, 255, 0.2)',   # Lighter fill color for contrast
                marker=dict(
                    size=5,
                    color='rgba(0, 0, 255, 0.9)',  # Light blue marker background
                    line=dict(width=2, color='rgba(0, 0, 255, 0.7)')  # Blue marker outline
                ),
            )

            # Add annotation for significant data points (optional)
            max_burden_year = df[df["Burden of Diabetes and kidney diseases"] == df["Burden of Diabetes and kidney diseases"].max()]["Year"].values[0]
            max_burden_value = df["Burden of Diabetes and kidney diseases"].max()

            fig.add_annotation(
                x=max_burden_year,
                y=max_burden_value,
                text="Highest Burden",
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-40,
                font=dict(size=12, color="black"),
                bgcolor="rgba(255, 255, 255, 0.7)",
                bordercolor="blue"
            )

            # Customize the layout for aesthetics and readability
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Diabetes and kidney diseases burden",
                plot_bgcolor='rgba(245, 245, 220, 0)',  # Light beige background
                title_font_size=18,
                title_x=0.5,
                height=500,
                yaxis=dict(showgrid=True, gridcolor='LightGray'),
                xaxis=dict(showgrid=False, tickmode='linear', dtick=5),  # Limit years shown (show every 5th year)
                font=dict(family="Arial", size=14),
                hoverlabel=dict(font_size=14, font_color="white"),
                hovermode="closest"  # Standard hover (remove x unified)
            )

            # Adding a vertical line to highlight the year with the maximum burden
            fig.add_vline(
                x=max_burden_year,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Peak in {max_burden_year}",
                annotation_position="top"
            )

            # Add color gradient to the area for better visualization
            fig.update_traces(
                fillcolor='rgba(0, 0, 255, 0.3)',
                line_shape='spline'  # Smooth curve
            )

            graph = fig.to_html()
            return render(request, 'diab1.html', {'graph': graph, 'entity': entity})
    
        else:
            return render(request, 'diab1.html', {'entity': entity})

def diab2(request):
    data=readburden()
    n=data["Year"].drop_duplicates().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        df = data[(data["Year"] == year) & (data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]

        # Get top 10 countries
        df = df.nlargest(10, "Burden of Diabetes and kidney diseases")

        # Create the bar chart
        fig = px.bar(
            df,
            x="Entity",
            y="Burden of Diabetes and kidney diseases",  # Make sure the y-axis reflects the correct metric
            title=f"Top 10 Countries with Highest Burden of Diabetes and Kidney Diseases in {year}",
            # text="Burden of Diabetes and kidney diseases"  # Display the values on the bars
        )

        # Update bar colors with a gradient
        fig.update_traces(marker=dict(
            color=df['Burden of Diabetes and kidney diseases'],  # Color based on burden values
            colorscale='purp',  # Choose a color scale
            showscale=True  # Optional: Show color scale
        ))

        # Update layout for aesthetics
        fig.update_layout(
            yaxis_title="Diabetes and Kidney Diseases Burden",
            xaxis_title="Countries",
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
            paper_bgcolor='rgba(242, 240, 239, 0)',  # Transparent paper background
            hoverlabel=dict(font_size=14, font_color="white"),
            title_font_size=20,
            title_x=0.5,height=500
        )

        graph=fig.to_html()
        return render(request,'diab2.html',{'graph':graph,'n':n})
    return render(request,'diab2.html',{'n':n})  

def diab3(request):
    data=readburden()
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=request.POST.get('year')
         # Filter the data for the specified year
        df = data.query(f"Year == {year}")

        fig = go.Figure(data=go.Choropleth(
            locations=df['Code'],  # Country codes
            z=df['Burden of Diabetes and kidney diseases'],  # Values for the choropleth
            text=df['Entity'],  # Country names for hover text
            colorscale = [
        "#E6E6FA",  # Light Lavender
        "#9B59B6",  # Medium Purple
        "#9966CC",  # Amethyst
        "#7B68EE",  # Dark Lavender
        "#663399",  # Rebecca Purple
        "#DDA0DD",  # Plum

    ],  # Lavender shades
            reversescale=False,  # Change to True if you want to reverse the color scale
            marker_line_color='darkgray',  # Border color for countries
            marker_line_width=0.5,  # Border width
            # colorbar_title='Diabetes and Kidney Disease Burden',  # Title for the color bar
        ))

        fig.update_layout(
            title_text=f"Burden of Diabetes and Kidney Diseases in {year}",
            geo=dict(
                showcoastlines=True,
                coastlinecolor='Black',
                projection_type='natural earth',  # Natural Earth projection
            ),height=600,title_x=0.5
        )

        graph=fig.to_html()
        return render(request,'diab3.html',{'graph':graph,'nyear':nyear})
    return render(request,'diab3.html',{'nyear':nyear})

def diab4(request):
    data=readburden()
    nyear = data["Year"].drop_duplicates().to_list()

    if request.method == "POST":
        start_year = int(request.POST.get('start_year'))
        end_year = int(request.POST.get('end_year'))
        # Data filtering and grouping
        df_filtered = data[(data["Year"] >= start_year) &
                        (data["Year"] <= end_year) &
                        (data["Code"].notnull()) &
                        (~data["Entity"].isin(["World", "G20"]))]

        df_grouped = df_filtered.groupby("Entity", as_index=False).agg({
            "Burden of Diabetes and kidney diseases": "sum"
        })

        # Rename the aggregated column for clarity
        df_grouped.rename(columns={"Burden of Diabetes and kidney diseases": "Total Burden"}, inplace=True)

        # Sort and get the top 10 countries
        df_top10 = df_grouped.sort_values(by="Total Burden", ascending=False).head(10)

        # Create a bubble chart
        fig = px.scatter(df_top10,
                        x="Entity",
                        y="Total Burden",
                        size="Total Burden",  # Bubble size based on total burden
                        title=f"Top 10 Countries by DALYs (Diabetes and Kidney Diseases) from {start_year} to {end_year}",
                        color="Total Burden",
                        color_continuous_scale=["#E6E6FA", "#9370DB", "#8A2BE2", "#4B0082"],

                        size_max=60)  # Adjust maximum bubble size

        # Update layout for aesthetics
        fig.update_layout(
            xaxis_title="Country",
            yaxis_title="Total Burden of Diabetes and Kidney Diseases",
            title_font_size=16,
            title_x=0.5,
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent background
            height=600
        )
        graph = fig.to_html()

        return render(request, 'diab4.html', {'graph': graph, 'year1': nyear, 'year2': nyear})

    return render(request, 'diab4.html', {'year1': nyear, 'year2': nyear})

def diab5(request):
    data=readburden()
    entity=data["Entity"].drop_duplicates().to_list()
    if request.method=="POST":
        countries=request.POST.getlist('country[]')
        # Filter the data for the specified countries
        df = data[data["Entity"].isin(countries)]

        # Get the minimum and maximum years in the dataset
        min_year = df['Year'].min()
        max_year = 2019

        # Create a scatter plot with lines
        fig = px.area(df,
                x="Year",
                y="Burden of Diabetes and kidney diseases",
                color="Entity",
                title="Cumulative Burden of Diabetes and Kidney Diseases Over Time",
                labels={
                    "Entity": "Country",
                    "Year": "Year",
                })


        # Add lines between points
        fig.update_traces(mode='lines+markers', marker=dict(size=5), line_shape='linear')

        # Add the range slider
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Total DALYs",
            title_x=0.5,  # Center the title
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            xaxis=dict(
                range=[min_year, max_year],  # Set the range based on the available data
                rangeslider=dict(visible=True),  # Enable range slider
                type="linear"
            ),hoverlabel=dict(font_size=14,font_color="white")
        )

        graph=fig.to_html()
        return render(request,'diab5.html',{'graph':graph,'entity':entity})

    return render(request,'diab5.html',{'entity':entity})

def diab6(request):
    data=readburden()
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=int(request.POST.get("year"))
        df = data[(data["Year"] == year) & (data["Code"].isnull()) & (~data["Entity"].isin(["World", "G20"]))]

        # Create a treemap
        fig = px.sunburst(
            df,
            path=['Entity'],  # Define the hierarchy (in this case, only regions)
            values='Burden of Diabetes and kidney diseases',
            title=f"Burden of Diabetes and Kidney Diseases by Region in {year}",
            color='Burden of Diabetes and kidney diseases',  # Color by burden values
            color_continuous_scale='Blues',
            labels={
                'Entity': 'Region',  # Ensure the key matches the DataFrame column
                'Burden of Diabetes and kidney diseases': 'Burden'
            }
        )

        fig.update_traces(
            hovertemplate='<b>Region:</b> %{label}<br><b>Burden:</b> %{value}<extra></extra>'
        )

        # Update layout for aesthetics
        fig.update_layout(
            title_font_size=20,
            title_x=0.5,
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
            height=600
        )

        graph=fig.to_html()
        return render(request, 'diab6.html',{'graph':graph,'nyear':nyear})
    return render(request,'diab6.html',{'nyear':nyear})

def diab7(request):
        data = readburden()  # Reading the data
        # Filter the data
        filtered_data = data[(data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]

        # Group the data by Year and Entity to get the total burden per country
        country_burden = filtered_data.groupby(['Year', 'Entity'], as_index=False).agg({'Burden of Diabetes and kidney diseases': 'sum'})

        # Calculate the total burden for each year
        total_burden_per_year = country_burden.groupby('Year', as_index=False).agg({'Burden of Diabetes and kidney diseases': 'sum'})
        total_burden_per_year.rename(columns={'Burden of Diabetes and kidney diseases': 'TotalBurden'}, inplace=True)

        # Merge to get the total burden alongside each country's burden
        merged_df = pd.merge(country_burden, total_burden_per_year, on='Year')

        # Calculate the percentage contribution
        merged_df['PercentageContribution'] = (merged_df['Burden of Diabetes and kidney diseases'] / merged_df['TotalBurden']) * 100

        # Get the top 20 countries by total burden
        top_countries = merged_df.groupby('Entity')['Burden of Diabetes and kidney diseases'].sum().nlargest(20).index
        top_20_data = merged_df[merged_df['Entity'].isin(top_countries)]

        # Create the treemap chart
        fig = px.treemap(
            top_20_data,
            path=['Year', 'Entity'],
            values='PercentageContribution',
            title='Percentage Contribution of Diabetes and kidney <br> diseases Burden by Top 20 Countries per Year',
            labels={
                'PercentageContribution': 'Percentage Contribution (%)',
                'labels': 'Year'
            }
        )

        fig.update_traces(
            hovertemplate='<b>Year:</b> %{label}<br>Percentage Contribution:</b> %{value:.2f}%<extra></extra>'
        )
        # Update layout to make the chart responsive
        fig.update_layout(
            height=600,
            title_x=0.5,
            width=1000
        )
        graph = fig.to_html()
        return render(request, 'diab7.html', {'graph': graph})


# Neurological     
def neuro1(request):
    data=readburden()
    entity=data["Entity"].drop_duplicates().tolist()
    if request.method=="POST":
        n=request.POST.get('country')
        df = data[data["Entity"] == n]

        # Create an area chart
        fig = px.area(
            df,
            x="Year",
            y="Burden of Neurological disorders",
            title=f"Burden of Neurological disorders in {n}",
            markers=True  # Adding markers for each data point
        )

        # Updating trace and layout for better aesthetics
        fig.update_traces(
            line_color='rgba(0, 0, 255, 0.7)',  # A more opaque line color
            fillcolor='rgba(0, 0, 255, 0.2)',   # Lighter fill color for contrast
            marker=dict(
                size=5,
                color='rgba(0, 0, 255, 0.9)',  # Light blue marker background
                line=dict(width=2, color='rgba(0, 0, 255, 0.7)')  # Blue marker outline
            ),
        )

        # Add annotation for significant data points (optional)
        max_burden_year = df[df["Burden of Neurological disorders"] == df["Burden of Neurological disorders"].max()]["Year"].values[0]
        max_burden_value = df["Burden of Neurological disorders"].max()

        fig.add_annotation(
            x=max_burden_year,
            y=max_burden_value,
            text="Highest Burden",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
            font=dict(size=12, color="black"),
            bgcolor="rgba(255, 255, 255, 0.7)",
            bordercolor="blue"
        )

        # Customize the layout for aesthetics and readability
        fig.update_layout(
            
            xaxis_title="Year",
            yaxis_title="Neurological disorders burden",
            plot_bgcolor='rgba(245, 245, 220, 0)',  # Light beige background
            title_font_size=25,
            title_x=0.5,
            yaxis=dict(showgrid=True, gridcolor='LightGray'),
            xaxis=dict(showgrid=False, tickmode='linear', dtick=5),  # Limit years shown (show every 5th year)
            font=dict(family="Arial", size=14),
            hoverlabel=dict(font_size=14, font_color="white"),
            hovermode="closest" , # Standard hover (remove x unified)
        
        )

        # Adding a vertical line to highlight the year with the maximum burden
        fig.add_vline(
            x=max_burden_year,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Peak in {max_burden_year}",
            annotation_position="top"
        )

        # Add color gradient to the area for better visualization
        fig.update_traces(
            fillcolor='rgba(0, 0, 255, 0.3)',
            line_shape='spline'  # Smooth curve
        )

        graph = fig.to_html(full_html=False, config={"responsive": True})

        return render(request,'neuro1.html',{'graph':graph,'entity':entity})
    return render(request,'neuro1.html',{'entity':entity})
    
def neuro2(request):
    data=readburden()
    n=data["Year"].drop_duplicates().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        df = data[(data["Year"] == year) & (data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]
            # Get top 10 countries
        df = df.nlargest(10, "Burden of Neurological disorders")

        # Create the bar chart
        fig = px.bar(
            df,
            x="Entity",
            y="Burden of Neurological disorders",  # Make sure the y-axis reflects the correct metric
            title=f"Top 10 Countries with Highest Burden of Neurological disorders in {year}",
            # text="Burden of Diabetes and kidney diseases"  # Display the values on the bars
        )

        # Update bar colors with a gradient
        fig.update_traces(marker=dict(
            color=df['Burden of Neurological disorders'],  # Color based on burden values
            colorscale='purp',  # Choose a color scale
            showscale=True  # Optional: Show color scale
        ))

        # Update layout for aesthetics
        fig.update_layout(
            yaxis_title="Neurological disorders Burden",
            xaxis_title="Countries",
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
            paper_bgcolor='rgba(242, 240, 239, 0)',  # Transparent paper background
            hoverlabel=dict(font_size=14, font_color="white"),
            title_font_size=16,
            title_x=0.5
        )

        graph=fig.to_html()
        return render(request,'neuro2.html',{'graph':graph,'n':n})
    return render(request,'neuro2.html',{'n':n})

def neuro3(request):
    data=readburden()
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=request.POST.get('year')
        # Filter the data for the specified year
        df = data.query(f"Year == {year}")

        # Create the choropleth map
        fig = go.Figure(data=go.Choropleth(
        locations = df['Code'],
        z = df['Burden of Neurological disorders'],
        text = df['Entity'],
        colorscale = 'purples',
        # autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        # colorbar_title = 'Neurological disorders Burden' 
        )
        )

        fig.update_layout(
                title_text='Burden of Cardiovascular Disease by Country',  # Add your title here
            title_x=0.5,
             title_y=0.92, 
             title_font=dict(
                size=25,  # Set the font size
                color='darkblue'  # Change the color of the title
            ),
                height=600,  # Set the height as desired
            )
        graph=fig.to_html()
        return render(request,'neuro3.html',{'graph':graph,'nyear':nyear})
    return render(request,'neuro3.html',{'nyear':nyear})

def neuro4(request):
    data=readburden()
    nyear = data["Year"].drop_duplicates().to_list()

    if request.method == "POST":
        start_year = int(request.POST.get('start_year'))
        end_year = int(request.POST.get('end_year'))
            # Data filtering and grouping
        df_filtered = data[(data["Year"] >= start_year) &
                        (data["Year"] <= end_year) &
                        (data["Code"].notnull()) &
                        (~data["Entity"].isin(["World", "G20"]))]

        df_grouped = df_filtered.groupby("Entity", as_index=False).agg({
            "Burden of Neurological disorders": "sum"
        })

        # Rename the aggregated column for clarity
        df_grouped.rename(columns={"Burden of Neurological disorders": "Total Burden"}, inplace=True)

        # Sort and get the top 10 countries
        df_top10 = df_grouped.sort_values(by="Total Burden", ascending=False).head(10)

        # Create a bubble chart
        fig = px.scatter(df_top10,
                        x="Entity",
                        y="Total Burden",
                        size="Total Burden",  # Bubble size based on total burden
                        title=f"Top 10 Countries by DALYs (Neurological disorders) from {start_year} to {end_year}",
                        color="Total Burden",
                        color_continuous_scale=["#E6E6FA", "#9370DB", "#8A2BE2", "#4B0082"],

                        size_max=60)  # Adjust maximum bubble size

        # Update layout for aesthetics
        fig.update_layout(
            xaxis_title="Country",
            yaxis_title="Total Burden of Neurological disorders",
            title_font_size=16,
            title_x=0.5,
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent background
            height=600
        )
        graph = fig.to_html()

        return render(request, 'neuro4.html', {'graph': graph, 'year1': nyear, 'year2': nyear})

    return render(request, 'neuro4.html', {'year1': nyear, 'year2': nyear})
      
def neuro5(request):
    data=readburden()
    entity=data["Entity"].drop_duplicates().to_list()
    if request.method=="POST":
        countries=request.POST.getlist('country[]')
       
            # Filter the data for the specified countries
        df = data[data["Entity"].isin(countries)]

        # Get the minimum and maximum years in the dataset
        min_year = df['Year'].min()
        max_year = 2019

        # Create a scatter plot with lines
        fig = px.area(df,
                x="Year",
                y="Burden of Neurological disorders",
                color="Entity",
                title="Cumulative Burden of Neurological disorders Over Time",
                labels={
                    "Entity": "Country",
                    "Year": "Year",
                })


        # Add lines between points
        fig.update_traces(mode='lines+markers', marker=dict(size=5), line_shape='linear')

        # Add the range slider
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Total DALYs",
            title_x=0.5,  # Center the title
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            xaxis=dict(
                range=[min_year, max_year],  # Set the range based on the available data
                rangeslider=dict(visible=True),  # Enable range slider
                type="linear"
            ),hoverlabel=dict(font_size=14,font_color="white")
        )
        graph=fig.to_html()
        return render(request,'neuro5.html',{'graph':graph,'entity':entity})

    return render(request,'neuro5.html',{'entity':entity})

def neuro6(request):
    data=readburden()
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=int(request.POST.get("year"))
        df = data[(data["Year"] == year) & (data["Code"].isnull()) & (~data["Entity"].isin(["World", "G20"]))]

        # Create a treemap
        fig = px.sunburst(
            df,
            path=['Entity'],  # Define the hierarchy (in this case, only regions)
            values='Burden of Neurological disorders',
            title=f"Burden of Neurological disorders by Region in {year}",
            color='Burden of Neurological disorders',  # Color by burden values
            color_continuous_scale='purples'  ,
            labels={
                'Entity': 'Region',  # Ensure the key matches the DataFrame column
                'Burden of Neurological disorders ': 'Burden'
            }
        )

        fig.update_traces(
            hovertemplate='<b>Region:</b> %{label}<br><b>Burden:</b> %{value}<extra></extra>'
        )

        # Update layout for aesthetics
        fig.update_layout(
            title_font_size=20,
            title_x=0.5,
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
            height=600
        )
        graph=fig.to_html()
        return render(request, 'neuro6.html',{'graph':graph,'nyear':nyear})
    return render(request,'neuro6.html',{'nyear':nyear})

def neuro7(request):
    data = readburden()  # Reading the data
    # Step 1: Filter the data to exclude non-country entries
    filtered_data = data[(data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]

    # Step 2: Group the data by Year and Entity to get the total burden per country
    country_burden = filtered_data.groupby(['Year', 'Entity'], as_index=False).agg({'Burden of Neurological disorders': 'sum'})

    # Step 3: Calculate the total burden for each year
    total_burden_per_year = country_burden.groupby('Year', as_index=False).agg({'Burden of Neurological disorders': 'sum'})
    total_burden_per_year.rename(columns={'Burden of Neurological disorders': 'TotalBurden'}, inplace=True)

    # Step 4: Merge to get the total burden alongside each country's burden
    merged_df = pd.merge(country_burden, total_burden_per_year, on='Year')

    # Step 5: Calculate the percentage contribution
    merged_df['PercentageContribution'] = (merged_df['Burden of Neurological disorders'] / merged_df['TotalBurden']) * 100

    # Step 6: Get the top 20 countries by total burden
    top_countries = merged_df.groupby('Entity')['Burden of Neurological disorders'].sum().nlargest(20).index
    top_20_data = merged_df[merged_df['Entity'].isin(top_countries)]

    # Step 7: Create the sunburst chart
    fig = px.sunburst(
        top_20_data,
        path=['Year', 'Entity'],
        values='PercentageContribution',
        title='Percentage Contribution of Neurological disorders Burden by Top 20 Countries per Year',
        labels={
            'PercentageContribution': 'Percentage Contribution (%)',
            'labels':'Year'

        },

    )

    fig.update_traces(
        hovertemplate='<b>Year:</b> %{label}<br>Percentage Contribution:</b> %{value:.2f}%<extra></extra>',
        insidetextorientation='radial'
    )
    # Update layout for better visual appeal
    fig.update_layout(
        title_x=0.5,  # Center the title
        width=1000,   # Set the desired width
    height=600    # Set the desired height
    )
    graph=fig.to_html()
    return render(request,'neuro7.html',{'graph':graph})


# Digestive Disease
def dig1(request):
    data=readburden()
    entity=data["Entity"].drop_duplicates().tolist()
    if request.method=="POST":
        n=request.POST.get('country')
        df=data[data["Entity"]==n]
        fig=px.line(df,x="Year",y="Burden of Digestive diseases",markers=True,
                    title=f"Burden of Digestive diseases in {n}",
                    labels={"Entity": "Country", "Digestive diseases": "Total DALYs"},
                    )
        fig.update_traces(line_color='rgba(0, 0, 255, 0.5)')
        fig.update_layout(xaxis_title="Year",yaxis_title="Digestive diseases Burden",plot_bgcolor='rgba(245, 245, 220, 0)', title_font_size=25,
                title_x=0.5,
                yaxis=dict(showgrid=True, gridcolor='LightGray'),
                font=dict(family="Arial", size=14),
                hoverlabel=dict(font_size=14,font_color="white"))
        graph=fig.to_html()
        return render(request,'dig1.html',{'graph':graph,'entity':entity})
    return render(request,'dig1.html',{'entity':entity})

def dig2(request):
    data=readburden()
    n=data["Year"].drop_duplicates().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        df = data[(data["Year"] == year) & (data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]

        # Get top 10 countries
        df = df.nlargest(10, "Burden of Digestive diseases")

        # Create the bar chart
        fig = px.bar(
            df,
            x="Entity",
            y="Burden of Digestive diseases",  # Make sure the y-axis reflects the correct metric
            title=f"Top 10 Countries with Highest Burden of Digestive diseases in {year}",
            # text="Burden of Diabetes and kidney diseases"  # Display the values on the bars
        )

        # Update bar colors with a gradient
        fig.update_traces(marker=dict(
            color=df['Burden of Digestive diseases'],  # Color based on burden values
            colorscale='purp',  # Choose a color scale
            showscale=True  # Optional: Show color scale
        ))

        # Update layout for aesthetics
        fig.update_layout(
            yaxis_title="Digestive diseases Burden",
            xaxis_title="Countries",
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
            paper_bgcolor='rgba(242, 240, 239, 0)',  # Transparent paper background
            hoverlabel=dict(font_size=14, font_color="white"),
            title_font_size=18,
            title_x=0.5
        )
        graph=fig.to_html()
        return render(request,'dig2.html',{'graph':graph,'n':n})
    return render(request,'dig2.html',{'n':n})   

def dig3(request):
    data=readburden()
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=request.POST.get('year')
        # Filter the data for the specified year
        df = data.query(f"Year == {year}")

        fig = go.Figure(data=go.Choropleth(
            locations=df['Code'],  # Country codes
            z=df['Burden of Digestive diseases'],  # Values for the choropleth
            text=df['Entity'],  # Country names for hover text
        colorscale = [
        "#4B0082",  # Indigo
        "#6A0B0B",  # Dark Red
        "#8A2BE2",  # Blue Violet
        "#4B0082",  # Dark Lavender
        "#7B68EE",  # Medium Slate Blue
        "#5C4033",  # Dark Brown
        "#9932CC",  # Dark Orchid
        "#8B0000",  # Dark Red
        "#8B4513",  # Saddle Brown
        "#2E8B57",  # Sea Green
        "#A52A2A",  # Brown
        "#2F4F4F",  # Dark Slate Gray
        "#FF4500",  # Orange Red
        "#4682B4",  # Steel Blue
        "#4B0082"   # Dark Violet
        ],

            reversescale=False,  # Change to True if you want to reverse the color scale
            marker_line_color='darkgray',  # Border color for countries
            marker_line_width=0.5,  # Border width
            colorbar_title='Digestive diseases Burden',  # Title for the color bar
        ))

        fig.update_layout(
            title_text=f"Burden of Digestive diseases in {year}",
            geo=dict(
                showcoastlines=True,
                coastlinecolor='Black',
                projection_type='natural earth',  # Natural Earth projection
            ),
            height=600,
            width=700,
            title_font=dict(
                size=25,  # Set the font size
                color='darkblue'  # Change the color of the title
            ),title_x=0.5
        )
        graph=fig.to_html()
        return render(request,'dig3.html',{'graph':graph,'nyear':nyear})
    return render(request,'dig3.html',{'nyear':nyear}) 

def dig4(request):
    data=readburden()
    nyear = data["Year"].drop_duplicates().to_list()

    if request.method == "POST":
        start_year = int(request.POST.get('start_year'))
        end_year = int(request.POST.get('end_year'))
        df_filtered = data[(data["Year"] >= start_year) &
                       (data["Year"] <= end_year) &
                       (data["Code"].notnull()) &
                       (~data["Entity"].isin(["World", "G20"]))]

        df_grouped = df_filtered.groupby("Entity", as_index=False).agg({
            "Burden of Digestive diseases": "sum"
        })

        df_top10 = df_grouped.sort_values(by="Burden of Digestive diseases", ascending=False).head(10)

        # Pie chart
        fig = px.pie(df_top10,
                    values="Burden of Digestive diseases",
                    names="Entity",
                    title=f"Top 10 Countries by DALYs (Digestive diseases) from {start_year} to {end_year}",
                    color="Entity",
                    color_discrete_sequence=px.colors.sequential.Plasma)
        
        fig.update_layout(
            
            title_x=0.5,
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent background
            height=600
        )

        fig.update_traces(textinfo='percent+label')
        graph = fig.to_html()

        return render(request, 'dig4.html', {'graph': graph, 'year1': nyear, 'year2': nyear})

    return render(request, 'dig4.html', {'year1': nyear, 'year2': nyear})    

def dig5(request):
    data=readburden()
    entity=data["Entity"].drop_duplicates().to_list()
    if request.method=="POST":
        countries=request.POST.getlist('country[]')
        df = data[data["Entity"].isin(countries)]

        fig = go.Figure()

        for country in countries:
            country_data = df[df["Entity"] == country]
            fig.add_trace(go.Scatter(
                x=country_data["Year"],
                y=country_data["Burden of Digestive diseases"],
                mode='lines+markers',
                name=country
            ))

        # Update layout
        fig.update_layout(
            title="Comparison of DALYs for Digestive diseases Over Time",
            xaxis_title="Year",
            yaxis_title="Total DALYs",
            title_x=0.5,
            hoverlabel=dict(font_size=14, font_color="white"),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            xaxis=dict(
                showgrid=True,  # Show x-axis grid
                gridcolor='LightGray',  # Grid color
                gridwidth=0.5  # Grid line width
            ),
            yaxis=dict(
                showgrid=True,  # Show y-axis grid
                gridcolor='LightGray',  # Grid color
                gridwidth=0.5  # Grid line width
            )
        )
        graph=fig.to_html()
        return render(request,'dig5.html',{'graph':graph,'entity':entity})

    return render(request,'dig5.html',{'entity':entity})      

def dig6(request):
    data=readburden()
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=int(request.POST.get("year"))
        df = data[(data["Year"] == year) & (data["Code"].isnull()) & (~data["Entity"].isin(["World", "G20"]))]

        # Create a bar chart
        fig = px.bar(df,
                    x="Entity",
                    y="Burden of Digestive diseases",
                    color="Entity",
                    title=f"Impact of Digestive diseases in Regions for the Year {year}",
                    color_discrete_sequence=px.colors.qualitative.Set2)

        # Add data labels
        fig.update_traces(text=df["Burden of Digestive diseases"], textposition='auto')

        # Update layout for better aesthetics
        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Burden of Digestive diseases",
            title_x=0.5,  # Center the title
            hoverlabel=dict(font_size=14, font_color="white"),
            plot_bgcolor='rgba(242, 240, 239, 0)',
            yaxis=dict(showgrid=True, gridcolor='LightGray'),
            font=dict(family="Arial", size=12),
            margin=dict(l=40, r=40, t=60, b=40)  # Adjust margins for better spacing
            ,height=600
        )
        graph=fig.to_html()
        return render(request, 'dig6.html',{'graph':graph,'nyear':nyear})
    return render(request,'dig6.html',{'nyear':nyear})
    
def dig7(request):
    data = readburden()
    # Step 1: Filter the data to exclude non-country entries
    filtered_data = data[(data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]

    # Step 2: Group the data by Year and Entity to get the total burden per country
    country_burden = filtered_data.groupby(['Year', 'Entity'], as_index=False).agg({'Burden of Digestive diseases': 'sum'})

    # Step 3: Calculate the total burden for each year
    total_burden_per_year = country_burden.groupby('Year', as_index=False).agg({'Burden of Digestive diseases': 'sum'})
    total_burden_per_year.rename(columns={'Burden of Digestive diseases': 'TotalBurden'}, inplace=True)

    # Step 4: Merge to get the total burden alongside each country's burden
    merged_df = pd.merge(country_burden, total_burden_per_year, on='Year')

    # Step 5: Calculate the percentage contribution
    merged_df['PercentageContribution'] = (merged_df['Burden of Digestive diseases'] / merged_df['TotalBurden']) * 100

    # Step 6: Get the top 20 countries by total burden
    top_countries = merged_df.groupby('Entity')['Burden of Digestive diseases'].sum().nlargest(20).index
    top_20_data = merged_df[merged_df['Entity'].isin(top_countries)]

    # Step 7: Create the sunburst chart
    fig = px.treemap(
        top_20_data,
        path=['Year', 'Entity'],
        values='PercentageContribution',
        title='Percentage Contribution of Digestive diseases Burden by Top 20 Countries per Year',
        labels={
            'PercentageContribution': 'Percentage Contribution (%)',
            'labels':'Year'

        }
    )

    fig.update_traces(
        hovertemplate='<b>Year:</b> %{label}<br>Percentage Contribution:</b> %{value:.2f}%<extra></extra>'
    )
    # Update layout for better visual appeal
    fig.update_layout(
       
        height=600,
            title_x=0.5,
            width=1000
    )
    graph=fig.to_html()
    return render(request,'dig7.html',{'graph':graph}) 


# Chronic respiratory disease
def resp1(request):
    data=readburden()
    entity = data["Entity"].drop_duplicates().tolist()
    
    if request.method == "POST":
        n = request.POST.get('country')
        df = data[data["Entity"] == n]

        # Create an area chart
        fig = px.area(
            df,
            x="Year",
            y="Burden of Chronic respiratory diseases",
            title=f"Burden of Chronic respiratory diseases in {n}",
            markers=True  # Adding markers for each data point
        )

        # Updating trace and layout for better aesthetics
        fig.update_traces(
            line_color='rgba(0, 0, 255, 0.7)',  # A more opaque line color
            fillcolor='rgba(0, 0, 255, 0.2)',   # Lighter fill color for contrast
            marker=dict(
                size=5,
                color='rgba(0, 0, 255, 0.9)',  # Light blue marker background
                line=dict(width=2, color='rgba(0, 0, 255, 0.7)')  # Blue marker outline
            ),
        )

        # Add annotation for significant data points (optional)
        max_burden_year = df[df["Burden of Chronic respiratory diseases"] == df["Burden of Chronic respiratory diseases"].max()]["Year"].values[0]
        max_burden_value = df["Burden of Chronic respiratory diseases"].max()

        fig.add_annotation(
            x=max_burden_year,
            y=max_burden_value,
            text="Highest Burden",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
            font=dict(size=12, color="black"),
            bgcolor="rgba(255, 255, 255, 0.7)",
            bordercolor="blue"
        )

        # Customize the layout for aesthetics and readability
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Chronic respiratory diseases burden",
            plot_bgcolor='rgba(245, 245, 220, 0)',  # Light beige background
            title_font_size=18,
            title_x=0.5,
            yaxis=dict(showgrid=True, gridcolor='LightGray'),
            xaxis=dict(showgrid=False, tickmode='linear', dtick=5),  # Limit years shown (show every 5th year)
            font=dict(family="Arial", size=14),
            hoverlabel=dict(font_size=14, font_color="white"),
            hovermode="closest"  # Standard hover (remove x unified)
        )

        # Adding a vertical line to highlight the year with the maximum burden
        fig.add_vline(
            x=max_burden_year,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Peak in {max_burden_year}",
            annotation_position="top"
        )

        # Add color gradient to the area for better visualization
        fig.update_traces(
            fillcolor='rgba(0, 0, 255, 0.3)',
            line_shape='spline'  # Smooth curve
        )
        graph=fig.to_html()
        return render(request,'resp1.html',{'graph':graph,'entity':entity})
    return render(request,'resp1.html',{'entity':entity})

def resp2(request):
    data=readburden()
    n=data["Year"].drop_duplicates().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        df = data[(data["Year"] == year) & (data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]

        # Get top 10 countries
        df = df.nlargest(10, "Burden of Chronic respiratory diseases")

        # Create the funnel chart
        fig = go.Figure(go.Funnel(
            y=df["Entity"],  # Countries on the y-axis
            x=df["Burden of Chronic respiratory diseases"],  # Burden values on the x-axis
            textinfo="value+percent initial"  # Display values and percentage
        ))

        # Update layout for aesthetics
        fig.update_layout(
            title=f"Top 10 Countries with Highest Burden of Chronic Respiratory Diseases in {year}",
            xaxis_title="Chronic respiratory diseases Burden",
            yaxis_title="Countries",
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
            paper_bgcolor='rgba(242, 240, 239, 0)',  # Transparent paper background
            hoverlabel=dict(font_size=14, font_color="white"),
            title_font_size=15,
            title_x=0.5
        )
        graph=fig.to_html()
        return render(request,'resp2.html',{'graph':graph,'n':n})
    return render(request,'resp2.html',{'n':n})

def resp3(request):
    data=readburden()
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=request.POST.get('year')
         # Filter the data for the specified year
        df = data.query(f"Year == {year}")

        fig = go.Figure(data=go.Choropleth(
            locations=df['Code'],  # Country codes
            z=df['Burden of Chronic respiratory diseases'],  # Values for the choropleth
            text=df['Entity'],  # Country names for hover text
            colorscale = [
        "#E6E6FA",  # Light Lavender
        "#9B59B6",  # Medium Purple
        "#9966CC",  # Amethyst
        "#7B68EE",  # Dark Lavender
        "#663399",  # Rebecca Purple
        "#DDA0DD",  # Plum

    ],  # Lavender shades
            reversescale=False,  # Change to True if you want to reverse the color scale
            marker_line_color='darkgray',  # Border color for countries
            marker_line_width=0.5,  # Border width
            # colorbar_title='Diabetes and Kidney Disease Burden',  # Title for the color bar
        ))

        fig.update_layout(
            title_text=f"Burden of Chronic respiratory diseases in {year}",
            geo=dict(
                showcoastlines=True,
                coastlinecolor='Black',
                projection_type='natural earth',  # Natural Earth projection
            ), height=600,
            width=700,title_x=0.5
        )
        graph=fig.to_html()
        return render(request,'resp3.html',{'graph':graph,'nyear':nyear})
    return render(request,'resp3.html',{'nyear':nyear}) 
    

def resp4(request):
    data=readburden()
    nyear = data["Year"].drop_duplicates().to_list()

    if request.method == "POST":
        start_year = int(request.POST.get('start_year'))
        end_year = int(request.POST.get('end_year'))
         # Data filtering and grouping
        df_filtered = data[(data["Year"] >= start_year) &
                        (data["Year"] <= end_year) &
                        (data["Code"].notnull()) &
                        (~data["Entity"].isin(["World", "G20"]))]

        df_grouped = df_filtered.groupby("Entity", as_index=False).agg({
            "Burden of Chronic respiratory diseases": "sum"
        })

        # Rename the aggregated column for clarity
        df_grouped.rename(columns={"Burden of Chronic respiratory diseases": "Total Burden"}, inplace=True)

        # Sort and get the top 10 countries
        df_top10 = df_grouped.sort_values(by="Total Burden", ascending=False).head(10)

        # Create a bubble chart
        fig = px.scatter(df_top10,
                        x="Entity",
                        y="Total Burden",
                        size="Total Burden",  # Bubble size based on total burden
                        title=f"Top 10 Countries by DALYs (Chronic respiratory diseases) from {start_year} to {end_year}",
                        color="Total Burden",
                        color_continuous_scale=["#E6E6FA", "#9370DB", "#8A2BE2", "#4B0082"],

                        size_max=60)  # Adjust maximum bubble size

        # Update layout for aesthetics
        fig.update_layout(
            xaxis_title="Country",
            yaxis_title="Total Burden of Chronic respiratory diseases",
            title_font_size=15,
            title_x=0.5,
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent background
            height=600
        )
        graph = fig.to_html()

        return render(request, 'resp4.html', {'graph': graph, 'year1': nyear, 'year2': nyear})

    return render(request, 'resp4.html', {'year1': nyear, 'year2': nyear}) 

def resp5(request):
    data=readburden()
    entity=data["Entity"].drop_duplicates().to_list()
    if request.method=="POST":
        countries=request.POST.getlist('country[]')
         # Filter the data for the specified countries
        df = data[data["Entity"].isin(countries)]

        # Create a new column for custom sizes (e.g., a fixed size or based on a different metric)
        df['Custom Size'] = df['Burden of Chronic respiratory diseases'] / df['Burden of Chronic respiratory diseases'].max() *2  # Scale it to a reasonable size

        # Create the dot plot with custom sizes
        fig = px.scatter(
            df,
            x='Year',
            y='Burden of Chronic respiratory diseases',
            color='Entity',
            title="Dot Plot of Chronic Respiratory Diseases Burden Over Time",
            labels={'Burden of Chronic respiratory diseases': 'Total DALYs'},
            # size='Custom Size',  # Use the new custom size column
            hover_name='Entity',  # Show country name on hover
            color_discrete_sequence=px.colors.qualitative.Vivid  # Distinct colors for each country
        )
        # Update layout for aesthetics
        fig.update_layout(
            title_x=0.5,
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
            paper_bgcolor='rgba(242, 240, 239, 0)',  # Transparent paper background
            hoverlabel=dict(font_size=14, font_color="white"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
        )
        graph=fig.to_html()
        return render(request,'resp5.html',{'graph':graph,'entity':entity})

    return render(request,'resp5.html',{'entity':entity})  

    

def resp6(request):
    data=readburden()
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=int(request.POST.get("year"))
        df = data[(data["Year"] == year) & (data["Code"].isnull()) & (~data["Entity"].isin(["World", "G20"]))]

        # Create a treemap
        fig = px.sunburst(
            df,
            path=['Entity'],  # Define the hierarchy (in this case, only regions)
            values='Burden of Chronic respiratory diseases',
            title=f"Burden of Chronic respiratory diseases by Region in {year}",
            color='Burden of Chronic respiratory diseases',  # Color by burden values
            color_continuous_scale='purples'  ,
            labels={
                'Entity': 'Region',  # Ensure the key matches the DataFrame column
                'Burden of Chronic respiratory diseases': 'Burden'
            }
        )

        fig.update_traces(
            hovertemplate='<b>Region:</b> %{label}<br><b>Burden:</b> %{value}<extra></extra>'
        )

        # Update layout for aesthetics
        fig.update_layout(
            title_font_size=20,
            title_x=0.5,
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
            height=600
        )
        graph=fig.to_html()
        return render(request, 'resp6.html',{'graph':graph,'nyear':nyear})
    return render(request,'resp6.html',{'nyear':nyear})
    

def resp7(request):
    data=readburden()
    # Step 1: Filter the data to exclude non-country entries
    filtered_data = data[(data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]

    # Step 2: Group the data by Year and Entity to get the total burden per country
    country_burden = filtered_data.groupby(['Year', 'Entity'], as_index=False).agg({'Burden of Chronic respiratory diseases': 'sum'})

    # Step 3: Calculate the total burden for each year
    total_burden_per_year = country_burden.groupby('Year', as_index=False).agg({'Burden of Chronic respiratory diseases': 'sum'})
    total_burden_per_year.rename(columns={'Burden of Chronic respiratory diseases': 'TotalBurden'}, inplace=True)

    # Step 4: Merge to get the total burden alongside each country's burden
    merged_df = pd.merge(country_burden, total_burden_per_year, on='Year')

    # Step 5: Calculate the percentage contribution
    merged_df['PercentageContribution'] = (merged_df['Burden of Chronic respiratory diseases'] / merged_df['TotalBurden']) * 100

    # Step 6: Get the top 20 countries by total burden
    top_countries = merged_df.groupby('Entity')['Burden of Chronic respiratory diseases'].sum().nlargest(20).index
    top_20_data = merged_df[merged_df['Entity'].isin(top_countries)]

    # Step 7: Create the sunburst chart
    fig = px.sunburst(
        top_20_data,
        path=['Year', 'Entity'],
        values='PercentageContribution',
        title='Percentage Contribution of Chronic respiratory diseases Burden by Top 20 Countries per Year',
        labels={
            'PercentageContribution': 'Percentage Contribution (%)',
            'labels':'Year'

        },

    )

    fig.update_traces(
        hovertemplate='<b>Year:</b> %{label}<br>Percentage Contribution:</b> %{value:.2f}%<extra></extra>',
        insidetextorientation='radial'
    )
    # Update layout for better visual appeal
    fig.update_layout(
        title_x=0.5,  # Center the title
        width=1000,   # Set the desired width
    height=600    # Set the desired height
    )
    graph=fig.to_html()

    return render(request,'resp7.html',{'graph':graph}) 

def disdisorder(request):
    return render(request,'disdisorder.html')

def disorder1(request):
    return render(request,'disorder1.html')


#Mental Disorder

def mentaldis(request):
    data=readburden()
    entity = data["Entity"].drop_duplicates().tolist()
    
    if request.method == "POST":
        n = request.POST.get('country')
        df=data[data["Entity"]==n]
        fig=px.line(df,x="Year",y="Burden of Mental disorders",markers=True,
                    title=f"Burden of Mental disorders in {n}",
                    labels={"Entity": "Country", "Cardiovascular diseases": "Total DALYs"},
                    )
        fig.update_traces(line_color='rgba(0, 0, 255, 0.5)')
        fig.update_layout(xaxis_title="Year",yaxis_title="Mental Disorder Burden",plot_bgcolor='rgba(245, 245, 220, 0)', title_font_size=25,
                title_x=0.5,
                yaxis=dict(showgrid=True, gridcolor='LightGray'),
                font=dict(family="Arial", size=14),
                hoverlabel=dict(font_size=14,font_color="white"),height=430,width=1000)
        graph=fig.to_html()
        return render(request,'mentaldis.html',{'entity':entity,'graph':graph})
    return render(request,'mentaldis.html',{'entity':entity})

def mentaldis1(request):
    data=readburden()
    n=data["Year"].drop_duplicates().tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        df = data[(data["Year"] == year) & (data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]
        # Get top 10 countries
        df = df.nlargest(10, "Burden of Mental disorders")

        # Create the bar chart
        fig = px.bar(
            df,
            x="Entity",
            y="Burden of Mental disorders",  # Make sure the y-axis reflects the correct metric
            title=f"Top 10 Countries with Highest Burden of Mental Disorders in {year}",
            # text="Burden of Diabetes and kidney diseases"  # Display the values on the bars
        )

        # Update bar colors with a gradient
        fig.update_traces(marker=dict(
            color=df['Burden of Mental disorders'],  # Color based on burden values
            colorscale='purp',  # Choose a color scale
            showscale=True  # Optional: Show color scale
        ))

        # Update layout for aesthetics
        fig.update_layout(
            yaxis_title="Mental Disorder Burden",
            xaxis_title="Countries",
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
            paper_bgcolor='rgba(242, 240, 239, 0)',  # Transparent paper background
            hoverlabel=dict(font_size=14, font_color="white"),
            title_font_size=20,
            title_x=0.5
        )
        graph=fig.to_html()
        return render(request,'mentaldis1.html',{'graph':graph,'n':n})
    return render(request,'mentaldis1.html',{'n':n})

def mentaldis2(request):
    data=readburden()
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=int(request.POST.get("year"))
         # Filter data for the specified year and regions
        df = data[(data["Year"] == year) & (data["Code"].isnull()) & (~data["Entity"].isin(["World", "G20"]))]

        # Create a bar chart
        fig = px.bar(df,
                    x="Entity",
                    y="Burden of Mental disorders",
                    color="Entity",
                    title=f"Impact of Mental Disorders in Regions for the Year {year}",
                    color_discrete_sequence=px.colors.qualitative.Set2)

        # Add data labels
        fig.update_traces(text=df["Burden of Mental disorders"], textposition='auto')

        # Update layout for better aesthetics
        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Burden of Mental Disorders",
            title_x=0.5,  # Center the title
            hoverlabel=dict(font_size=14, font_color="white"),
            plot_bgcolor='rgba(242, 240, 239, 0)',
            yaxis=dict(showgrid=True, gridcolor='LightGray'),
            font=dict(family="Arial", size=12),
            margin=dict(l=40, r=40, t=60, b=40),  # Adjust margins for better spacing
            width=900
        )
        graph=fig.to_html()
        return render(request, 'mentaldis2.html',{'graph':graph,'nyear':nyear})

    return render(request,'mentaldis2.html',{'nyear':nyear})

def mentaldis3(request):
    data=readburden()
    nyear = data["Year"].drop_duplicates().to_list()

    if request.method == "POST":
        start_year = int(request.POST.get('start_year'))
        end_year = int(request.POST.get('end_year'))
         # (Data filtering and grouping as before)
        df_filtered = data[(data["Year"] >= start_year) &
                        (data["Year"] <= end_year) &
                        (data["Code"].notnull()) &
                        (~data["Entity"].isin(["World", "G20"]))]

        df_grouped = df_filtered.groupby("Entity", as_index=False).agg({
            "Burden of Mental disorders": "sum"
        })

        df_top10 = df_grouped.sort_values(by="Burden of Mental disorders", ascending=False).head(10)

        # Pie chart
        fig = px.pie(df_top10,
                    values="Burden of Mental disorders",
                    names="Entity",
                    title=f"Top 10 Countries by DALYs (Mental disorders) from {start_year} to {end_year}",
                    color="Entity",
                    color_discrete_sequence=px.colors.sequential.Plasma)

        fig.update_traces(textinfo='percent+label')
        fig.update_layout(width=1000)
        graph = fig.to_html()
        return render(request, 'mentaldis3.html', {'graph': graph, 'year1': nyear, 'year2': nyear})
    return render(request, 'mentaldis3.html', {'year1': nyear, 'year2': nyear}) 

def mentaldis4(request):
    data=readburden()
    nyear=data["Year"].drop_duplicates().to_list()
    if request.method=="POST":
        year=request.POST.get('year')
        # Filter the data for the specified year
        df = data.query(f"Year == {year}")

        fig = go.Figure(data=go.Choropleth(
            locations=df['Code'],  # Country codes
            z=df['Burden of Mental disorders'],  # Values for the choropleth
            text=df['Entity'],  # Country names for hover text
        colorscale = [
        "#4B0082",  # Indigo
        "#6A0B0B",  # Dark Red
        "#8A2BE2",  # Blue Violet
        "#4B0082",  # Dark Lavender
        "#7B68EE",  # Medium Slate Blue
        "#5C4033",  # Dark Brown
        "#9932CC",  # Dark Orchid
        "#8B0000",  # Dark Red
        "#8B4513",  # Saddle Brown
        "#2E8B57",  # Sea Green
        "#A52A2A",  # Brown
        "#2F4F4F",  # Dark Slate Gray
        "#FF4500",  # Orange Red
        "#4682B4",  # Steel Blue
        "#4B0082"   # Dark Violet
    ]



    ,

            reversescale=False,  # Change to True if you want to reverse the color scale
            marker_line_color='darkgray',  # Border color for countries
            marker_line_width=0.5,  # Border width
            colorbar_title='Mental disorder Burden',  # Title for the color bar
        ))

        fig.update_layout(
            title_text=f"Burden of Mental Disorder in {year}",
            geo=dict(
                showcoastlines=True,
                coastlinecolor='Black',
                projection_type='natural earth',  # Natural Earth projection
            ),width=1000
        )
        graph=fig.to_html()
        return render(request,'mentaldis4.html',{'graph':graph,'nyear':nyear})
    return render(request,'mentaldis4.html',{'nyear':nyear}) 

def mentaldis5(request):
    data=readburden()
    entity=data["Entity"].drop_duplicates().to_list()
    if request.method=="POST":
        countries=request.POST.getlist('country[]')
        # Filter the data for the specified countries
        df = data[data["Entity"].isin(countries)]

        fig = go.Figure()

        for country in countries:
            country_data = df[df["Entity"] == country]
            fig.add_trace(go.Scatter(
                x=country_data["Year"],
                y=country_data["Burden of Mental disorders"],
                mode='lines+markers',
                name=country
            ))

        # Update layout
        fig.update_layout(
            title="Comparison of DALYs for Mental Disorders Over Time",
            xaxis_title="Year",
            yaxis_title="Total DALYs",
            title_x=0.5, 
            plot_bgcolor='rgba(0, 0, 0, 0)',
            hoverlabel=dict(font_size=14, font_color="white"),height=400
        )
        graph=fig.to_html()
        return render(request,'mentaldis5.html',{'graph':graph,'entity':entity})
    return render(request,'mentaldis5.html',{'entity':entity})   

def mentaldis6(request):
    data=readburden()
    # Step 1: Filter the data to exclude non-country entries
    filtered_data = data[(data["Code"].notnull()) & (~data["Entity"].isin(["World", "G20"]))]

    # Step 2: Group the data by Year and Entity to get the total burden per country
    country_burden = filtered_data.groupby(['Year', 'Entity'], as_index=False).agg({'Burden of Mental disorders': 'sum'})

    # Step 3: Calculate the total burden for each year
    total_burden_per_year = country_burden.groupby('Year', as_index=False).agg({'Burden of Mental disorders': 'sum'})
    total_burden_per_year.rename(columns={'Burden of Mental disorders': 'TotalBurden'}, inplace=True)

    # Step 4: Merge to get the total burden alongside each country's burden
    merged_df = pd.merge(country_burden, total_burden_per_year, on='Year')

    # Step 5: Calculate the percentage contribution
    merged_df['PercentageContribution'] = (merged_df['Burden of Mental disorders'] / merged_df['TotalBurden']) * 100

    # Step 6: Get the top 20 countries by total burden
    top_countries = merged_df.groupby('Entity')['Burden of Mental disorders'].sum().nlargest(20).index
    top_20_data = merged_df[merged_df['Entity'].isin(top_countries)]

    # Step 7: Create the sunburst chart
    fig = px.treemap(
        top_20_data,
        path=['Year', 'Entity'],
        values='PercentageContribution',
        title='Percentage Contribution of Mental disorders Burden by Top 20 Countries per Year',
        labels={
            'PercentageContribution': 'Percentage Contribution (%)',
            'labels':'Year'

        }
    )

    fig.update_traces(
        hovertemplate='<b>Year:</b> %{label}<br>Percentage Contribution:</b> %{value:.2f}%<extra></extra>'
    )
    # Update layout for better visual appeal
    fig.update_layout(
        title_x=0.5 , # Center the title
        width=1000,   # Set the desired width
    height=600
    )
    graph=fig.to_html()
    return render(request,'mentaldis6.html',{'graph':graph})

def healthexpense(request):
    return render(request,'healthexpense.html')


def diseasecards(request):
    return render(request,'diseasecards.html') 

def disordercards(request):
    return render(request,'disordercards.html') 

def anxanalysis(request):
    return render(request,'anxanalysis.html')


def readanx():
    anxdisease = pd.read_csv("anxietydisorders.csv")
    return anxdisease

def anx1(request):
    anxdisease = readanx()
    # Only include countries that have a non-null code and not null population
    country_list = anxdisease[(anxdisease["Code"].notnull()) & (anxdisease["Population"].notnull())]["Entity"].  drop_duplicates().tolist()

    if request.method == "POST":
        selected_country = request.POST.get('country')  # Get the selected country from the form
        df = anxdisease[anxdisease["Code"].notnull()]
        
        # Filter by the selected country
        df = df[df["Entity"] == selected_country]
        
        # Apply the year range filter
        df = df[(df["Year"] > 1990) & (df["Year"] < 2020)]
        
        # Create the plot
        fig = px.line(df, x='Year', y='Population', markers=True, 
                      title=f"Population affected by Anxiety disorders in {selected_country}")
        fig.update_layout(xaxis_title="Year", yaxis_title="Population", 
                          plot_bgcolor='rgba(245, 245, 220, 0)', title_font_size=25,
                          title_x=0.5, yaxis=dict(showgrid=True, gridcolor='LightGray'),
                          font=dict(family="Arial", size=14),
                          hoverlabel=dict(font_size=14, font_color="white"),width=1000)
        graph = fig.to_html()

        return render(request, 'anx1.html', {'entity': country_list, 'graph': graph})
    
    return render(request, 'anx1.html', {'entity': country_list})

def anx2(request):
    anxdisease = readanx()
    
    anxdisease["Year"] = pd.to_numeric(anxdisease["Year"], errors='coerce')

    # Extract unique years and filter them
    n = anxdisease["Year"].drop_duplicates()

    # Filter years to start from 1990 and exclude any negative years
    n = n[(n >= 1990) & (n >= 0)].tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        df=anxdisease[(anxdisease["Year"]==year) & (anxdisease["Code"].notnull()) & (anxdisease["Entity"]!="World")]
        df=df.nlargest(10,"Population")
        fig=px.bar(df,x="Entity",y="Population",
                    title=f"Top 10 Countries with Highest Anxiety Disorders in {year}")

        # Update bar colors with a gradient
        fig.update_traces(marker=dict(
                color=df['Population'],  # Color based on burden values
                colorscale='purp',  # Choose a color scale
                showscale=True  # Optional: Show color scale
            ))
        fig.update_layout(yaxis_title="Anxiety Disorder", xaxis_title="Countries", plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
        paper_bgcolor='rgba(242, 240, 239, 0)',hoverlabel=dict(font_size=14,font_color="white"),title_font_size=20,
                title_x=0.5,width=1000)
        graph=fig.to_html()
        return render(request,'anx2.html',{'graph':graph,'n':n})
    return render(request,'anx2.html',{'n':n})
        
def anx3(request):
    anxdisease = readanx()
    anxdisease["Year"] = pd.to_numeric(anxdisease["Year"], errors='coerce')

    # Extract unique years and filter them
    nyear = anxdisease["Year"].drop_duplicates()

    # Filter years to start from 1990 and exclude any negative years
    nyear = nyear[(nyear >= 1990) & (nyear >= 0)].tolist()
    if request.method=="POST":
        year=int(request.POST.get("year"))
        # Filter for regions (where 'Code' is null and 'Entity' is not 'World')
        reg = anxdisease[(anxdisease["Year"] == year) & (anxdisease["Code"].isnull()) & (anxdisease["Entity"] != "World")]

        # Sort by population and select the top 5 regions
        top5_regions = reg.nlargest(5, 'Population')

        # Create a pie chart for the top 5 regions with plasma color scale
        fig_regions = px.pie(top5_regions, names="Entity", values="Population",
                            title=f"Top 5 Regions with Highest Anxiety Disorders in {year}",
                            color_discrete_sequence=px.colors.sequential.Plasma,
                            hole=0.4)  # Optional: donut chart style for better clarity

        # Update the hover template to show region name and percentage
        fig_regions.update_traces(textinfo='percent+label',
                                hovertemplate='<b>%{label}</b><br>Population: %{value}<br>Percentage: %{percent}')

        # Update layout for visual improvements
        fig_regions.update_layout(
            title_font_size=20, title_x=0.5,
            paper_bgcolor='rgba(242, 240, 239, 0)',  # Transparent background
            hoverlabel=dict(font_size=14, font_color="white"),width=1000
        )
        graph=fig_regions.to_html()
        return render(request, 'anx3.html',{'graph':graph,'nyear':nyear})

    return render(request,'anx3.html',{'nyear':nyear})

def anx4(request):
    anxdisease = readanx()
    anxdisease["Year"] = pd.to_numeric(anxdisease["Year"], errors='coerce')

    # Extract unique years and filter them
    nyear = anxdisease["Year"].drop_duplicates()

    # Filter years to start from 1990 and exclude any negative years
    nyear = nyear[(nyear >= 1990) & (nyear >= 0)].tolist()

    if request.method == "POST":
        start_year = int(request.POST.get('start_year'))
        end_year = int(request.POST.get('end_year'))
        # Step 1: Filter the data to exclude non-country entries and restrict years
        filtered_data = anxdisease[(anxdisease["Code"].notnull()) &
                            (~anxdisease["Entity"].isin(["World", "G20"])) &
                            (anxdisease["Year"].between(start_year, end_year))]

        # Step 2: Group the data by Year and Entity to get the total burden per country
        country_burden = filtered_data.groupby(['Year', 'Entity'], as_index=False).agg({'Population': 'sum'})

        # Step 3: Get the top 20 countries by total burden of anxiety disorders across all years
        top_countries = country_burden.groupby('Entity')['Population'].sum().nlargest(10).index
        top_20_data = country_burden[country_burden['Entity'].isin(top_countries)]

        # Step 4: Create the treemap to visualize the burden of anxiety disorders
        fig = px.sunburst(
            top_20_data,
            path=['Year', 'Entity'],
            values='Population',
            title=f'Burden of Anxiety Disorders by Top 10 Countries ({start_year}-{end_year})',
            color='Population',  # Color based on population
            color_continuous_scale='plasma'  # Choose a color scale
        )

        # Update layout for better visuals
        fig.update_layout(
            paper_bgcolor='rgba(242, 240, 239, 0)',  # Transparent background
            plot_bgcolor='rgba(242, 240, 239, 0)',
            title_font_size=20,
            title_x=0.5,width=1000,height=500
        )
        graph = fig.to_html()
        return render(request, 'anx4.html', {'graph': graph, 'year1': nyear, 'year2': nyear})
    return render(request, 'anx4.html', {'year1': nyear, 'year2': nyear})

def anx5(request):
    anxdisease = readanx()
    anxdisease["Year"] = pd.to_numeric(anxdisease["Year"], errors='coerce')

    # Extract unique years and filter them
    nyear = anxdisease["Year"].drop_duplicates()

    # Filter years to start from 1990 and exclude any negative years
    nyear = nyear[(nyear >= 1990) & (nyear >= 0)].tolist()
    if request.method=="POST":
        year=request.POST.get('year')
        # Filter the data for the specified year
        df = anxdisease.query(f"Year == {year}")

        # Create the choropleth map
        fig = go.Figure(data=go.Choropleth(
        locations = df['Code'],
        z = df['Population'],
        text = df['Entity'],
        colorscale = 'purples',
        # autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'Population affected',
    ))
        fig.update_layout(title_text=f"Burden of Mental Disorder in {year}",title_x=0.5,width=1000)
        graph=fig.to_html()
        return render(request,'anx5.html',{'graph':graph,'nyear':nyear})
    return render(request,'anx5.html',{'nyear':nyear}) 
        
def anx6(request):
    anxdisease = readanx()
    entity = anxdisease[(anxdisease["Code"].notnull()) & (anxdisease["Population"].notnull())]["Entity"].  drop_duplicates().tolist()
    
    # Get unique years, filtering to include only those >= 1990 and >= 0 (to exclude negatives)
    nyear = anxdisease["Year"].drop_duplicates()
    nyear = nyear[(nyear >= 1990) & (nyear >= 0)].to_list()
    
    if request.method == "POST":
        countries = request.POST.getlist('country[]')
        
        # Here, you can select a specific year for analysis. 
        # Make sure to choose a single year or handle multiple years accordingly.
        selected_year = nyear[0]  # For example, selecting the first year from the filtered list

        # Filter for the specified countries and the given year
        df = anxdisease[(anxdisease["Year"] == selected_year) & (anxdisease["Entity"].isin(countries))]

        # Check if the DataFrame is empty to avoid issues while plotting
        if df.empty:
            return render(request, 'anx6.html', {'graph': None, 'entity': entity, 'nyear': nyear})

        # Create a horizontal bar chart to compare the selected countries with lavender shades
        fig_countries = px.bar(
            df,
            x="Population",
            y="Entity",
            title=f"Anxiety Disorders in {', '.join(countries)} in {selected_year}",
            color="Entity",  # Use country names for color distinction
            text="Population",  # Show population values on bars
            orientation='h',
            color_discrete_sequence=["#D8BFD8", "#9370DB", "#8A2BE2", "#4B0082"]  # Lavender shades
        )

        # Update layout for visual improvements
        fig_countries.update_layout(
            xaxis_title="Anxiety Disorder Population",
            yaxis_title="Countries",
            plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
            paper_bgcolor='rgba(242, 240, 239, 0)',
            hoverlabel=dict(font_size=14, font_color="white"),
            title_font_size=20,
            title_x=0.5,width=1000
        )
        
        graph = fig_countries.to_html()
        return render(request, 'anx6.html', {'graph': graph, 'entity': entity, 'nyear': nyear})

    return render(request, 'anx6.html', {'entity': entity, 'nyear': nyear})
 

def anx7(request):
    anxdisease = readanx()
    # Step 1: Filter the data to exclude non-country entries and restrict years to 1990-2020
    filtered_data = anxdisease[(anxdisease["Code"].notnull()) &
                         (~anxdisease["Entity"].isin(["World", "G20"])) &
                         (anxdisease["Year"].between(1990, 2020))]

    # Step 2: Group the data by Year and Entity to get the total burden per country
    country_burden = filtered_data.groupby(['Year', 'Entity'], as_index=False).agg({'Population': 'sum'})

    # Step 3: Calculate the total burden for each year
    total_burden_per_year = country_burden.groupby('Year', as_index=False).agg({'Population': 'sum'})
    total_burden_per_year.rename(columns={'Population': 'TotalBurden'}, inplace=True)

    # Step 4: Merge to get the total burden alongside each country's burden
    merged_df = pd.merge(country_burden, total_burden_per_year, on='Year')

    # Step 5: Calculate the percentage contribution
    merged_df['PercentageContribution'] = (merged_df['Population'] / merged_df['TotalBurden']) * 100

    # Step 6: Get the top 20 countries by total population contribution across all years
    top_countries = merged_df.groupby('Entity')['Population'].sum().nlargest(20).index
    top_20_data = merged_df[merged_df['Entity'].isin(top_countries)]

    # Step 7: Create the sunburst chart
    fig = px.treemap(
        top_20_data,
        path=['Year', 'Entity'],
        values='PercentageContribution',
        title='Percentage Contribution of Anxiety Disorder Burden by Top 20 Countries (1990-2020)',
        labels={'PercentageContribution': 'Percentage Contribution (%)'}
    )

    fig.update_traces(
        hovertemplate='<b>Year:</b> %{label}<br><b>Percentage Contribution:</b> %{value:.2f}%<extra></extra>'
    )

    # Update layout for better visual appeal
    fig.update_layout(
        title_x=0.5,  # Center the title
         width=1000,   # Set the desired width
    height=600
    )
    graph=fig.to_html()
    return render(request,'anx7.html',{'graph':graph})

def depanalysis(request):
    return render(request,'depsnalysis.html')

def readadep():
    depdisease = pd.read_csv("depression.csv")
    return depdisease

def dep1(request):
    depdisease = readadep()
    # Only include countries that have a non-null code and a non-null population
    country = depdisease[(depdisease["Code"].notnull()) & (depdisease["Population"].notnull())]["Entity"].drop_duplicates().tolist()
    
    if request.method == "POST":
        selected_country = request.POST.get('country')  # Get the selected country from the form

        # Filter the DataFrame based on the selected country
        df = depdisease[(depdisease["Code"].notnull()) & (depdisease["Entity"] == selected_country)]
        
        # Apply the year range filter to the country-specific DataFrame
        df = df[(df["Year"] > 1990) & (df["Year"] < 2020)]

        # Check if df is empty after filtering
        if df.empty:
            return render(request, 'dep1.html', {'entity': country, 'graph': None})

        # Create the line plot
        fig = px.line(
            df,
            x='Year',
            y='Population',
            markers=True,
            title=f"Population affected by Depression disorders in {selected_country}"
        )
        
        # Update layout for visual improvements
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Population",
            plot_bgcolor='rgba(245, 245, 220, 0)',
            title_font_size=25,
            title_x=0.5,
            yaxis=dict(showgrid=True, gridcolor='LightGray'),
            font=dict(family="Arial", size=14),
            hoverlabel=dict(font_size=14, font_color="white"),
            width=1000
        )
        
        graph = fig.to_html()
        
        return render(request, 'dep1.html', {'entity': country, 'graph': graph})

    return render(request, 'dep1.html', {'entity': country})

def dep2(request):
    depdisease = readadep()
    depdisease["Year"] = pd.to_numeric(depdisease["Year"], errors='coerce')

    # Extract unique years and filter them
    n = depdisease["Year"].drop_duplicates()

    # Filter years to start from 1990 and exclude any negative years
    n = n[(n >= 1990) & (n >= 0)].tolist()
    if request.method=="POST":
        year=int(request.POST.get('year'))
        df=depdisease[(depdisease["Year"]==year) & (depdisease["Code"].notnull()) & (depdisease["Entity"]!="World")]
        df=df.nlargest(10,"Population")
        fig=px.bar(df,x="Entity",y="Population",
                    title=f"Top 10 Countries with Highest Depression Disorders in {year}")

        # Update bar colors with a gradient
        fig.update_traces(marker=dict(
                color=df['Population'],  # Color based on burden values
                colorscale='purp',  # Choose a color scale
                showscale=True  # Optional: Show color scale
            ))
        fig.update_layout(yaxis_title="Depression Disorder", xaxis_title="Countries", plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
        paper_bgcolor='rgba(242, 240, 239, 0)',hoverlabel=dict(font_size=14,font_color="white"),title_font_size=20,
                title_x=0.5,width=1000)
        graph=fig.to_html()
        return render(request,'dep2.html',{'graph':graph,'n':n})
    return render(request,'dep2.html',{'n':n})
    
def dep3(request):
    depdisease = readadep()
    depdisease["Year"] = pd.to_numeric(depdisease["Year"], errors='coerce')

    # Extract unique years and filter them
    nyear = depdisease["Year"].drop_duplicates()

    # Filter years to start from 1990 and exclude any negative years
    nyear = sorted(nyear[(nyear >= 1990) & (nyear >= 0)].tolist())
    if request.method=="POST":
        year=int(request.POST.get("year"))
         # Filter for regions (where 'Code' is null and 'Entity' is not 'World')
        reg = depdisease[(depdisease["Year"] == year) & (depdisease["Code"].isnull()) & (depdisease["Entity"] != "World")]

        # Sort by population and select the top 5 regions
        top5_regions = reg.nlargest(5, 'Population')

        # Create a pie chart for the top 5 regions with plasma color scale
        fig_regions = px.pie(top5_regions, names="Entity", values="Population",
                            title=f"Top 5 Regions with Highest Depression Disorders in {year}",
                            color_discrete_sequence=px.colors.sequential.Plasma,
                            hole=0.4)  # Optional: donut chart style for better clarity

        # Update the hover template to show region name and percentage
        fig_regions.update_traces(textinfo='percent+label',
                                hovertemplate='<b>%{label}</b><br>Population: %{value}<br>Percentage: %{percent}')

        # Update layout for visual improvements
        fig_regions.update_layout(
            title_font_size=20, title_x=0.5,
            paper_bgcolor='rgba(242, 240, 239, 0)',  # Transparent background
            hoverlabel=dict(font_size=14, font_color="white"),
            width=1000
        )
        graph=fig_regions.to_html()
        return render(request, 'dep3.html',{'graph':graph,'nyear':nyear})

    return render(request,'dep3.html',{'nyear':nyear})

def dep4(request):
    depdisease = readadep()
    depdisease["Year"] = pd.to_numeric(depdisease["Year"], errors='coerce')

    # Extract unique years and filter them
    nyear = depdisease["Year"].drop_duplicates()

    # Filter years to start from 1990 and exclude any negative years
    nyear =sorted(nyear[(nyear >= 1990) & (nyear >= 0)].tolist())

    if request.method == "POST":
        start_year = int(request.POST.get('start_year'))
        end_year = int(request.POST.get('end_year'))
         # Step 1: Filter the data to exclude non-country entries and restrict years
        filtered_data = depdisease[(depdisease["Code"].notnull()) &
                            (~depdisease["Entity"].isin(["World", "G20"])) &
                            (depdisease["Year"].between(start_year, end_year))]

        # Step 2: Group the data by Year and Entity to get the total burden per country
        country_burden = filtered_data.groupby(['Year', 'Entity'], as_index=False).agg({'Population': 'sum'})

        # Step 3: Get the top 20 countries by total burden of anxiety disorders across all years
        top_countries = country_burden.groupby('Entity')['Population'].sum().nlargest(10).index
        top_20_data = country_burden[country_burden['Entity'].isin(top_countries)]

        # Step 4: Create the treemap to visualize the burden of anxiety disorders
        fig = px.sunburst(
            top_20_data,
            path=['Year', 'Entity'],
            values='Population',
            title=f'Burden of Anxiety Disorders by Top 20 Countries ({start_year}-{end_year})',
            color='Population',  # Color based on population
            color_continuous_scale='plasma'  # Choose a color scale
        )

        # Update layout for better visuals
        fig.update_layout(
            paper_bgcolor='rgba(242, 240, 239, 0)',  # Transparent background
            plot_bgcolor='rgba(242, 240, 239, 0)',
            title_font_size=20,
            title_x=0.5,width=1000,height=500
        )
        graph = fig.to_html()
        return render(request, 'dep4.html', {'graph': graph, 'year1': nyear, 'year2': nyear})
    return render(request, 'dep4.html', {'year1': nyear, 'year2': nyear})

def dep5(request):
    depdisease = readadep()
    # nyear=depdisease["Year"].drop_duplicates().to_list()
    depdisease["Year"] = pd.to_numeric(depdisease["Year"], errors='coerce')

    # Extract unique years and filter them
    nyear = depdisease["Year"].drop_duplicates()

    # Filter years to start from 1990 and exclude any negative years
    nyear =sorted(nyear[(nyear >= 1990) & (nyear >= 0)].tolist())
    if request.method=="POST":
        year=request.POST.get('year')       
        # Filter the data for the specified year
        df = depdisease.query(f"Year == {year}")

        fig = go.Figure(data=go.Choropleth(
            locations=df['Code'],  # Country codes
            z=df['Population'],  # Values for the choropleth
            text=df['Entity'],  # Country names for hover text
        colorscale = [
        "#4B0082",  # Indigo
        "#6A0B0B",  # Dark Red
        "#8A2BE2",  # Blue Violet
        "#4B0082",  # Dark Lavender
        "#7B68EE",  # Medium Slate Blue
        "#5C4033",  # Dark Brown
        "#9932CC",  # Dark Orchid
        "#8B0000",  # Dark Red
        "#8B4513",  # Saddle Brown
        "#2E8B57",  # Sea Green
        "#A52A2A",  # Brown
        "#2F4F4F",  # Dark Slate Gray
        "#FF4500",  # Orange Red
        "#4682B4",  # Steel Blue
        "#4B0082"   # Dark Violet
    ]



    ,

            reversescale=False,  # Change to True if you want to reverse the color scale
            marker_line_color='darkgray',  # Border color for countries
            marker_line_width=0.5,  # Border width
            colorbar_title='Depression disorder',  # Title for the color bar
        ))

        fig.update_layout(
            title_text=f"Burden of Depression disorder in {year}",
            geo=dict(
                showcoastlines=True,
                coastlinecolor='Black',
                projection_type='natural earth',  # Natural Earth projection
            ),width=1000
        )
        graph=fig.to_html()
        return render(request,'dep5.html',{'graph':graph,'nyear':nyear})
    return render(request,'dep5.html',{'nyear':nyear}) 

def dep6(request):
    depdisease = readadep()

    # Get unique entities (countries) with non-null code and population
    entity = depdisease[(depdisease["Code"].notnull()) & (depdisease["Population"].notnull())]["Entity"].drop_duplicates().tolist()

    depdisease["Year"] = pd.to_numeric(depdisease["Year"], errors='coerce')

    # Extract unique years and filter them
    nyear = depdisease["Year"].drop_duplicates()

    # Filter years to start from 1990 and exclude any negative years
    nyear =sorted(nyear[(nyear >= 1990) & (nyear >= 0)].tolist())
    if request.method == "POST":
        countries = request.POST.getlist('country[]')
        selected_year = request.POST.get('year')  # Get the selected year from the form
        
        # Check if the selected year is valid
        if selected_year and selected_year.isdigit():
            selected_year = int(selected_year)
            # Filter for the specified countries and the selected year
            df = depdisease[(depdisease["Year"] == selected_year) & (depdisease["Entity"].isin(countries))]
            
            # Check if the DataFrame is empty after filtering
            if df.empty:
                return render(request, 'dep6.html', {'graph': None, 'entity': entity, 'nyear': nyear})

            # Create a horizontal bar chart
            fig_countries = px.bar(
                df,
                x="Population",
                y="Entity",
                title=f"Depression Disorders in {', '.join(countries)} in {selected_year}",
                color="Entity",  # Use country names for color distinction
                text="Population",  # Show population values on bars
                orientation='h',
                color_discrete_sequence=["#D8BFD8", "#9370DB", "#8A2BE2", "#4B0082"]  # Lavender shades
            )

            # Update layout for visual improvements
            fig_countries.update_layout(
                xaxis_title="Depression Disorder Population",
                yaxis_title="Countries",
                plot_bgcolor='rgba(242, 240, 239, 0)',  # Transparent plot background
                paper_bgcolor='rgba(242, 240, 239, 0)',
                hoverlabel=dict(font_size=14, font_color="white"),
                title_font_size=20,
                title_x=0.5,
                width=1000
            )

            graph = fig_countries.to_html()
            return render(request, 'dep6.html', {'graph': graph, 'entity': entity, 'nyear': nyear})

    return render(request, 'dep6.html', {'entity': entity, 'nyear': nyear})

def dep7(request):
    depdisease = readadep()
    # Step 1: Filter the data to exclude non-country entries and restrict years to 1990-2020
    filtered_data = depdisease[(depdisease["Code"].notnull()) &
                         (~depdisease["Entity"].isin(["World", "G20"])) &
                         (depdisease["Year"].between(1990, 2020))]

    # Step 2: Group the data by Year and Entity to get the total burden per country
    country_burden = filtered_data.groupby(['Year', 'Entity'], as_index=False).agg({'Population': 'sum'})

    # Step 3: Calculate the total burden for each year
    total_burden_per_year = country_burden.groupby('Year', as_index=False).agg({'Population': 'sum'})
    total_burden_per_year.rename(columns={'Population': 'TotalBurden'}, inplace=True)

    # Step 4: Merge to get the total burden alongside each country's burden
    merged_df = pd.merge(country_burden, total_burden_per_year, on='Year')

    # Step 5: Calculate the percentage contribution
    merged_df['PercentageContribution'] = (merged_df['Population'] / merged_df['TotalBurden']) * 100

    # Step 6: Get the top 20 countries by total population contribution across all years
    top_countries = merged_df.groupby('Entity')['Population'].sum().nlargest(20).index
    top_20_data = merged_df[merged_df['Entity'].isin(top_countries)]

    # Step 7: Create the sunburst chart
    fig = px.treemap(
        top_20_data,
        path=['Year', 'Entity'],
        values='PercentageContribution',
        title='Percentage Contribution of Cardiovascular Disease Burden by Top 20 Countries (1990-2020)',
        labels={'PercentageContribution': 'Percentage Contribution (%)'}
    )

    fig.update_traces(
        hovertemplate='<b>Year:</b> %{label}<br><b>Percentage Contribution:</b> %{value:.2f}%<extra></extra>'
    )

    # Update layout for better visual appeal
    fig.update_layout(
        title_x=0.5,  # Center the title
         width=1000,   # Set the desired width
    height=600
    )

    graph=fig.to_html()
    return render(request,'dep7.html',{'graph':graph})


def readexp():
    healthexpense = pd.read_csv("public-health-expenditure-share-gdp.csv")
    return healthexpense

def health1(request):
    healthexpense=readexp()
    # Group by country and calculate the mean expenditure
    df_avg = healthexpense.groupby("Entity", as_index=False)["public_health_expenditure_pc_gdp"].mean()

    # Create a bar plot with a color gradient
    fig = px.bar(df_avg, x="Entity", y="public_health_expenditure_pc_gdp",
                 title="Average Public Health Expenditure of all Countries",
                 labels={"public_health_expenditure_pc_gdp": "Average Expenditure (% of GDP)"},
                 text="public_health_expenditure_pc_gdp",
                 color="public_health_expenditure_pc_gdp",  # Use the value as color
                 color_continuous_scale=px.colors.sequential.Plasma)

    # Update layout
    fig.update_layout(
        title={'x': 0.5},
        xaxis_title="Country",
        yaxis_title="Average Expenditure (% of GDP)",
        plot_bgcolor="white",
        font=dict(size=14),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),
        coloraxis_showscale=False , # Hide color bar
        width=1000,height=600
    )

    # Add text to bars for clarity
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    graph=fig.to_html()
    return render(request,'health1.html',{'graph':graph})

def health2(request):
    healthexpense = readexp()
    # Only include countries that have a non-null code and a non-null population
    country = healthexpense[(healthexpense["Code"].notnull()) & (healthexpense["public_health_expenditure_pc_gdp"].notnull())]["Entity"].drop_duplicates().tolist()
    
    if request.method == "POST":
        selected_country = request.POST.get('country')  # Get the selected country from the form
        
        # Filter data for the specified country and starting from 1990
        df_country = healthexpense[(healthexpense['Entity'] == selected_country) & (healthexpense['Year'] >= 1990)]
        
        # Create the line chart
        fig = px.line(df_country,
                      x='Year',
                      y='public_health_expenditure_pc_gdp',
                      markers=True,
                      title=f'Public Health Expenditure as % of GDP Over Time for {selected_country}',
                      labels={'public_health_expenditure_pc_gdp': 'Public Health Expenditure (% of GDP)'},
                      )

        # Customize the layout
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Public Health Expenditure (% of GDP)',
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(245, 245, 220, 0)', title_font_size=25,
            title_x=0.5,
            yaxis=dict(showgrid=True, gridcolor='LightGray'), height=450, width=1000
        )
        graph = fig.to_html()

        return render(request, 'health2.html', {'entity': country, 'graph': graph})

    return render(request, 'health2.html', {'entity': country})

def health3(request):
    healthexpense = readexp()
    
    # Get unique years starting from 1990 and sort them
    n = sorted(healthexpense["Year"].drop_duplicates().tolist())
    n = [year for year in n if year >= 1990]  # Filter years to start from 1990

    if request.method == "POST":
        year = int(request.POST.get('year'))
        # Filter data for the specific year
        df_year = healthexpense[healthexpense['Year'] == year]

        # Sort data by public health expenditure percentage
        df_year = df_year.sort_values(by='public_health_expenditure_pc_gdp', ascending=False)

        # Create the bar chart with enhancements
        fig = px.bar(df_year,
                     x='Entity',
                     y='public_health_expenditure_pc_gdp',
                     text='public_health_expenditure_pc_gdp',  # Display values on bars
                     color='public_health_expenditure_pc_gdp',  # Use color to differentiate by value
                     color_continuous_scale="Viridis")  # Use a color scale (or any other preferred palette)

        # Customize chart appearance
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')  # Show values with 2 decimal places
        fig.update_layout(
            title=f'Public Health Expenditure as % of GDP in {year}',  # Add chart title
            xaxis_title='Country',  # Customize X-axis label
            yaxis_title='Public Health Expenditure (% of GDP)',  # Customize Y-axis label
            xaxis_tickangle=-45,  # Tilt X-axis labels for better readability
            uniformtext_minsize=8, uniformtext_mode='hide',  # Adjust text size
            height=450, width=1000,
            coloraxis_colorbar=dict(
                title="Expenditure % of GDP"  # Fixed color bar title
            ),
            title_font_size=25,
            title_x=0.5,
            plot_bgcolor='rgba(245, 245, 220, 0)'
        )
        
        graph = fig.to_html()
        return render(request, 'health3.html', {'graph': graph, 'n': n})

    return render(request, 'health3.html', {'n': n})

def health4(request):
    healthexpense = readexp()
    # Get unique entities (countries) with non-null code and population
    entity = healthexpense[(healthexpense["Code"].notnull()) & (healthexpense["public_health_expenditure_pc_gdp"].notnull())]["Entity"].drop_duplicates().tolist()

    if request.method == "POST":
        countries = request.POST.getlist('country[]')
        # Filter data for selected countries and years
        df_filtered = healthexpense[
            (healthexpense["Entity"].isin(countries)) &
            (healthexpense["Year"] >= 1990) &
            (healthexpense["Year"] <= 2020)
        ]

        # Create a line plot
        fig = px.line(
            df_filtered,
            x="Year",
            y="public_health_expenditure_pc_gdp",
            color="Entity",
            title=f"Public Health Expenditure Trend ({1990}-{2020})",
            labels={"public_health_expenditure_pc_gdp": "Expenditure (% of GDP)", "Year": "Year"},
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Safe
        )

        # Update layout
        fig.update_layout(
            title={'x': 0.5},
            xaxis_title="Year",
            yaxis_title="Expenditure (% of GDP)",
            plot_bgcolor="white",
            hovermode="x unified",
            font=dict(size=14),
            legend_title_text='Country',
            legend=dict(x=1.02, y=0.98, xanchor='left', yanchor='top'),  # Legend on the right
            xaxis=dict(showgrid=True, gridcolor='lightgrey'),
            yaxis=dict(showgrid=True, gridcolor='lightgrey'),
            width=1000,height=400
        )
        graph = fig.to_html()
        return render(request, 'health4.html', {'graph': graph, 'entity': entity})

    return render(request, 'health4.html', {'entity': entity})

def health5(request):
    healthexpense = readexp()
     # Get unique years starting from 1990 and sort them
    n = sorted(healthexpense["Year"].drop_duplicates().tolist())
    n = [year for year in n if year >= 1990]  # Filter years to start from 1990

    if request.method == "POST":
        year = int(request.POST.get('year'))
        # Filter data for the given year
        df_year = healthexpense[healthexpense["Year"] == year]

        # Sort by expenditure and get the top N countries
        df_year_sorted = df_year.sort_values(by="public_health_expenditure_pc_gdp", ascending=False).head(10)

        # Create a bar plot
        fig = px.bar(df_year_sorted, x="Entity", y="public_health_expenditure_pc_gdp",
                    title=f"Top {10} Countries by Public Health Expenditure in {year}",
                    labels={"public_health_expenditure_pc_gdp": "Expenditure (% of GDP)"},
                    text="public_health_expenditure_pc_gdp",
                    color="Entity",
                    color_discrete_sequence=px.colors.qualitative.Pastel)

        # Update layout
        fig.update_layout(
            title={'x': 0.5},
            xaxis_title="Country",
            yaxis_title="Expenditure (% of GDP)",
            plot_bgcolor="white",
            font=dict(size=14),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='lightgrey'),
            width=1000,height=500
        )

        # Add text to bars for clarity
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        graph = fig.to_html()
        return render(request, 'health5.html', {'graph': graph, 'n': n})

    return render(request, 'health5.html', {'n': n})

def health6(request):
    healthexpense = readexp()
    # Only include countries that have a non-null code and a non-null population
    country = healthexpense[(healthexpense["Code"].notnull()) & (healthexpense["public_health_expenditure_pc_gdp"].notnull())]["Entity"].drop_duplicates().tolist()
    
    if request.method == "POST":
        selected_country = request.POST.get('country')  # Get the selected country from the form
        
        # Filter data for the selected country
        df_country = healthexpense[healthexpense["Entity"] == selected_country].sort_values(by="Year")

        # Calculate year-over-year growth rate for the country
        df_country["Growth_Rate"] = df_country["public_health_expenditure_pc_gdp"].pct_change() * 100

        # Remove rows with missing values (first year will have NaN growth rate)
        df_country = df_country.dropna(subset=["Growth_Rate"])

        # Create an area chart with a curvy line and markers
        fig = px.area(
            df_country,
            x="Year",
            y="Growth_Rate",
            title=f"Year-Over-Year Growth Rate of Public Health Expenditure for {selected_country}",
            labels={"Growth_Rate": "Growth Rate (%)", "Year": "Year"},
            color_discrete_sequence=["#4baf47"]  # Lighter dark green color for the area
        )

        # Update traces for curvy lines and markers
        fig.update_traces(
            line_shape='spline',  # Makes the line curvy
            line_smoothing=0.6,   # Adjust the smoothness (0 to 1)
            mode='lines+markers',  # Add markers to the area chart
            marker=dict(size=10, line=dict(width=2, color='white'))  # Customize markers
        )

        # Highlight the highest and lowest points
        max_value = df_country["Growth_Rate"].max()
        min_value = df_country["Growth_Rate"].min()
        max_year = df_country.loc[df_country["Growth_Rate"] == max_value, "Year"].values[0]
        min_year = df_country.loc[df_country["Growth_Rate"] == min_value, "Year"].values[0]

        # Add scatter points for max and min
        fig.add_trace(
            px.scatter(
                x=[max_year],
                y=[max_value],
                labels={"x": "Year", "y": "Growth Rate (%)"}
            ).data[0].update(marker=dict(color='red', size=12, symbol='star'), name='Highest Point', showlegend=True)
        )

        fig.add_trace(
            px.scatter(
                x=[min_year],
                y=[min_value],
                labels={"x": "Year", "y": "Growth Rate (%)"}
            ).data[0].update(marker=dict(color='red', size=12, symbol='diamond'), name='Lowest Point', showlegend=True)
        )

        # Customize the chart layout
        fig.update_layout(
            title={'x': 0.5},
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            plot_bgcolor="white",
            hovermode="x unified",
            font=dict(size=14),
            xaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Show grid for clarity
            yaxis=dict(showgrid=True, gridcolor='lightgrey'),
            margin=dict(l=40, r=40, t=60, b=40),  # Adjust margins for better layout
            width=1000
        )
        
        graph = fig.to_html()
        return render(request, 'health6.html', {'entity': country, 'graph': graph})

    return render(request, 'health6.html', {'entity': country})

def health7(request):
    healthexpense = readexp()

    # Step 1: Filter the data to exclude non-country entries and years before 1990
    filtered_data = healthexpense[
        (healthexpense["Code"].notnull()) & 
        (~healthexpense["Entity"].isin(["World", "G20"])) & 
        (healthexpense["Year"] >= 1990)  # Include only years from 1990 onwards
    ]

    # Step 2: Group the data by Year and Entity to get the total health expenditure per country
    country_expenditure = filtered_data.groupby(['Year', 'Entity'], as_index=False).agg({'public_health_expenditure_pc_gdp': 'sum'})

    # Step 3: Calculate the total expenditure for each year
    total_expenditure_per_year = country_expenditure.groupby('Year', as_index=False).agg({'public_health_expenditure_pc_gdp': 'sum'})
    total_expenditure_per_year.rename(columns={'public_health_expenditure_pc_gdp': 'TotalExpenditure'}, inplace=True)

    # Step 4: Merge to get the total expenditure alongside each country's expenditure
    merged_df = pd.merge(country_expenditure, total_expenditure_per_year, on='Year')

    # Step 5: Calculate the percentage contribution
    merged_df['PercentageContribution'] = (merged_df['public_health_expenditure_pc_gdp'] / merged_df['TotalExpenditure']) * 100

    # Step 6: Get the top 20 countries by total expenditure
    top_countries = merged_df.groupby('Entity')['public_health_expenditure_pc_gdp'].sum().nlargest(20).index
    top_20_data = merged_df[merged_df['Entity'].isin(top_countries)]

    # Step 7: Create the sunburst chart
    fig = px.treemap(
        top_20_data,
        path=['Year', 'Entity'],
        values='PercentageContribution',
        title='Percentage Contribution of Public Health Expenditure by Top 20 Countries per Year',
        labels={
            'PercentageContribution': 'Percentage Contribution (%)',
            'labels': 'Year'
        }
    )

    fig.update_traces(
        hovertemplate='<b>Year:</b> %{label}<br>Percentage Contribution:</b> %{value:.2f}%<extra></extra>'
    )

    # Update layout for better visual appeal
    fig.update_layout(
        title_x=0.5,  # Center the title
        width=1000,
        height=650
    )

    graph = fig.to_html()
    return render(request, 'health7.html', {'graph': graph})

def dashboard(request):
    return render(request,'dashboard.html')


def dash(request):
    
    return render(request,'dash.html')

#dashboard without google
# def dash(request):
#     user = register_model.objects.get(email=request.session['email'])
#     # Split the username to get only the first name
#     first_name = user.username.split(" ")[0] if user.username else ""

#     return render(request, 'dash.html', {'user': user, 'first_name': first_name}) 

# def dash(request):
#     # Check if the user is authenticated via Google or if the session has the 'em' key
#     if not (request.user.is_authenticated or request.session.get('email')):
#         return redirect('login')

#     user_data = None

#     # Google OAuth authenticated user
#     if request.user.is_authenticated:
#         try:
#             user_social = UserSocialAuth.objects.filter(user=request.user, provider='google-oauth2').first()
#             if user_social:
#                 # Retrieve or create user data in user_register
#                 user, created = register_model.objects.get_or_create(
#                     email=request.user.email,
#                     defaults={'name': request.user.get_full_name() or request.user.username}  # Use default profile image if available
#                 )

#                 if created:
#                     user.save()

#                 user_data = {
#                     'name': user.username,
#                     'email': user.email,
#                     'image_ed': user.image_ed,
#                 }
#             else:
#                 return redirect('login')
#         except UserSocialAuth.DoesNotExist:
#             return redirect('login')

#     # Session-based authenticated user
#     elif 'email' in request.session:
#         email = request.session.get('email')
#         try:
#             user = get_object_or_404(register_model, email=email)
#             user_data = {
#                 'name': user.username,
#                 'email': user.email,
#                 'image_ed': user.image_ed,
#             }
#         except register_model.DoesNotExist:
#             return redirect('login')

#     return render(request, "dash.html", {"user": user_data})


# Predictions
def predictionmain(request):
    return render(request,'predictionmain.html')

def preddiscards(request):
    return render(request,'preddiscards.html')


def cdisease_prediction(request):
    return render(request,'cdisease_prediction.html')

def arima_result(request):
    return render(request,'arima_result.html')
    

def cdisease_prediction(request):
    if request.method == 'POST':
        # Load the dataset
        df = pd.read_csv("burden-of-disease-by-cause.csv", parse_dates=['Year'])
        
        # Get the selected country from the POST request
        country = request.POST.get('country')
        
        # Filter data for the selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'DALYs (Disability-Adjusted Life Years) - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)']]
        production = production.sort_values('Year').set_index('Year')
        y = production
        
        # Define the parameter ranges for SARIMA
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        # Initialize variables for finding the best model
        min_aic = float('inf')
        best_param = None
        best_seasonal_param = None
        
        # Loop through all combinations of SARIMA parameters
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    # Fit the SARIMA model with the given parameters
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit(maxiter=1000, disp=False)
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_param = param
                        best_seasonal_param = param_seasonal
                except:
                    continue
        
        # Fit the best SARIMA model
        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_param,
                                        seasonal_order=best_seasonal_param,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit(maxiter=1000, disp=False)
        
        # Forecasting
        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
        
        # Create the line chart
        fig = go.Figure()

        # Actual values trace (line chart)
        # Actual values trace with lines and markers (dots)
        # Actual values trace with lines, markers (dots), and fill color
        fig.add_trace(go.Scatter(
            x=y.index,
            y=y['DALYs (Disability-Adjusted Life Years) - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)'],
            name='Actual Value',
            mode='lines+markers',  # Adds both lines and dots
            line=dict(color='#7C00FE'),  # Line color
            marker=dict(size=8, color='#7C00FE', symbol='circle'),  # Dot styling
            fill='tozeroy',  # Fill color to zero on the y-axis
            fillcolor='rgba(124, 0, 254, 0.2)',  # Light transparent fill color
            hoverinfo='x+y'
        ))

        # Predicted values trace with lines, markers (dots), and fill color
        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index,
            y=pred_uc.predicted_mean,
            name='Predicted Value',
            mode='lines+markers',  # Adds both lines and dots
            line=dict(color='#cf2d11'),  # Line color
            marker=dict(size=8, color='#cf2d11', symbol='circle'),  # Dot styling
            fill='tozeroy',  # Fill color to zero on the y-axis
            fillcolor='rgba(207, 45, 17, 0.2)',  # Light transparent fill color
            hoverinfo='x+y'
        ))



        # Update layout
        fig.update_layout(
            title=f"Cardiovascular Disease BUrden Prediction for {country}",
            xaxis_title="Year",
            yaxis_title="DALYs (Number)",
            legend_title="Legend",
            height=600,
            width=1000,
            title_font_size=26,
            font=dict(family="Arial, sans-serif", size=16, color="black"),
            title_font=dict(color='darkblue'),
            title_x=0.5,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black",
                tickangle=45
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black"
            ),
            margin=dict(l=70, r=40, t=100, b=40)
        )

        # Convert the figure to HTML for rendering in Django template
        graph = fig.to_html()
        return render(request, 'arima_result.html', {'graph': graph, 'name':'cardio'})

    else:
        # Render the country selection form if it's a GET request
        data = pd.read_csv("burden-of-disease-by-cause.csv")
        # column = data["Entity"].drop_duplicates().tolist()
        column = data[(data["Code"].notnull()) & (data["DALYs (Disability-Adjusted Life Years) - Cardiovascular diseases - Sex: Both - Age: All Ages (Number)"].notnull())]["Entity"].  drop_duplicates().tolist()
        return render(request, 'cdisease_prediction.html', {"data": column, 'name':'cardio'})

        

def nprediction(request):
    if request.method == 'POST':
        # Load the dataset
        df = pd.read_csv("burden-of-disease-by-cause.csv", parse_dates=['Year'])
        
        # Get the selected country from the POST request
        country = request.POST.get('country')
        
        # Filter data for the selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'DALYs (Disability-Adjusted Life Years) - Neurological disorders - Sex: Both - Age: All Ages (Number)']]
        production = production.sort_values('Year').set_index('Year')
        y = production
        
        # Define the parameter ranges for SARIMA
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        # Initialize variables for finding the best model
        min_aic = float('inf')
        best_param = None
        best_seasonal_param = None
        
        # Loop through all combinations of SARIMA parameters
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    # Fit the SARIMA model with the given parameters
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_param = param
                        best_seasonal_param = param_seasonal
                except:
                    continue

        # Fit the best SARIMA model
        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_param,
                                        seasonal_order=best_seasonal_param,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations

        # Forecasting
        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
        
        # Create the area chart
        fig = go.Figure()

        # Actual values trace with improved styling (Area chart)
        fig.add_trace(go.Scatter(
            x=y.index,
            y=y['DALYs (Disability-Adjusted Life Years) - Neurological disorders - Sex: Both - Age: All Ages (Number)'],
            mode='lines',
            name='Actual Value',
            line=dict(color='#7C00FE'),  # Lavender color for actual values
            fill='tozeroy',  # Fill area under the line
            hoverinfo='x+y'
        ))

        # Predicted values trace (Area chart)
        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index,
            y=pred_uc.predicted_mean,
            mode='lines',
            name='Predicted Value',
            line=dict(color='#cf2d11'),  # Soft red shade for predicted values
            fill='tozeroy',  # Fill area under the line
            hoverinfo='x+y'
        ))

                # Update layout for button-triggered animation only
        fig.update_layout(
            title=f"Neurological Disease Burden Prediction for {country}",
            xaxis_title="Year",
            yaxis_title="DALYs (Number)",
            legend_title="Legend",
            height=600,
            width=1000,
            title_font_size=26,
            font=dict(family="Arial, sans-serif", size=16, color="black"),
            title_font=dict(color='darkblue'),
            title_x=0.5,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black",
                tickangle=45
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black"
            ),
            margin=dict(l=70, r=40, t=100, b=40),
                    # Only use buttons for animation
            updatemenus=[{
            'buttons': [
                {'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate'}],  # Duration set to 100ms
                'label': 'Play',
                'method': 'animate'},
                {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'}
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }]

        )

       # Define frames
        frames = [go.Frame(
            data=[
                go.Scatter(
                    x=y.index[:i],
                    y=y['DALYs (Disability-Adjusted Life Years) - Neurological disorders - Sex: Both - Age: All Ages (Number)'][:i],
                    fill='tozeroy',
                    line=dict(color='#7C00FE'),
                    name='Actual Value'
                ),
                go.Scatter(
                    x=pred_uc.predicted_mean.index[:i],
                    y=pred_uc.predicted_mean[:i],
                    fill='tozeroy',
                    line=dict(color='#cf2d11'),
                    name='Predicted Value'
                )
            ],
            name=str(i)
        ) for i in range(1, len(y) + 1)]

        fig.frames = frames

        # Update layout for button-triggered animation only
        fig.update_layout(
            updatemenus=[{
            'buttons': [
                {'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate'}],  # Duration set to 100ms
                'label': 'Play',
                'method': 'animate'},
                {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'}
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }]

        )




        



        # Convert the figure to HTML for rendering in Django template
        graph = fig.to_html()
        return render(request, 'arima_result.html', {'graph': graph,'name':'neuro'})

    else:
        # Render the country selection form if it's a GET request
        data = pd.read_csv("burden-of-disease-by-cause.csv")
        # column = data["Entity"].drop_duplicates().tolist()
        column = data[(data["Code"].notnull()) & (data["DALYs (Disability-Adjusted Life Years) - Neurological disorders - Sex: Both - Age: All Ages (Number)"].notnull())]["Entity"].  drop_duplicates().tolist()
        return render(request, 'nprediction.html', {"data": column,'name':'neuro'})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess

@csrf_exempt  # Only for development; use CSRF token in production
def run_prediction(request):
    if request.method == 'POST':
        try:
            # Run the command-line process
            subprocess.run(['python', 'nprediction.py'], check=True)  # Replace with your script
            return JsonResponse({'success': True})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt  # Only for development; use CSRF token in production
def run_prediction1(request):
    if request.method == 'POST':
        try:
            # Run the command-line process
            subprocess.run(['python', 'cdisease_prediction.py'], check=True)  # Replace with your script
            return JsonResponse({'success': True})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        
@csrf_exempt  # Only for development; use CSRF token in production
def run_prediction2(request):
    if request.method == 'POST':
        try:
            # Run the command-line process
            subprocess.run(['python', 'digprediction.py'], check=True)  # Replace with your script
            return JsonResponse({'success': True})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)   

@csrf_exempt  # Only for development; use CSRF token in production
def run_prediction4(request):
    if request.method == 'POST':
        try:
            # Run the command-line process
            subprocess.run(['python', 'dkprediction.py'], check=True)  # Replace with your script
            return JsonResponse({'success': True})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)  

@csrf_exempt  # Only for development; use CSRF token in production
def run_prediction5(request):
    if request.method == 'POST':
        try:
            # Run the command-line process
            subprocess.run(['python', 'rprediction.py'], check=True)  # Replace with your script
            return JsonResponse({'success': True})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)   

@csrf_exempt  # Only for development; use CSRF token in production
def run_prediction6(request):
    if request.method == 'POST':
        try:
            # Run the command-line process
            subprocess.run(['python', 'mentalprediction.py'], check=True)  # Replace with your script
            return JsonResponse({'success': True})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)  

@csrf_exempt  # Only for development; use CSRF token in production
def run_prediction7(request):
    if request.method == 'POST':
        try:
            # Run the command-line process
            subprocess.run(['python', 'anxietyrprediction.py'], check=True)  # Replace with your script
            return JsonResponse({'success': True})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)  

@csrf_exempt  # Only for development; use CSRF token in production
def run_prediction8(request):
    if request.method == 'POST':
        try:
            # Run the command-line process
            subprocess.run(['python', 'depressprediction.py'], check=True)  # Replace with your script
            return JsonResponse({'success': True})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)    

@csrf_exempt  # Only for development; use CSRF token in production
def run_prediction9(request):
    if request.method == 'POST':
        try:
            # Run the command-line process
            subprocess.run(['python', 'healthprediction.py'], check=True)  # Replace with your script
            return JsonResponse({'success': True})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)                                                 

def digprediction(request):
    if request.method == 'POST':
        # Load the dataset
        df = pd.read_csv("burden-of-disease-by-cause.csv", parse_dates=['Year'])
        
        # Get the selected country from the POST request
        country = request.POST.get('country')
        
        # Filter data for the selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'DALYs (Disability-Adjusted Life Years) - Digestive diseases - Sex: Both - Age: All Ages (Number)']]
        production = production.sort_values('Year').set_index('Year')
        y = production
        
        # Define the parameter ranges for SARIMA
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        # Initialize variables for finding the best model
        min_aic = float('inf')
        best_param = None
        best_seasonal_param = None
        
        # Loop through all combinations of SARIMA parameters
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    # Fit the SARIMA model with the given parameters
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_param = param
                        best_seasonal_param = param_seasonal
                except:
                    continue

        # Fit the best SARIMA model
        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_param,
                                        seasonal_order=best_seasonal_param,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations

        # Forecasting
        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
        
        # Create the area chart
        fig = go.Figure()

        # Actual values trace with improved styling (Area chart)
        fig.add_trace(go.Scatter(
            x=y.index,
            y=y['DALYs (Disability-Adjusted Life Years) - Digestive diseases - Sex: Both - Age: All Ages (Number)'],
            mode='lines',
            name='Actual Value',
            line=dict(color='#7C00FE'),  # Lavender color for actual values
            fill='tozeroy',  # Fill area under the line
            hoverinfo='x+y'
        ))

        # Predicted values trace (Area chart)
        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index,
            y=pred_uc.predicted_mean,
            mode='lines',
            name='Predicted Value',
            line=dict(color='#cf2d11'),  # Soft red shade for predicted values
            fill='tozeroy',  # Fill area under the line
            hoverinfo='x+y'
        ))

                # Update layout for button-triggered animation only
        fig.update_layout(
            title=f"Digestive Disease Burden Prediction for {country}",
            xaxis_title="Year",
            yaxis_title="DALYs (Number)",
            legend_title="Legend",
            height=600,
            width=1000,
            title_font_size=26,
            font=dict(family="Arial, sans-serif", size=16, color="black"),
            title_font=dict(color='darkblue'),
            title_x=0.5,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black",
                tickangle=45
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black"
            ),
            margin=dict(l=70, r=40, t=100, b=40),
                    # Only use buttons for animation
            updatemenus=[{
            'buttons': [
                {'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate'}],  # Duration set to 100ms
                'label': 'Play',
                'method': 'animate'},
                {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'}
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }]

        )

       # Define frames
        frames = [go.Frame(
            data=[
                go.Scatter(
                    x=y.index[:i],
                    y=y['DALYs (Disability-Adjusted Life Years) - Digestive diseases - Sex: Both - Age: All Ages (Number)'][:i],
                    fill='tozeroy',
                    line=dict(color='#7C00FE'),
                    name='Actual Value'
                ),
                go.Scatter(
                    x=pred_uc.predicted_mean.index[:i],
                    y=pred_uc.predicted_mean[:i],
                    fill='tozeroy',
                    line=dict(color='#cf2d11'),
                    name='Predicted Value'
                )
            ],
            name=str(i)
        ) for i in range(1, len(y) + 1)]

        fig.frames = frames

        # Update layout for button-triggered animation only
        fig.update_layout(
            updatemenus=[{
            'buttons': [
                {'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate'}],  # Duration set to 100ms
                'label': 'Play',
                'method': 'animate'},
                {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'}
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }]

        )
        # Convert the figure to HTML for rendering in Django template
        graph = fig.to_html()
        return render(request, 'arima_result.html', {'graph': graph,'name':'dig'})

    else:
        # Render the country selection form if it's a GET request
        data = pd.read_csv("burden-of-disease-by-cause.csv")
        # column = data["Entity"].drop_duplicates().tolist()
        column = data[(data["Code"].notnull()) & (data["DALYs (Disability-Adjusted Life Years) - Digestive diseases - Sex: Both - Age: All Ages (Number)"].notnull())]["Entity"].  drop_duplicates().tolist()
        return render(request, 'digprediction.html', {"data": column,'name':'dig'})


def dkprediction(request):
    if request.method == 'POST':
        # Load the dataset
        df = pd.read_csv("burden-of-disease-by-cause.csv", parse_dates=['Year'])
        
        # Get the selected country from the POST request
        country = request.POST.get('country')
        
        # Filter data for the selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'DALYs (Disability-Adjusted Life Years) - Diabetes and kidney diseases - Sex: Both - Age: All Ages (Number)']]
        production = production.sort_values('Year').set_index('Year')
        y = production
        
        # Define the parameter ranges for SARIMA
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
        
        # Initialize variables for finding the best model
        min_aic = float('inf')
        best_param = None
        best_seasonal_param = None
        
        # Loop through all combinations of SARIMA parameters
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    # Fit the SARIMA model with the given parameters
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_param = param
                        best_seasonal_param = param_seasonal
                except:
                    continue
        
        # Fit the best SARIMA model
        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_param,
                                        seasonal_order=best_seasonal_param,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations
        
        # Forecasting
        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
        
        # Create the bar chart
        fig = go.Figure()

        # Actual values trace with improved styling
        fig.add_trace(go.Bar(
            x=y.index,
            y=y['DALYs (Disability-Adjusted Life Years) - Diabetes and kidney diseases - Sex: Both - Age: All Ages (Number)'],
            name='Actual Value',
            marker_color='#7C00FE ',  
            hoverinfo='x+y',
            marker_line_color='rgba(0,0,0,0.5)',  # Light border color
            marker_line_width=1.5,
            
        ))

        # Predicted values trace with improved styling
        fig.add_trace(go.Bar(
            x=pred_uc.predicted_mean.index,
            y=pred_uc.predicted_mean,
            name='Predicted Value',
            marker_color='#cf2d11',  # Soft red shade
            hoverinfo='x+y',
            marker_line_color='rgba(0,0,0,0.5)',
            marker_line_width=1.5,
            
        ))

        # Update layout for improved design
        fig.update_layout(
            title=f"Diabetic Kidney Disease Burden Prediction for {country}",
            xaxis_title="Year",
            yaxis_title="DALYs (Number)",
            legend_title="Legend",
            # plot_bgcolor='rgba(245, 245, 245, 0)',  # Subtle light background
            height=600,
            width=1000,
            title_font_size=26,  # Larger title font size
            
            font=dict(family="Arial, sans-serif", size=16, color="black"),  # Clean font family
            title_font=dict(color='darkblue'),
            title_x=0.5,  # Center the title
            xaxis=dict(
                showgrid=False,  # Remove grid lines for a cleaner look
                zeroline=False,  # No zero line
                showline=True,
                linecolor="black",  # Black axis line
                tickangle=45  # Tilted ticks for better readability
            ),
            yaxis=dict(
                showgrid=False,  # Remove grid lines
                zeroline=False,  # No zero line
                showline=True,
                linecolor="black"  # Black axis line
            ),
            margin=dict(l=70, r=40, t=100, b=40),  # Balanced margins
            bargap=0.15,  # Smaller gap between bars
            barmode='group',  # Grouped bars
            transition_duration=500,  # Slightly slower transitions for smoother effect
            updatemenus=[{
                'buttons': [
                    {'args': [None, {'frame': {'duration': 200, 'redraw': True}, 'fromcurrent': True}],
                    'label': 'Play',
                    'method': 'animate'},
                    {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'}
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'type': 'buttons',
                'x': 0.1,
                'xanchor': 'right',
                'y': 0,
                'yanchor': 'top'
            }]
        )

        # Update hover information
        fig.update_traces(
            hoverinfo='text',
            hovertemplate='Year: %{x}<br>DALYs: %{y:,.0f}'  # Cleaner hover template
        )

        # Frames for smooth animation
        frames = [go.Frame(
            data=[
                go.Bar(
                    x=y.index[:i],
                    y=y['DALYs (Disability-Adjusted Life Years) - Diabetes and kidney diseases - Sex: Both - Age: All Ages (Number)'][:i],
                    marker_color='#7C00FE',
                    name='Actual Value'
                ),
                go.Bar(
                    x=pred_uc.predicted_mean.index[:i],
                    y=pred_uc.predicted_mean[:i],
                    marker_color='#cf2d11',
                    name='Predicted Value'
                )
            ],
            name=str(i)
        ) for i in range(1, len(y) + 1)]

        fig.frames = frames  # Add animation frames

        
        # Convert the figure to HTML for rendering in Django template
        graph = fig.to_html()
        return render(request, 'arima_result.html', {'graph': graph,'name':'dk'})

    else:
        # Render the country selection form if it's a GET request
        data = pd.read_csv("burden-of-disease-by-cause.csv")
        # column = data["Entity"].drop_duplicates().tolist()
        column = data[(data["Code"].notnull()) & (data["DALYs (Disability-Adjusted Life Years) - Diabetes and kidney diseases - Sex: Both - Age: All Ages (Number)"].notnull())]["Entity"].  drop_duplicates().tolist()
        return render(request, 'dkprediction.html', {"data": column,'name':'dk'})     

def rprediction(request):

    if request.method == 'POST':
        # Load the dataset
        df = pd.read_csv("burden-of-disease-by-cause.csv", parse_dates=['Year'])
        
        # Get the selected country from the POST request
        country = request.POST.get('country')
        
        # Filter data for the selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'DALYs (Disability-Adjusted Life Years) - Chronic respiratory diseases - Sex: Both - Age: All Ages (Number)']]
        production = production.sort_values('Year').set_index('Year')
        y = production
        
        # Define the parameter ranges for SARIMA
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
        
        # Initialize variables for finding the best model
        min_aic = float('inf')
        best_param = None
        best_seasonal_param = None
        
        # Loop through all combinations of SARIMA parameters
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    # Fit the SARIMA model with the given parameters
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_param = param
                        best_seasonal_param = param_seasonal
                except:
                    continue
        
        # Fit the best SARIMA model
        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_param,
                                        seasonal_order=best_seasonal_param,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations
        
        # Forecasting
        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
        
        # Create the bar chart
        fig = go.Figure()

        # Actual values trace with improved styling
        fig.add_trace(go.Bar(
            x=y.index,
            y=y['DALYs (Disability-Adjusted Life Years) - Chronic respiratory diseases - Sex: Both - Age: All Ages (Number)'],
            name='Actual Value',
            marker_color='#7C00FE ',  
            hoverinfo='x+y',
            marker_line_color='rgba(0,0,0,0.5)',  # Light border color
            marker_line_width=1.5,
            
        ))

        # Predicted values trace with improved styling
        fig.add_trace(go.Bar(
            x=pred_uc.predicted_mean.index,
            y=pred_uc.predicted_mean,
            name='Predicted Value',
            marker_color='#cf2d11',  # Soft red shade
            hoverinfo='x+y',
            marker_line_color='rgba(0,0,0,0.5)',
            marker_line_width=1.5,
            
        ))

        # Update layout for improved design
        fig.update_layout(
            title=f"Chronic Respiratory Disease Burden Prediction for {country}",
            xaxis_title="Year",
            yaxis_title="DALYs (Number)",
            legend_title="Legend",
            # plot_bgcolor='rgba(245, 245, 245, 0)',  # Subtle light background
            height=600,
            width=1000,
            title_font_size=26,  # Larger title font size
            
            font=dict(family="Arial, sans-serif", size=16, color="black"),  # Clean font family
            title_font=dict(color='darkblue'),
            title_x=0.5,  # Center the title
            xaxis=dict(
                showgrid=False,  # Remove grid lines for a cleaner look
                zeroline=False,  # No zero line
                showline=True,
                linecolor="black",  # Black axis line
                tickangle=45  # Tilted ticks for better readability
            ),
            yaxis=dict(
                showgrid=False,  # Remove grid lines
                zeroline=False,  # No zero line
                showline=True,
                linecolor="black"  # Black axis line
            ),
            margin=dict(l=70, r=40, t=100, b=40),  # Balanced margins
            bargap=0.15,  # Smaller gap between bars
            barmode='group',  # Grouped bars
            transition_duration=500,  # Slightly slower transitions for smoother effect
            updatemenus=[{
                'buttons': [
                    {'args': [None, {'frame': {'duration': 200, 'redraw': True}, 'fromcurrent': True}],
                    'label': 'Play',
                    'method': 'animate'},
                    {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'}
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'type': 'buttons',
                'x': 0.1,
                'xanchor': 'right',
                'y': 0,
                'yanchor': 'top'
            }]
        )

        # Update hover information
        fig.update_traces(
            hoverinfo='text',
            hovertemplate='Year: %{x}<br>DALYs: %{y:,.0f}'  # Cleaner hover template
        )

        # Frames for smooth animation
        frames = [go.Frame(
            data=[
                go.Bar(
                    x=y.index[:i],
                    y=y['DALYs (Disability-Adjusted Life Years) - Chronic respiratory diseases - Sex: Both - Age: All Ages (Number)'][:i],
                    marker_color='#7C00FE',
                    name='Actual Value'
                ),
                go.Bar(
                    x=pred_uc.predicted_mean.index[:i],
                    y=pred_uc.predicted_mean[:i],
                    marker_color='#cf2d11',
                    name='Predicted Value'
                )
            ],
            name=str(i)
        ) for i in range(1, len(y) + 1)]

        fig.frames = frames  # Add animation frames

        
        # Convert the figure to HTML for rendering in Django template
        graph = fig.to_html()
        return render(request, 'arima_result.html', {'graph': graph,'name':'resp'})

    else:
        # Render the country selection form if it's a GET request
        data = pd.read_csv("burden-of-disease-by-cause.csv")
        # column = data["Entity"].drop_duplicates().tolist()
        column = data[(data["Code"].notnull()) & (data["DALYs (Disability-Adjusted Life Years) - Chronic respiratory diseases - Sex: Both - Age: All Ages (Number)"].notnull())]["Entity"].  drop_duplicates().tolist()

        return render(request, 'rprediction.html', {"data": column,'name':'resp'})
    


def predictiondiscards(request):
    return render(request,'predictiondiscards.html')   

def mentalprediction(request):
    if request.method == 'POST':
        # Load the dataset
        df = pd.read_csv("burden-of-disease-by-cause.csv", parse_dates=['Year'])
        
        # Get the selected country from the POST request
        country = request.POST.get('country')
        
        # Filter data for the selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'DALYs (Disability-Adjusted Life Years) - Mental disorders - Sex: Both - Age: All Ages (Number)']]
        production = production.sort_values('Year').set_index('Year')
        y = production
        
        # Define the parameter ranges for SARIMA
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
        
        # Initialize variables for finding the best model
        min_aic = float('inf')
        best_param = None
        best_seasonal_param = None
        
        # Loop through all combinations of SARIMA parameters
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    # Fit the SARIMA model with the given parameters
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit(maxiter=1000, disp=False)
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_param = param
                        best_seasonal_param = param_seasonal
                except:
                    continue
        
        # Fit the best SARIMA model
        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_param,
                                        seasonal_order=best_seasonal_param,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit(maxiter=1000, disp=False)
        
        # Forecasting
        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
        
        # Create the animated time-series chart
        fig = go.Figure()

        # Trace for actual values
        fig.add_trace(go.Scatter(
            x=y.index,
            y=y['DALYs (Disability-Adjusted Life Years) - Mental disorders - Sex: Both - Age: All Ages (Number)'],
            mode='lines+markers',
            name='Actual Value',
            line=dict(color='#7C00FE', width=2),
            marker=dict(size=6),
            hoverinfo='x+y'
        ))

        # Trace for predicted values
        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index,
            y=pred_uc.predicted_mean,
            mode='lines+markers',
            name='Predicted Value',
            line=dict(color='#cf2d11', width=2),
            marker=dict(size=6),
            hoverinfo='x+y'
        ))

        # Add frames for animation (loop through actual and predicted data)
        frames = [go.Frame(
            data=[
                go.Scatter(
                    x=y.index[:i],
                    y=y['DALYs (Disability-Adjusted Life Years) - Mental disorders - Sex: Both - Age: All Ages (Number)'][:i],
                    mode='lines+markers',
                    line=dict(color='#7C00FE', width=2),
                    marker=dict(size=6),
                    name='Actual Value'
                ),
                go.Scatter(
                    x=pred_uc.predicted_mean.index[:i],
                    y=pred_uc.predicted_mean[:i],
                    mode='lines+markers',
                    line=dict(color='#cf2d11', width=2),
                    marker=dict(size=6),
                    name='Predicted Value'
                )
            ],
            name=f'frame{i}'
        ) for i in range(1, len(y) + 1)]
        
        fig.frames = frames  # Add the frames for the animation

        # Layout and Animation Settings
        fig.update_layout(
            title=f"Mental Disorder Burden Prediction for {country}",
            xaxis_title="Year",
            yaxis_title="DALYs (Number)",
            height=600,
            width=1000,
            title_font_size=26,
            font=dict(family="Arial, sans-serif", size=16, color="black"),
            title_font=dict(color='darkblue'),
            title_x=0.5,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black",
                tickangle=45
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black"
            ),
            margin=dict(l=70, r=40, t=100, b=40),
            transition_duration=500,
            updatemenus=[{
                'buttons': [
                    {'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True}],
                    'label': 'Play',
                    'method': 'animate'},
                    {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'}
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'type': 'buttons',
                'x': 0.1,
                'xanchor': 'right',
                'y': 0,
                'yanchor': 'top'
            }]
        )

        # Convert the figure to HTML for rendering in Django template
        graph = fig.to_html()
        return render(request, 'arima_result.html', {'graph': graph, 'name': 'mental'})

    else:
        # Render the country selection form if it's a GET request
        data = pd.read_csv("burden-of-disease-by-cause.csv")
        # column = data["Entity"].drop_duplicates().tolist()
        column = data[(data["Code"].notnull()) & (data["DALYs (Disability-Adjusted Life Years) - Mental disorders - Sex: Both - Age: All Ages (Number)"].notnull())]["Entity"].  drop_duplicates().tolist()

        return render(request, 'mentalprediction.html', {"data": column, 'name': 'mental'})

def anxietyprediction(request):
    if request.method == 'POST':
                # Load the dataset
        df = pd.read_csv("anxietydisorders.csv")

        # Convert 'Year' column to datetime format
        df['Year'] = pd.to_datetime(df['Year'], errors='coerce', format='%Y')

        # Filter out rows where 'Year' is less than 1990
        df = df[df['Year'].dt.year >= 1990]

        # Ensure Population is of numeric type and drop rows where 'Population' is null
        df['Population'] = pd.to_numeric(df['Population'], errors='coerce')  # Convert to numeric
        df = df.dropna(subset=['Population'])  # Drop rows where 'Population' is null

        
        # Get the selected country from the POST request
        country = request.POST.get('country')
        
        # Filter data for the selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'Population']]
        production = production.sort_values('Year').set_index('Year')
        y = production
        
        # Define the parameter ranges for SARIMA
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
        
        # Initialize variables for finding the best model
        min_aic = float('inf')
        best_param = None
        best_seasonal_param = None
        
        # Loop through all combinations of SARIMA parameters
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    # Fit the SARIMA model with the given parameters
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_param = param
                        best_seasonal_param = param_seasonal
                except:
                    continue
        
        # Fit the best SARIMA model
        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_param,
                                        seasonal_order=best_seasonal_param,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations
        
        # Forecasting
        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
        
        # Create the bar chart
        fig = go.Figure()

        # Actual values trace with improved styling
        fig.add_trace(go.Bar(
            x=y.index,
            y=y['Population'],
            name='Actual Value',
            marker_color='#7C00FE ',  
            hoverinfo='x+y',
            marker_line_color='rgba(0,0,0,0.5)',  # Light border color
            marker_line_width=1.5,
            
        ))

        # Predicted values trace with improved styling
        fig.add_trace(go.Bar(
            x=pred_uc.predicted_mean.index,
            y=pred_uc.predicted_mean,
            name='Predicted Value',
            marker_color='#cf2d11',  # Soft red shade
            hoverinfo='x+y',
            marker_line_color='rgba(0,0,0,0.5)',
            marker_line_width=1.5,
            
        ))

        # Update layout for improved design
        fig.update_layout(
            title=f"Anxiety Disorder Burden Prediction for {country}",
            xaxis_title="Year",
            yaxis_title="DALYs (Number)",
            legend_title="Legend",
            # plot_bgcolor='rgba(245, 245, 245, 0)',  # Subtle light background
            height=600,
            width=1000,
            title_font_size=26,  # Larger title font size
            
            font=dict(family="Arial, sans-serif", size=16, color="black"),  # Clean font family
            title_font=dict(color='darkblue'),
            title_x=0.5,  # Center the title
            xaxis=dict(
                showgrid=False,  # Remove grid lines for a cleaner look
                zeroline=False,  # No zero line
                showline=True,
                linecolor="black",  # Black axis line
                tickangle=45  # Tilted ticks for better readability
            ),
            yaxis=dict(
                showgrid=False,  # Remove grid lines
                zeroline=False,  # No zero line
                showline=True,
                linecolor="black"  # Black axis line
            ),
            margin=dict(l=70, r=40, t=100, b=40),  # Balanced margins
            bargap=0.15,  # Smaller gap between bars
            barmode='group',  # Grouped bars
            transition_duration=500,  # Slightly slower transitions for smoother effect
            updatemenus=[{
                'buttons': [
                    {'args': [None, {'frame': {'duration': 200, 'redraw': True}, 'fromcurrent': True}],
                    'label': 'Play',
                    'method': 'animate'},
                    {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'}
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'type': 'buttons',
                'x': 0.1,
                'xanchor': 'right',
                'y': 0,
                'yanchor': 'top'
            }]
        )

        # Update hover information
        fig.update_traces(
            hoverinfo='text',
            hovertemplate='Year: %{x}<br>DALYs: %{y:,.0f}'  # Cleaner hover template
        )

        # Frames for smooth animation
        frames = [go.Frame(
            data=[
                go.Bar(
                    x=y.index[:i],
                    y=y['Population'][:i],
                    marker_color='#7C00FE',
                    name='Actual Value'
                ),
                go.Bar(
                    x=pred_uc.predicted_mean.index[:i],
                    y=pred_uc.predicted_mean[:i],
                    marker_color='#cf2d11',
                    name='Predicted Value'
                )
            ],
            name=str(i)
        ) for i in range(1, len(y) + 1)]

        fig.frames = frames  # Add animation frames

        
        # Convert the figure to HTML for rendering in Django template
        graph = fig.to_html()
        return render(request, 'arima_result.html', {'graph': graph,'name':'anx'})

    else:
        # Render the country selection form if it's a GET request
        data = pd.read_csv("anxietydisorders.csv")
        # column = data["Entity"].drop_duplicates().tolist()
        column = data[(data["Code"].notnull()) & (data["Population"].notnull())]["Entity"].  drop_duplicates().tolist()
        return render(request, 'anxietyprediction.html', {"data": column,'name':'anx'})
   

def depressprediction(request):
    if request.method == 'POST':
        # Load the dataset
        df = pd.read_csv("depression.csv")

        # Convert 'Year' column to datetime format
        df['Year'] = pd.to_datetime(df['Year'], errors='coerce', format='%Y')

        # Filter out rows where 'Year' is less than 1990
        df = df[df['Year'].dt.year >= 1990]
        
        
        # Get the selected country from the POST request
        country = request.POST.get('country')
        
        # Filter data for the selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'Population']]
        production = production.sort_values('Year').set_index('Year')
        y = production
        
        # Define the parameter ranges for SARIMA
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        # Initialize variables for finding the best model
        min_aic = float('inf')
        best_param = None
        best_seasonal_param = None
        
        # Loop through all combinations of SARIMA parameters
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    # Fit the SARIMA model with the given parameters
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_param = param
                        best_seasonal_param = param_seasonal
                except:
                    continue

        # Fit the best SARIMA model
        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_param,
                                        seasonal_order=best_seasonal_param,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit(maxiter=1000, disp=False)  # Increase max iterations

        # Forecasting
        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
        
        # Create the area chart
        fig = go.Figure()

        # Actual values trace with improved styling (Area chart)
        fig.add_trace(go.Scatter(
            x=y.index,
            y=y['Population'],
            mode='lines',
            name='Actual Value',
            line=dict(color='#7C00FE'),  # Lavender color for actual values
            fill='tozeroy',  # Fill area under the line
            hoverinfo='x+y'
        ))

        # Predicted values trace (Area chart)
        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index,
            y=pred_uc.predicted_mean,
            mode='lines',
            name='Predicted Value',
            line=dict(color='#cf2d11'),  # Soft red shade for predicted values
            fill='tozeroy',  # Fill area under the line
            hoverinfo='x+y'
        ))

                # Update layout for button-triggered animation only
        fig.update_layout(
            title=f"Depression Disorder Burden Prediction for {country}",
            xaxis_title="Year",
            yaxis_title="DALYs (Number)",
            legend_title="Legend",
            height=600,
            width=1000,
            title_font_size=26,
            font=dict(family="Arial, sans-serif", size=16, color="black"),
            title_font=dict(color='darkblue'),
            title_x=0.5,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black",
                tickangle=45
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black"
            ),
            margin=dict(l=70, r=40, t=100, b=40),
                    # Only use buttons for animation
            updatemenus=[{
            'buttons': [
                {'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate'}],  # Duration set to 100ms
                'label': 'Play',
                'method': 'animate'},
                {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'}
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }]

        )

       # Define frames
        frames = [go.Frame(
            data=[
                go.Scatter(
                    x=y.index[:i],
                    y=y['Population'][:i],
                    fill='tozeroy',
                    line=dict(color='#7C00FE'),
                    name='Actual Value'
                ),
                go.Scatter(
                    x=pred_uc.predicted_mean.index[:i],
                    y=pred_uc.predicted_mean[:i],
                    fill='tozeroy',
                    line=dict(color='#cf2d11'),
                    name='Predicted Value'
                )
            ],
            name=str(i)
        ) for i in range(1, len(y) + 1)]

        fig.frames = frames

        # Update layout for button-triggered animation only
        fig.update_layout(
            updatemenus=[{
            'buttons': [
                {'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate'}],  # Duration set to 100ms
                'label': 'Play',
                'method': 'animate'},
                {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'}
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }]

        )
        # Convert the figure to HTML for rendering in Django template
        graph = fig.to_html()
        return render(request, 'arima_result.html', {'graph': graph,'name':'depress'})

    else:
        # Render the country selection form if it's a GET request
        data = pd.read_csv("depression.csv")
        # column = data["Entity"].drop_duplicates().tolist()
        column = data[(data["Code"].notnull()) & (data["Population"].notnull())]["Entity"].  drop_duplicates().tolist()
        return render(request, 'depressprediction.html', {"data": column,'name':'depress'})
    

def healthprediction(request):
    if request.method == 'POST':
        # Load the dataset
        df = pd.read_csv("public-health-expenditure-share-gdp.csv", parse_dates=['Year'])
        
        # Get the selected country from the POST request
        country = request.POST.get('country')
        
        # Filter data for the selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'public_health_expenditure_pc_gdp']]
        production = production.sort_values('Year').set_index('Year')
        y = production
        
        # Define the parameter ranges for SARIMA
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        # Initialize variables for finding the best model
        min_aic = float('inf')
        best_param = None
        best_seasonal_param = None
        
        # Loop through all combinations of SARIMA parameters
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    # Fit the SARIMA model with the given parameters
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit(maxiter=1000, disp=False)
                    if results.aic < min_aic:
                        min_aic = results.aic
                        best_param = param
                        best_seasonal_param = param_seasonal
                except:
                    continue
        
        # Fit the best SARIMA model
        mod = sm.tsa.statespace.SARIMAX(y,
                                        order=best_param,
                                        seasonal_order=best_seasonal_param,
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = mod.fit(maxiter=1000, disp=False)
        
        # Forecasting
        steps = int(request.POST.get('steps'))
        pred_uc = results.get_forecast(steps=steps)
        
        # Create the line chart
        fig = go.Figure()

        # Actual values trace (line chart)
        # Actual values trace with lines and markers (dots)
        # Actual values trace with lines, markers (dots), and fill color
        fig.add_trace(go.Scatter(
            x=y.index,
            y=y['public_health_expenditure_pc_gdp'],
            name='Actual Value',
            mode='lines+markers',  # Adds both lines and dots
            line=dict(color='#7C00FE'),  # Line color
            marker=dict(size=8, color='#7C00FE', symbol='circle'),  # Dot styling
            fill='tozeroy',  # Fill color to zero on the y-axis
            fillcolor='rgba(124, 0, 254, 0.2)',  # Light transparent fill color
            hoverinfo='x+y'
        ))

        # Predicted values trace with lines, markers (dots), and fill color
        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index,
            y=pred_uc.predicted_mean,
            name='Predicted Value',
            mode='lines+markers',  # Adds both lines and dots
            line=dict(color='#cf2d11'),  # Line color
            marker=dict(size=8, color='#cf2d11', symbol='circle'),  # Dot styling
            fill='tozeroy',  # Fill color to zero on the y-axis
            fillcolor='rgba(207, 45, 17, 0.2)',  # Light transparent fill color
            hoverinfo='x+y'
        ))



        # Update layout
        fig.update_layout(
            title=f"Health Expenses Burden Prediction for {country}",
            xaxis_title="Year",
            yaxis_title="DALYs (Number)",
            legend_title="Legend",
            height=600,
            width=1000,
            title_font_size=26,
            font=dict(family="Arial, sans-serif", size=16, color="black"),
            title_font=dict(color='darkblue'),
            title_x=0.5,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black",
                tickangle=45
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="black"
            ),
            margin=dict(l=70, r=40, t=100, b=40)
        )

        # Convert the figure to HTML for rendering in Django template
        graph = fig.to_html()
        return render(request, 'arima_result.html', {'graph': graph, 'name':'health'})

    else:
        # Render the country selection form if it's a GET request
        data = pd.read_csv("public-health-expenditure-share-gdp.csv")
        # column = data["Entity"].drop_duplicates().tolist()
        column = data[(data["Code"].notnull()) & (data["public_health_expenditure_pc_gdp"].notnull())]["Entity"].  drop_duplicates().tolist()
        return render(request, 'healthprediction.html', {"data": column, 'name':'health'})


# Load the trained model
model1 = load_model('lungcancerpred2.keras')

# Example class label mapping (replace with actual labels from your dataset)
class_labels = {
    0: 'Lung adenocarcinoma',
    1: 'Lung benign tissue',
    2: 'Lung squamous cell carcinoma'

}



def heartupload(request):
    if request.method == 'POST' and request.FILES['image']:
        # Handle the uploaded image
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        file_path = fs.save(uploaded_image.name, uploaded_image)
        image_url = fs.url(file_path)
        full_path = fs.path(file_path)

        # Preprocess the image for plant disease detection
        img = image.load_img(full_path, target_size=(256, 256))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = img_array / 255.0  # Normalize for the plant disease model

        # Make prediction with the plant disease model
        predictions = model1.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]

        # Map class index to readable label
        predicted_label = class_labels.get(predicted_class, "Unknown Disease")
       

        return render(request, 'heartresult.html', {'label': predicted_label, 'image_url': image_url})

    return render(request, 'heartupload.html')




def heartresult(request,file_path):
    context = {
        'image_url': file_path,
        
    }
    return render(request, 'heartresult.html',context)



import numpy as np
from django.shortcuts import render
import joblib

# Load saved models and scalers
scaler = joblib.load('scaler.pkl')
model = joblib.load('heart_model.pkl')

def predictheart(request):
    if request.method == 'POST':
        # Collect data from POST request
        age = int(request.POST.get('age'))
        gender = int(request.POST.get('gender'))
        cp = int(request.POST.get('cp'))
        trestbps = int(request.POST.get('trestbps'))
        chol = int(request.POST.get('chol'))
        fbs = int(request.POST.get('fbs'))
        restecg = int(request.POST.get('restecg'))
        thalach = int(request.POST.get('thalach'))
        exang = int(request.POST.get('exang'))
        oldpeak = float(request.POST.get('oldpeak'))
        slope = int(request.POST.get('slope'))
        ca = int(request.POST.get('ca'))
        thal = int(request.POST.get('thal'))

        # Prepare feature array for prediction
        features = np.array([[age, gender, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

        # Scaling the features
        features_scaled = scaler.transform(features)

        # Make the prediction
        prediction = model.predict(features_scaled)
        result = prediction[0]  # Get the prediction result

        # Render the result page with the prediction result
        return render(request, 'predresultheart.html', {'result': result})

    # For GET requests, render the form
    return render(request, 'predictheart.html')


def about(request):
    return render(request,'about.html')

def eda(request):
    return render(request,'eda.html')   
 
def eda1(request):
    return render(request,'eda1.html')    

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render
from django.conf import settings
import os

def edagraph(request):
    # Load the heart disease dataset
    hearteda = pd.read_csv("heart.csv")

    # Define the color for the background of the plot
    background_color = "#ffe6e6"

    # Map numerical values of 'sex' and 'target' to their respective categories
    hearteda['sex'] = hearteda['sex'].map({1: 'Male', 0: 'Female'})
    hearteda['target'] = hearteda['target'].map({1: 'Heart Disease', 0: 'No Heart Disease'})

    # Drop any rows with missing values in 'sex' or 'target'
    hearteda_cleaned = hearteda.dropna(subset=['sex', 'target'])

    # Create a count plot to visualize heart disease frequency by sex
    plt.figure(figsize=(6, 4))
    plt.gca().set_facecolor(background_color)  # Set the axes background color
    sns.countplot(x='sex', hue='target', data=hearteda_cleaned, palette='Set1')

    # Add labels and title
    plt.title('Heart Disease Frequency for Males and Females', fontsize=16)
    plt.xlabel('Sex', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.legend(title='Heart Disease', loc='upper right')  # Ensure the legend is shown

    # Save the plot to a temporary image file
    plt.tight_layout()  # Adjust the layout to prevent clipping
    
    # Define the path for saving the plot
    plot_path = os.path.join(settings.MEDIA_ROOT, 'plot.png')  # Using MEDIA_ROOT for paths
    plt.savefig(plot_path)  # Save the plot to the specified path
    plt.close()  # Close the plot to free memory

    # Pass the relative path to the image for rendering in the template
    return render(request, 'edagraph.html', {'graph': os.path.join(settings.MEDIA_URL, 'plot.png')})  # Pass the path to the saved image

def edagraph1(request):

    #Load the heart disease dataset
    hearteda = pd.read_csv("heart.csv")

    # Define the color for the background of the plot
    background_color = "#ffe6e6"

    # Map numerical values of 'sex' and 'target' to their respective categories
    hearteda['sex'] = hearteda['sex'].map({1: 'Male', 0: 'Female'})
    hearteda['target'] = hearteda['target'].map({1: 'Heart Disease', 0: 'No Heart Disease'})

    # Drop any rows with missing values in 'sex' or 'target'
    hearteda_cleaned = hearteda.dropna(subset=['sex', 'target'])

    # Filter the dataset for people with heart disease (target = 'Heart Disease')
    heart_disease_only = hearteda_cleaned[hearteda_cleaned['target'] == 'Heart Disease']

    # Create a figure with the custom background color
    plt.figure(figsize=(10, 6))
    
    # Plot a histogram for age distribution only for people with heart disease
    sns.histplot(data=heart_disease_only, x='age', kde=False, color='#5833ff', bins=15)

    # Set the background color
    plt.gca().set_facecolor(background_color)
    plt.gcf().set_facecolor(background_color)

    # Add title and labels
    plt.title('Age Distribution for People with Heart Disease', fontsize=16, fontweight='bold')
    plt.xlabel('Age', fontsize=12)
    plt.ylabel('Count', fontsize=12)

    # Save the plot to a temporary image file using MEDIA_ROOT
    plt.tight_layout()  # Adjust the layout to prevent clipping
    plot_path = os.path.join(settings.MEDIA_ROOT, 'age_distribution.png')  # Using MEDIA_ROOT for paths
    plt.savefig(plot_path)  # Save the plot to the specified path
    plt.close()  # Close the plot to free memory

    # Pass the relative path to the image for rendering in the template
    return render(request, 'edagraph1.html', {'graph': os.path.join(settings.MEDIA_URL, 'age_distribution.png')})

import warnings
def edagraph2(request):
    warnings.filterwarnings("ignore")
    # Load the heart disease dataset
    hearteda = pd.read_csv("heart.csv")
    
    background_color = "#ffe6e6"
    color_palette = ["#800000", "#8000ff", "#6aac90", "#5833ff", "#da8829"]
    
    feature_plots = {}
    features = ['sex', 'exang', 'ca', 'cp', 'fbs', 'restecg', 'slope', 'thal']
    
    # Create individual plots for each feature
    for feature in features:
        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor(background_color)
        ax.set_facecolor(background_color)
        
        ax.grid(color='#000000', linestyle=':', axis='y', zorder=0, dashes=(1, 5))
        sns.countplot(ax=ax, data=hearteda, x=feature, palette=color_palette[:4])
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        
        plot_path = os.path.join(settings.MEDIA_ROOT, f'{feature}_plot.png')
        plt.savefig(plot_path)
        plt.close()
        
        feature_plots[feature] = os.path.join(settings.MEDIA_URL, f'{feature}_plot.png')
    
    return render(request, 'edagraph2.html', {'feature_plots': feature_plots})

def edagraph3(request):
    # Load the heart disease dataset
    hearteda = pd.read_csv("heart.csv")

    # Map target values to their labels
    hearteda['target'] = hearteda['target'].map({1: 'Heart Disease', 0: 'No Heart Disease'})

    # Count the number of occurrences for each target value
    target_counts = hearteda['target'].value_counts()

    # Create a figure for the pie chart with the desired background color
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.patch.set_facecolor("#ffe6e6")  # Set the figure background color
    ax.set_facecolor("#ffe6e6")  # Set the axes background color

    # Create the pie chart
    ax.pie(target_counts, labels=target_counts.index, autopct='%1.1f%%', startangle=90,
           colors=["#800000", "#5833ff"], shadow=True, explode=(0.1, 0))  # explode the first slice

    # Add a title
    ax.set_title('Distribution of Heart Disease', fontsize=16, fontweight='bold')

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    # Save the figure to a file
    plot_path = os.path.join(settings.MEDIA_ROOT, 'heart_disease_distribution.png')
    plt.savefig(plot_path)
    plt.close()

    # Pass the relative path to the image for rendering in the template
    return render(request, 'edagraph3.html', {'graph': os.path.join(settings.MEDIA_URL, 'heart_disease_distribution.png')})


def edagraph4(request):
    # Load the heart disease dataset
    hearteda = pd.read_csv("heart.csv")

    # Define the relevant features to analyze
    features_to_analyze = ['cp', 'exang', 'ca', 'thal', 'restecg']

    # Create a DataFrame to hold the counts
    counts = {}

    # Count occurrences for each feature (0 and 1)
    for feature in features_to_analyze:
        counts[feature] = hearteda[feature].value_counts()

    # Convert the counts dictionary to a DataFrame
    counts_df = pd.DataFrame(counts).fillna(0)

    # Calculate total counts for each feature (summing 0 and 1)
    counts_df['Total'] = counts_df.sum(axis=1)

    # Reset index to have feature names as a column
    counts_df = counts_df.reset_index().rename(columns={'index': 'Feature'})

    # Sort by total counts
    counts_df = counts_df.sort_values(by='Total', ascending=False)

    # Calculate percentage
    counts_df['Percentage'] = (counts_df['Total'] / counts_df['Total'].sum()) * 100

    # Define a custom color list
    custom_palette = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0']

    # Plotting
    plt.figure(figsize=(10, 9))
    ax = sns.barplot(x='Feature', y='Total', data=counts_df, palette=custom_palette)

    # Title and labels
    plt.title('Most Common Symptoms/Risk Factors Contributing to Heart Disease', fontsize=16)
    plt.xlabel('Symptoms/Risk Factors', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)

    # Set x-ticks with meaningful labels
    plt.xticks(ticks=range(len(features_to_analyze)),
               labels=[
                   'Chest Pain',    # cp
                   'Exercise Angina',  # exang
                   'Major Vessels',  # ca
                   'Thalassemia',    # thal
                   'Resting ECG'     # restecg
               ],
               rotation=45)

    # Display percentage on top of each bar
    for i, p in enumerate(ax.patches):
        ax.annotate(f'{p.get_height():.1f} ({counts_df["Percentage"].iloc[i]:.1f}%)',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black',
                    xytext=(0, 2), textcoords='offset points')

    plt.gcf().set_facecolor('#ffe6e6')  # Set background color

    # Save the figure to a file
    plot_path = os.path.join(settings.MEDIA_ROOT, 'symptoms_risk_factors.png')
    plt.savefig(plot_path)
    plt.close()

    # Pass the relative path to the image for rendering in the template
    return render(request, 'edagraph4.html', {'graph': os.path.join(settings.MEDIA_URL, 'symptoms_risk_factors.png')})


def edagraph5(request):
    # Load the heart disease dataset
    hearteda = pd.read_csv("heart.csv")

    # Step 1: Calculate summary statistics for thalach by target
    thalach_summary = hearteda.groupby('target')['thalach'].agg(['min', 'max', 'mean']).reset_index()

    # Rename columns for better understanding
    thalach_summary.columns = ['Heart Disease Status', 'Min Thalach', 'Max Thalach', 'Mean Thalach']

    # Display the summary statistics in console (optional)
    print(thalach_summary)

    # Step 2: Visual Representation
    plt.figure(figsize=(10, 6))

    # Bar plot for Mean Thalach
    bars = plt.bar(thalach_summary['Heart Disease Status'].map({0: 'No Heart Disease', 1: 'Heart Disease'}), 
                   thalach_summary['Mean Thalach'], 
                   color=["#E0B0FF", "#CD853F"])
    
    plt.title('Impact of Maximum Heart Rate Achieved on Heart Disease Status', fontsize=16)
    plt.xlabel('Heart Disease Status', fontsize=12)
    plt.ylabel('Maximum Heart Rate Achieved (thalach)', fontsize=12)
    plt.xticks(rotation=0)
    plt.gcf().set_facecolor('#ffe6e6')  # Set background color

    # Add numbers on top of the bars
    for bar in bars:
        yval = bar.get_height()  # Get the height of the bar
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}', ha='center', va='bottom', fontsize=10, color='black')

    # Save the figure to a file
    plot_path = os.path.join(settings.MEDIA_ROOT, 'thalach_summary.png')
    plt.savefig(plot_path)
    plt.close()  # Close the plot to free memory

    # Pass the relative path to the image for rendering in the template
    return render(request, 'edagraph5.html', {'graph': os.path.join(settings.MEDIA_URL, 'thalach_summary.png')})

def progheartcards(request):
    return render(request,'progheartcards.html')

def chatbot(request):
    return render(request,'chatbot.html')


def chatbotnav(request):
    return render(request,'chatbotnav.html')   

def navbar(request):
    return render(request,'navbar.html') 

def blogs(request):
    all_blogs = Blogs.objects.all()  # Fetch all blog entries
    return render(request, 'blogs.html', {'all_blogs': all_blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blogs, id=blog_id)  # Fetch the blog post based on the ID
    return render(request, 'blog_detail.html', {'blog': blog})   

from datetime import date,datetime,timedelta

def news(request):
    newsapi = NewsApiClient(api_key='3ba86abce05142e5afe689196a952ccb')

    # Fetch articles from the past 29 days
    json_data = newsapi.get_everything(
        q='smart medical',
        language='en',
        from_param=(datetime.today() - timedelta(days=29)).strftime('%Y-%m-%d'),
        to=datetime.today().strftime('%Y-%m-%d'),
        page_size=30,
        page=2,
        sort_by='relevancy'
    )

    articles = json_data['articles']
    return render(request, 'news.html', {'k': articles})

   
import requests
from django.shortcuts import render

def identify_pill(request):
    result = None
    error = None

    if request.method == 'POST':
        color = request.POST.get('color', '').strip().lower()
        shape = request.POST.get('shape', '').strip().lower()
        imprint = request.POST.get('imprint', '').strip().lower()

        search_terms = []
        if color:
            search_terms.append(f"openfda.color:{color}")
        if shape:
            search_terms.append(f"openfda.shape:{shape}")
        if imprint:
            search_terms.append(f"openfda.imprint:{imprint}")

        if search_terms:
            query_string = "+AND+".join(search_terms)
            url = f"https://api.fda.gov/drug/label.json?search=openfda.color:pink&limit=5"  # Limit results for testing

            try:
                response = requests.get(url)
                response.raise_for_status()  # Raises HTTPError for bad responses
                data = response.json()
                
                if "results" in data and data["results"]:
                    result = data["results"]
                else:
                    error = "No matches found for the given criteria."
                    
            except requests.exceptions.HTTPError as http_err:
                error = f"HTTP error: {http_err}"
            except requests.exceptions.RequestException as e:
                error = f"Error fetching data from NDC API: {e}"

    return render(request, 'pill.html', {'result': result, 'error': error})


# views.py
from django.shortcuts import render
from .models import Pill

# Define color and shape options here, or retrieve from a backend source
COLOR_OPTIONS = ["White", "Blue", "Red", "Green", "Yellow", "Pink"]
SHAPE_OPTIONS = ["Round", "Oval", "Square", "Rectangle", "Triangle"]

def pill_search(request):
    if request.method == "GET" and "imprint" in request.GET:
        # Retrieve the search parameters from the form
        imprint = request.GET.get("imprint")
        color = request.GET.get("color")
        shape = request.GET.get("shape")

        # Search the database for pills matching the input criteria
        pills = Pill.objects.filter(imprint__iexact=imprint, color__iexact=color, shape__iexact=shape)


        # Check if any pills were found
        if pills.exists():
            # Render the results if pills are found in the database
            return render(request, "pill_search.html", {
                "pill_data": pills,
                "colors": COLOR_OPTIONS,
                "shapes": SHAPE_OPTIONS,
            })
        else:
            # If no pills are found, display an error message
            return render(request, "pill_search.html", {
                "error": "No pills found for the given criteria.",
                "colors": COLOR_OPTIONS,
                "shapes": SHAPE_OPTIONS,
            })

    # Render the search form with color and shape options
    return render(request, "pill_search.html", {
        "colors": COLOR_OPTIONS,
        "shapes": SHAPE_OPTIONS,
    })
