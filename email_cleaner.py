#!/usr/bin/env python
# coding: utf-8
import argparse
import pandas as pd

# Create an argument parser
parser = argparse.ArgumentParser(description='Process email messages data.')

# Add arguments for input and output file paths
parser.add_argument('input_file', type=str, help='Path to the input TSV file.')
parser.add_argument('output_file', type=str, help='Path to the output TSV file.')

# Parse the arguments
args = parser.parse_args()

# Load the input TSV file into a pandas DataFrame
df = pd.read_csv(args.input_file, sep='\t')

# Split the addresses by comma and count the number of addresses
df['num_addresses'] = df['TO'].str.split(',').str.len()

# Filter out the rows where the number of addresses is greater than 12
df = df[df['num_addresses'] <= 12]

# Drop the 'num_addresses' column
df.drop('num_addresses', axis=1, inplace=True)

# Filter out addresses that do not end with "@0.test"
df['FROM'] = df['FROM'][df['FROM'].str.endswith('@0.test')]
df['TO'] = df['TO'].apply(lambda x: ','.join([addr for addr in x.split(',') if addr.endswith('@0.test')]))

# Remove the rows where either 'FROM' or 'TO' column value is missing
df.dropna(subset=['FROM', 'TO'], inplace=True)

# Save the resulting DataFrame to a new TSV file
df.to_csv(args.output_file, sep='\t')
