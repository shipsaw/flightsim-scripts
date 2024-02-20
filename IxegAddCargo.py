# https://forums.x-plane.org/index.php?/files/file/71874-ixeg-737-classic-exterior-cargo-conversion/
import os
import re
import shutil

newAcf = 'B733_Cargo.acf'
newRainGlassObj = 'B733_Cargo_Rain_Glass.obj'

obj_count_regex = re.compile('P _obja/count (\\d*)')
points_count_regex = re.compile('POINT_COUNTS\\s(\\d*)\\s0\\s0\\s(\\d*)')
obj_to_remove_regex = re.compile('P _obja/(\\d*)/_v10_att_file_stl B733_Rain_Glass.obj')
obj_row_regex = re.compile('P _obja/(\\d+)')
obj_count_regex = re.compile('P _obja/count (\\d*)')
rain_glass_regex = re.compile('\\sTRIS\\s(3534)\\s(113988)')

window_covers_object = [
    'P _obja/{obj_number}/_obj_flags 156',
    'P _obja/{obj_number}/_v10_att_body -1',
    'P _obja/{obj_number}/_v10_att_file_stl B733_Cargo_Window_Covers.obj',
    'P _obja/{obj_number}/_v10_att_gear -1',
    'P _obja/{obj_number}/_v10_att_phi_ref 0.000000000',
    'P _obja/{obj_number}/_v10_att_psi_ref 0.000000000',
    'P _obja/{obj_number}/_v10_att_the_ref 0.000000000',
    'P _obja/{obj_number}/_v10_att_wing -1',
    'P _obja/{obj_number}/_v10_att_x_acf_prt_ref 0.000000000',
    'P _obja/{obj_number}/_v10_att_y_acf_prt_ref 0.000000000',
    'P _obja/{obj_number}/_v10_att_z_acf_prt_ref 0.000000000',
    'P _obja/{obj_number}/_v10_is_internal 0',
    'P _obja/{obj_number}/_v10_steers_with_gear 0',
]

cargo_rain_glass_object = [
    'P _obja/{obj_number}/_obj_flags 8194',
    'P _obja/{obj_number}/_v10_att_body -1',
    'P _obja/{obj_number}/_v10_att_file_stl B733_Cargo_Rain_Glass.obj',
    'P _obja/{obj_number}/_v10_att_gear -1',
    'P _obja/{obj_number}/_v10_att_phi_ref 0.000000000',
    'P _obja/{obj_number}/_v10_att_psi_ref 0.000000000',
    'P _obja/{obj_number}/_v10_att_the_ref 0.000000000',
    'P _obja/{obj_number}/_v10_att_wing -1',
    'P _obja/{obj_number}/_v10_att_x_acf_prt_ref 0.000000000',
    'P _obja/{obj_number}/_v10_att_y_acf_prt_ref 0.000000000',
    'P _obja/{obj_number}/_v10_att_z_acf_prt_ref 0.000000000',
    'P _obja/{obj_number}/_v10_is_internal 0',
    'P _obja/{obj_number}/_v10_steers_with_gear 0',
]


def copy_files():
    if os.path.exists(newAcf):
        input("Aircraft has already been updated. Press enter to exit...")
        exit(0)
    shutil.copyfile('./B733.acf', f'./{newAcf}')
    shutil.copyfile('./objects/B733_Rain_Glass.obj', f'./objects/{newRainGlassObj}')


def remove_obj(obj_regex):
    try:
        with open(f'{newAcf}', 'r', encoding='utf-8') as file:
            data = file.readlines()

        obj_rows = []
        deleted_object_obj_number = 0
        first_obj_row_index = 0
        last_obj_row_index = 0
        new_obj_number = 0
        object_count_line_number = 0
        for i, line in enumerate(data):
            obj_count_match = re.match(obj_count_regex, line)
            obj_row_match = re.match(obj_row_regex, line)
            obj_to_remove_match = re.match(obj_regex, line)
            if obj_count_match:
                object_count_line_number = i
                new_obj_number = int(obj_count_match.group(1)) - 1

            if obj_row_match:
                if first_obj_row_index == 0:
                    first_obj_row_index = i
                obj_rows.append((obj_row_match.group(1), line))
            elif first_obj_row_index != 0 and last_obj_row_index == 0:
                last_obj_row_index = i
            if obj_to_remove_match:
                deleted_object_obj_number = int(obj_to_remove_match.group(1))

        filtered_obj_rows = []
        for obj_row in obj_rows:
            if int(obj_row[0]) == deleted_object_obj_number:
                continue
            elif int(obj_row[0]) > deleted_object_obj_number:
                new_obj_number_str = str(int(obj_row[0]) - 1)
                new_line = re.sub(obj_row_regex, f'P _obja/{new_obj_number_str}', obj_row[1])
                filtered_obj_rows.append((new_obj_number_str, new_line))
            else:
                filtered_obj_rows.append(obj_row)

        sorted_obj_rows = sorted(filtered_obj_rows, key=lambda obj_row: obj_row[0])
        for i, row in enumerate(sorted_obj_rows):
            sorted_obj_rows[i] = row[1]

        data[object_count_line_number] = "P _obja/count " + str(new_obj_number) + '\n'
        data_start = data[:first_obj_row_index]
        data_end = data[last_obj_row_index:]
        data = data_start + sorted_obj_rows + data_end
        with open(f'{newAcf}', 'w', encoding='utf-8') as file:
            file.writelines(data)
    except (FileNotFoundError, PermissionError, OSError):
        input(f'Unable to open/write to {newAcf}. Press enter to exit...')
        exit(1)
    return new_obj_number


