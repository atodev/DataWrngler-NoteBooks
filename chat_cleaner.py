#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Clean and filter chat data.')

# Add arguments for the input and output file paths
parser.add_argument('input', type=str, help='path to the input TSV file')
parser.add_argument('output', type=str, help='path to the output TSV file')

# Parse the command-line arguments
args = parser.parse_args()

# Read in the TSV file from the input path
df = pd.read_csv(args.input, sep='\t')

# Split the addresses by comma and count the number of addresses
df['num_addresses'] = df['To'].str.split(',').str.len()

# Filter out the rows where the number of addresses is greater than 12
df = df[df['num_addresses'] <= 12]

# Drop the 'num_addresses' column
df.drop('num_addresses', axis=1, inplace=True)

# Drop rows where either the 'From' or 'To' columns are null
df.dropna(subset=['From', 'To'], inplace=True)

# Filter out addresses that do not end with "@0.test"
df['From'] = df['From'][df['From'].str.endswith('@0.test')]
df['To'] = df['To'].apply(lambda x: ','.join([addr for addr in x.split(',') if addr.endswith('@0.test')]))

# Replace empty strings with NaN values
df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

# Drop rows where either the 'From' or 'To' columns are null again, in case any were created by the previous step
df.dropna(subset=['From', 'To'], inplace=True)

# Select the 'From', 'To', and 'Sent' columns, and rename the 'Sent' column to 'Date'
df = df[['From', 'To', 'Sent']].copy()
df.rename(columns={'Sent': 'Date'}, inplace=True)

# Add a new column named 'Direction' to the DataFrame with the value 'internal'
df['Direction'] = 'internal'

# Write the modified DataFrame to a new TSV file at the output path
df.to_csv(args.output, sep='\t', index=False)
