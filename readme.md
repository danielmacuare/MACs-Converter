
# MACs - Converter

The script will take a list (or a file) of valid and invalid MAC Addresses and will format them in any of the 3 following formats deping on the the delimiter (-d ) being passed:

--delimiter -d Options:

1. Colon ':' is the default delimiter - AA:23:45:67:89:AB
2. Dash '-' - AA-23-45-67-89-AB
3. Dot '.' - AA2.345.678.9AB


## Usage
You can pass a file or a list of MACs from the cli. Next you can see valid examples on how to run the script:
1. Passing a file with MACs:

```
python mac_formatter.py --file macs.txt  
python mac_formatter.py --file macs.txt -d -  
python mac_formatter.py --file macs.txt -d .  
```

2. Passing a list of MACs:

```
python mac_formatter.py --file macs.txt --list AA:23:45:67:89:AB BB:23:45:67:89:AB -d -  
python mac_formatter.py --file macs.txt --list AA:23:45:67:89:AB BB:23:45:67:89:AB -d .  
```

## Getting Started

Clone the repo
```
git clone git@github.com:danielmacuare/MACs-Converter.git
```

### Prerequisites
For debugging (optional)
```
pip install pprint
```