def add_obj(new_object_array):
    try:
        with open(f'{newAcf}', 'r', encoding='utf-8') as file:
            data = file.readlines()

        obj_rows = []
        deleted_object_obj_number = 0
        first_obj_row_index = 0
        last_obj_row_index = 0
        new_obj_number = 0
        last_obj_number = 0
        object_count_line_number = 0
        for i, line in enumerate(data):
            obj_count_match = re.match(obj_count_regex, line)
            obj_row_match = re.match(obj_row_regex, line)
            if obj_count_match:
                object_count_line_number = i
                new_obj_number = int(obj_count_match.group(1)) + 1

            if obj_row_match:
                obj_number = obj_row_match.group(1)
                if first_obj_row_index == 0:
                    first_obj_row_index = i
                obj_rows.append((obj_row_match.group(1), line))
                if int(obj_number) > last_obj_number:
                    last_obj_number = int(obj_number)
            elif first_obj_row_index != 0 and last_obj_row_index == 0:
                last_obj_row_index = i

        for new_object_string in new_object_array:
            obj_rows.append((last_obj_number + 1, new_object_string.format(obj_number=last_obj_number + 1) + '\n'))

        sorted_obj_rows = sorted(obj_rows, key=lambda obj_row: str(obj_row[0]))
        for i, row in enumerate(sorted_obj_rows):
            sorted_obj_rows[i] = row[1]

        data[object_count_line_number] = "P _obja/count " + str(new_obj_number) + '\n'
        data_start = data[:first_obj_row_index]
        data_end = data[last_obj_row_index:]
        data = data_start + sorted_obj_rows + data_end
        with open(f'{newAcf}', 'w', encoding='utf-8') as file:
            file.writelines(data)
    except (FileNotFoundError, PermissionError, OSError):
        input(f'Unable to open/write to {newAcf}. Press enter to exit...')
        exit(1)


def update_acf_metadata():
    try:
        with open(f'{newAcf}', 'r', encoding='utf-8') as file:
            data = file.readlines()

        for i, line in enumerate(data):
            if line.startswith('P acf/_is_airliner'):
                data[i] = 'P acf/_is_airliner 0\n'
            if line.startswith('P acf/_is_cargo'):
                data[i] = 'P acf/_is_cargo 1\n'
            if line.startswith('P acf/_name'):
                data[i] = 'P acf/_name IXEG B-737-300 Cargo\n'

        with open(f'{newAcf}', 'w', encoding='utf-8') as file:
            file.writelines(data)
    except (FileNotFoundError, PermissionError, OSError):
        input(f'Unable to open/write to {newAcf}. Press enter to exit...')
        exit(1)


def update_window_covers():
    try:
        with open(f'objects/{newRainGlassObj}', 'r', encoding='utf-8') as file:
            data = file.readlines()

        for i, line in enumerate(data):
            match = re.match(rain_glass_regex, line)
            if match:
                new_line = line.replace('113988', '324')
                data[i] = new_line

        with open(f'objects/{newRainGlassObj}', 'w', encoding='utf-8') as file:
            file.writelines(data)
    except (FileNotFoundError, PermissionError, OSError):
        input(f'Unable to open/write to {newRainGlassObj}. Press enter to exit...')
        exit(1)


copy_files()
remove_obj(obj_to_remove_regex)
add_obj(window_covers_object)
add_obj(cargo_rain_glass_object)
update_acf_metadata()
update_window_covers()
input("Avitab install completed, press enter to exit...")
