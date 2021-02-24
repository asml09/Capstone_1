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
import numpy as np
df = pd.read_csv("washington-race.csv", delimiter = ',')

# drop empty columns
# LatinX - ancetry from Latin American countries regardless of language, Hispanic - ancestry from Spanish-speaking countries
    # Combine to Hispanic - includes both these groups in this df
df.drop(['Tests_AIAN', 'Tests_Asian', 'Tests_Black', 'Tests_Ethnicity_Hispanic', 'Tests_Ethnicity_NonHispanic', 'Tests_Ethnicity_Unknown',
    'Tests_LatinX', 'Tests_Multiracial', 'Tests_NHPI', 'Tests_Other', 'Tests_White', 'Tests_Total', 'State'], axis = 1, inplace = True, )
df['Cases_Hispanic'] = df['Cases_Ethnicity_Hispanic'] + df['Cases_LatinX']
df['Deaths_Hispanic'] = df['Deaths_Ethnicity_Hispanic'] + df['Deaths_LatinX']
df['Hospitalizations_Hispanic'] = df['Hospitalizations_Ethnicity_Hispanic'] + df['Hospitalizations_LatinX']
cols = ['Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White', 'Cases_Hispanic', 'Cases_Total',
    'Deaths_Asian', 'Deaths_AIAN', 'Deaths_Black', 'Deaths_White', 'Deaths_Hispanic', 'Deaths_Total', 
    'Hospitalizations_Asian', 'Hospitalizations_AIAN', 'Hospitalizations_Black', 'Hospitalizations_White', 
    'Hospitalizations_Hispanic', 'Hospitalizations_Total']
# fill Na with mean of column, change date to DateTime
nan_values = df.isna()
nan_columns = nan_values.any()
columns_with_nan = df.columns[nan_columns].tolist()
for column in columns_with_nan:
    df[column].fillna(value=df[column].mean(), inplace=True)
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='coerce')
#df['Hospitalizations_White'].fillna(value=df['Hospitalizations_White'].mean(), inplace=True)
#print(df['Hospitalizations_White'])


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

def plot_by_date(columns, labels, title, df):
    fig, ax = plt.subplots()
    for tup in zip(columns, labels):
        ax.plot(df['Date'], df[tup[0]], label = tup[1])
    ax.legend()
    ax.set_title(title)
    plt.xticks(rotation = 90)
    ax.tick_params(axis='x', which='major', labelsize=5)
    plt.show()  

Races_cases = ['Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White', 'Cases_Hispanic', 'Cases_Total']
Races_deaths = ['Deaths_Asian', 'Deaths_AIAN', 'Deaths_Black', 'Deaths_White', 'Deaths_Hispanic', 'Deaths_Total']
Races_hospitalization = ['Hospitalizations_Asian', 'Hospitalizations_AIAN', 'Hospitalizations_Black', 'Hospitalizations_White', 
    'Hospitalizations_Hispanic', 'Hospitalizations_Total']
Labels = ["Asian", "Native American", "Black", "White", "Hispanic", "Total"]

#plot_by_date(Races_cases, Labels, "Corona cases for all the races", df)
#plot_by_date(Races_deaths, Labels, "Corona deaths for all the races", df)
#plot_by_date(Races_hospitalization, Labels, "Corona hospitalizations for all the races", df)

#print(df.columns)

# df_prop has only the cases. This dataframe sums all the cases from all the days, and they are converted to cases per 10,000 people 
# This is adjusted from the fact that Washington is 9.6% Asian, 1.9% Native American, 4.4% Black, 67.5% White, 13% Hispanic
    # with a population of 7,614,893
# df_prop will only have the first row of df, which is the total number of cases on 02/21/2021 (NOT new cases) as this is the most recent data
num_eachrace = np.array([.096, .019, .044, .675, .13, 1, .096, .019, .044, .675, .13, 1, .096, .019, .044, .675, .13, 1])
num_eachrace *= 7614893
num_eachrace *= (1 / 10000)

num_eachrace = pd.DataFrame([num_eachrace], columns = cols)

# row 3 is cases per 10,000
df_prop = df[cols]
# df_prop = df_prop.loc[0:1, :]
df_prop = df_prop.append(num_eachrace, ignore_index=True)
for i in range(91):
    df_prop.loc[i] = df_prop.loc[i] / df_prop.loc[91]
df_prop['Date'] = df['Date']
df_prop.drop([91], axis = 0, inplace=True)
#print(df_prop)
#plot_by_date(Races_cases, Labels, "Corona cases per 10,000 for all the races", df_prop)
#plot_by_date(Races_deaths, Labels, "Corona deaths per 10,000 for all the races", df_prop)
# plot_by_date(Races_hospitalization, Labels, "Corona hospitalizations per 10,000 for all the races", df_prop)


#df_prop_sector is the first row of df, to be used to merge with the sector data
df_prop_sector = df_prop.loc[0:1, :]
df_prop_sector.drop(['Deaths_Asian', 'Deaths_AIAN',
       'Deaths_Black', 'Deaths_White', 'Deaths_Hispanic', 'Deaths_Total',
       'Hospitalizations_Asian', 'Hospitalizations_AIAN',
       'Hospitalizations_Black', 'Hospitalizations_White',
       'Hospitalizations_Hispanic', 'Hospitalizations_Total', 'Date'], axis = 1, inplace=True)
#df_prop_sector['Sector'] = ['Filler', 'Filler']


df_sector = pd.read_csv("population_percent2.csv", delimiter = ',,', engine = 'python')


# print(df_sector.head())
# print(df_prop_sector)

df_sector = df_sector.rename(columns={'Race / Ethnicity': 'Sector', 'Hispanic': 'Cases_Hispanic', 'Non-Hispanic White':'Cases_White', 
    'Non-Hispanic Asian':'Cases_Asian', 'Non-Hispanic Black':'Cases_Black', ' American Indian or Alaska Native': 'Cases_AIAN'})
df_sector.drop(0, axis = 0, inplace = True)
df_sector.drop("Unnamed: 6", axis = 1, inplace = True)
df_sector.reset_index(inplace=True)
df_sector.drop("index", axis = 1, inplace = True)


for cases in Races_cases[0:5]:
    df_sector[cases] = df_sector[cases].str.rstrip('%').astype('float') / 100.0


# print(df_sector.head())
# Now we have all the percents as decimals from rows 0:7, and from 8:9 the number of cummulative cases on 02/21/2021
# Next step: multiply rows -0:7 by row 8, to get cases per 10,000 in each industry sector
sector_final = pd.concat([df_sector, df_prop_sector], ignore_index=True)

print(sector_final[['Cases_Asian', 'Cases_AIAN']])
Races_cases = ['Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White', 'Cases_Hispanic', 'Cases_Total']

