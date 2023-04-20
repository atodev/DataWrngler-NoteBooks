
#!/usr/bin/env python
# coding: utf-8

import argparse
import pandas as pd

# define command-line arguments
parser = argparse.ArgumentParser(description='Filter data from input TSV file and write to output CSV and TSV files')
parser.add_argument('input_file', type=str, help='Path to input TSV file')
parser.add_argument('csv_output_file', type=str, help='Path to output CSV file')
parser.add_argument('tsv_output_file', type=str, help='Path to output TSV file')

# parse command-line arguments
args = parser.parse_args()

# read input TSV file into DataFrame
df = pd.read_csv(args.input_file, sep='\t', low_memory=False)

# filter DataFrame to keep only rows where 'NWOW_SCOPE_INDICATOR' column has value 'Yes'
yes_df = df[df['NWOW_SCOPE_INDICATOR'] == 'Yes']
yes_df = yes_df.reset_index(drop=True)

# create DataFrame of email addresses
addresses_df = pd.DataFrame(yes_df['EMPL_EMAIL_ALIAS'], columns=['Addresses'])

# move 'EMPL_EMAIL_ALIAS' column to first position and rename to 'Subject'
subject_col = yes_df.pop('EMPL_EMAIL_ALIAS')
yes_df.insert(0, 'Subject', subject_col)

# write email addresses DataFrame to TSV file
addresses_df.to_csv(args.tsv_output_file, sep='\t', index=False)

# write filtered DataFrame to CSV file
yes_df.to_csv(args.csv_output_file, index=False)
