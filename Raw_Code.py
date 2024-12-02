import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### delcaring pis as the variable for the dataset
pis = pd.read_csv("CSV_Personal_Income_State.csv")

### removing the given columns for better merging experience later
ctremove = ["22_Q2_dollars","22_Q3_dollars","22_Q4_dollars","23_Q1_dollars","23_Q2_dollars","22_Q2_percentage", "22_Q3_percentage", "23_Q1_percentage", "23_Q2_dollars","22_Q4_percentage", "23_Q2_percentage", "23_Prank_Q2"]

### declaring new cleaned dataset
pis_cleaned = pis.drop(columns=ctremove)

### rename Unnamed column
pis_cleaned.rename(columns={"Unnamed: 0":"Name"}, inplace=True)

# Convert values to uppercase where they are not "United States"
pis_cleaned['Name'] = pis_cleaned['Name'].apply(lambda x: x.upper() if x != 'United States' else x)

### set index to be the names of the states
pis_cleaned.set_index("Name", inplace=True)

### Removing regions for better merging experience
pis_cleaned.drop("NEW ENGLAND ", axis=0, inplace=True)
pis_cleaned.drop("ROCKY MOUNTAIN ", axis=0, inplace=True)
pis_cleaned.drop("FAR WEST", axis=0, inplace=True)
pis_cleaned.drop("PLAINS ", axis=0, inplace=True)
pis_cleaned.drop("GREAT LAKES ", axis=0, inplace=True)
pis_cleaned.drop("SOUTHEAST ", axis=0, inplace=True)
pis_cleaned.drop("SOUTHWEST ", axis=0, inplace=True)
pis_cleaned.drop("MIDEAST ", axis=0, inplace=True)

### Turn empty space in dataset to display none
pis_cleaned.replace("........", None, inplace=True)

### Sort values in alphabetical order with United States at the top
pis_cleaned = pis_cleaned.loc[
    ["United States"] + sorted([state for state in pis_cleaned.index if state != "United States"])
]

### remove extra spaces from the end
pis_cleaned.index = pis_cleaned.index.str.strip().str.replace(r'\s+', ' ', regex=True)

# Rename the columns of the dataframe
pis_cleaned.rename(columns = {'2021_dollars':'2021_dollars_pi', '2022_dollars':'2022_dollars_pi', '2022_percentage':'2022_percentage_pi','22_PRank':'22_prank_pi'}, inplace = True)


### display
#pis_cleaned.head(60)

# Read the dataset of GDP by state and county
gdp_state_county = pd.read_csv('CSV_GDP_State_County.csv')
# Drop the 2019 year column
gdp_state_county.drop('2019_GDP', axis = 1, inplace = True)
# Drop the 2020 year column
gdp_state_county.drop('2020_GDP', axis = 1, inplace = True)
# Drop the 2020 percentage column
gdp_state_county.drop('2020_percentage', axis = 1, inplace = True)
# Provide a name to the unnamed column
gdp_state_county.rename(columns = {'Unnamed: 0': 'Name'}, inplace = True)

# Set the name as the index of the dataframe
gdp_state_county.set_index('Name', inplace = True)

# Drop all the null/blank rows
gdp_state_county.dropna(inplace = True)

# Rename the columns of the dataset
gdp_state_county.rename(columns = {'2022_rank':'2022_rank_gdp', '2021_percentage':'2021_percentage_gdp', '2022_percentage':'2022_percentage_gdp', '2022_prank':'2022_prank_gdp'}, inplace = True)

# List of state names
state_names = [
    "ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", "COLORADO", 
    "CONNECTICUT", "DELAWARE", "DISTRICT OF COLUMBIA", "FLORIDA", "GEORGIA", "HAWAII", "IDAHO", 
    "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY", "LOUISIANA", 
    "MAINE", "MARYLAND", "MASSACHUSETTS", "MICHIGAN", "MINNESOTA", "MISSISSIPPI", 
    "MISSOURI", "MONTANA", "NEBRASKA", "NEVADA", "NEW HAMPSHIRE", "NEW JERSEY", 
    "NEW MEXICO", "NEW YORK", "NORTH CAROLINA", "NORTH DAKOTA", "OHIO", 
    "OKLAHOMA", "OREGON", "PENNSYLVANIA", "RHODE ISLAND", "SOUTH CAROLINA", 
    "SOUTH DAKOTA", "TENNESSEE", "TEXAS", "UTAH", "VERMONT", "VIRGINIA", 
    "WASHINGTON", "WEST VIRGINIA", "WISCONSIN", "WYOMING"
]


