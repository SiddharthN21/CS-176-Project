import pandas as pd

### delcaring pis as the variable for the dataset
pis = pd.read_csv("CSV_Personal_Income_State.csv")

### removing the given columns for better merging experience later
ctremove = ["22_Q2_dollars","22_Q3_dollars","22_Q4_dollars","23_Q1_dollars","23_Q2_dollars","22_Q2_percentage", "22_Q3_percentage", "23_Q1_percentage", "23_Q2_dollars","22_Q4_percentage", "23_Q2_percentage", "23_Prank_Q2"]

### declaring new cleaned dataset
pis_cleaned = pis.drop(columns=ctremove)

### rename Unnamed column
pis_cleaned.rename(columns={"Unnamed: 0":"Name"}, inplace=True)

### set index to be the names of the states
pis_cleaned.set_index("Name", inplace=True)

### Removing regions for better merging experience
pis_cleaned.drop("New England ", axis=0, inplace=True)
pis_cleaned.drop("Rocky Mountain ", axis=0, inplace=True)
pis_cleaned.drop("Far West", axis=0, inplace=True)
pis_cleaned.drop("Plains ", axis=0, inplace=True)
pis_cleaned.drop("Great Lakes ", axis=0, inplace=True)
pis_cleaned.drop("Southeast ", axis=0, inplace=True)
pis_cleaned.drop("Southwest ", axis=0, inplace=True)
pis_cleaned.drop("Mideast ", axis=0, inplace=True)

### Turn empty space in dataset to display none
pis_cleaned.replace("........", None, inplace=True)

### display
pis_cleaned.head(60)


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

# Replace null values with None
gdp_state_county.replace('--', 'None', inplace = True)
gdp_state_county.head(5)



# Read the dataset of Personal income by county
pi_county = pd.read_csv('Personal_Income_State_County.csv')
# Drop the 2020 year columns
pi_county.drop('2020_dollars', axis = 1, inplace = True)
# Provide a name to the unnamed column
pi_county.rename(columns = {'Unnamed: 0': 'Name'}, inplace = True)
# Set the name as the index of the dataframe
pi_county.set_index('Name', inplace = True)

# Drop all states from the dataframe
# Create a list of states
state_names = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
               'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
               'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
               'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
               'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
# Remove all rows that are states
for i in state_names:
    pi_county.drop(i, axis = 0, inplace = True)
    
# Drop all the null/blank rows
pi_county.dropna(inplace = True)

# Replace null values with None
pi_county.replace('--', 'None', inplace = True)
pi_county.head(5)
