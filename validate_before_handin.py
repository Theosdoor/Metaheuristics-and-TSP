#####
##### THIS PROGRAM VALIDATES THE PROGRAMS, TOUR FILES AND PROFORMA BEFORE YOU HAND IT IN.
##### YOU SHOULD RUN THIS PROGRAM BEFORE HAND-IN. YOU NEED A FOLDER IN WHICH THERE IS:
#####    a) THIS PROGRAM
#####    b) A FOLDER NAMED WHATEVER YOUR USER-NAME IS, E.G., "abcd12", WITH ALL YOUR FILES IN
#####       (THAT IS, ALL YOUR PROGRAMS, ALL YOUR TOURS AND YOUR PROFORMA)
#####    c) A FOLDER NAMED "city-files" THAT HOLDS ALL THE CITY FILES
#####    d) THE SUPPLIED TEXT FILE "alg_codes_and_tariffs.txt" (CONTAINING DATA RELATING TO THE
#####       ALGORITHM CODES AND TARIFFS).
#####    e) AN ORIGINAL UNTOUCHED COPY OF 'skeleton.py' (TO CHECK AGAINST - DOWNLOAD THIS COPY FROM
#####                                                    ULTRA JUST BEFORE YOU INTEND TO VALIDATE).
#####
##### NOTE THAT YOU WILL ONLY HAND IN THE FILES IN THE ABOVE FOLDER FROM b) (THAT IS, "abcd12") WITHIN
##### WHICH YOU WILL ALSO PLACE THE FEEDBACK FILE "AISearchValidationFeedback.txt" OBTAINED FROM YOUR
##### FINAL VALIDATION.
#####    
##### YOU SHOULD SCROLL DOWN TO THE NEXT BLOCK OF CAPITILIZED COMMENTS.
##### DO NOT TOUCH THE CODE IN BETWEEN! I REPEAT: DO NOT TOUCH THE CODE IN BETWEEN!
#####

import os
import sys
import time

flag_dictionary = {
    "validate_format_of_city_files" : {
        0: "all city files are properly formatted and these files have been registered",
        1: "*** fatal error: the folder of city files does not exist",
        2: "*** fatal error: the 'folder' of city files exists but is not a folder",
        3: "*** fatal error: there are no city files in the city file folder",
        4: "*** fatal error: a proposed city file is not a text file",
        5: "*** fatal error: a proposed city file name has '_' in it",
        6: "*** fatal error: there is a tag-based error when reading a city file",
        7: "*** fatal error: there are too few cities in a city file",
        8: "*** fatal error: the 'NOTE =' tag is missing in a city file",
        9: "*** fatal error: the number of city-to-city distances is incorrect in a city file"},
    "between_tag_pair" : {
        0 : "tags have been found",
        1 : "*** fatal error: a required tag is the empty tag",
        2 : "*** fatal error: a required tag does not exist",
        3 : "*** fatal error: the second tag after a found first tag does not exist"},
    "up_to_next_comma" : {
        0 : "a following comma has been found",
        1 : "*** fatal error : a following comma does not exist"},
    "collect_data_from_program_file" : {
        0 : "the data has been read correctly from the program file",
        1 : "*** error: the program file does not exist",
        2 : "*** error: the user-name or the algorithm code has not been correctly formatted",
        3 : "*** error: you haven't supplied an original untouched copy of 'skeleton.py' to check against"},
    "validate_a_program" : {
        0 : "successful validation",
        1 : "*** error: the definitive user-name and the program file user-name do not match",
        2 : "*** error: the algorithm code in the program file is illegal",
        3 : "*** error: an illegal module has been imported"},
    "collect_data_from_tour_file" : {
        0 : "the data has been read correctly from the tour file",
        1 : "*** error: the tour file does not exist",
        2 : "*** error: the tour file is not correctly formatted",
        3 : "*** error: the tour in the tour file does not consist of the stated number of cities"},
    "validate_a_tour" : {
        0 : "the tour file has successfully been validated against the appropriate city file",
        1 : "*** error: the definitive user-name and the user-name in the tour file do not match",
        2 : "*** error: the algorithm code in the tour file is illegal",
        3 : "*** error: corresponding progam cluster is invalid",
        4 : "*** error: there is a mis-match involving algorithm codes",
        5 : "*** error: the name of the city file in the tour file is illegal",
        6 : "*** error: numbers of cities in the tour file and the city file dont match",
        7 : "*** error: the tour does not contain the claimed number of cities",
        8 : "*** error: there are duplicate cities in the tour",
        9 : "*** error: cities in the tour are mis-named",
        10: "*** error: the tour doesn't have the length claimed",
        11: "*** error: mismatch between tour file name and city file in tour file",
        12: "*** error: there is an invalid run-time for the execution producing the tour"},
    "validating student programs" : {
        0 : "the student's programs validate",
        1 : "*** error: the algorithm codes in the two programs mis-match",
        2 : "*** error: two program clusters have the same algorithm code"}
}

