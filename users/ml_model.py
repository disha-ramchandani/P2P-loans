import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn import tree

model = None

def ensure_model_trained():

    global model

    if model: return

    print("Starting training...")

    df = pd.read_csv('dataset.csv')
    inputs = df.drop(['loan_grade'],axis=1)
    target = df['loan_grade']

    le_person_home_ownership = LabelEncoder()

    inputs['home_ownership'] = le_person_home_ownership.fit_transform(inputs['person_home_ownership'])
    # We are anyways dropping this column
    # inputs['loan_intent'] = le_person_home_ownership.fit_transform(inputs['loan_intent'])
    inputs['person_default_on_file'] = le_person_home_ownership.fit_transform(inputs['cb_person_default_on_file'])

    inputs_n = inputs.drop(['person_home_ownership','loan_intent','cb_person_default_on_file'],axis=1)

    model = tree.DecisionTreeClassifier()
    model.fit(inputs_n, target)
    model.score(inputs_n,target)

    print("Completed training.")

def predict_for_raw_data(raw_data):
    ensure_model_trained()
    return model.predict([raw_data])[0]

def predict_grade_for_user(profile):
    ensure_model_trained()
    return model.predict([[0, profile.person_age, profile.person_income, profile.person_emp_length, profile.loan_amnt, profile.loan_int_rate, profile.loan_percent_income, profile.cb_person_cred_hist_length, profile.person_home_ownership, 1 if profile.cb_person_default_on_file else 0]])[0]