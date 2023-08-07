# Define each column name as a separate constant
GROUP = 'Group'
SOURCE_PROJECT = 'Source Project'
SOURCE_TYPE = 'Source Type'
SOURCE_SCHEMA = 'Source Schema'
SOURCE_TABLE = 'Source Table'
SOURCE_COLUMN = 'Source Column'

JOIN_TABLE_1 ='Join Table1'
JOINER_COLUMN_1 ='Join Table1 Joiner column'
JOIN_TYPE1 ='Join Table1 type'


TARGET_TABLE = 'Target Table'
TRANSFORMATION_RULE = 'Transformation Rule'
TARGET_COLUMN = 'Target Column'


SOURCE_TYPE_BASE_VALUE='Base'
SOURCE_TYPE_SELF_VALUE='Self'

# Define a list that contains all the column names
ALL_COLUMN_NAMES = [GROUP,SOURCE_PROJECT,SOURCE_TYPE, SOURCE_SCHEMA, SOURCE_TABLE,SOURCE_COLUMN,JOIN_TABLE_1,JOINER_COLUMN_1,JOIN_TYPE1,TARGET_TABLE,TRANSFORMATION_RULE,TARGET_COLUMN]
#DATA_FILE_NAME='data_final.xlsx'
DATA_FILE_NAME= 'data_final.xlsx'
OUTPUT_FILE_NAME='GBQ_Query.txt'