# Dictionary of postal codes
state_postal_codes = {
    "ALABAMA": "AL", "ALASKA": "AK", "ARIZONA": "AZ", "ARKANSAS": "AR", "CALIFORNIA": "CA",
    "COLORADO": "CO", "CONNECTICUT": "CT", "DELAWARE": "DE", "DISTRICT OF COLUMBIA": "DC", "FLORIDA": "FL", "GEORGIA": "GA",
    "HAWAII": "HI", "IDAHO": "ID", "ILLINOIS": "IL", "INDIANA": "IN", "IOWA": "IA",
    "KANSAS": "KS", "KENTUCKY": "KY", "LOUISIANA": "LA", "MAINE": "ME", "MARYLAND": "MD",
    "MASSACHUSETTS": "MA", "MICHIGAN": "MI", "MINNESOTA": "MN", "MISSISSIPPI": "MS", 
    "MISSOURI": "MO", "MONTANA": "MT", "NEBRASKA": "NE", "NEVADA": "NV", "NEW HAMPSHIRE": "NH",
    "NEW JERSEY": "NJ", "NEW MEXICO": "NM", "NEW YORK": "NY", "NORTH CAROLINA": "NC", 
    "NORTH DAKOTA": "ND", "OHIO": "OH", "OKLAHOMA": "OK", "OREGON": "OR", 
    "PENNSYLVANIA": "PA", "RHODE ISLAND": "RI", "SOUTH CAROLINA": "SC", 
    "SOUTH DAKOTA": "SD", "TENNESSEE": "TN", "TEXAS": "TX", "UTAH": "UT", 
    "VERMONT": "VT", "VIRGINIA": "VA", "WASHINGTON": "WA", "WEST VIRGINIA": "WV", 
    "WISCONSIN": "WI", "WYOMING": "WY"
}

# Replace null values with None
gdp_state_county.replace('--', 'None', inplace = True)



# Function to add state postal code to county names
def add_state_code_to_counties(df, state_names, state_postal_codes):
    index_names = df.index.tolist()
    current_state = None
    
    for i, name in enumerate(index_names):
        # Check if the row is a state row
        if ((name in state_names) and (df.loc[name, '2022_rank_gdp'] == 'None') and (df.loc[name, '2022_prank_gdp'] == 'None')):
            current_state = name
        # If the row is not a state, it's a county
        elif (current_state is not None):
            # Add the state postal code to the county name
            index_names[i] = f"{name}_{state_postal_codes[current_state]}"
    
    # Assign the modified index back to the dataframe
    df.index = index_names
    return df

# and (df.loc[name, '2022_prank_gdp'] == 'None')
# Call the add state code function
gdp_state_county = add_state_code_to_counties(gdp_state_county, state_names, state_postal_codes)

# Display the gdp by state and county
#gdp_state_county.head(70)



# Read the dataset of Personal income by county
pi_county = pd.read_csv('CSV_Personal_Income_State_County.csv')
# Drop the 2020 year columns
pi_county.drop('2020_dollars', axis = 1, inplace = True)
# Provide a name to the unnamed column
pi_county.rename(columns = {'Unnamed: 0': 'Name'}, inplace = True)
# Set the name as the index of the dataframe
pi_county.set_index('Name', inplace = True)

# Rename the columns of the dataset
pi_county.rename(columns = {'2021_dollars':'2021_dollars_pi', '2022_dollars':'2022_dollars_pi', '2022_rank':'2022_rank_pi', 
                            '2021_percentage ':'2021_percentage_pi', '2022_percentage':'2022_percentage_pi', '2022_prank':'2022_prank_pi'},
                       inplace = True)

# Drop all the null/blank rows
pi_county.dropna(inplace = True)

# Replace null values with None
pi_county.replace('--', 'None', inplace = True)

# List of state names
state_names = [
    "ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", "COLORADO", 
    "CONNECTICUT", "DELAWARE", "DISTRICT OF COLUMBIA", "FLORIDA", "GEORGIA", "HAWAII", "IDAHO", 
    "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY", "LOUISIANA", 
    "MAINE", "MARYLAND", "MASSACHUSETTS", "MICHIGAN", "MINNESOTA", "MISSISSIPPI", 
    "MISSOURI", "MONTANA", "NEBRASKA", "NEVADA", "NEW HAMPSHIRE", "NEW JERSEY", 
    "NEW MEXICO", "NEW YORK", "NORTH CAROLINA", "NORTH DAKOTA", "OHIO", 
    "OKLAHOMA", "OREGON", "PENNSYLVANIA", "RHODE ISLAND", "SOUTH CAROLINA", 
    "SOUTH DAKOTA", "TENNESSEE", "TEXAS", "UTAH", "VERMONT", "VIRGINIA", 
    "WASHINGTON", "WEST VIRGINIA", "WISCONSIN", "WYOMING"
]


