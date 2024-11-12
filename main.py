import csv


file1_path = 'C:\\compare\\fdl_corp_CURRENCY_EXCHANGE_old_EFDRP.csv'
file2_path = 'C:\\compare\\fdl_corp_CURRENCY_EXCHANGE_new_FDRP.csv'


def compare_csv_ignore_columns(file1, file2, columns_to_ignore):
    records_dict1 = {}
    records_dict2 = {}
    has_messagef1 = False
    has_messagef2 = False


    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        reader1 = csv.DictReader(f1)
        reader2 = csv.DictReader(f2)


        for row1 in reader1:
            key = (row1['BEGIN_DATE'],row1['BUSINESS_UNIT_ID'],row1['BUSINESS_UNIT_CURRENCY_CODE'],row1['CURRENCY_EXCHANGE_RATE_TYPE'],row1['SOURCE_CURRENCY_CODE'],row1['TARGET_CURRENCY_CODE'])
            records_dict1[key] = {col: row1[col].strip() for col in row1 if col not in columns_to_ignore}


        for row2 in reader2:
             key = (row2['BEGIN_DATE'],row2['BUSINESS_UNIT_ID'],row2['BUSINESS_UNIT_CURRENCY_CODE'],row2['CURRENCY_EXCHANGE_RATE_TYPE'],row2['SOURCE_CURRENCY_CODE'],row2['TARGET_CURRENCY_CODE'])
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
                if not has_messagef1:
                    print('Records present in file 1 but not present in file 2')
                has_messagef1 = True
               
                print(key)


        for key in records_dict2:
            if key not in records_dict1:
                if not has_messagef2:
                    print('Records present in file 2 but not present in file 1')
                has_messagef2 = True
                print(key)


        return differing_records


columns_to_ignore = ['UPDATE_UID', 'UPDATE_DATE']  # Replace with column names you want to ignore


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
