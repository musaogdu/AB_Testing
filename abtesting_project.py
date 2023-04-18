
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


dataframe_control = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")
dataframe_test = pd.read_excel("ab_testing.xlsx", sheet_name="Test Group")

df_control= dataframe_control.copy()
df_test = dataframe_test.copy()

def check_df(dataframe):
    print("###Shape###")
    print(dataframe.shape)
    print("###Types###")
    print(dataframe.dtypes)
    print("###Head###")
    print(dataframe.head())
    print("###Tail###")
    print(dataframe.tail())
    print("###NA###")
    print(dataframe.isnull().sum())
    print("###Quantiles###")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_test)
check_df(df_control)

df_control["group"] = "control"
df_test["group"] = "test"

df= pd.concat([df_control, df_test], axis=0, ignore_index=True)
df.head()
df.tail()


## H0 : M1 = M2 (Avarage bidding maximum biddingden daha fazla dönüşüm getirmemektedir)
## H1 : M1 != M2 (Avarage bidding maximum biddingden daha fazla dönüşüm getirmektedir)


## Normallik varsayımı

df.groupby("group").agg({"Purchase" : "mean"})

test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue) )

## p-value = 0.5891

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue) )

##p-value = 0.1541


## Varyans homojenliği

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue) )

## p-value = 0.1083

test_stat, pvalue = ttest_ind(df.loc[df["group"]== "control", "Purchase"],
                              df.loc[df["group"]== "test", "Purchase"],
                              equal_var=True)
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue) )

## p-value = 0.3493