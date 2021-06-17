import pandas as pd
from datetime import date, datetime
from re import sub
from repository import zipcodes
from repository import model as rmd


def create_prequote(quote_det):
    zip = clean_zip(quote_det['zip'])
    dob = clean_dob(quote_det['dob'])
    gender = clean_gender(quote_det['gender'])
    dwelling = clean_dwelling(quote_det['dwelling'])
    deductible = clean_deductible(quote_det['deductible'])
    data = [[zip, dob, gender, dwelling, deductible]]

    linear_reg_model = rmd.get_lr_model()
    premium_est = linear_reg_model.predict(data)[0]
    # Add to repository
    return premium_est

def clean_dob(dob):
    today = date.today()
    born = datetime.strptime(dob, '%m/%d/%Y').date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def clean_zip(zip):
    zip_obj = zipcodes.get_avg_pre_zip(zip)
    avg_premium = [item['premium'] for item in zip_obj][0]
    value = float(sub(r'[^\d.]', '', avg_premium))
    return value

def clean_gender(gender):
    if gender == 'M':
        return 1
    else:
        return 0

def clean_dwelling(dwe):
    return int(dwe.replace(',',''))

def clean_deductible(ded):
    deductible_dict = {
        'A': 4,
        'B': 2,
        'C': 1,
        'D': 2,
        'E': 3
    }
    return int(deductible_dict[ded])

def clean_premium(pre):
    return float(pre)