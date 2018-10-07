#!/usr/bin/env python
import re
import argparse
import logging
from pprint import pprint

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

    logger.debug('\t1 - Function Name: "get_invalid_macs"')
    logger.debug('\t  1.1 - Invalid Macs: {}'.format(invalid_macs))
    logger.debug('\t  1.2 - Blank lines are located in lines/elements: {}\n'.format(blank_lines))
    return invalid_macs, blank_lines

def rem_invalid_macs(macs_list, invalid_macs):
    valid_macs = [x for x in macs_list if x not in invalid_macs]
    logger.debug('\t2 - Function Name: "rem_invalid_macs"')
    logger.debug('\t  2.1 - Valid Macs (That were not removed): {}\n'.format(valid_macs))
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
    logger.debug('\t3 - Function Name: "no_delimiter_macs"')
    logger.debug('\t  3.1 - Dict = original_macs: no_delimiter_macs - {}\n'.format(no_sep_macs))
    return no_sep_macs


def add_delimiter(no_sep_macs, delimiter):
    separated_macs = {}
    logger.debug('\t4 - Function Name: "add_delimiter"')
    logger.debug('\t  4.1 - The delimiter passed is:  "{}"'.format(delimiter))
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

    logger.debug('\t  4.2 - Dict = original_macs: macs_with_delimiter :  "{}"\n'.format(separated_macs))
    return(separated_macs)


##################################### END DEFS #########################################
#Parsing arguments
parser = argparse.ArgumentParser(description='''Process a list or a file containing MACs and returns a \ 
    list of valid(formatted) MACs and a list of invalid_MACs''')

# Creating mutually exclusive args --list or --file. One of them must be passed to the script.
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--list', metavar='MACS', type=str, nargs='+',
                    help='a list of MAC strings separated by whitespaces [MAC1 MAC2 MAC3 ...]')

group.add_argument('--file', metavar='FILENAME', type=str, help='File with only MAC addreses',)

# Parsing normal arguments
parser.add_argument('--delimiter', '-d', metavar='[-.:]', type=str, default=':',
                    help='Default is colon ":" - Defines the output notation of the MACS [: - .]')

# When the --deubg option is used, args.parse will return True because of action='store_true'
parser.add_argument('--debug', default='None', action='store_true',
                    help='This option writes debug statements to ./macs_converte.log')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

args = parser.parse_args()
filename= str(args.file)


# Enabling logging
timestamp = '%d-%m-%Y %H:%M:%S'

# Creates a new logger. If the --debug option is passed logging to a file.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if args.debug == True else logging.INFO)

# Creates a file handler which logs debug events to a file
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    timestamp)

file_handler = logging.FileHandler('macs_converter.log')
file_handler.setFormatter(formatter)

# create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)


# Adds the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Defining the input of the macs_list
if args.list:
    macs_list = args.list
elif args.file:
    with open(filename, 'r') as f:
        read_file = f.read()
    macs_list = read_file.splitlines()

delim = args.delimiter


logger.debug('\t0 - Parameters passed via cli:')
logger.debug('\t  0.1 - args Parameters:  "{}"'.format(args))
logger.debug('\t  0.2 - args.file Parameters:  "{}"'.format(args.file))
logger.debug('\t  0.3 - args.list Parameters:  "{}"'.format(args.list))
logger.debug('\t  0.4 - args.debu Parameters:  "{}"'.format(args.debug))
logger.debug('\t  0.5 - Original mac\'s list passed to "get_invalid_macs()":  "{}"\n'.format(macs_list))

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

# Debugs - Showing blank lines and line numbers. 
blanks_number = len(blank_lines) 
logger.debug('\t5 - There are "{}" blank lines in the list/file passed:'.format(blanks_number))
for index, line in enumerate(blank_lines):
    logger.debug('\t  5.{} Blank line - (Line {})'.format(index + 1, line))
logger.debug('\n')
