from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm
from . import ml_model

def landing_page(request):
    return render(request, 'users/landing_page.html')

def home(request):
    return render(request, 'users/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

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
        form = SignupForm()
        
    context = { 'form': form }
    return render(request, 'users/signup.html', context)
