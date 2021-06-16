import pandas as pd
from datetime import date, datetime
from re import sub
from decimal import Decimal
from sklearn import linear_model

def retrieve_state_zips(file, state):
    az = pd.read_csv(file)
    state_zips = az[az['state'] == state]
    return state_zips

def clean_dob(dob):
    today = date.today()
    born = datetime.strptime(dob, '%m/%d/%Y').date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def clean_zip(zip, avg_prm_for_zip):
    avg_premium = avg_prm_for_zip.loc[avg_prm_for_zip['zip'] == zip, 'premium'].iloc[0]
    value = Decimal(sub(r'[^\d.]', '', avg_premium))
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

def clean_data(input_df, avg_prm_for_zip):
    output_df = pd.DataFrame()
    #Zip Code Clean Up
    output_df['zip'] = [clean_zip(zip, avg_prm_for_zip) for zip in input_df['zip']]
    #DOB clean up
    output_df['dob'] = list(map(clean_dob, input_df['dob']))
    #Gender cleanup
    output_df['gender'] = list(map(clean_gender, input_df['gender']))
    #Dwelling
    output_df['dwelling'] = list(map(clean_dwelling, input_df['dwelling']))
    #Deductible
    output_df['deductible'] = list(map(clean_deductible, input_df['deductible']))
    #Premium
    output_df['premium'] = list(map(clean_premium, input_df['premium']))
    return output_df

def generate_linear_model(df):
    X = df[['zip', 'dob', 'gender', 'dwelling', 'deductible']]
    Y = df['premium']
    regr = linear_model.LinearRegression()
    regr.fit(X,Y)
    return regr

if __name__ == "__main__":
    nc_data = pd.read_csv('training_data.csv')
    #print((nc_data.head(5)))
    state_zip_file = r'/Users/reidrelatores/PycharmProjects/QuickRate/nerdwallet_scraper/zip_avg_premium.csv'
    state = 'Washington'
    avg_prm_for_zip = retrieve_state_zips(state_zip_file, state)
    c_data = clean_data(nc_data, avg_prm_for_zip)
    model = generate_linear_model(c_data)

    input_dict = {
        'zip': clean_zip(98155, avg_prm_for_zip),
        'dob': clean_dob('1/1/1970'),
        'gender': clean_gender('M'),
        'dwelling': clean_dwelling('270000'),
        'deductible': clean_deductible('A')
    }
    input_data = [list(input_dict.values())]


    print('Intercept: ', model.intercept_)
    print('Coefficients: ', model.coef_)
    print('Prediction:', input_data, model.predict(input_data))

