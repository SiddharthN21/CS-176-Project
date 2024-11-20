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