legal_modules = ['abc', 'aifc', 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit', 'audioop',
                 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2',
                 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections', 'colorsys',
                     'compileall', 'concurrent', 'configparser', 'contextlib', 'contextvars', 'copy', 'copyreg', 'CProfile',
                     'crypt', 'csv', 'ctypes', 'curses',
                 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils', 'doctest', 'dummy_threading',
                 'email', 'encodings', 'ensurepip', 'enum', 'errno',
                 'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib', 'functools',
                 'gc', 'getopt', 'getpass', 'gettext', 'glob', 'grp', 'gzip',
                 'hashlib', 'heapq', 'hmac', 'html', 'http',
                 'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 'io', 'ipaddress', 'itertools',
                 'json',
                 'keyword',
                 'lib2to3', 'linecache', 'locale', 'logging', 'lzma',
                 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 'msilib', 'msvcrt', 'multiprocessing',
                 'netrc', 'nis', 'nntplib', 'numbers',
                 'operator', 'optparse', 'os', 'ossaudiodev',
                 'parser', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'poplib', 'posix',
                     'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc',
                 'queue', 'quopri',
                 'random', 're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy',
                 'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr',
                     'socket', 'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess',
                     'sunau', 'symbol', 'symtable', 'sys', 'sysconfig', 'syslog',
                 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter',
                     'token', 'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 'turtledemo', 'types', 'typing',
                 'unicodedata', 'unittest', 'urllib', 'uu', 'uuid',
                 'venv',
                 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg', 'winsound', 'wsgiref',
                 'xdrlib', 'xml', 'xmlrpc',
                 'zipapp', 'zipfile', 'zipimport', 'zlib']

#####
##### ALL YOU HAVE TO DO IS SET THE VARIABLE "user_name" EQUAL TO YOUR USER-NAME,
##### E.G., user_name = "abcd12"
#####
##### DO NOT TOUCH ANYTHING ELSE!
#####

user_name = "abcd12"

#####
##### DO NOT TOUCH ANY OF THE CODE THAT FOLLOWS! I REPEAT: DO NOT TOUCH ANY OF THE CODE THAT FOLLOWS!
#####
    
programs_to_submit = [["AlgAbasic.py", "AlgAenhanced.py"], ["AlgBbasic.py", "AlgBenhanced.py"]]
programs_prefix = ["AlgA", "AlgB"]
prefix_dictionary = {"AlgA" : ["AlgAbasic.py", "AlgAenhanced.py"], "AlgB" : ["AlgBbasic.py", "AlgBenhanced.py"]}
tour_files_to_submit = [["AlgA_AISearchfile012.txt", "AlgA_AISearchfile017.txt", "AlgA_AISearchfile021.txt", "AlgA_AISearchfile026.txt", "AlgA_AISearchfile042.txt",
                         "AlgA_AISearchfile048.txt", "AlgA_AISearchfile058.txt", "AlgA_AISearchfile175.txt", "AlgA_AISearchfile180.txt", "AlgA_AISearchfile535.txt"],
                        ["AlgB_AISearchfile012.txt", "AlgB_AISearchfile017.txt", "AlgB_AISearchfile021.txt", "AlgB_AISearchfile026.txt", "AlgB_AISearchfile042.txt",
                         "AlgB_AISearchfile048.txt", "AlgB_AISearchfile058.txt", "AlgB_AISearchfile175.txt", "AlgB_AISearchfile180.txt", "AlgB_AISearchfile535.txt"]]
additional_items_to_submit = ["AISearchProforma.pdf", "AISearchValidationFeedback.txt"]
city_file_folder = "city-files"
alg_codes_file = "alg_codes_and_tariffs.txt"

def integerize(the_string):
    length = len(the_string)
    stripped_string = "0"
    for i in range(0, length):
        if ord(the_string[i]) >= 48 and ord(the_string[i]) <= 57:
            stripped_string = stripped_string + the_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def between_tag_pair(the_string, tag_pair, start_location):
    batch = "between_tag_pair"
    flag = (batch, 0)
    if len(tag_pair[0]) == 0:
        flag = (batch, 1)
        return "", -1, flag
    start_first = the_string.find(tag_pair[0], start_location)
    if start_first == -1:
        flag = (batch, 2)
        return "", -1, flag
    start_second = the_string.find(tag_pair[1], start_first + len(tag_pair[0]))
    if start_second == -1:
        flag = (batch, 3)
        return "", -1, flag
    sandwich = the_string[start_first + len(tag_pair[0]):start_second]
    return sandwich, start_second + 1, flag

def strings_between_tag_pairs(the_string, tag_pairs, start_location):
    batch = "strings_between_tag_pairs"
    flag = (batch, 0)
    num_tag_pairs = len(tag_pairs)
    ok, i, values = True, 0, []
    while ok:
        sandwich, new_start_location, flag \
            = between_tag_pair(the_string, tag_pairs[i], start_location)
        if flag[1] == 0:
            values.append(sandwich)
            i = i + 1
            start_location = new_start_location
            if i == num_tag_pairs:
                ok = False
        else:
            ok = False
            start_location = -1
    return values, start_location, flag

def remove_all_spaces(the_string):
    length = len(the_string)
    new_string = ""
    for i in range(length):
        if the_string[i] != " ":
            new_string = new_string + the_string[i]
    return new_string

def read_file_into_string(input_file, ord_range):
    the_file = open(input_file, mode = 'r', encoding = 'utf-8')
    current_char = the_file.read(1)
    file_string = ""
    length = len(ord_range)
    while current_char != "":
        i = 0
        while i < length:
            if ord(current_char) >= ord_range[i][0] and ord(current_char) <= ord_range[i][1]:
                file_string = file_string + current_char
                i = length
            else:
                i = i + 1
        current_char = the_file.read(1)
    the_file.close()
    return file_string

