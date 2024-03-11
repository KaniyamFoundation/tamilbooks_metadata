# This script groups the WC data by OCLC Number which was executed first time
import pandas as pd

# Load the CSV file
df = pd.read_csv('tamil.csv')

# Define a function to fill missing values from other rows in the same group
def fill_missing_values(group):
    print(f"Processing OCLC: {group['oclcNumber'].iloc[0]}")

    # Identify the row with the maximum number of non-NA values
    idx_max_filled = group.notna().sum(axis=1).idxmax()
    reference_row = group.loc[idx_max_filled]
    
    # Fill missing values in the reference row with values from other rows in the group
    for col in group.columns:
        if pd.isna(reference_row[col]):
            # Find a non-NA value for the current column in the group if available
            for idx, row in group.iterrows():
                if not pd.isna(row[col]):
                    reference_row[col] = row[col]
                    break
    return reference_row

# Group by 'oclc' and apply the filling function
filled_df = df.groupby('oclcNumber', as_index=False).apply(fill_missing_values).reset_index(drop=True)

# Save the processed DataFrame to a new CSV file
filled_df.to_csv('processed_file.csv', index=False)
