# About

Search in list of dictionaries with lookups! Like in ORM!  
Say goodbye to complicated loops and conditions when searching through lists of dictionaries!  
With this simple Python tool, you can easily filter and find what you need using ORM-style lookups, making data searches
feel smooth and intuitive.

# How to install
```
pip install list_search
```

# How to use

You can search non-complex types like `int`, `string`, `bool`, etc. in list

```python
from list_search import search

lst = [1, 2, 3, 'apple', 'banana', True, False]
result = search(lst, 'apple')
```

Output

```
['apple']
```

---
Or you can search complex objects - `list` or `dict`. If `list` - finds full match. If `dict` - finds by fields  
The advantage of this approach is that you can put ONLY the fields **you need**, NOT the whole dict!  
Lookups: `["__in","__any","__gt","__gte","__lt","__lte","__isnull"]`. Up to date lookups you can find
in `SUPPORTED_FILTERING_LOOKUPS`

```python
from list_search import search

lst = [
    {
        "author": {
            "name": "John",
            "last_name": "Wick",
        },
        "books": [
            "Book 1",
            "Book 2"
        ],
        "birth_year": 1950
    },
    {
        "author": {
            "name": "Jack",
            "last_name": "Thompson",
        },
        "books": [
            "Another Book 1",
            "Another Book 2"
        ],
        "birth_year": 1930
    }
]

# search by the fields you need WITH LOOKUPS! 
# You can put only one field, and the elements will be filtered out.
query = {
    "author.name": "John",
    "books__in": ["Book 2"],
    "birth_year__gte": 1945
}
result = search(lst, query)
```

Output

```
{
    "author": {
        "name": "John",
        "last_name": "Wick",
    },
    "books": [
        "Book 1",
        "Book 2"
    ],
    "birth_year": 1950
}
```
