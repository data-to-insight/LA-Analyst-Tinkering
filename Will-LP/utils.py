import pandas as pd

#from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sp
import matplotlib.dates as mdates


def sample_graph(years, line_on=True):
    ChildIdentifiers = pd.read_csv('/workspaces/LA-Analyst-Tinkering/FAKE-CIN-DATA/FakeChildIdentifiers.csv')
    CINdetails = pd.read_csv('/workspaces/LA-Analyst-Tinkering/FAKE-CIN-DATA/FakeCINdetails.csv')

    merged_df = CINdetails.merge(ChildIdentifiers, left_on='LAchildID', right_on='LAchildID', how='left')


    df = merged_df[['LAchildID', 'PersonBirthDate', 'CINreferralDate', 'CINclosureDate']]

    df_dates = df.loc[:,['PersonBirthDate', 'CINreferralDate', 'CINclosureDate']].apply(
        pd.to_datetime, format='%Y/%m/%d', errors='coerce'
    )

    df_dates = df_dates[df_dates['CINclosureDate'].notna()]

    df_dates['CINrefToClose'] = (df_dates['CINclosureDate'] - df_dates['CINreferralDate'])
    df_dates['CINrefToClose'] = df_dates['CINrefToClose'].astype('timedelta64[h]')
    df_dates['CINrefToClose'] = df_dates['CINrefToClose'].astype(float) / 24
    df_dates = df_dates[(df_dates['PersonBirthDate'].dt.year >= years[0]) & (df_dates['PersonBirthDate'].dt.year <= years[1])]

    y = df_dates['CINrefToClose']
    x = mdates.date2num(df_dates['PersonBirthDate'])

    sns.set_style('darkgrid')
    plt.plot(df_dates['PersonBirthDate'], y, 'o')

    slope, intercept, r_value, p_value, std_err =sp.linregress(x,y)
    xf = np.linspace(min(x),max(x),100)
    xf1 = xf.copy()
    yf = (slope*xf)+intercept

     
    if line_on:
        pass

    plt.plot(xf1, yf, lw=3, label=f'Linear regression (r={r_value})')

    plt.tight_layout()
    plt.title('Birth date versus CIN referral to closure date')
    plt.xlabel('Birth date')
    plt.ylabel('TIme between CIN referral and CIN closure (years)')
    plt.legend()
    plt.show()

