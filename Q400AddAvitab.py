# https://forums.x-plane.org/index.php?/files/file/88863-flyjsim-q4xp-avitab-integration/
import re

objCount = re.compile('P _obja/count (\\d*)')
pointsCount = re.compile('POINT_COUNTS\\s(\\d*)\\s0\\s0\\s(\\d*)')

planeMakerString = """P _obja/{objNumber}/_obj_flags 13
P _obja/{objNumber}/_v10_att_body -1
P _obja/{objNumber}/_v10_att_file_stl Avitab/Ipad.obj
P _obja/{objNumber}/_v10_att_gear -1
P _obja/{objNumber}/_v10_att_phi_ref 0.000000000
P _obja/{objNumber}/_v10_att_psi_ref 0.000000000
P _obja/{objNumber}/_v10_att_the_ref 0.000000000
P _obja/{objNumber}/_v10_att_wing -1
P _obja/{objNumber}/_v10_att_x_acf_prt_ref 0.000000000
P _obja/{objNumber}/_v10_att_y_acf_prt_ref 0.000000000
P _obja/{objNumber}/_v10_att_z_acf_prt_ref 0.000000000
P _obja/{objNumber}/_v10_is_internal 0
P _obja/{objNumber}/_v10_steers_with_gear 0
"""

pointsString = """VT -0.78536737 0.38269272 -13.86926460 0.65875959 0.37543550 0.65198463 0 0
VT -0.79364312 0.38252532 -13.86080647 0.65875959 0.37543550 0.65198463 0 1
VT -0.78874958 0.39397341 -13.87234306 0.65875959 0.37543550 0.65198463 1 0
VT -0.78874958 0.39397341 -13.87234306 0.66004431 0.37425861 0.65136170 1 0
VT -0.79364312 0.38252532 -13.86080647 0.66004431 0.37425861 0.65136170 0 1
VT -0.79701293 0.39381117 -13.86387634 0.66004431 0.37425861 0.65136170 1 1
VT -0.93533695 0.29601395 -13.63562679 0.67889237 0.43063426 0.59469253 -0.00000018 0.32226562
VT -0.99943161 0.46313506 -13.68347454 0.67889237 0.43063426 0.59469253 0.00000109 0.48339397
VT -0.83014393 0.47121748 -13.88258362 0.67889237 0.43063426 0.59469253 0.26855427 0.48339736
VT -0.76604235 0.30408621 -13.83471298 0.67883188 0.43070045 0.59471375 0.26855454 0.32226643
VT -0.93533695 0.29601395 -13.63562679 0.67883188 0.43070045 0.59471375 -0.00000018 0.32226562
VT -0.83014393 0.47121748 -13.88258362 0.67883188 0.43070045 0.59471375 0.26855427 0.48339736
"""

idxString = """IDX10 27436 27437 27438 27439 27440 27441 27442 27443 27444 27445
IDX 27446
IDX 27447
"""

animString = """
ANIM_begin
ANIM_hide    0    0    FJS/Q4XP/JPAD/JPAD_HideLeft
ANIM_show    1    1    FJS/Q4XP/JPAD/JPAD_HideLeft
        ATTR_no_cockpit
        ATTR_draw_disable
        ATTR_manip_command button avitab/Home
    TRIS 76167 6
        ATTR_cockpit
        ATTR_draw_enable
        ATTR_light_level 0 1 avitab/brightness
        ATTR_shiny_rat 0.97
    TRIS 76173 6
        ATTR_light_level_reset
        ATTR_no_cockpit
        ATTR_draw_disable
ANIM_end
"""


def update_acf():
    try:
        with open('Q4XP.acf', 'r', encoding='utf-8') as file:
            data = file.readlines()

        new_object_line_number = 0
        new_obj_number = 0
        last_object_line_number = 0
        for i, line in enumerate(data):
            if "Avitab/Ipad.obj" in line:
                input("Aircraft has already been updated. Press enter to exit...")
                exit(0)
            match = re.match(objCount, line)
            if match:
                new_object_line_number = i
                new_obj_number = match.group(1)

        for i, line in enumerate(data):
            if ("P _obja/" + str(int(new_obj_number) - 1)) in line:
                last_object_line_number = i + 1

        data[new_object_line_number] = "P _obja/count " + str((int(new_obj_number) + 1)) + '\n'
        data.insert(last_object_line_number, planeMakerString.format(objNumber=new_obj_number))
        with open('Q4XP.acf', 'w', encoding='utf-8') as file:
            file.writelines(data)
    except (FileNotFoundError, PermissionError, OSError):
        input("Unable to open/write to Q4XP.acf. Press enter to exit...")
        exit(1)


def update_obj():
    try:
        with open('Q4XP_cockpit.obj', 'r', encoding='utf-8') as file:
            data = file.readlines()

        last_vt_index = 0
        last_idx_index = 0
        for i, line in enumerate(data):
            match = re.match(pointsCount, line)
            if match:
                first_num = match.group(1)
                second_num = match.group(2)
                first_num_replaced = line.replace(first_num, str(int(first_num) + len(pointsString.splitlines())))
                second_num_replaced = first_num_replaced.replace(second_num,
                                                                 str(int(second_num) + len(pointsString.splitlines())))
                data[i] = second_num_replaced
            if line.startswith("VT"):
                last_vt_index = i + 1
            if line.startswith("IDX"):
                last_idx_index = i + 1
    except (FileNotFoundError, PermissionError, OSError):
        input("Unable to open/write to Q4XP_cockpit.obj. Press enter to exit...")
        exit(1)

    data.insert(last_idx_index, idxString)
    data.insert(last_vt_index, pointsString)
    data.append(animString)

    with open('Q4XP_cockpit.obj', 'w', encoding='utf-8') as file:
        file.writelines(data)


update_acf()
update_obj()
input("Avitab install completed, press enter to exit...")
