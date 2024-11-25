import pandas as pd

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
df_merged.head(70)
