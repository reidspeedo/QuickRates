import pandas as pd
from services import prequote as cd
from repository import model as rmd
from sklearn import linear_model


def run_model(file):
    nc_data_df = pd.read_csv(file)
    cl_data_df = clean_training_data(nc_data_df)
    model = generate_linear_model(cl_data_df)
    id = rmd.update_lr_model(model)
    return id

def update_model(file):
    nc_data_df = pd.read_csv(file)
    cl_data_df = clean_training_data(nc_data_df)
    model = generate_linear_model(cl_data_df)
    id = rmd.update_lr_model(model)
    return id

def clean_training_data(input_df):
    output_df = pd.DataFrame()
    #Zip Code Clean Up
    output_df['zip'] = [cd.clean_zip(zip) for zip in input_df['zip']]
    #DOB clean up
    output_df['dob'] = list(map(cd.clean_dob, input_df['dob']))
    #Gender cleanup
    output_df['gender'] = list(map(cd.clean_gender, input_df['gender']))
    #Dwelling
    output_df['dwelling'] = list(map(cd.clean_dwelling, input_df['dwelling']))
    #Deductible
    output_df['deductible'] = list(map(cd.clean_deductible, input_df['deductible']))
    #Premium
    output_df['premium'] = list(map(cd.clean_premium, input_df['premium']))
    return output_df

def generate_linear_model(df):
    X = df[['zip', 'dob', 'gender', 'dwelling', 'deductible']]
    Y = df['premium']
    regr = linear_model.LinearRegression()
    regr.fit(X, Y)
    return regr