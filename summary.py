import os
import pandas as pd
import warnings

# get a list of all TSV files in the local directory
tsv_files = [f for f in os.listdir() if f.endswith('.tsv')]

# create an empty DataFrame to store the activity summary data
activity_summary = pd.DataFrame(columns=['File Name', 'Address', 'Sent', 'Received'])

# loop over each TSV file and process the data
for file_name in tsv_files:
    # read the TSV file into a DataFrame
    df = pd.read_csv(file_name, sep='\t')
    
    # group by the 'Local' column and count the number of unique values in the 'Remote' column
    activity_counts = df.groupby('Local').agg({'Remote': 'nunique'}).reset_index()

    # rename the columns to reflect the contents of the DataFrame
    activity_counts.columns = ['Address', 'Sent']

    # loop over each unique address and get the corresponding activity data
    for address in activity_counts['Address']:
        # create a DataFrame containing only edges for the current address
        address_data = df[df['Local'] == address]

        # count the number of unique values in the 'Remote' column to get the number of edges sent
        sent_count = address_data['Remote'].nunique()

        # create a DataFrame containing only edges where the current address is the destination
        received_data = df[df['Remote'] == address]

        # count the number of unique values in the 'Local' column to get the number of edges received
        received_count = received_data['Local'].nunique()

        # create a new row for the activity_summary DataFrame
        new_row = {'File Name': file_name, 'Address': address, 'Sent': sent_count, 'Received': received_count}

        # append the new row to the activity_summary DataFrame
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            activity_summary = activity_summary.append(new_row, ignore_index=True)
    
# output the activity summary to a single CSV file
summary_file_name = 'all_summary.csv'
activity_summary.to_csv(summary_file_name, index=False)
