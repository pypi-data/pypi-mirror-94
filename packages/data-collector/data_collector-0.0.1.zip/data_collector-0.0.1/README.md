# Module data_collector
The module includes two submodules:
1) Data gathering from sources: collector
2) Data processing: data_parser

Script collect_taxpayers.py is implementing list of taxpayers processing.

## 1. Installation
Python 3.9 must be installed.

Install dependencies using:

pip install -r requirements.txt

For cx_Oracle one should make ORA directories in the following way:

export ORACLE_HOME=/[location]/ora122/[place of ORACLE client]
export DYLD_LIBRARY_PATH=$ORACLE_HOME
export LD_LIBRARY_PATH=$ORACLE_HOME
export PATH=$ORACLE_HOME:$PATH

You may also add ORACLE_HOME directory path to the dictionary ORACLE_HOME_DIRS in settings_utils.py.


## 2. Data Collector Module
### 2.1 Objective
Collects SIGTAS and EDI data

DB setting are in the settings.py

### 2.2 Data sources

All data sources are in the module: collector/queries

For tax returns use script collect_tax_return_lines.py. You have to provide year
and tax_type_no (this is value from SIGTAS table TAX_TYPE.TAX_TYPE_NO).
Now there is tax_type_no = 34 <-- VAT

For getting invoices data use script collect_sales_data.py. You have to provide year.
The script will consider only VAT liable taxpayers (others do not have data in the EDI1).

## 3. Data Parser Module objectives
### 3.1 Objective
The module is used to transform operational data to the format, which is used
for machine learning model.

### 3.2 Use cases
The Collector module reads data from the operational data sources and provides the data to Data Parser. The 
Data Parser module transform data for every taxpayer to the specified format.

Transformation rules are in the folder "data_parser/rules".
Grammar is in the folder "data_parser/metadata"

To parse rules we use Lark module. Documentation is here: https://lark-parser.readthedocs.io/en/latest/
Also, see here: http://blog.erezsh.com/how-to-write-a-dsl-in-python-with-lark/

### 3.3 Implementation
1. Reading from sources is implemented in the loader_services.py, which is located in the 
   folder "collector"

2. Transformations are implemented in the class CalcTransformer.py

### 3.4 Transformation rules
Transformation rules are in Excel file, which is located in the folder "data_parser/metadata/docs"
