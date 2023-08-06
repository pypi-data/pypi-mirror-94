# lite3
It helps to create an sqlite3 database easily and maintainable without MYSQL syntax with just using simple familar python functions with the same names as sqlite3 python builtin module.

## Installation
'''pip install lite3'''

## Documentation
'''https://lite3.herokuapp.com/'''

## Usage

'''python
import lite3

db = lite3.lite('customers.db', 'connect', 'cursor')

table = 'Common'
cols = ['name', 'gender']

db.execute(table, cols)
# creates a database with a Table name common with two columns

'''