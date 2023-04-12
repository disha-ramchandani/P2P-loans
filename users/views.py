from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import BorrowerSignUpForm, LenderSignUpForm
from . import ml_model
import math


def landing_page(request):
    return render(request, 'users/landing_page.html')

def home(request):
    if request.user.is_authenticated:
        user_is_borrower = hasattr(request.user.profile, "is_borrower") and request.user.profile.is_borrower
        if user_is_borrower:
            return render(request, 'users/borrower/home.html')
        else:
            loan_grades = ['A', 'B', 'C', 'D', 'E']
            liquid_funds = math.inf

            if request.method == "POST":
                liquid_funds = request.data.liquid_funds
                

            relevant_profiles = Profile.objects.filter(is_borrower=True, loan_grade__in=loan_grades, loan_amnt__lte=liquid_funds)

            return render(request, 'users/lender/home.html', {"profiles": relevant_profiles, "loan_options": BorrowerSignUpForm.PERSON_LOAN_INTENT_OPTIONS})
    
    return redirect("getstarted")

def getstarted(request):
    if request.user.is_authenticated:
        return redirect("home")

    return render(request, 'users/get_started.html')

def signup_borrower(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        form = BorrowerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.profile.is_borrower = True

            # user.profile.birth_date = form.cleaned_data.get('birth_date')
            
            user.profile.person_age = form.cleaned_data.get('age')
            user.profile.person_income = form.cleaned_data.get('monthly_income')
            user.profile.person_home_ownership = form.cleaned_data.get('home_ownership_status')
            user.profile.person_emp_length = form.cleaned_data.get('employment_length')
            user.profile.loan_intent = form.cleaned_data.get('loan_intent')            

            user.profile.loan_amnt = form.cleaned_data.get('loan_amount')
            user.profile.loan_int_rate = form.cleaned_data.get('expected_loan_interest_rate')

            user.profile.loan_percent_income = float(user.profile.loan_amnt) / float(user.profile.person_income)
            user.profile.cb_person_default_on_file = form.cleaned_data.get('default_on_file')
            user.profile.cb_person_cred_hist_length = form.cleaned_data.get('credit_history_length')

            # Requires ML prediction
            user.profile.loan_grade = ml_model.predict_grade_for_user(user.profile)

            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = BorrowerSignUpForm()
        
    context = { 'form': form }
    return render(request, 'users/borrower/signup.html', context)

def signup_lender(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        form = LendferSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.is_borrower = False
            user.profile.liquid_funds = form.cleaned_data.get('liquid_funds')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = LenderSignUpForm()
        
    context = { 'form': form }
    return render(request, 'users/lender/signup.html', context)

def logout_page(request):
    logout(request)
    return redirect("landing")