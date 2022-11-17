'''Day to day workshop explaining how to merge tables, plot a
scatter, add a line of fit, and do a linear regression.'''

import pandas as pd
import datetime
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

ChildIdentifiers = pd.read_csv('/workspaces/LA-Analyst-Tinkering/FAKE-CIN-DATA/FakeChildIdentifiers.csv')
CINdetails = pd.read_csv('/workspaces/LA-Analyst-Tinkering/FAKE-CIN-DATA/FakeCINdetails.csv')

print(CINdetails)
print(ChildIdentifiers)

merged_df = CINdetails.merge(ChildIdentifiers, left_on='LAchildID', right_on='LAchildID', how='left')
print(merged_df)

df = merged_df[['LAchildID', 'PersonBirthDate', 'CINreferralDate', 'CINclosureDate']]
df[['PersonBirthDate', 'CINreferralDate', 'CINclosureDate']] = df[['PersonBirthDate', 'CINreferralDate', 'CINclosureDate']].apply(
    pd.to_datetime, format='%Y/%m/%d', errors='coerce'
)
df = df[df['CINclosureDate'].notna()]
df['CINrefToClose'] = df['CINclosureDate'] - df['CINreferralDate']
print(df)

plt.style.use('seaborn')
plt.plot_date(df['PersonBirthDate'], df['CINrefToClose'], 'o')

m, b = np.polyfit(df['PersonBirthDate'], df['CINrefToClose'], 1)
plt.plot(df['PersonBirthDate'], m*df['PersonBirthDate']+b)

plt.tight_layout()
plt.title('Birth date versus CIN referral to closure date')
plt.xlabel('Birth date')
plt.ylabel('TIme between CIN referral and CIN closure (years)')
plt.show()

