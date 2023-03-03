from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):

    PERSON_HOME_OWNERSHIP_OPTIONS = (
        ('0', 'Mortgage'),
        ('1', 'Others'),
        ('2', 'Own'),
        ('3', 'Rent'),
    )

    PERSON_LOAN_INTENT_OPTIONS = (
        ('EDUCATION', 'Education'),
        ('HOMEIMPROVEMENT', 'Home Improvement'),
        ('DEBTCONSOLIDATION', 'Debt Consolidation'),
        ('VENTURE', 'Venture'),
        ('MEDICAL', 'Medical'),
        ('PERSONAL', 'Personal'),
    )

    first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address.')

    age = forms.FloatField(min_value=18, max_value=120, help_text="Please make sure that you are at least an adult to be be eligible to apply for a loan.")
    monthly_income = forms.FloatField()    
    home_ownership_status = forms.ChoiceField(widget=forms.Select, choices=PERSON_HOME_OWNERSHIP_OPTIONS)
    employment_length = forms.FloatField(help_text='For how many years have you been employed?')
    loan_intent = forms.ChoiceField(widget=forms.Select, choices=PERSON_LOAN_INTENT_OPTIONS)

    loan_amount = forms.FloatField()
    expected_loan_interest_rate = forms.FloatField()
    default_on_file = forms.BooleanField()

    credit_history_length = forms.FloatField()

    # birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'age', 'monthly_income', 'home_ownership_status', 'employment_length', 'loan_intent', 'loan_amount', 'expected_loan_interest_rate', 'default_on_file', 'credit_history_length')