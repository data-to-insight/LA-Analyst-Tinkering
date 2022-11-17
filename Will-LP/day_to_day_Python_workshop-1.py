'''This code gets CIN census data in zip file from a download link on the DfE website, selects the 
national referrals data table (a1) from the list of CSVs in the zip file, and puts it into a 
pandas data frame. It then slices the data frame by category and category_type columns to only take
columns equal to Referrals and Referrals in the year. Finally, it uses seaborn to make a bar-plot of 
that data, plotting referrals against year. This includes changing the data type of the number column 
to floas as pandas infers its type as object on import.

Note that a quirk of using VScode/Codespaces is that you need to run it as a notebook to show plots. Accordingly,
you need to preceed your code with # %% and only run it using the 'run cell' option at the top of the code. 
If the option to run code doesnt appear, you may need to open the command palette with ctrl+shift+p, search rebuild,
and select rebuild container.'''



#  Packages for reading data from url download links and extracting data from them 
#  if they're zip files.
import requests 
import io 
import zipfile

#  Package for 
import pandas as pd

#  Plotting packages
import seaborn as sns
import matplotlib.pyplot as plt

#  Assigns the url for the CIN census download link as a string to the url variabke
url = 'https://content.explore-education-statistics.service.gov.uk/api/releases/dc190008-a8f7-41a4-faa6-08d973655eae/files'

#  Uses the requests, io, and zipfile packages to get data from the download link, concert it from Bytes to 
#  a Python readable format, and unzips the zip file.
r = requests.get(url, stream=True)
r = zipfile.ZipFile(io.BytesIO(r.content))

#  When uncommented this prints a list of the names of the files in the zip file downloaded fromt he DfE website
#  These filenames can then be passed to pd.read_csv to turn them into data frames.
# print(r.namelist())

#  Reads the a1 table in the data folder of the zipfile in the r variable as a dataframe.
data = pd.read_csv(r.open('data/a1_cin_referrals_assessments_2013_to_2021.csv'))

#  Uncommented this would print info about the dataframe, data, column names &c.
#print(data.info())


#  When uncommented these lines print out all the unique values in the category and category_type columns of data so we
#  can decide what to make a plot of and slice by.
#print(data['category'].unique())
#print(data['category_type'].unique())

#  These lines slice the data dataframe according to rows where the category and category_type columns are
#  equal to Referrals and Referrals in the year respectively, allowing us to easily make our bar plot.
#condition_1 = (data['category'] == 'Referrals')
#data = data[condition_1]
#condition_2 = (data['category_type'] == 'Referrals in the year')
#data = data[condition_2]


#  A better way of slicing by joining multiple conditions in one slice.
data = data[(data['category'] == 'Referrals') &
            (data['category_type'] == 'Referrals in the year')]

#  Chnages the data in the number column to the float type so we can plot it, Python infers it's type as 
#  object so, otherwise seaborn plots it as categorical instead of as numbers.
data['number'] = data['number'].astype(float)

#  Plots a barplot using seaborn with the data dataframe as the data (sorry that's confusing),
#  the time_period column as x, the number column as y, and using the crest palette to choose bar colours.
fig = sns.barplot(data=data, 
                x='time_period', 
                y='number', 
                palette='crest')

#  Sets the title, x_label, and y_label for the plot.
fig.set_title('National referrals by year')
fig.set_xlabel('Year')
fig.set_ylabel('Referrals')

#  Shows the plot
plt.show()


