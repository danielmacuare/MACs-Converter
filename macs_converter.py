#!/usr/bin/env python
import re
#from pprint import pprint
import argparse
import csv


# python mac_formatter.py --list FF253456789AB EX:2///34/56789/AB aa-23-45-67-89-AB --delimiter '.'
# python mac_formatter.py --file macs.csv --delimiter '.'

#################################### DEFS  ##############################################
def get_invalid_macs(macs_list):
    invalid_macs = []
    invalid_list = []
    blank_lines = []
    line_id = 0

    for original_macs in macs_list:
        line_id += 1
        if original_macs == '':
            blank_lines.append(line_id)
            invalid_macs.append(original_macs)
            continue
        if len(original_macs) < 40:
            new_mac = re.sub(r'[^a-fA-F0-9]', '', original_macs)
            if len(new_mac) != 12:
                invalid_macs.append(original_macs)

    #print(invalid_macs)
    #print(blank_lines)
    return invalid_macs, blank_lines

def rem_invalid_macs(macs_list, invalid_macs):
    valid_macs = [x for x in macs_list if x not in invalid_macs]
    #print(valid_macs)
    return valid_macs

'''
# Above is the same than
   for x in macs_list:
       if x not in invalid_macs:
           valid_macs.append(x)
'''

def no_delimiter_macs(valid_macs):
    no_sep_macs = {}
    for original_mac in valid_macs:
        no_sep_mac = re.sub(r'[^a-fA-F0-9]', '', original_mac)
        no_sep_macs.update({original_mac: no_sep_mac})
    #print(no_sep_macs)
    return no_sep_macs


def add_delimiter(no_sep_macs, delimiter):
    separated_macs = {}
    #print(delimiter)
    if delimiter == ':' or delimiter == '-':
        for original_mac, no_sep_mac in no_sep_macs.items():
            temp_mac = no_sep_mac
            formatted_mac = delimiter.join(temp_mac[i:i+2] for i in range(0, 12, 2))
            separated_macs.update({original_mac: formatted_mac.upper()})
    elif delimiter == '.':
        for original_mac, no_sep_mac in no_sep_macs.items():
            temp_mac = no_sep_mac
            formatted_mac = delimiter.join(temp_mac[i:i+3] for i in range(0, 12, 3))
            separated_macs.update({original_mac: formatted_mac.upper()})
    else:
        raise Exception('delimiter should be one of [:-.]. You passed: {}'.format(delimiter))

   # pprint(separated_macs)
    return(separated_macs)


##################################### END DEFS #########################################
#Parsing arguments
parser = argparse.ArgumentParser(description=''''Process a list or a file containing MACs and returns a 
    list of valid(formatted) MACs and a list of invalid_MACs''')

# Creating mutually exclusive args --list or --file. One of them must be passed to the script.
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--list', metavar='MACS', type=str, nargs='+',
                    help='a list of MAC strings separated by whitespaces [MAC1 MAC2 MAC3 ...]')

group.add_argument('--file', metavar='FILENAME', type=str, help='File with only MAC addreses',)

# Parsing normal arguments
parser.add_argument('--delimiter', '-d', metavar='[-.:]', type=str, default=':',
                    help='Default is colon ":" - Defines the output notation of the MACS [: - .]')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

args = parser.parse_args()
filename= str(args.file)


# Defining the input of the macs_list
if args.list:
    macs_list = args.list
elif args.file:
    with open(filename, 'r') as f:
        read_file = f.read()
    macs_list = read_file.splitlines()

delim = args.delimiter

#print(args)
#print(args.file)
#print(args.list)
#print(macs_list)

#########################FUNCTION CALLS ####################
invalid_macs, blank_lines = get_invalid_macs(macs_list)
valid_macs = (rem_invalid_macs(macs_list, invalid_macs))
no_sep_macs = no_delimiter_macs(valid_macs)
formatted_macs = add_delimiter(no_sep_macs, delimiter=delim)


if formatted_macs:
    print(' - The following is a list of formatted MACs:')
    for elements in formatted_macs.values():
        print(elements)
    print('')
    if not invalid_macs:
        print('- All the MACs were correctly processed')
else:
    print('- No MACs were formatted - Check for invalid MACs')

if invalid_macs:
    print('')
    print('- The following MACs are invalid:')
    for macs in invalid_macs:
        if macs:
            print(macs)
        else:
            continue

# For Debugging - Count blank lines
#print('\n')
#print("- There are {} blank lines in the list:".format(len(blank_lines)))
#for line in blank_lines:
#    print('Blank line - (Line {})'.format(line))
