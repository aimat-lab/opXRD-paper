from collections import defaultdict
from data_collector.resources import get_template_csv

import os
import zipfile, csv

def log(to_log : str):
    print(to_log)


def get_zip_path_mapping(path_list: list[str]) -> dict:
    name_counter = defaultdict(int)
    zip_path_dict = {}

    for path in path_list:
        try:
            file_name = os.path.basename(path)
            foldername = os.path.basename(os.path.dirname(path))
            base_path = os.path.join(foldername,file_name)

            if not base_path in name_counter:
                name_counter[base_path] = 1
            else:
                name_counter[base_path] += 1

            name = f"{foldername}_{name_counter[base_path]}"
            zip_path = os.path.join(name, file_name)

        except Exception as e:
            zip_path = path
            print(f"Error processing path '{path}': {e}")

        zip_path_dict[path] = zip_path

    return zip_path_dict



def zip_file_list(path_list: list[str], zipfile_path : str):
    zip_path_dict = get_zip_path_mapping(path_list=path_list)

    if os.path.isfile(zipfile_path):
        log(to_log=f'Target path {zipfile_path} already exists. Aborting ...')
        return

    with zipfile.ZipFile(zipfile_path, 'a') as zipf:
        for file_path in path_list:
            zip_path = zip_path_dict[file_path]
            zipf.write(file_path, zip_path)

    print(f"ZIP archive created at {zipfile_path}")



def produce_csv_file(absolute_path_list : list[str], target_path : str):
    zip_path_dict = get_zip_path_mapping(path_list=absolute_path_list)
    zip_path_list = list(zip_path_dict.values())
    template_path = get_template_csv()

    if os.path.isfile(target_path):
        print(f'Target CSV path {target_path} already exists. Aborting ...')
        return

    with open(template_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    for i, string in enumerate(zip_path_list, start=2):  # Starting from index 2 (third row)
        if i < len(data):
            data[i][0] = string
        else:
            data.append([string])

    with open(target_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"CSV file created at {target_path}")


if __name__ == "__main__":
    source_path = ["/home/work/Desktop/test1/asdf2.png"]
    the_target_path = "/home/work/Desktop/target"

    zip_file_list(source_path, the_target_path)

