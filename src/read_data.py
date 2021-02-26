from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns; sns.set_theme()


df = pd.read_csv("washington-race.csv", delimiter = ',')

# DATA CLEANING for dataframe "df"
# drop empty columns
# LatinX - ancetry from Latin American countries regardless of language, Hispanic - ancestry from Spanish-speaking countries
# Combine to Hispanic - includes both these groups in this df
# fill Na with mean of column, change date to DateTime
df.drop(['Tests_AIAN', 'Tests_Asian', 'Tests_Black', 'Tests_Ethnicity_Hispanic', 'Tests_Ethnicity_NonHispanic', 'Tests_Ethnicity_Unknown',
    'Tests_LatinX', 'Tests_Multiracial', 'Tests_NHPI', 'Tests_Other', 'Tests_White', 'Tests_Total', 'State'], axis = 1, inplace = True, )
df['Cases_Hispanic'] = df['Cases_Ethnicity_Hispanic'] + df['Cases_LatinX']
df['Deaths_Hispanic'] = df['Deaths_Ethnicity_Hispanic'] + df['Deaths_LatinX']
df['Hospitalizations_Hispanic'] = df['Hospitalizations_Ethnicity_Hispanic'] + df['Hospitalizations_LatinX']
cols = ['Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White', 'Cases_Hispanic', 'Cases_Total',
    'Deaths_Asian', 'Deaths_AIAN', 'Deaths_Black', 'Deaths_White', 'Deaths_Hispanic', 'Deaths_Total', 
    'Hospitalizations_Asian', 'Hospitalizations_AIAN', 'Hospitalizations_Black', 'Hospitalizations_White', 
    'Hospitalizations_Hispanic', 'Hospitalizations_Total']
nan_values = df.isna()
nan_columns = nan_values.any()
columns_with_nan = df.columns[nan_columns].tolist()
for column in columns_with_nan:
    df[column].fillna(value=df[column].mean(), inplace=True)
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='coerce')

# function to plot coronavirus cases, deaths, or hospitalizations through time
def plot_by_date(columns, labels, title, df, xlabel, ylabel):
    fig, ax = plt.subplots()
    fig.tight_layout(pad = 4)
    for tup in zip(columns, labels):
        ax.plot(df['Date'], df[tup[0]], label = tup[1])
    ax.legend()
    ax.set_title(title, size = 14.5)
    ax.set_xlabel(xlabel, size = 9)
    ax.set_ylabel(ylabel, size = 9)
    plt.xticks(rotation = 90, size = 9)
    ax.tick_params(axis='x', which='major', labelsize=8)
    ax.tick_params(axis='y', which='major', labelsize=8)
    plt.savefig()

Races_cases = ['Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White', 'Cases_Hispanic', 'Cases_Total']
Races_deaths = ['Deaths_Asian', 'Deaths_AIAN', 'Deaths_Black', 'Deaths_White', 'Deaths_Hispanic', 'Deaths_Total']
Races_hospitalization = ['Hospitalizations_Asian', 'Hospitalizations_AIAN', 'Hospitalizations_Black', 'Hospitalizations_White', 
    'Hospitalizations_Hispanic', 'Hospitalizations_Total']
Labels = ["Asian", "Native American", "Black", "White", "Hispanic", "Total"]

# Plots raw counts
plot_by_date(Races_cases, Labels, "Corona cases for all the races", df, 'Date', 'Number Cases')
plot_by_date(Races_deaths, Labels, "Corona deaths for all the races", df, 'Date', 'Number Cases')
plot_by_date(Races_hospitalization, Labels, "Corona hospitalizations for all the races", df, 'Date', 'Number Cases')

# DATA CLEANING 
# df_prop has only the cases. This dataframe sums all the cases from all the days, and they are converted to 
# cases per 10,000 people 
# This is adjusted from the fact that Washington is 9.6% Asian, 1.9% Native American, 4.4% Black, 67.5% White, 
# 13% Hispanic with a population of 7,614,893
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

# Plots per 10,000
plot_by_date(Races_cases[0:5], Labels[0:5], "Corona cases per 10,000 for all the races", df_prop, 'Date', 'Number Cases per 10,000')
plot_by_date(Races_deaths[0:5], Labels[0:5], "Corona deaths per 10,000 for all the races", df_prop, 'Date', 'Number Cases per 10,000')
plot_by_date(Races_hospitalization[0:5], Labels[0:5], "Corona hospitalizations per 10,000 for all the races", df_prop, 'Date', 'Number Cases per 10,000')

#df_prop_sector is the first row of df, to be used to merge with the sector data
df_prop_sector = df_prop.loc[0:1, :]
df_prop_sector.drop(['Deaths_Asian', 'Deaths_AIAN',
       'Deaths_Black', 'Deaths_White', 'Deaths_Hispanic', 'Deaths_Total',
       'Hospitalizations_Asian', 'Hospitalizations_AIAN',
       'Hospitalizations_Black', 'Hospitalizations_White',
       'Hospitalizations_Hispanic', 'Hospitalizations_Total', 'Date', 'Cases_Total'], axis = 1, inplace=True)

# DATA CLEANING, and combining population-percent.csv with df from above
df_sector = pd.read_csv("population-percent.csv", delimiter = ',,', engine = 'python')


