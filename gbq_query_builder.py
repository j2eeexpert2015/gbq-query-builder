from application_constants import *
import pandas as pd
import sys

def validate_column_presence(file_name):
    print("Validating column presence ")
    # Read the Excel file
    df = pd.read_excel(file_name)
    #list for missing columns in the input file
    missing_columns =[]

    # Check if all the necessary columns exist in the DataFrame
    for col in ALL_COLUMN_NAMES:
        if col not in df.columns:
            missing_columns.append(col)
    if missing_columns:
        print(f"Error !!!! Skipping query generation as columns '{missing_columns}' missing in the input file '{file_name}'.")
        sys.exit()
    else:
        print("All required columns are present ....continuing further processing.")


def generate_base_queries(file_name,output_file):
    print("generate_base_queries .... started ")
    # Read the Excel file
    df = pd.read_excel(file_name)
    # Filter the DataFrame based on the 'Source Type' column
    df = df.loc[df[SOURCE_TYPE] == SOURCE_TYPE_BASE_VALUE]

    if not df.empty:
        # Group the DataFrame by the 'Group', 'Source Table', and 'Target Table' columns
        grouped = df.groupby([GROUP, SOURCE_SCHEMA, SOURCE_TABLE, TARGET_TABLE])
        """
        print("grouped df:\n")
        for key, item in grouped:
            print(grouped.get_group(key), "\n\n")
        """
        # Open the output file
        with open(output_file, 'w') as f:
            f.write("-- All Base Queries " + '\n')
            # Iterate over each group
            for (group, source_schema, source_table, target_table), group_df in grouped:
                # Check if the source table and target table are the same for all rows in the group
                if group_df[SOURCE_TABLE].nunique() > 1 or group_df[TARGET_TABLE].nunique() > 1:
                    print(f"Source Table and Target Table are not the same for all rows in group {group}. Skipping.")
                    continue
                # Combine the Source Column values into a comma-separated string
                source_column_values = ', '.join(group_df[SOURCE_COLUMN].astype(str))
                columns = ', '.join([f"{col}" for col in source_column_values.split(', ')])
                query = f"""SELECT DISTINCT \n{columns} \nFROM {source_schema}.{source_table}  EXCEPT DISTINCT \nSELECT {columns} \nFROM {target_table};\n"""
                # Print the SQL query
                #print(query)
                # Write the SQL query to the output file
                f.write(query + '\n')
    else:
        print('No entry found for base queries')
    print("generate_base_queries .... completed ")



def generate_self_queries(file_name, output_file):
    print("generate_self_queries .... started ")
    # Read the Excel file
    df = pd.read_excel(file_name)
    # Filter the DataFrame based on the 'Source Type' column
    df = df.loc[df[SOURCE_TYPE] == SOURCE_TYPE_SELF_VALUE]
    if not df.empty:
        # Open the output file
        with open(output_file, 'a') as f:
            f.write("-- All Self Queries " + '\n')
            # Iterate over each row
            for index, row in df.iterrows():
                target_table = row[TARGET_TABLE]
                target1 = row[SELF_TARGET_1]
                target2 = row[SELF_TARGET_2]

                # Form the SQL query
                query = f"""SELECT {target1}, {target2} \nCASE WHEN {target1} = {target2} THEN 'False' \nELSE 'True' \nEND \nFROM {target_table};\n"""
                #print(query)
                # Write the SQL query to the output file
                f.write(query + '\n')

    else:
        print('No entry found for Self queries')
    print("generate_self_queries .... ended ")




# Specify the name of the Excel file and the column names
file_name = DATA_FILE_NAME

# Use the constants to define the column names
column_names = ALL_COLUMN_NAMES
# Specify the name of the output file
output_file = OUTPUT_FILE_NAME
validate_column_presence(file_name)
generate_base_queries(file_name,output_file)
generate_self_queries(file_name,output_file)