def get_the_modules_imported(program_file):
    ord_range = [[0, 127]]
    program_file_string = read_file_into_string(program_file, ord_range)
    import_sandwiches = []
    location = 0
    if program_file_string[0:6] == "import":
        location = program_file_string.find("\n")
        if location != -1:
            import_sandwiches.append(program_file_string[6:location])
        else:
            import_sandwiches.append(program_file_string[6:])
            location = len(program_file_string)
    found = 0
    while found != -1:
        found = program_file_string.find("\nimport", location)
        if found != -1:
            location = program_file_string.find("\n", found + 7)
            if location != -1:
                import_sandwiches.append(program_file_string[found + 7:location])
            else:
                import_sandwiches.append(program_file_string[found + 7:])
                found = -1
    from_sandwiches = []
    location = 0
    if program_file_string[0:4] == "from":
        location = program_file_string.find("\n")
        if location != -1:
            import_sandwiches.append(program_file_string[4:location])
        else:
            import_sandwiches.append(program_file_string[4:])
            location = len(program_file_string)
        from_sandwiches.append(program_file_string[4:location])
    found = 0
    while found != -1:
        found = program_file_string.find("\nfrom", location)
        if found != -1:
            location = program_file_string.find("\n", found + 5)
            if location != -1:
                from_sandwiches.append(program_file_string[found + 5:location])
            else:
                from_sandwiches.append(program_file_string[found + 5:])
                found = -1       
    the_imports = []
    for item in import_sandwiches:
        found, location = 0, 0
        while found != -1:
            found = item.find(",", location)
            if found != -1:
                as_found = item.find(" as ", location, found)
                if as_found != -1:
                    the_imports.append(remove_all_spaces(item[location:as_found]))
                else:
                    the_imports.append(remove_all_spaces(item[location:found]))
                location = found + 1
            else:
                as_found = item.find(" as ", location)
                if as_found != -1:
                    the_imports.append(remove_all_spaces(item[location:as_found]))
                else:
                    the_imports.append(remove_all_spaces(item[location:]))
    for item in from_sandwiches:
        found = item.find("import")
        if found != -1:
            the_imports.append(remove_all_spaces(item[0:found]))      
    length = len(the_imports)
    for i in range(0, length):
        found = the_imports[i].find(".")
        if found != -1:
            the_imports[i] = the_imports[i][0:found]

    the_imports = list(set(the_imports))
    the_imports.sort()    
    return the_imports

def partition_a_program_string(program_string):
    start_program = []
    end_program = []
    look_for_string = "############ START OF SECTOR 0 (IGNORE THIS COMMENT)"
    start_program.append(program_string.find(look_for_string))
    look_for_string = "############ END OF SECTOR 0 (IGNORE THIS COMMENT)"
    end_program.append(program_string.find(look_for_string, start_program[0]))
    end_program[0] = end_program[0] + len(look_for_string) - 1
    look_for_string = "############ START OF SECTOR 1 (IGNORE THIS COMMENT)"
    start_program.append(program_string.find(look_for_string, end_program[0]))
    look_for_string = "############ END OF SECTOR 1 (IGNORE THIS COMMENT)"
    end_program.append(program_string.find(look_for_string, start_program[1]))
    end_program[1] = end_program[1] + len(look_for_string) - 1
    look_for_string = "############ START OF SECTOR 2 (IGNORE THIS COMMENT)"
    start_program.append(program_string.find(look_for_string, end_program[1]))
    look_for_string = "############ END OF SECTOR 2 (IGNORE THIS COMMENT)"
    end_program.append(program_string.find(look_for_string, start_program[2]))
    end_program[2] = end_program[2] + len(look_for_string) - 1
    look_for_string = "############ START OF SECTOR 3 (IGNORE THIS COMMENT)"
    start_program.append(program_string.find(look_for_string, end_program[2]))
    look_for_string = "############ END OF SECTOR 3 (IGNORE THIS COMMENT)"
    end_program.append(program_string.find(look_for_string, start_program[3]))
    end_program[3] = end_program[3] + len(look_for_string) - 1
    look_for_string = "############ START OF SECTOR 4 (IGNORE THIS COMMENT)"
    start_program.append(program_string.find(look_for_string, end_program[3]))
    look_for_string = "############ END OF SECTOR 4 (IGNORE THIS COMMENT)"
    end_program.append(program_string.find(look_for_string, start_program[4]))
    end_program[4] = end_program[4] + len(look_for_string) - 1
    look_for_string = "############ START OF SECTOR 5 (IGNORE THIS COMMENT)"
    start_program.append(program_string.find(look_for_string, end_program[4]))
    look_for_string = "############ END OF SECTOR 5 (IGNORE THIS COMMENT)"
    end_program.append(program_string.find(look_for_string, start_program[5]))
    end_program[5] = end_program[5] + len(look_for_string) - 1
    look_for_string = "############ START OF SECTOR 6 (IGNORE THIS COMMENT)"
    start_program.append(program_string.find(look_for_string, end_program[5]))
    look_for_string = "############ END OF SECTOR 6 (IGNORE THIS COMMENT)"
    end_program.append(program_string.find(look_for_string, start_program[6]))
    end_program[6] = end_program[6] + len(look_for_string) - 1
    look_for_string = "############ START OF SECTOR 7 (IGNORE THIS COMMENT)"
    start_program.append(program_string.find(look_for_string, end_program[6]))
    look_for_string = "############ END OF SECTOR 7 (IGNORE THIS COMMENT)"
    end_program.append(program_string.find(look_for_string, start_program[7]))
    end_program[7] = end_program[7] + len(look_for_string) - 1
    look_for_string = "############ START OF SECTOR 8 (IGNORE THIS COMMENT)"
    start_program.append(program_string.find(look_for_string, end_program[7]))
    look_for_string = "############ END OF SECTOR 8 (IGNORE THIS COMMENT)"
    end_program.append(program_string.find(look_for_string, start_program[8]))
    end_program[8] = end_program[8] + len(look_for_string) - 1
    look_for_string = "############ START OF SECTOR 9 (IGNORE THIS COMMENT)"
    start_program.append(program_string.find(look_for_string, end_program[8]))
    look_for_string = "############ END OF SECTOR 9 (IGNORE THIS COMMENT)"
    end_program.append(program_string.find(look_for_string, start_program[9]))
    end_program[9] = end_program[9] + len(look_for_string) - 1
    look_for_string = "############ START OF SECTOR 10 (IGNORE THIS COMMENT)"
    start_program.append(program_string.find(look_for_string, end_program[8]))
    look_for_string = "############ END OF SECTOR 10 (IGNORE THIS COMMENT)"
    end_program.append(program_string.find(look_for_string, start_program[9]))
    end_program[10] = end_program[10] + len(look_for_string) - 1
    return start_program, end_program

