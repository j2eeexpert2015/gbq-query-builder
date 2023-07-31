from application_constants import *
import pandas as pd
import sys

def validate_column_presence(file_name):
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
    #print(df)
    # Filter the DataFrame based on the 'Source Type' column
    df = df.loc[df[SOURCE_TYPE] == SOURCE_TYPE_BASE_VALUE]

    if not df.empty:
        # Group the DataFrame by the 'Group', 'Source Table', and 'Target Table' columns
        grouped = df.groupby([GROUP, SOURCE_SCHEMA, SOURCE_TABLE, JOIN_TABLE_1,JOINER_COLUMN_1,JOIN_TYPE1,TARGET_TABLE])
        """
        print("grouped df:\n")
        for key, item in grouped:
            print(grouped.get_group(key), "\n\n")
        """
        # Open the output file
        with open(output_file, 'w') as f:
            f.write("-- All Base Queries " + '\n')
            source_table_alias='s'
            join_table_alias = 'j'
            # Iterate over each group
            for (group, source_schema, source_table,join_table_1,join_column1,join_type_1 ,target_table), group_df in grouped:
                # Check if the source table and target table are the same for all rows in the group
                if group_df[SOURCE_TABLE].nunique() > 1 or group_df[TARGET_TABLE].nunique() > 1 or group_df[JOIN_TABLE_1].nunique() > 1:
                    print(f"Source Table ,Target Table and JOIN Table are not the same for all rows in group {group}. Skipping.")
                    continue
                # Combine the Source Column values into a comma-separated string
                column_values = ', '.join(group_df[SOURCE_COLUMN].astype(str))
                source_columns = ', '.join([f"{source_table_alias}.{col}" for col in column_values.split(', ')])
                target_columns = ', '.join([f"{col}" for col in column_values.split(', ')])
                if join_type_1 =='L':
                    join_type_1='LEFT OUTER JOIN'
                query =  f"""SELECT DISTINCT \n{source_columns} \nFROM `{source_schema}.{source_table}`  as {source_table_alias} \n {join_type_1} \n `{source_schema}.{join_table_1}` as {join_table_alias} \n on {source_table_alias}.{join_column1}={join_table_alias}.{join_column1} \n EXCEPT \n DISTINCT \nSELECT {target_columns} \nFROM `{target_table}`;\n"""

                # Print the SQL query
                #print(query)
                # Write the SQL query to the output file
                f.write(query + '\n')
                #print(f"Base queries written to file '{output_file}'.")
    else:
        print('!! No entry found for base queries,hence no queries generated')
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
                target1 = row[TRANSFORMATION_RULE]
                target2 = row[TARGET_COLUMN]

                # Form the SQL query
                query = f"""SELECT {target1}, {target2} \nCASE WHEN {target1} = {target2} THEN 'False' \nELSE 'True' \nEND \nFROM `{target_table}`;\n"""
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
print(f"Process ,completed . Please check output file '{output_file}' ")



