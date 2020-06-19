import re
import random


def fill_the_column(f, n_f, e, p):
    i = 0
    line_list = []
    tmp_line = ''

    for line in f:
        line_list = []
        tmp_line = ''
        if line[0] == ',' and check_the_line(line) == 'Valid' \
                and i < len(e):
            line_list = line.split(', ')
            line_list[0] = e[i]
            line_list[len(line_list) - 1] = line_list[len(line_list) - 1].replace('\n', '')
            line_list.append(p[i])
            i += 1
        elif line[0] == 'E':
            line = line.replace('\n', ', ')
            line += 'PASSWORD\n'
        if line_list:
            for elem in line_list:
                if line_list.index(elem) == len(line_list) - 1:
                    tmp_line += elem + '\n'
                else:
                    tmp_line += elem + ', '
        else:
            tmp_line = line
        n_f.write(tmp_line)


def check_password(pasw):
    up = False
    low = False
    digit = False
    special = False

    s = pasw
    for c in s:
        if c.isalpha():
            if c.isupper():
                up = True
            else:
                low = True
        elif c.isdigit():
            digit = True
        elif [c for tmp in "! @ # $ % ^ & * ( ) - +".split() if c == tmp]:
            special = True
        else:
            break
    if not all([up, low, digit, special]):
        return "Not valid"
    else:
        return "Valid"


def gen_password(l):
    password = ''
    while len(password) != l:
        password += random.choice('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-+')
    return password


def passw_gen():
    lenght = 12
    passw = ''

    while check_password(passw) != 'Valid':
        passw = gen_password(lenght)
    return (passw)


def passw_arr_gen(len):
    passw_arr = []

    for i in range(len):
        passw_arr.append(passw_gen())
    return passw_arr


def email_gen(list_of_names):
    emails = []
    for i in list_of_names:
        letter = 1
        while i[1] + '.' + i[0][0:letter] + '@company.io' in emails:
            letter += 1
        emails.append(i[1] + '.' + i[0][0:letter] + '@company.io')
    return emails


def check_the_pnumber(pnumber):
    if len(pnumber) == 7 and not re.match(r'(\w)\1{4,}', pnumber):
        return 'Valid'
    else:
        return 'Not valid'


def check_the_line(line):
    line_list = line.split(', ')
    check = 0

    for elem in line_list:
        if elem:
            if elem[0].isdigit():
                if check_the_pnumber(elem) == 'Not valid':
                    continue
            elif not re.match(r'\b[A-Z]\w*', elem) or re.match(r'[A-Z]{2,}', elem):
                continue
            check += 1
    if check < 4:
        return 'Not valid'
    else:
        return 'Valid'


def find_names(file):
    list_names = []

    for line in file:
        if line[0] != ',' or check_the_line(line) == 'Not valid':
            continue
        else:
            name = []
            tmp = ''
            i = 0
            for c in line:
                if i == 3:
                    break
                elif c == ',':
                    if i >= 1:
                        name.append(tmp)
                        tmp = ''
                    i += 1
                elif c.isalpha():
                    tmp += c
            list_names.append(name)
    return list_names


def make_copyf(name):
    spl_sting = re.split(r'\.', name)
    copy_name = spl_sting[0] + '_copy.' + spl_sting[1]
    f = open(name)
    try:
        f_c = open(copy_name, 'x')
    except FileExistsError:
        pass
    else:
        for line in f:
            f_c.write(line)
        f_c.close()
    f.close()


def mainfoo():
    fname = 'task_file.txt'
    names = []
    passwords = []
    emails = []

    make_copyf(fname)
    file = open(fname)
    names = find_names(file)
    emails = email_gen(names)
    passwords = passw_arr_gen(len(names))
    file.close()
    file = open('task_file.txt')
    new_file = open('new_task_file.txt', 'w')
    fill_the_column(file, new_file, emails, passwords)
    file.close()
    new_file.close()
    file = open('task_file.txt', 'w')
    new_file = open('new_task_file.txt')
    for line in new_file:
        if check_the_line(line) == 'Valid':
            file.write(line)
        elif line.split(',')[0] == 'EMAIL':
            file.write(line)
    file.close()
    new_file.close()


mainfoo()
