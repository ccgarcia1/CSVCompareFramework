import csv

file1_path = 'C:\\compare\\fdl_corp_sub_region_CSV_after.csv'  # OLD PROD
file2_path = 'C:\\compare\\fdl_corp_sub_region_CSV_before.csv'  # PROD

def compare_csv_ignore_columns(file1, file2, columns_to_ignore):
    records_dict1 = {}
    records_dict2 = {}

    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        reader1 = csv.DictReader(f1)
        reader2 = csv.DictReader(f2)

        for row1 in reader1:
            key = (row1['SUB_REGION_CODE'])
            records_dict1[key] = {col: row1[col].strip() for col in row1 if col not in columns_to_ignore}

        for row2 in reader2:
            key = (row2['SUB_REGION_CODE'])
            records_dict2[key] = {col: row2[col].strip() for col in row2 if col not in columns_to_ignore}

        # Find differences between the dictionaries
        differing_records = {}

        for key in records_dict1:
            if key in records_dict2:
                if records_dict1[key] != records_dict2[key]:
                    differing_records[key] = {
                        'file1_data': records_dict1[key],
                        'file2_data': records_dict2[key],
                        'differences': {}
                    }
                    for col in records_dict1[key]:
                        if records_dict1[key][col] != records_dict2[key].get(col):
                            differing_records[key]['differences'][col] = {
                                'file1_value': records_dict1[key][col],
                                'file2_value': records_dict2[key].get(col)
                            }
            else:
                print('Records present in PROD but not present in OLD PROD')
                print(key)

        for key in records_dict2:
            if key not in records_dict1:
                print('Records present in OLD PROD but not present in PROD')
                print(key)

        return differing_records

columns_to_ignore = ['UPDATE_DATE', 'MODIFY_DATE']  # Replace with column names you want to ignore

differences = compare_csv_ignore_columns(file1_path, file2_path, columns_to_ignore)
if differences:
    print("Differences found:")
    print(len(differences.keys()))
    for key, value in differences.items():
        print(f"Compound Key: {key}")
        print("File 1 data:", value['file1_data'])
        print("File 2 data:", value['file2_data'])
        print("Detailed differences:")
        for col, diff in value['differences'].items():
            print(f" - {col}: File 1 value = {diff['file1_value']}, File 2 value = {diff['file2_value']}")
        print(f"********************")    
else:
    print("No differences found.")