def has_it_been_touched(program_file):
    touch_flag = False
    sector_flag = []
    skeleton_flag = False
    path_to_skeleton = os.path.join("..", "skeleton.py")
    if not os.path.isfile(path_to_skeleton):
        skeleton_flag = True
        return touch_flag, skeleton_flag, sector_flag
    
    ord_range = [[0, 127]]
    skeleton_file_string = read_file_into_string(path_to_skeleton, ord_range)
    program_file_string = read_file_into_string(program_file, ord_range)
    
    start_skeleton, end_skeleton = partition_a_program_string(skeleton_file_string)
    start_program, end_program = partition_a_program_string(program_file_string)

    num_partitions = len(start_skeleton)
    for i in range(0, num_partitions):
        if start_program[i] == -1 or end_program[i] == -1:
            touch_flag = True
            sector_flag.append(i)
        elif skeleton_file_string[start_skeleton[i] : end_skeleton[i]] != program_file_string[start_program[i] : end_program[i]]:
            touch_flag = True
            sector_flag.append(i)
    return touch_flag, skeleton_flag, sector_flag
    
def collect_data_from_program_file(program_file, file_list):
    batch = "collect_data_from_program_file"
    flag = [(batch, 0)]
    program_file_data = ["", "", "", [[], []], [False, []]]
    if not program_file in file_list:
        flag.append((batch, 1))
        program_file_data[0] = "N"
        return program_file_data, flag
    else:
        program_file_data[0] = "Y"
    ord_range = non_control_ord_range()
    program_file_string = read_file_into_string(program_file, ord_range)
    program_file_string = remove_all_spaces(program_file_string)
    tag_pairs = [["my_user_name=\"", "\""], ["algorithm_code=\"", "\""]]
    start_location = 0
    values, new_location, sub_flag = strings_between_tag_pairs(program_file_string, tag_pairs, start_location)
    if sub_flag[1] > 0:
        flag.append((batch, 2))
        return program_file_data, flag
    program_file_data[1] = values[0]
    program_file_data[2] = values[1]
    program_file_data[3] = [get_the_modules_imported(program_file), []]
    touch_flag, skeleton_flag, sector_flag = has_it_been_touched(program_file)
    program_file_data[4][0] = touch_flag
    length = len(sector_flag)
    for i in range(0, length):
        program_file_data[4][1].append(sector_flag[i])
    if skeleton_flag == True:
        flag.append((batch, 3))
    return program_file_data, flag

def validate_a_program(user_name, program_file_data, code_dictionary, legal_modules):
    batch = "validate_a_program"
    flag = [(batch, 0)]
    if program_file_data[1] != user_name:
        flag.append((batch, 1))
    if not program_file_data[2] in code_dictionary:
        flag.append((batch, 2))
    bad_module = False
    for item in program_file_data[3][0]:
        if not item in legal_modules:
            program_file_data[3][0].remove(item)
            program_file_data[3][1].append(item)
            bad_module = True
    if bad_module == True:
        flag.append((batch, 3))
    return program_file_data, flag

def up_to_next_comma(the_string, start_location):
    batch = "up_to_next_comma"
    flag = (batch, 0)
    found_comma = the_string.find(",", start_location)
    if found_comma == -1:
        flag = (batch, 1)
        return "", -1, flag
    sandwich = the_string[start_location:found_comma]
    return sandwich, found_comma + 1, flag 

