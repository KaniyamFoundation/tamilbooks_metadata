# This script groups the WC data by 'title', 'creator', 'specificFormat', 'edition', 'publisher', 'publicationDate' to remove few duplicates

import pandas as pd

# Load the CSV file
df = pd.read_csv('tamil.csv')
print("CSV loaded.")

# Identify columns for grouping
group_columns = ['title', 'creator', 'specificFormat', 'edition', 'publisher', 'publicationDate']

# Separate unique rows that cannot be grouped
unique_mask = df.duplicated(subset=group_columns, keep=False)
unique_rows = df[~unique_mask]
groupable_rows = df[unique_mask]
print("Separated unique rows from groupable rows.")

def fill_group(group):
    filled_row = group.ffill().bfill().iloc[0]
    return filled_row

# Group the data and fill missing values within each group
grouped = groupable_rows.groupby(group_columns, as_index=False)
filled_groups = grouped.apply(fill_group)
print("Processed grouped rows.")

# Concatenate the filled groups with the unique rows
final_df = pd.concat([filled_groups, unique_rows], ignore_index=True)
print("Combined processed groups with unique rows.")

# Save the final DataFrame to a new CSV file
final_df.to_csv('your_output_file.csv', index=False)
print("CSV file has been processed and saved as 'your_output_file.csv'.")
