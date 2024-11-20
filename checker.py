import csv

def print_single_row(file_path, row_index):
    print(f"Printing row {row_index} from file: {file_path}")
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        current_row = 0
        for row in csvreader:
            if current_row == row_index:
                print(row)  # Print the entire row as a list
                break
            current_row += 1
        else:
            print(f"Row {row_index} not found in the file.")

# print_single_row('facebook_dataset.csv', 0)
# print_single_row('google_dataset.csv', 0)
# print_single_row('website_dataset.csv', 0)
print_single_row('fourth_dataset.csv', 1)