def collect_data_from_tour_file(tour_file, file_list):
    batch = "collect_data_from_tour_file"
    flag = [(batch, 0)]
    tour_file_data = ["", "", "", "", 0, 0, [], "-1", "-1"]
    if not tour_file in file_list:
        flag.append((batch, 1))
        tour_file_data[0] = "N"
        return tour_file_data, flag
    else:
        tour_file_data[0] = "Y"
    ord_range = non_control_ord_range()
    tour_file_string = read_file_into_string(tour_file, ord_range)
    tour_file_string = remove_all_spaces(tour_file_string)
    tag_pairs = [["USER=", ","], ["ALGORITHMCODE=", ","], ["NAMEOFCITY-FILE=", ","],
                 ["SIZE=", ","], ["TOURLENGTH=", ","]]
    start_location = 0
    values, new_location, sub_flag = strings_between_tag_pairs(tour_file_string, tag_pairs, start_location)
    if sub_flag[1] > 0:
        flag.append((batch, 2))
        return tour_file_data, flag
    start_bracket = values[0].find("(", start_location)
    if start_bracket != -1:
        values[0] = values[0][0:start_bracket]
    tour_file_data[1] = values[0]
    tour_file_data[2] = values[1]
    tour_file_data[3] = values[2]
    tour_file_data[4] = integerize(values[3])
    tour_file_data[5] = integerize(values[4])
    start_note_tag = tour_file_string.find("NOTE=", new_location)
    if start_note_tag == -1:
        flag.append((batch, 2))
        return tour_file_data, flag
    ok, count, the_tour = True, 0, []
    while (new_location < start_note_tag) and (ok == True):
        sandwich, new_location, sub_flag = up_to_next_comma(tour_file_string, new_location)
        if (sub_flag[1] > 0) or (new_location > start_note_tag):
            flag.append((batch, 2))
            ok = False
        else:
            the_tour.append(integerize(sandwich))
            count = count + 1
    if len(flag) != 1:
        return tour_file_data, flag
    counted_tour_cities = len(the_tour)
    if counted_tour_cities != tour_file_data[4]:
        flag.append((batch, 3))
    else:
        found_zero, i = False, 0
        while i < counted_tour_cities and found_zero == False:
            if the_tour[i] == 0:
                zero_location = i
                found_zero = True
            i = i + 1
        if found_zero == True:
            if zero_location != 0:
                before_value = the_tour[zero_location - 1]
            else:
                before_value = the_tour[counted_tour_cities - 1]
            if zero_location != counted_tour_cities - 1:
                after_value = the_tour[zero_location + 1]
            else:
                after_value = the_tour[0]
            if after_value >= before_value: 
                write_right = True
            else:
                write_right = False
            copy_the_tour = the_tour[:]
            for i in range(0,counted_tour_cities):
                if (zero_location + i) >= counted_tour_cities and write_right == True:
                    j = zero_location + i - counted_tour_cities
                elif (zero_location + i) < counted_tour_cities and write_right == True:
                    j = zero_location + i
                elif (zero_location - i) >= 0 and write_right == False:
                    j = zero_location - i
                elif (zero_location - i) < 0 and write_right == False:
                    j = counted_tour_cities + zero_location - i
                the_tour[i] = copy_the_tour[j]
    tour_file_data[6] = the_tour
    run_time_tag = tour_file_string.find("RUN-TIME=", start_note_tag)
    if run_time_tag == -1:
        flag.append((batch, 2))                     # there is no tag "RUN-TIME =" - fatal error)
        return tour_file_data, flag
    tag_pair = ["RUN-TIME=", "seconds."]
    sandwich, end_location, sub_flag = between_tag_pair(tour_file_string, tag_pair, run_time_tag)
    if sub_flag[1] != 0:
        flag.append((batch, 2))                     # there is no tag "seconds." after "RUN-TIME="
    else:
        tour_file_data[7] = sandwich                # run-time found (as a string)
    certificate_tag = tour_file_string.find("CERTIFICATE=", run_time_tag)
    if certificate_tag == -1:
        flag.append((batch, 2))                     # there is no tag "CERTIFICATE =" - fatal error)
        return tour_file_data, flag
    tag_pair = ["CERTIFICATE=", "."]
    sandwich, end_location, sub_flag = between_tag_pair(tour_file_string, tag_pair, certificate_tag)
    if sub_flag[1] != 0:
        flag.append((batch, 2))                     # there is no tag "\n" after "CERTIFICATE ="
        return tour_file_data, flag
    else:
        try:
            cert_as_a_number = int(sandwich)
        except:
            flag.append((batch, 2))                 # the certificate is not integral
            return tour_file_data, flag
        tour_file_data[8] = cert_as_a_number        # the certificate (as an integer)    
    return tour_file_data, flag

def validate_a_tour(user_name, tour_file, tour_file_data, city_dictionary, code_dictionary,
                    programs_to_submit, prefix_dictionary, student_record):
    batch = "validate_a_tour"
    flag = [(batch, 0)]
    tour_data = []
    for item in tour_file_data:
        tour_data.append(item)
    tour_data.append(0)
    if tour_file_data[1] != user_name:
        flag.append((batch, 1))
    if not tour_file_data[2] in code_dictionary:
        flag.append((batch, 2))
    if tour_file[len(tour_file) - len(tour_file_data[3]):] != tour_file_data[3]:
        flag.append((batch, 11))
    underscore = tour_file.find("_")
    tour_prefix = tour_file[0:underscore]
    tour_cluster = prefix_dictionary[tour_prefix]
    if student_record[tour_cluster[0]][2] == "N":
        flag.append((batch, 3))
    if student_record[tour_cluster[0]][0][2] != tour_file_data[2]:
        flag.append((batch, 4))
    if not tour_file_data[3] in city_dictionary:
        flag.append((batch, 5))
        return tour_data, flag
    else:
        if city_dictionary[tour_file_data[3]][0] != tour_file_data[4]:
            flag.append((batch, 6))
            return tour_data, flag
    real_tour_size = len(tour_file_data[6])
    if real_tour_size != tour_file_data[4]:
        flag.append((batch, 7))
        return tour_data, flag
    duplicate, bad_city = False, False
    for i in range(0, tour_file_data[4]):
        if tour_file_data[6][i] < 0 or tour_file_data[6][i] > tour_file_data[4] - 1:
            bad_city = True
        for j in range(i + 1, tour_file_data[4]):
            if tour_file_data[6][i] == tour_file_data[6][j]:
                duplicate = True
    if duplicate == True:
        flag.append((batch, 8))
    if bad_city  == True:
        flag.append((batch, 9))
    if duplicate == False and bad_city == False:
        check_tour_length = 0
        for i in range(tour_file_data[4] - 1):
            check_tour_length = check_tour_length + \
                        city_dictionary[tour_file_data[3]][1][tour_file_data[6][i]][tour_file_data[6][i + 1]]
        check_tour_length = check_tour_length + \
                        city_dictionary[tour_file_data[3]][1][tour_file_data[6][tour_file_data[4] - 1]][tour_file_data[6][0]]
        if check_tour_length != tour_file_data[5]:
            flag.append((batch, 10))
        tour_data[8] = check_tour_length
    if tour_data[7] == -1:
        flag.append((batch, 12))
    return tour_data, flag

def non_control_ord_range():
    ord_range = []
    first_range = [32,127]
    ord_range.append(first_range)
    return ord_range

