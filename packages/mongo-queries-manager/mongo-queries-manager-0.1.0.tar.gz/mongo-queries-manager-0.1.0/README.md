# MongoDBQueriesManager
![Codecov](https://img.shields.io/codecov/c/github/comic31/MongoDBQueriesManager?style=for-the-badge)
![Travis (.com)](https://img.shields.io/travis/com/comic31/MongoDBQueriesManager?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/mongo-queries-manager?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/comic31/MongoDBQueriesManager?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mongo-queries-manager?style=for-the-badge)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg?style=for-the-badge)](code_of_conduct.md)

Convert query parameters from API urls to MongoDB queries !

This project was inspired by [api-query-params](https://github.com/loris/api-query-params) (JS Library).

## Features:
- **Powerful**: Supports most of MongoDB operators ($in, $regexp, ...) and features (nested objects, type casting, ...)
- **Agnostic**: Works with any web frameworks (Flask, Sanic, ...) and/or MongoDB libraries (pymongo, motor, ...)
- **Simple**: ~150 LOC, Python typing
- **Tested**: 100% tested

## Installation:
```shell script
pipenv install mongo-queries-manager
```

## Usages:
### Api
`mqm(string_query: str) -> Dict[str, Any]:`

###### Description
Converts `string_query` into a MongoDB query dict.

###### Arguments
- `string_query`: query string of the requested API URL (ie, `frist_name=John&limit=10`), Works with url encoded. [required]

###### Returns
The resulting dictionary contains the following properties:
- `filter`: Contains the query criteria.
- `sort`: Contains the sort criteria (cursor modifiers).
- `skip`: Contains the skip criteria (cursor modifiers).
- `limit`:  Contains the limit criteria (cursor modifiers).

###### Exception
In case of error the following exception was raised:

- `MongoDBQueriesManagerBaseError`: Base MongoDBQueriesManager errors.
- `SkipError`: Raised when skip is negative / bad value.
- `LimitError`: Raised when limit is negative / bad value.
- `ListOperatorError`: Raised list operator was not possible.
- `FilterError`: Raised when parse filter method fail to find a valid match.



###### Examples:
```python
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from mongo_queries_manager import mqm

client: MongoClient = MongoClient('localhost', 27017)
db: Database = client['test-database']
collection: Collection = db['test-collection']

mongodb_query = mqm(string_query="status=sent&toto=true&timestamp>2016-01-01&"
                                 "author.firstName=/john/i&limit=100&skip=50&sort=-timestamp")

result = collection.find(**mongodb_query)
```