# Dictionary of postal codes
state_postal_codes = {
    "ALABAMA": "AL", "ALASKA": "AK", "ARIZONA": "AZ", "ARKANSAS": "AR", "CALIFORNIA": "CA",
    "COLORADO": "CO", "CONNECTICUT": "CT", "DELAWARE": "DE", "DISTRICT OF COLUMBIA": "DC", "FLORIDA": "FL", "GEORGIA": "GA",
    "HAWAII": "HI", "IDAHO": "ID", "ILLINOIS": "IL", "INDIANA": "IN", "IOWA": "IA",
    "KANSAS": "KS", "KENTUCKY": "KY", "LOUISIANA": "LA", "MAINE": "ME", "MARYLAND": "MD",
    "MASSACHUSETTS": "MA", "MICHIGAN": "MI", "MINNESOTA": "MN", "MISSISSIPPI": "MS", 
    "MISSOURI": "MO", "MONTANA": "MT", "NEBRASKA": "NE", "NEVADA": "NV", "NEW HAMPSHIRE": "NH",
    "NEW JERSEY": "NJ", "NEW MEXICO": "NM", "NEW YORK": "NY", "NORTH CAROLINA": "NC", 
    "NORTH DAKOTA": "ND", "OHIO": "OH", "OKLAHOMA": "OK", "OREGON": "OR", 
    "PENNSYLVANIA": "PA", "RHODE ISLAND": "RI", "SOUTH CAROLINA": "SC", 
    "SOUTH DAKOTA": "SD", "TENNESSEE": "TN", "TEXAS": "TX", "UTAH": "UT", 
    "VERMONT": "VT", "VIRGINIA": "VA", "WASHINGTON": "WA", "WEST VIRGINIA": "WV", 
    "WISCONSIN": "WI", "WYOMING": "WY"
}

# Function to add state postal code to county names
def add_state_code_to_countiespi(df, state_names, state_postal_codes):
    index_names = df.index.tolist()
    current_state = None
    
    for i, name in enumerate(index_names):
        # Check if the row is a state row
        if ((name in state_names) and (df.loc[name, '2022_rank_pi'] == 'None') and (df.loc[name, '2022_prank_pi'] == 'None')):
            current_state = name
        # If the row is not a state, it's a county
        elif (current_state is not None):
            # Add the state postal code to the county name
            index_names[i] = f"{name}_{state_postal_codes[current_state]}"
    
    # Assign the modified index back to the dataframe
    df.index = index_names
    return df

# Call the add state code function
pi_county = add_state_code_to_countiespi(pi_county, state_names, state_postal_codes)

# Drop all states from the dataframe
# Remove all rows that are states
for i in state_names:
    pi_county.drop(i, axis = 0, inplace = True)

# Display the personal income by county
#pi_county.head(5)



# merge pis_cleaned and gdp_state_county
df_combined = pd.merge(gdp_state_county, pis_cleaned, how = 'left', left_index = True, right_index = True)
# merge df_combined and pi_county
df_merged = pd.merge(df_combined, pi_county, how = 'left', left_index = True, right_index = True, suffixes = ['_state', '_county'])

# Fill the missing values of the merged dataframe
df_merged.fillna({'2021_dollars_pi_state':'N/A', '2022_dollars_pi_state':'N/A', '2022_percentage_pi_state':'N/A', '22_prank_pi':'N/A'}, inplace = True)
df_merged.fillna({'2021_dollars_pi_county':'N/A', '2022_dollars_pi_county':'N/A', '2022_rank_pi':'N/A', '2021_percentage_pi':'N/A', '2022_percentage_pi_county':'N/A',
                 '2022_prank_pi':'N/A'}, inplace = True)

# Display the merged data
#df_merged.head(70)

# Filter the merged data to only get the states
df_state_filtered = df_merged[(df_merged.index.isin(state_names)) & (df_merged['2022_rank_gdp'] == 'None') & (df_merged['2022_prank_gdp'] == 'None')]
df_state_filtered.drop(columns = ['2021_dollars_pi_county', '2022_dollars_pi_county', '2022_rank_pi', '2021_percentage_pi', '2022_percentage_pi_county', '2022_prank_pi'], inplace = True)
df_state_filtered.drop(columns = ['2022_rank_gdp', '2022_prank_gdp'], inplace = True)
df_state_filtered.drop(index = 'DISTRICT OF COLUMBIA', inplace = True)

# Display the filtered data
#df_state_filtered