def read_in_algorithm_codes_and_tariffs(alg_codes_file):
    batch = "read_in_algorithm_codes_and_tariffs"
    flag = (batch, 0)
    code_dictionary = {}
    tariff_dictionary = {}
    data_file_list = os.listdir()
    if not alg_codes_file in data_file_list:
        flag = (batch, 1)
        return code_dictionary, tariff_dictionary, flag
    ord_range = non_control_ord_range()
    file_string = read_file_into_string(alg_codes_file, ord_range)
    start_location = 0
    EOF = False
    code_list = []
    while EOF == False:
        sandwich, new_location, sub_flag = up_to_next_comma(file_string, start_location)
        if sub_flag[1] > 0:
            EOF = True
            code_list.append(file_string[start_location:])
        else:
            code_list.append(sandwich)
            start_location = new_location
    length = len(code_list)
    if length % 3 != 0:
        flag = (batch, 2)
    elif length == 0:
        flag = (batch, 3)
    else:
        third_length = int(length/3)
        for i in range(third_length):
            code_list[3 * i + 1] = code_list[3 * i + 1].lstrip()
            code_list[3 * i + 1] = code_list[3 * i + 1].rstrip()
            if len(code_list[3 * i]) != 2:
                flag = (batch, 4)
            elif code_list[3 * i + 1] == "":
                flag = (batch, 5)
            elif integerize(code_list[3 * i + 2]) < 0 or integerize(code_list[3 * i + 2]) > 10:
                flag =(batch, 6)
            else:
                code_dictionary[code_list[3 * i]] = code_list[3 * i + 1]
                tariff_dictionary[code_list[3 * i]] = integerize(code_list[3 * i + 2])
    return code_dictionary, tariff_dictionary, flag

def build_student_feedback_file(name_of_file, user_name, student_record, programs_to_submit, programs_prefix, tour_files_to_submit,
                                additional_items_to_submit, extraneous_material, code_dictionary, tariff_dictionary, flag_dictionary, the_time):
    f = open(name_of_file, "w")
    f.write("Feedback for user-ID " + user_name + " at " + the_time + "\n\n")
    f.write("Throughout this validation, as many error messages as possible are returned in order to help you ")
    f.write("understand what might have gone wrong. However, note that sometimes a single error might lead to ")
    f.write("early termination of the validation process so that fixing this error results in more, as yet ")
    f.write("unseen, errors. So, the list of error messages might not be exhaustive but it's the best I can do!\n")
    f.write("\n")
    f.write("The first part of this feedback is validation of the program files that you submitted, in terms ")
    f.write("of the key information they need to contain. At this stage, the programs are not executed; that ")
    f.write("will follow later. Please note that for any program cluster, if any of the following are true ")
    f.write("then the program cluster is INVALID and neither it nor the tours it produces will secure any marks:\n")
    f.write(" - the basic program does not exist\n")
    f.write(" - the basic program exists but its user-name mis-matches the definitive user-name\n")
    f.write(" - the basic program exists but its algorithm code is illegal\n")
    f.write(" - the basic program exists but it imports an illegal module\n")
    f.write(" - the enhanced program exists but its user-name mismatches the definitive user-name\n")
    f.write(" - the enhanced program exists but its algorithm code mis-matches with that of the basic program\n")
    f.write(" - the enhanced program exists but it imports an illegal module.\n")
    f.write("Also, if you have two valid program clusters but they have the same algorithm code then both ")
    f.write("clusters are invalid. (Of course, invalidity can be avoided if you check your programs using this ")
    f.write("program prior to submission!)\n")
    f.write("\n")
    f.write("By the way, if you don't bother to validate prior to submission and so don't include the validation ")
    f.write("feedback in your submission then I will do absolutely nothing to fix any errors in your submission, ")
    f.write("no matter how trivial they are.\n")
    f.write("\n")
    f.write("#####  Program submission\n")
    num_clusters = len(programs_to_submit)
    for i in range(0,num_clusters):
        f.write("#####   * program cluster {0}:\n".format(programs_prefix[i]))
        for item in programs_to_submit[i]:
            f.write("#####      - {0}: ".format(item))
            if len(student_record[item][1]) == 1:   # student_record[basic] = [[exists, prog-user-name, prog-alg-code, [[good modules used],[bad modules used]], 
                                                    #                          [T/F for whether touched, [list of touched sectors]]], [list of flags], overall-validity]
                                                    # student_record[enhanced] = [[exists, prog-user-name, prog-alg-code, [[good modules used],[bad modules used]], 
                                                    #                             [T/F for whether touched, [list of touched sectors]]], [list of flags], matched_code]
                f.write("{0} ({1}, tariff {2})\n".format(flag_dictionary[student_record[item][1][0][0]][student_record[item][1][0][1]], \
                                                         code_dictionary[student_record[item][0][2]], tariff_dictionary[student_record[item][0][2]]))
            else:
                if student_record[item][0][2] == "":
                    f.write("there were validation errors (algorithm code ?)\n")
                else:
                    f.write("there were validation errors (algorithm code {0})\n".format(student_record[item][0][2]))
                length = len(student_record[item][1])   # number of individual flags, the first of which is (batch, 0)
                for j in range(1, length):
                    f.write("#####         {0}\n".format(flag_dictionary[student_record[item][1][j][0]][student_record[item][1][j][1]]))
                    if student_record[item][1][j][0] == "validate_a_program" and student_record[item][1][j][1] == 3:
                        f.write("#####             bad modules used:")
                        length_bad_codes = len(student_record[item][0][3][1])
                        for k in range(0, length_bad_codes):
                            f.write(" {0}".format(student_record[item][0][3][1][k]))
                            if k < length_bad_codes - 1:
                                f.write(", ")
                            else:
                                f.write("\n")
            if student_record[item][0][4][0] == True:
                f.write("*** Warning: you appear to have altered the core skeleton code even though I told you ")
                f.write("not to! So, your code might not run for me. I would fix this if I were you. ")
                f.write("Discrepancies appear in sectors")
                num_bad_sectors = len(student_record[item][0][4][1])
                for j in range(0, num_bad_sectors):
                    f.write(" {0}".format(student_record[item][0][4][1][j]))
                    if j == num_bad_sectors - 1:
                        f.write(".\n")
                    elif j == num_bad_sectors - 2:
                        f.write(" and")
                    else:
                        f.write(",")
        if student_record[programs_to_submit[i][0]][2] == "N":
            f.write("#####     *** MAJOR ERROR: THIS PROGRAM CLUSTER IS INVALID!\n")
    f.write("\n")
    f.write("The next part of this feedback is validation of the tour files that you submitted. Each has been ")
    f.write("validated and the outcome is described below. If any tour has an associated error message then it ")
    f.write("is deemed to be invalid and it will secure no marks. Remember: as stated above, any tours arising ")
    f.write("from an invalid program cluster will not secure any marks (irrespective of whether they are ")
    f.write("actually legal tours or not). The tour lengths of successfully validated tours given below go to ")
    f.write("form your tour-quality mark.\n")
    f.write("\n")
    f.write("#####  Tour file submission\n")
    num_batches = len(tour_files_to_submit)
    for i in range(0,num_batches):
        f.write("#####   * program cluster {0}:\n".format(programs_prefix[i]))
        for item in tour_files_to_submit[i]:
            f.write("#####      - {0}: ".format(item))
            if len(student_record[item][1]) == 1:   # student_record[tour-file] = [[exists, tour-user-name, tour-alg-code,
                                                    # tour-city-file, tour-size, tour-length, tour, run-time, real-tour-length], [list of flags]]
                f.write("valid tour of length {0} ({1}, run-time {2} seconds)\n".format(student_record[item][0][8], code_dictionary[student_record[item][0][2]], student_record[item][0][7]))
            else:
                f.write("there were validation errors:\n")
                length = len(student_record[item][1])   # number of individual flags, the first of which is (batch, 0)
                for j in range(1, length):
                    f.write("#####        {0}\n".format(flag_dictionary[student_record[item][1][j][0]][student_record[item][1][j][1]]))                       
                if student_record[item][0][5] == student_record[item][0][8] and student_record[item][0][8] > 0:
                    f.write("#####        (as it happens, you have a legal tour of length {0})\n".format(student_record[item][0][8]))
    f.write("\n")
    f.write("The next part of this feedback states whether the proforma and the validation feedback were submitted.\n")
    f.write("\n")
    f.write("#####  Additional items submission\n")
    length = len(additional_items_to_submit)
    for i in range(0, length):
        f.write("#####   * {0}: ".format(additional_items_to_submit[i]))
        if student_record["additional_items"][i] == "Y":
            f.write("submitted\n")
        else:
            f.write("not submitted\n")
    f.write("\n")
    f.write("Of course, the validation feedback file might be flagged as 'not submitted' as it should be this file!\n")
    length_extraneous = len(extraneous_material)
    if length_extraneous > 0:
        f.write("\n")
        f.write("By the way, you have extraneous material in your folder '{0}' that should be removed.\n".format(user_name))
        f.write("\n")
        f.write("#####  Extraneous material:\n")
        f.write("#####   * ")
        for i in range(0, length_extraneous):
            if i < length_extraneous - 1:
                f.write(extraneous_material[i] + "; ")
            else:
                f.write(extraneous_material[i] + ".\n")
    f.close()
    return

