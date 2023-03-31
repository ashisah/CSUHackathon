import pandas as pd

# Read in the CSV file
df = pd.read_csv('kits.csv')

# Iterate over each row in the DataFrame
for index, row in df.iterrows():

    # Split the third column into separate values
    values = row['status_history'][1:-1].split(', ')

    # Add each value as a new column to the DataFrame
    for i, val in enumerate(values):
        df.at[index, f'Column {i+4}'] = val.strip()[1:-1]

    
    


# Save the modified DataFrame to a new CSV file
df.to_csv('cleaned.csv', index=False)


split_df = pd.DataFrame()


# Read in the CSV file
df = pd.read_csv('cleaned.csv')



for i in range(4, df.shape[1]):
    column_name = df.columns[i]

    for index, row in df.iterrows():
        cell_value = row[i]

        #print(i, 'th: ' , cell_value)
        
        if isinstance(cell_value, str):
             
             if len(cell_value.split()) > 2:

                action = cell_value.split()[0]
                
                date = cell_value.split()[1]
                
                institution = " ".join(cell_value.split()[2:])
                
                #print(cell_value)


                split_df.loc[index, f'action{i-3}'] = action
                split_df.loc[index, f'date{i-3}'] = date
                split_df.loc[index, f'institution{i-3}'] = institution
                
            

split_df = pd.concat([df.iloc[:, :3], split_df], axis=1)

simplified_df = split_df.iloc[:, :15]

# Save the new DataFrame to a new CSV file
split_df.to_csv('split_data.csv', index=False)

simplified_df.to_csv('simplified_data.csv', index=False)









        
        