# Visualization 1
# Create a grouped bar chart of GDP of each state in 2021 and 2022
# Convert GDP columns to numeric after removing commas
df_state_filtered['2021_GDP'] = pd.to_numeric(df_state_filtered['2021_GDP'].str.replace(',', ''))
df_state_filtered['2022_GDP'] = pd.to_numeric(df_state_filtered['2022_GDP'].str.replace(',', ''))
fig, ax = plt.subplots(figsize=(15, 8))
width = 0.4  # Bar width
# Creating bar positions
x = range(len(df_state_filtered))
x_2021 = [i - width / 2 for i in x]
x_2022 = [i + width / 2 for i in x]
# Plot bars
ax.bar(x_2021, df_state_filtered['2021_GDP'] / 1e9, width=width, label='2021 GDP')
ax.bar(x_2022, df_state_filtered['2022_GDP'] / 1e9, width=width, label='2022 GDP')
ax.set_xlabel("States", fontsize=12)
ax.set_ylabel("GDP (in trillions)", fontsize=12)
ax.set_title("GDP of States in 2021 and 2022", fontsize=16)
ax.set_xticks(x)
ax.set_xticklabels(df_state_filtered.index, rotation=90, fontsize=10)
ax.legend()
plt.tight_layout()
plt.show()

# Reshape DataFrame for pivoting
df_pivot = df_state_filtered
df_pivot.drop(columns = ['2021_percentage_gdp', '2022_percentage_gdp', '2021_dollars_pi_state', '2022_dollars_pi_state', '2022_percentage_pi_state',
                        '22_prank_pi'], inplace = True)
df_pivot = df_pivot.reset_index().melt(id_vars="index", var_name="Year", value_name="GDP")

# Rename the index column to state and sort by state
df_pivot.rename(columns = {'index':'State'}, inplace = True)
df_pivot.sort_values(by = 'State', inplace = True)

# Pivot the DataFrame
df_pivot = df_pivot.pivot(index="Year", columns="State", values="GDP")

# Visualization 2
# Create a box plot of GDP of all states for 2021 and 2022
# Extract GDP data for boxplot
gdp_2021 = pd.Series(df_pivot.loc["2021_GDP"].values)
gdp_2022 = pd.Series(df_pivot.loc["2022_GDP"].values)
# Plotting the boxplot
plt.figure(figsize=(8, 6))
plt.boxplot([gdp_2021, gdp_2022], labels=["2021", "2022"])
# Combine GDP data
gdp_data = [gdp_2021, gdp_2022]
# Annotate the min, Q1, median, Q3, and max values
for i, year_data in enumerate(gdp_data, start=1):
    q1 = year_data.quantile(0.25)
    median = year_data.median()
    q3 = year_data.quantile(0.75)
    min_value = year_data.min()
    max_value = year_data.max()
    # Add annotations for the boxplot statistics
    plt.text(i, min_value, f"Min: {min_value}", fontsize=9, ha='left', color='green')
    plt.text(i, q1, f"Q1: {q1}", fontsize=9, ha='right', color='blue')
    plt.text(i, median, f"Med: {median}", fontsize=9, ha='left', color='black')
    plt.text(i, q3, f"Q3: {q3}", fontsize=9, ha='right', color='blue')
    plt.text(i, max_value, f"Max: {max_value}", fontsize=9, ha='center', color='green')
plt.title("Boxplot of GDP for All States (2021 vs 2022)")
plt.xlabel("Year")
plt.ylabel("GDP (in trillion $)")
plt.grid(axis="y")
plt.show()



# Filter the merged data to only get the counties
df_county_filtered = df_merged[~df_merged.index.isin(state_names)]
df_county_filtered.drop(columns = ['2021_dollars_pi_state', '2022_dollars_pi_state', '2022_percentage_pi_state', '22_prank_pi'], inplace = True)
df_county_filtered.drop(index = 'United States', inplace = True)


# Convert the 2021_percentage_gdp column to numeric
df_county_filtered['2021_percentage_gdp'] = pd.to_numeric(df_county_filtered['2021_percentage_gdp'], errors='coerce')
# Convert the 2022_percentage_gdp column to numeric
df_county_filtered['2022_percentage_gdp'] = pd.to_numeric(df_county_filtered['2022_percentage_gdp'], errors='coerce')
# Get the positive and negative changes in GDP for 2022
positive_count22 = (df_county_filtered['2021_percentage_gdp'] > 0).sum()
negative_count22 = (df_county_filtered['2021_percentage_gdp'] < 0).sum()
negative_count22 = negative_count22 + (df_county_filtered['2021_percentage_gdp'] == 0).sum()
# Get the positive and negative changes in GDP for 2021
positive_count21 = (df_county_filtered['2022_percentage_gdp'] > 0).sum()
negative_count21 = (df_county_filtered['2022_percentage_gdp'] < 0).sum()
negative_count21 = negative_count21 + (df_county_filtered['2022_percentage_gdp'] == 0).sum()