def build_distance_matrix(number_of_cities, distances, city_format):
    dist_matrix = []
    i = 0
    if city_format == "full":
        for j in range(number_of_cities):
            row = []
            for k in range(number_of_cities):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    elif city_format == "upper_tri":
        for j in range(number_of_cities):
            row = []
            for k in range(j):
                row.append(0)
            for k in range(number_of_cities - j):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    else:
        for j in range(number_of_cities):
            row = []
            for k in range(j + 1):
                row.append(0)
            for k in range(number_of_cities - (j + 1)):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    if city_format == "upper_tri" or city_format == "strict_upper_tri":
        for i in range(number_of_cities):
            for j in range(number_of_cities):
                if i > j:
                    dist_matrix[i][j] = dist_matrix[j][i]
    return dist_matrix

def convert_to_list_of_int(the_string):
    list_of_integers = []
    location = 0
    length = len(the_string)
    while location < length:
        found_comma = the_string.find(',', location)
        if found_comma == -1:
            location = length
        else:
            list_of_integers.append(integerize(the_string[location:found_comma]))
            location = found_comma + 1
    return list_of_integers

def validate_format_of_city_files(the_folder):
    batch = "validate_format_of_city_files"
    flag = (batch, 0)
    city_dictionary = {}
    city_file_list = []
    if not os.path.exists(the_folder):
        flag = (batch, 1)
        return city_file_list, city_dictionary, flag
    else:
        if not os.path.isdir(the_folder):
            flag = (batch, 2)
            return city_file_list, city_dictionary, flag
    os.chdir(the_folder)
    city_file_list = os.listdir()
    os.chdir("..")
    for item in city_file_list:
        if item[len(item) - 4:len(item)] != ".txt":
            city_file_list.remove(item)
    city_file_list.sort()
    length = len(city_file_list)
    if length == 0:
        flag = (batch, 3)
        return city_file_list, city_dictionary, flag
    for i in range(length):
        length = len(city_file_list[i])
        if city_file_list[i][length - 4:length] != ".txt":
            flag = (batch, 4)
        elif "_" in city_file_list[i]:
            flag = (batch, 5)
    if flag[1] > 0:
        return city_file_list, city_dictionary, flag
    ord_range = non_control_ord_range()
    for city_file in city_file_list:
        number_of_cities, dist_matrix = 0, []
        os.chdir(the_folder)
        city_file_string = read_file_into_string(city_file, ord_range)
        city_file_string = remove_all_spaces(city_file_string)
        os.chdir("..")
        tag_pair = ["SIZE=", ","]
        start_location = 0
        sandwich, new_location, flag = between_tag_pair(city_file_string, tag_pair, start_location)
        if flag[1] > 0:
            flag = (batch, 6)
        if flag[1] == 0:
            number_of_cities = integerize(sandwich)
            if number_of_cities < 4:
                flag = (batch, 7)
        if flag[1] == 0:
            the_tag = "NOTE="
            start_note_tag = city_file_string.find(the_tag, new_location)
            if start_note_tag == -1:
                flag = (batch, 8)
        if flag[1] == 0:
            distances = convert_to_list_of_int(city_file_string[new_location:start_note_tag])
            counted_distances = len(distances)
            if counted_distances == number_of_cities * number_of_cities:
                city_format = "full"
            elif counted_distances == (number_of_cities * (number_of_cities + 1))/2:
                city_format = "upper_tri"
            elif counted_distances == (number_of_cities * (number_of_cities - 1))/2:
                city_format = "strict_upper_tri"
            else:
                flag = (batch, 10)
        if flag[1] == 0:
            dist_matrix = build_distance_matrix(number_of_cities, distances, city_format)
        city_dictionary[city_file] = [number_of_cities, dist_matrix]
    return city_file_list, city_dictionary, flag

