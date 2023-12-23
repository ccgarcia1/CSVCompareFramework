file1_path = 'C:\\trash\\DGPM_DAO_part_master.csv'
file2_path = 'C:\\trash\\DGPM_EMEA_part_master.csv'

def compare_csv_ignore_columns(file1, file2, columns_to_ignore):
    records_dict1 = {}
    records_dict2 = {}

    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        reader1 = csv.DictReader(f1)
        reader2 = csv.DictReader(f2)

        for row1 in reader1:
            key = (row1['PART_NUM'], row1['CCN'])
            records_dict1[key] = {col: row1[col].strip() for col in row1 if col not in columns_to_ignore}


        for row2 in reader2:
            key = (row2['PART_NUM'], row2['CCN'])
            records_dict2[key] = {col: row2[col].strip() for col in row2 if col not in columns_to_ignore}

        # Find differences between the dictionaries
        differing_records = {}
        #print(records_dict1)

        for key in records_dict1:
            if key in records_dict2:
                if records_dict1[key] != records_dict2[key]:
                    differing_records[key] = {
                        'file1_data': records_dict1[key],
                        'file2_data': records_dict2[key]
                    }
            else:
                print('Records present in File2 but not present in File 1')
                print(key)

        for key in records_dict2:
            if key not in records_dict1:
                print('Records present in File2 but not present in File 1')
                print(key)
        return differing_records

columns_to_ignore = ['WIP_TRACKING_FLAG']  # Replace with column names you want to ignore

differences = compare_csv_ignore_columns(file1_path, file2_path, columns_to_ignore)
if differences:
    print("Differences found:")
    for key, value in differences.items():
        print(f"Compound Key: {key}")
        print("File 1 data:", value['file1_data'])
        print("File 2 data:", value['file2_data'])
else:
    print("No differences found.")