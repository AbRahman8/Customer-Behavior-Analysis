import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

df= pd.read_csv('customer_shopping_behavior.csv')
print(df.head())
print(df.shape)
# print(df.info())
print(df.isnull().sum())

#Fixing Coloumn name
df.columns = df.columns.str.lower().str.replace(" ", "_")
print(df.info())
df = df.rename(columns = {'purchase_amount_(usd)' : 'purchase_amount'})



# Imputing missing values in Review Rating column with the median rating of the product category
df['review_rating'] = df.groupby('category')['review_rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())

#Create new column age_group
labels = ['Young Adult', 'Adult', 'Middle-Aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)
print(df[['age', 'age_group']].head(10))

# create new column purchase_frequency_days
print(df['frequency_of_purchases'].unique())

frequency_mapping = {
    'Fortnightly' : 14, "Weekly" : 7, 'Annually' : 365,
    'Quarterly' : 90, 'Bi-Weekly': 14, 'Monthly' : 30,
    'Every 3 Months' : 90
}

df['frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['frequency_of_purchases','frequency_days']].head())

#CHECK and REMOVE unneccesry Column
print(df[['discount_applied','promo_code_used']].head())

print((df['discount_applied'] == df['promo_code_used']).all())

df = df.drop('promo_code_used', axis= 1)
print(df.columns)



# Connecting Python to MySQL
from sqlalchemy import create_engine
from urllib.parse import quote_plus

username = 'root'
password = 
host = 
port = 3306
database = 'customer_behavior'

engine = create_engine(
    f"mysql+pymysql://{username}:{quote_plus(password)}@{host}:{port}/{database}"
)

# Load DataFrame into MySQL
table_name = 'customer_details'

df.to_sql(
    table_name,
    con=engine,
    if_exists='replace',
    index=False
)

print(f"DataFrame loaded into MySQL table '{table_name}' successfully.")

# Read back sample (SQL Server uses TOP instead of LIMIT)
# pd.read_sql("SELECT TOP 5 * FROM customer_details;", engine)





