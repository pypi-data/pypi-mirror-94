![Test Python package](https://github.com/Pytlicek/sheet2dict/workflows/Test%20Python%20package/badge.svg) [![codecov](https://codecov.io/gh/Pytlicek/sheet2dict/branch/main/graph/badge.svg?token=JL4BOX947I)](https://codecov.io/gh/Pytlicek/sheet2dict) ![Upload Python Package to PyPI](https://github.com/Pytlicek/sheet2dict/workflows/Upload%20Python%20Package%20to%20PyPI/badge.svg) ![PythonVersions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue) [![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# sheet2dict
A simple XLSX/CSV to dictionary converter.  

## Installing
To install the package from pip, first run:
```bash
python3 -m pip install --no-cache-dir sheet2dict
```

Required pip packages for sheet2doc: csv, openpyxl

<p align="center"><img src="/img/sheet2dict.gif?raw=true"/></p>

## Usage
This library has 2 main features: reading a spreadsheet files and converting them to array of python dictionaries.  

### - XLSX
Use `xlsx_to_dict()` method  when converting form spreadsheets.  
Supported file formats for spreadsheets are: .xlsx,.xlsm,.xltx,.xltm  

```python3
# Import the library
from sheet2dict import Worksheet

# Create an object
ws = Worksheet()

# Convert 
ws.xlsx_to_dict(path='inventory.xlsx')

# object.headers returns first row with the data in a spreadsheet 
print(ws.headers)

# object.sheet_items returns converted rows as dictionaries in the array 
print(ws.sheet_items)

```

You can parse data when worksheet is an object

```python3
# Import the library
from sheet2dict import Worksheet

# Example: read spreadsheet as object
path = 'inventory.xlsx'
xlsx_file = open(path, 'rb')
xlsx_file = BytesIO(xlsx_file.read())

# Parse spreadsheet from object
ws = Worksheet()
ws.xlsx_to_dict(path=xlsx_file)
print(ws.headers)

```

### - CSV
Use `csv_to_dict()` method  when converting form csv.  
CSV is a format with many variations, better handle encodings and delimiters on user side and not within module itself.

```python3
# Import the library
from sheet2dict import Worksheet

# Create an object
ws = Worksheet()

# Read CSV file
csv_file = open('inventory.csv', 'r', encoding='utf-8-sig')

# Convert 
ws.csv_to_dict(csv_file=csv_file, delimiter=';')

# object.headers returns first row with the data in a spreadsheet 
print(ws.headers)

# object.sheet_items returns converted rows as dictionaries in the array 
print(ws.sheet_items)
```

### - Other functions
Worksheet **object.headers** returns first row with the data in a spreadsheet 
```python
Python 3.9.1
[Clang 12.0.0 (clang-1200.0.32.28)] on darwin
>>> from sheet2dict import Worksheet
>>> ws = Worksheet()
>>> ws.xlsx_to_dict(path="inventory.xlsx")

>>> ws.headers
{'country': 'SK', 'city': 'Bratislava', 'citizens': '400000', 'random_field': 'cc'}
```

Worksheet **object.sanitize_sheet_items** removes None or empty dictionary keys from `sheet_items`
```python
>>> from sheet2dict import Worksheet
>>> ws = Worksheet()
>>> ws.xlsx_to_dict(path="inventory.xlsx")

>>> ws.sheet_items
[
  {'country': 'CZ', 'city': 'Prague', 'citizens': '600000', None: '22', 'random_field': 'cc'},
  {'country': 'UK', 'city': 'London', 'citizens': '2000000', None: '33', 'random_field': 'cc'}
]

>>> ws.sanitize_sheet_items
[
  {'country': 'CZ', 'city': 'Prague', 'citizens': '600000', 'random_field': 'cc'},
  {'country': 'UK', 'city': 'London', 'citizens': '2000000', 'random_field': 'cc'}
]
```
