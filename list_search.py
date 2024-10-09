import re
from copy import deepcopy
from typing import Any

SUPPORTED_FILTERING_LOOKUPS = [
    "__in",
    "__any",
    "__gt",
    "__gte",
    "__lt",
    "__lte",
    "__isnull",
]


def search(
        lst: list[Any],
        element_or_query: dict | Any,
) -> list[Any]:
    """
    Search element in the list
    You may pass non-complex types like int, string, bool, etc.
    And complex ones - list, dict. If list - finds full match. If dict - finds by fields
    If you pass dict with dunders - finds by dunders (in priority)
    NOTE: __index__ starts from 1 (not from 0)
    If you pass dict with multiple conditions - finds by ALL conditions

    Example (or):
    {
        __index__: 5, 'first', 'last'
        __regex__: r"^\d{3}$"
        id: 12345
        name: 'Apple'
        author.name: 'John Wick'
        fruits__in: ['apple', 'banana', 'orange']
        likes__gte: 100
    }
    NOTE: author is dict, hashtags is list of dict, so you can do nested search
    See supported filtering operators in SUPPORTED_FILTERING_LOOKUPS
    """
    matches = deepcopy(lst)  # then we'll filter out elements, that match criteria

    if not isinstance(element_or_query, dict):
        return [item for item in matches if item == element_or_query]

    if "__index__" in element_or_query:
        index_val = element_or_query["__index__"]
        if isinstance(index_val, int):
            index = index_val - 1 if index_val > 0 else 0
        else:
            index = 0 if index_val == "first" else -1
        matches = [_get_element_or_query_by_index(matches, index)]

    if "__regex__" in element_or_query:
        element_or_queries_to_match = [item for item in matches if isinstance(item, str | int)]
        match_res = [
            item
            for item in element_or_queries_to_match
            if re.match(element_or_query["__regex__"], str(item))
        ]
        matches = [item for item in matches if item in match_res]

    # if these are not reserved keys (like above)
    if any(key for key in list(element_or_query.keys()) if not key.startswith("__")):
        fields_query = {
            key: element_or_query[key]
            for key in list(element_or_query.keys())
            if not key.startswith("__")
        }
        matches = [item for item in matches if _match_query(item, fields_query)]

    return matches


def _get_element_or_query_by_index(lst: list, index: int) -> Any:
    try:
        return lst[index]
    except IndexError:
        return None


def _match_query(obj: list | dict, query: dict) -> bool:
    """
    Check if obj matches query
    For example:
    obj = {
        'a': {
            'b': 1
        },
        'c': 1
    }
    query = {
        'a.b': 1
    }
    returns True
    """
    for key, value in query.items():
        path = key.split(".")
        if not _match_path(obj, path, value):
            return False
    return True


def _match_path(  # noqa: PLR0911
        obj: list | dict,
        path: str,
        value: Any,
        operator: str | None = None,
) -> bool:
    """
    Searching value in object by path
    For example:
    obj = {
        'a': {
            'b': 1
        },
        'c': 1
    }
    path = 'a.b'
    value = 1
    returns True
    """
    if not path:
        if operator:
            match operator:
                case "in":
                    match value:
                        case str():
                            return value in obj
                        case list():
                            return all(item in obj for item in value)
                        case _:
                            return obj == value
                case "any":
                    match value:
                        case str():
                            return value in obj
                        case list():
                            return any(item in obj for item in value)
                        case _:
                            return obj == value
                case "gt":
                    return obj > value
                case "gte":
                    return obj >= value
                case "lt":
                    return obj < value
                case "lte":
                    return obj <= value
                case "isnull":
                    return bool(obj) != value
        return obj == value

    key = path[0]
    rest = path[1:]
    operator = (
        key.split("__")[-1]
        if any(path[0].endswith(operator) for operator in SUPPORTED_FILTERING_LOOKUPS)
        else None
    )
    # we remove operator from the key
    for lookup in SUPPORTED_FILTERING_LOOKUPS:
        if key.endswith(lookup):
            key = key[: -len(lookup)]
            break

    if isinstance(obj, dict):
        if key in obj:
            # we call it recursively and pass path from the current rest
            return _match_path(obj[key], rest, value, operator)
        return False
    elif isinstance(obj, list):
        # check if any item in the list matches the path
        return _match_path(obj, path, value, operator)
    return False


__all__ = ["search"]