##### main program #####

city_file_list, city_dictionary, flag = validate_format_of_city_files(city_file_folder)

if flag[1] != 0:
    print(flag_dictionary[flag[0]][flag[1]])
    sys.exit()

code_dictionary, tariff_dictionary, flag = read_in_algorithm_codes_and_tariffs(alg_codes_file)

if flag[1] != 0:
    print("*** fatal error: there is something wrong with " + alg_codes_file)
    sys.exit()

if not os.path.isdir(user_name):
    print("*** fatal error: the folder " + user_name + " does not exist.")
    sys.exit()
    
student_record = {}

os.chdir(user_name)

file_list = os.listdir()

extraneous_material = []
for file in file_list:
    if not file in programs_to_submit[0] and not file in programs_to_submit[1]:
        if not file in tour_files_to_submit[0] and not file in tour_files_to_submit[1]:
            if not file in additional_items_to_submit:
                extraneous_material.append(file)

batch = "validating student programs"
for program_cluster in programs_to_submit:
    program_file_data, flag = collect_data_from_program_file(program_cluster[0], file_list)
    if len(flag) == 1:
        program_file_data, flag = validate_a_program(user_name, program_file_data, code_dictionary, legal_modules)
    student_record[program_cluster[0]] = [program_file_data, flag]
    if len(program_cluster) == 2:
        program_file_data, flag = collect_data_from_program_file(program_cluster[1], file_list)
        if len(flag) == 1:
            program_file_data, flag = validate_a_program(user_name, program_file_data, code_dictionary, legal_modules)
        student_record[program_cluster[1]] = [program_file_data, flag]
        matched_codes = "Y"
        if student_record[program_cluster[0]][0][0] == "Y" and student_record[program_cluster[1]][0][0] == "Y":
            if student_record[program_cluster[0]][0][2] != student_record[program_cluster[1]][0][2]:
                matched_codes = "N"
                student_record[program_cluster[1]][1].append((batch, 1))
        student_record[program_cluster[1]].append(matched_codes)
    overall_validity = "Y"
    if len(student_record[program_cluster[0]][1]) > 1:
        overall_validity = "N"
    elif len(program_cluster) == 2:
        if student_record[program_cluster[1]][0][0] == "Y":
            if len(student_record[program_cluster[1]][1]) > 1:
                overall_validity = "N"
    student_record[program_cluster[0]].append(overall_validity)
list_of_bad_clusters = []
length = len(programs_to_submit)                
for i in range(0, length):                      
    for j in range(i + 1, length):
        if student_record[programs_to_submit[i][0]][2] == "Y" and student_record[programs_to_submit[j][0]][2] == "Y" \
        and student_record[programs_to_submit[i][0]][0][2] == student_record[programs_to_submit[j][0]][0][2]:
            list_of_bad_clusters.append(programs_to_submit[i])
            list_of_bad_clusters.append(programs_to_submit[j])
for item in list_of_bad_clusters:
    student_record[item[0]][2] = "N"
    student_record[item[0]][1].append((batch, 2))
    
for tour_file_batch in tour_files_to_submit:
    for tour_file in tour_file_batch:
        tour_file_data, flag = collect_data_from_tour_file(tour_file, file_list)
        if len(flag) == 1:
            tour_file_data, flag = validate_a_tour(user_name, tour_file, tour_file_data, city_dictionary,
                                                    code_dictionary, programs_to_submit, prefix_dictionary, student_record)
        else:
            tour_file_data.append(0)
        student_record[tour_file] = [tour_file_data, flag]
        
items_submitted = []
for item in additional_items_to_submit:
    if item in file_list:
        items_submitted.append("Y")
    else:
        items_submitted.append("N")
student_record["additional_items"] = items_submitted

os.chdir("..")

local_time = time.asctime(time.localtime(time.time()))
the_time = local_time[4:19]

name_of_file = "AISearchValidationFeedback.txt"
        
build_student_feedback_file(name_of_file, user_name, student_record, programs_to_submit, programs_prefix, tour_files_to_submit,
                            additional_items_to_submit, extraneous_material, code_dictionary, tariff_dictionary, flag_dictionary, the_time)
    

    



















