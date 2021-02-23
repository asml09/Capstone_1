# import tabula
# df = tabula.read_pdf("https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/data-tables/COVID-19MorbidityMortalityRaceEthnicityLanguageWAState.pdf", 
# pages = 5)
# print(df)

# with open('table1.1.rtf') as f:
#     # lines = f.readlines()
#     # print(lines)
#     for line in f:
#         print(line.strip())
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("washington-race.csv", delimiter = ',')

# drop empty columns
df.drop(['Tests_AIAN', 'Tests_Asian', 'Tests_Black', 'Tests_Ethnicity_Hispanic', 'Tests_Ethnicity_NonHispanic', 'Tests_Ethnicity_Unknown',
    'Tests_LatinX', 'Tests_Multiracial', 'Tests_NHPI', 'Tests_Other', 'Tests_White', 'Tests_Total', 'State'], axis = 1, inplace = True, )


# fill Na with mean of column, change date to DateTime
nan_values = df.isna()
nan_columns = nan_values.any()
columns_with_nan = df.columns[nan_columns].tolist()
for column in columns_with_nan:
    df[column].fillna(value=df[column].mean(), inplace=True)
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='coerce')
#df['Hospitalizations_White'].fillna(value=df['Hospitalizations_White'].mean(), inplace=True)
#print(df['Hospitalizations_White'])

print(df.columns)

#line plot of cases per day over time 
# fig, ax = plt.subplots()
# for tup in zip(Races_cases, Labels):
#     ax.plot(df['Date'], df[tup[0]], label = tup[1])
#ax.plot(df['Date'], df['Cases_Asian'], label = "Asian")
#ax.plot(df['Date'], df['Cases_Black'])
# ax.legend()
# ax.set_title("Corona cases for all the races")
# plt.xticks(rotation = 90)
# ax.tick_params(axis='x', which='major', labelsize=5)
# plt.show()

#pd.to_datetime('13000101', format='%Y%m%d', errors='coerce')
#print(df['Date'].head())

def plot_by_date(columns, labels, title):
    fig, ax = plt.subplots()
    for tup in zip(columns, labels):
        ax.plot(df['Date'], df[tup[0]], label = tup[1])
    ax.legend()
    ax.set_title(title)
    plt.xticks(rotation = 90)
    ax.tick_params(axis='x', which='major', labelsize=5)
    plt.show()  

Races_cases = ['Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White', 'Cases_Ethnicity_Hispanic', 'Cases_Total']
Races_deaths = ['Deaths_Asian', 'Deaths_AIAN', 'Deaths_Black', 'Deaths_White', 'Deaths_Ethnicity_Hispanic', 'Deaths_Total']
Races_hospitalization = ['Hospitalizations_Asian', 'Hospitalizations_AIAN', 'Hospitalizations_Black', 'Hospitalizations_White', 
    'Hospitalizations_Ethnicity_Hispanic', 'Hospitalizations_Total']
Labels = ["Asian", "Native American", "Black", "White", "Hispanic", "Total"]

#plot_by_date(Races_cases, Labels, "Corona cases for all the races")
plot_by_date(Races_deaths, Labels, "Corona deaths for all the races")