# Visualization 3
# Create a pie chart to show the percentage change of personal income for 2021 and 2022 respectively of all counties=
# Set the data for the plots
data_2021 = [positive_count21, negative_count21]
data_2022 = [positive_count22, negative_count22]
# Labels for the pie charts
labels = ['Positive', 'Negative']
# Create a figure and subplots
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
# Pie chart for 2021
ax[0].pie(data_2021, labels=labels, autopct='%1.1f%%', startangle=90)
ax[0].set_title('2021 County Percentage Change of Personal Income')
# Pie chart for 2022
ax[1].pie(data_2022, labels=labels, autopct='%1.1f%%', startangle=90)
ax[1].set_title('2022 County Percentage Change of Personal Income')
plt.tight_layout()
plt.show()


# Convert GDP columns to numeric, handling non-numeric values
df_county_filtered["2021_GDP"] = pd.to_numeric(df_county_filtered["2021_GDP"].str.replace(",", ""), errors='coerce')
df_county_filtered["2022_GDP"] = pd.to_numeric(df_county_filtered["2022_GDP"].str.replace(",", ""), errors='coerce')
# Drop NaN values
df_county_filtered = df_county_filtered.dropna(subset=['2021_GDP', '2022_GDP'])


# Visualization 4
# Create histograms for county GDP in 2021 and 2022
# Use logarithmic transformation to obtain GDP values
df_county_filtered['2021_GDP_log'] = np.log10(df_county_filtered['2021_GDP'].replace(0, pd.NA)).fillna(0)
df_county_filtered['2022_GDP_log'] = np.log10(df_county_filtered['2022_GDP'].replace(0, pd.NA)).fillna(0)
fig, ax = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
# Plot histogram for 2021 GDP
ax[0].hist(df_county_filtered['2021_GDP_log'], bins=30, edgecolor='black')
ax[0].set_title("County GDP in 2021")
ax[0].set_xlabel("GDP")
ax[0].set_ylabel("Number of Counties")
# Plot histogram for 2022 GDP
ax[1].hist(df_county_filtered['2022_GDP_log'], bins=30, edgecolor='black')
ax[1].set_title("County GDP in 2022")
ax[1].set_xlabel("GDP")
plt.tight_layout()
plt.show()


# Filter the merged data to only get the states
df_state_filtered2 = df_merged[(df_merged.index.isin(state_names)) & (df_merged['2022_rank_gdp'] == 'None') & (df_merged['2022_prank_gdp'] == 'None')]
df_state_filtered2.drop(columns = ['2021_dollars_pi_county', '2022_dollars_pi_county', '2022_rank_pi', '2021_percentage_pi', '2022_percentage_pi_county', '2022_prank_pi'], inplace = True)
df_state_filtered2.drop(columns = ['2022_rank_gdp', '2022_prank_gdp'], inplace = True)
df_state_filtered2.drop(index = 'DISTRICT OF COLUMBIA', inplace = True)

# Convert the personal income columns to int
df_state_filtered2['2021_dollars_pi_state'] = pd.to_numeric(df_state_filtered2['2021_dollars_pi_state'].str.replace(",", ""))
df_state_filtered2['2022_dollars_pi_state'] = pd.to_numeric(df_state_filtered2['2022_dollars_pi_state'].str.replace(",", ""))



# Visualization 5
# Scatter plot of the personal incomes of each state in 2021 and 2022
states_pos = df_state_filtered2.index
x_positions = range(len(states_pos))  # Numeric positions for states on the x-axis
# Create the a stacked bar graph
plt.figure(figsize=(15, 6))
# Plot the bars for 2021
plt.bar(x_positions, df_state_filtered2["2021_dollars_pi_state"], label="2021", color="blue")
# Plot the bars for 2022 on top of 2021
plt.bar(x_positions, df_state_filtered2["2022_dollars_pi_state"], bottom=df_state_filtered2["2021_dollars_pi_state"], label="2022", color="orange")
plt.xticks(x_positions, states_pos, rotation=90)  # Set state names as x-axis labels
plt.xlabel("States")
plt.ylabel("Personal Income (Trillion Dollars)")
plt.title("Total Personal Income of US States in 2021 and 2022")
plt.legend()
plt.tight_layout()
plt.show()
