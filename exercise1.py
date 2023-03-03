import pandas as pd

# data files for exercise:
constituent_info = 'https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons.csv'

# Boolean values: 1 = True, 0 = False
email_addresses = 'https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email.csv'

# Only care about statuses where chapter_id is 1
# If email not present, assumed to still be subscribed where chapter_id is 1
subscription_status = 'https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email_chapter_subscription.csv'

# Create dataframes with necessary columns from CSV files:

# Of the two options, I used 'source' for source code, as it had more meaningful data for a client
# I used the created and modified dates from the consituents file as the exercise wanted the dates relevant to the person
constituents = pd.read_csv(constituent_info, usecols = ['cons_id', 'source', 'create_dt', 'modified_dt'])
emails = pd.read_csv(email_addresses, usecols = ['cons_email_id', 'cons_id', 'is_primary', 'email'])
status = pd.read_csv(subscription_status, usecols = ['cons_email_id', 'chapter_id', 'isunsub'])

# Check value counts to confirm correct data on join
# print(emails['is_primary'].value_counts())
# Number of rows where is_primary is 1 = 605639

# Filter emails dataframe by primary emails
emails = emails[emails['is_primary'] == 1]

# Filter status dataframe by chapter_id 1
status = status[status['chapter_id'] == 1]

# Create people dataframe by joining relevant columns from email and status dataframes
people = emails[['cons_email_id', 'cons_id', 'email']].merge(status[['cons_email_id', 'isunsub']], on='cons_email_id', how='left')

# Join relevant columns from constituents dataframe to people dataframe
people = people.merge(constituents[['source', 'create_dt', 'modified_dt', 'cons_id']], on='cons_id', how='left')

# drop unneeded columns
people.drop(['cons_email_id', 'cons_id'], axis=1, inplace=True)

# convert isunsub 0/1 values to booleans
people.loc[people['isunsub'] == 1, 'isunsub'] = True
people.loc[people['isunsub'] == 0, 'isunsub'] = False

# replace empty isunsub values with false as they are assumed to still be subscribed
people['isunsub'].fillna(False, inplace=True)

# pop isunsub column from dataframe
is_unsub = people.pop('isunsub')

# insert column in correct location with corrected name
people.insert(loc = 2, column = 'is_unsub', value = is_unsub)

# renaname columns
people.columns = ['email', 'code', 'isunsub', 'created_dt', 'updated_dt']

# set correct data types
people = people.astype({'created_dt': 'datetime64', 'updated_dt': 'datetime64'})

# save to csv
people.to_csv('people.csv')