df_sector = df_sector.rename(columns={'Race / Ethnicity': 'Sector', 'Hispanic': 'Cases_Hispanic', 'Non-Hispanic White':'Cases_White', 
    'Non-Hispanic Asian':'Cases_Asian', 'Non-Hispanic Black':'Cases_Black', ' American Indian or Alaska Native': 'Cases_AIAN'})
df_sector.drop(0, axis = 0, inplace = True)
df_sector.drop("Unnamed: 6", axis = 1, inplace = True)
df_sector.reset_index(inplace=True)
df_sector.drop("index", axis = 1, inplace = True)
for cases in Races_cases[0:5]:
    df_sector[cases] = df_sector[cases].str.rstrip('%').astype('float') / 100.0

# Now we have all the percents as decimals from rows 0:7, and from 8:9 the number of cummulative cases on 02/21/2021
# Next step: multiply rows 0:7 by row 8, to get cases per 10,000 in each industry sector
sector_final = pd.concat([df_sector, df_prop_sector], ignore_index=True)
Races_cases = ['Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White', 'Cases_Hispanic', 'Cases_Total']
temp = sector_final.drop(['Sector'], axis = 1)
for i in range(8):
    temp.loc[i] = temp.loc[i] * temp.loc[8]
#sector_10k has the cases per industry per 10,000
sector_10k = sector_final[['Sector']].join(temp)
#print(sector_10k[['Sector', 'Cases_Hispanic']])
sector_10k.drop([8, 9], axis = 0, inplace=True)
sector_10k = sector_10k.set_index('Sector')
sector_10k = sector_10k.rename(index = {'"Agriculture, Forestry, Fishing and Hunting"': 'Agriculture',
     'Health Care and Social Assistance' : 'Health Care', 'Accommodation and Food Services': 'Food Service', 
     'Retail Trade': 'Retail', 'Public Administration': 'Public Admin', 'Transportation and Warehousing': 'Transportation'})
#sector_10k.drop(['Sector'], axis = 0, inplace=True)
# print(sector_10k.index)

#Hypothesis testing
# THe health care industry is seen generally as the most dangerous, and thus health care workers were one of the first to 
# receive the vaccine. However, other sectors also appear to have a high ammount of cases. Test for a significant 
# difference between all industries
print(sector_10k)
sector_10k['Cases_Total'] = sector_10k.sum(axis = 1)
# Find the p-value for whether there is a significant difference in covid cases between two industries 
def find_p(industry1, industry2):
    all_industries_cases = sector_10k["Cases_Total"].sum(axis = 0)
    shared_freq = (sector_10k.loc[industry1, "Cases_Total"] + sector_10k.loc[industry2, "Cases_Total"]) / all_industries_cases
    shared_var = (2 * (shared_freq) * (1 - shared_freq))/ all_industries_cases
    diff_prop = stats.norm(0, np.sqrt(shared_var))
    diff_in_sample_prop = abs(sector_10k.loc[industry1, "Cases_Total"] - sector_10k.loc[industry2, "Cases_Total"]) / all_industries_cases
    p_val = 1 - diff_prop.cdf(diff_in_sample_prop)  
    return p_val

all_industries_cases = sector_10k["Cases_Total"].sum(axis = 0)
shared_freq = (sector_10k.loc['Retail', "Cases_Total"] + sector_10k.loc['Manufacturing', "Cases_Total"]) / all_industries_cases
# shared_var = n_retail * p(1 - p) + n_manufacture * p(1 - p) 
shared_var = (sector_10k.loc['Retail', "Cases_Total"] + sector_10k.loc['Manufacturing', "Cases_Total"]) * (shared_freq) * (1 - shared_freq)
diff_prop = stats.norm(0, np.sqrt(shared_var))
diff_in_sample = abs(sector_10k.loc['Retail', "Cases_Total"] - sector_10k.loc['Manufacturing', "Cases_Total"]) 

# plot of p-value region for Manufacturing vs Retail 
fig, ax = plt.subplots()
x = np.linspace(-50, 50, num=250)
palette = sns.color_palette("mako_r", 6)
ax = sns.lineplot(
    x= x, y=diff_prop.pdf(x),
    palette=palette)
ax.fill_between(x, diff_prop.pdf(x), 
    where=(x >= diff_in_sample), color="red", alpha=0.5)
p = find_p('Retail', 'Manufacturing')
ax.set_title("Retail vs Manufacturing p-val region, p = 0.285")
ax.set_xlabel("Cases Manufacturing - Cases Retail", fontsize = 9)
plt.savefig()


# Make the np arrray of p-values for all hypothesis tests for each industry vs each other industry
#print(sector_10k.loc["Retail", "Cases_Total"])
array_pval = np.empty((8, 8))
for industry, i in zip(sector_10k.index, range(8)):
    for other_industry, j in zip(sector_10k.index, range(8)):
        array_pval[i, j] = find_p(industry, other_industry)

# heatmap of p-values for all hypothesis tests 
fig, ax = plt.subplots()
fig.tight_layout(pad = 5)
sns.set(font_scale = 0.8)
ax = sns.heatmap(np.array(array_pval), xticklabels = sector_10k.index, yticklabels = sector_10k.index)
ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize = 8.5, rotation = 90)
ax.set_yticklabels(ax.get_xmajorticklabels(), fontsize = 8.5)
ax.set_title("p-values across industries", fontsize = 13)
plt.savefig()







