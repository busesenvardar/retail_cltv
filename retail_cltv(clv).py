############################################
# CUSTOMER LIFETIME VALUE
############################################

##################################################
# 1. Data Preparation
##################################################

# Data
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# The dataset contains sales data of an online store between 01/12/2009 - 09/12/2011

# Variables
# InvoiceNo: Invoice number. The unique number of each transaction. Aborted operation if it starts with C.
# StockCode: Product code. Unique number for each product.
# Description: Product name
# Quantity: Number of products. It expresses how many of the products on the invoices have been sold.
# InvoiceDate: Invoice date and time.
# UnitPrice: Product price (in GBP)
# CustomerID: Unique customer number
# Country: Country name. Country where the customer lives.

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_ = pd.read_excel("datasets/week_3/online_retail_II.xlsx", sheet_name="Year 2009-2010")

df = df_.copy()

df.head()

df.isnull().sum()

df = df[~df["Invoice"].str.contains("C", na=False)]

df.describe().T

df = df[(df['Quantity'] > 0)]

df.dropna(inplace=True)

df["TotalPrice"] = df["Quantity"] * df["Price"]

prep_cltv = df.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                        'Quantity': lambda x: x.sum(),
                                        'TotalPrice': lambda x: x.sum()})

prep_cltv.columns = ['total_transaction', 'total_unit', 'total_price']


prep_cltv
##################################################
# 2. Average Order Value
# average_order_value = total_price / total_transaction
##################################################

prep_cltv.head()

prep_cltv["average_order_value"] = prep_cltv["total_price"] / prep_cltv["total_transaction"]

##################################################
# 3. Purchase Frequency
# total_transaction / total_number_of_customers
##################################################

prep_cltv.shape[0]

prep_cltv["purchase_frequency"] = prep_cltv["total_transaction"] / prep_cltv.shape[0]

##################################################
# 4. Repeat Rate & Churn Rate
##################################################

repeat_rate = prep_cltv[prep_cltv["total_transaction"] > 1].shape[0] / prep_cltv.shape[0]

churn_rate = 1 - repeat_rate

##################################################
# 5. Profit Margin
# profit_margin =  total_price * 0.10
##################################################

prep_cltv['profit_margin'] = prep_cltv['total_price'] * 0.10

##################################################
# 6. Customer Value
# customer_value = average_order_value * purchase_frequency
##################################################

prep_cltv['customer_value'] = prep_cltv['average_order_value'] * prep_cltv["purchase_frequency"]

##################################################
# 7. Customer Lifetime Value
# CLTV = (customer_value / churn_rate) x profit_margin
##################################################

prep_cltv["cltv"] = (prep_cltv["customer_value"] / churn_rate) * prep_cltv["profit_margin"]

prep_cltv.sort_values(by="cltv", ascending=False).head()


##################################################
# 8. Creating Segments
##################################################

prep_cltv.sort_values(by="cltv", ascending=False).tail()

prep_cltv["segment"] = pd.qcut(prep_cltv["cltv"], 4, labels=["D", "C", "B", "A"])

prep_cltv.sort_values(by="cltv", ascending=False).head()

prep_cltv.groupby("segment").agg({"count", "mean", "sum"})



























