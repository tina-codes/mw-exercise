import pandas as pd

# Create dataframe with only created_dt column
people = pd.read_csv('/home/cnicosia/src/MissionWired/people.csv', usecols = ['created_dt'])

# Convert created_dt to date type  - datetime object wont aggregate properly
people['created_dt'] = pd.to_datetime(people['created_dt']).dt.date

# Create aquisition_facts dataframe using value counts from people dataframe, rename columns
acquisition_facts = people['created_dt'].value_counts().rename_axis('acquisition_date').reset_index(name='acquisitions')

# Convert data type back to datetime
acquisition_facts['acquisition_date'] = pd.to_datetime(acquisition_facts['acquisition_date'])

# save to csv
acquisition_facts.to_csv('acquisition_facts.csv')
