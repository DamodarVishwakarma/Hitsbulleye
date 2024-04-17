# from tldextract import extract
from tldextract import extract


def greater_or_equal(field, value):
    """
    Prepare query greater or equal query
    :param field:
    :param value:
    :return:
    """
    return {"range": {
        field: {
            "gte": value,
        },
    }}


def smaller_or_equal(field, value):
    """
    Prepare query smaller or equal query

    :param field:
    :param value:
    :return:
    """
    return {"range": {
        field: {
            "lte": value,
        },
    }}


def filter_range(field, minimum, maximum):
    """
    Create query to filter the values for smaller and greater than
    :param field:
    :param minimum:
    :param maximum:
    :return:
    """
    return {"range": {
        field: {
            "lte": maximum,
            "gte": minimum,
        },
    }}


def filter_nested(field: str, sub_field: str, values: list):
    """
    filter on nested fields
    :param field:
    :param sub_field:
    :param values:
    :return:
    """
    return {"nested": {
        "path": field,
        "query": {
            "bool": {
                "should": [
                    {"match": {f"{field}.{sub_field}": value}} for value in values
                ] if isinstance(values, list) else [
                    {"match": {f"{field}.{sub_field}": f'{values}'}}
                ]
            }
        }
    }}


def filter_nested_name(field: str, sub_field: str, value: str):
    """
    filter on nested fields
    :param field:
    :param sub_field:
    :param values:
    :return:
    """
    return {"nested": {
        "path": field,
        "query": {
            "bool": {
                "should": [
                    {
                        "prefix": {
                            f"{field}.{sub_field}": {
                                "value": f"{value}",
                                "boost": 500
                            }
                        }
                    },
                    {
                        "match_phrase_prefix": {
                            f"{field}.{sub_field}": {
                            "query": f"{value}",
                            "boost": 200
                            }
                        }
                    }
                ]
            }
        }
    }}


def filter_nested_range(field: str, sub_field: str, minimum, maximum):
    """
    filter on nested fields
    :param field:
    :param sub_field:
    :param values:
    :return:
    """
    return {"nested": {
        "path": field,
        "query": {
            "bool": {
                "must": [
                    {"range": {f"{field}.{sub_field}": {"gte":minimum,"lte":maximum}}}
                ]
            }
        }
    }}


def wild_card_search(field, value):
    """
    search for wild card
    :param field:
    :param value:
    :return:
    """
    return {
        "wildcard": {
            field: {
                "value": f'*{value}*',
                "case_insensitive": True
            }
        }
    }


def match(field, value):
    """
    exact match
    :param field:
    :param value:
    :return:
    """
    return {
        "match": {
            field: value
        }}


def filter_any_list(id_key, values: list, include_missing:bool = False):
    """
    get query for match at least one value form list
    :param id_key:
    :param values:
    :return:
    """
    q = {
        "bool": {
            "should": [
                {"match": {f"{id_key}": value}} for value in values
            ] if isinstance(values, list) else [
                {"match": {f"{id_key}": f'{values}'}}
            ]
        }
    }
    if include_missing:
        q["bool"]["should"].append(
            {
                "bool": {
                    "must_not": {"exists": {"field": id_key}}
                }
            }
        )
    return q


def filter_any_list_dict(filters):
    """
    get query for match at least one value form list
    :param id_key:
    :param values:
    :return:
    """
    q = {
        "bool": {
            "should": filters
        }
    }
    return q


def missing_filter(id_key,is_nested: bool = False):
    """
    get query for match at least one value form list
    :param id_key:
    :param values:
    :return:
    """
    if is_nested:
        q = {"bool": {
                "must_not":{
                    "nested": {
                        "path": id_key,
                        "query": {
                            "exists": {
                                "field": id_key
                            }
                        }
                    }
                }
            }
        }
    elif id_key in ["deal_teams", "reversed_integer_country_id"] and not is_nested:
        q = {
                "bool": {
                    "should": [
                        {
                            "match": {f"{id_key}": 0}
                        },
                        {
                            "bool": {"must_not": {"exists": {"field": id_key}}}
                        }
                    ]
                }
            }
    else:
        q = {"bool": {
                    "must_not": {"exists": {"field": id_key}}
                }
            }
    return q


def get_multiple_ids(id_key, values: list):
    """
    get query for ids
    :param id_key:
    :param values:
    :return:
    """
    return {
        id_key: {
            "values": values
        }}


def nested_sorting(field, sub_field, order_type):
    """
    sortign on nested fields
    :param field:
    :param sub_field:
    :param order_type:
    :return:
    """
    return {f'{field}.{sub_field}': {"order": f'{order_type}',
                                     "mode": "min",
                                     "missing" : "_last",
                                     "nested": {
                                         "path": f"{field}",
                                     }}}


def nested_fuzzy_search(field, sub_field, value):
    """
    fuzzty search on nested fields
    :param field:
    :param sub_field:
    :param value:
    :return:
    """
    return {"nested": {
        "path": field,
        "query": {
            "bool": {
                "should": [
                    {"fuzzy": {
                        f"{field}.{sub_field}": value}}
                ]
            }
        }
    }}


def get_fixed_records(id_key, values: list):
    """
    get query for fixed records
    :param id_key:
    :param values:
    :return:
    """
    return [{
        "filter": {"match": {f"{id_key}": f"{value}"}},
        "weight": len(values) + 10 - index
    } for index, value in enumerate(values)]


def fuzzy_search(field, value):
    """Fuzzy search"""
    return {
        "fuzzy": {
            field: {
                "value": f"{value}",
                "transpositions": "true"
            }
        }
    }


def fuzzy_search_with_match(field  , value):
    """Fuzzy search with match"""
    return (
        {
            "prefix": {
                f"{field}": {
                  "value": f"{value}",
                  "boost": 300
               }
            }
        },
        {
             "match_phrase_prefix": {
                f"{field}": {
                  "query": f"{value}",
                  "boost": 200
               }
            }
        }
    )


def fuzzy_search_with_match_not_name(field, value):
    """Fuzzy search with match"""
    value=value.lower()
    return (
        {
            "prefix": {
                f"{field}": {
                  "value": f"{value.split(' ')[0]}",
                  "boost": 300
               }
            }
        },
        {
             "match_phrase_prefix": {
                f"{field}": {
                  "query": f"{value}",
                  "boost": 200
               }
            }
        },
    )


def fuzzy_search_with_match_email_domian(field, value):
    """Fuzzy search with match"""
    value = value.lower()
    return (
        {
            "match": {
                f"{field}": {
                    "query": f"{value}",
                    "boost": 800
                }
            }
        },
        {
            "prefix": {
                f"{field}": {
                  "value": f"{value}",
                  "boost": 300
               }
            }
        },
    )


def fuzzy_search_with_match_old(field, value):
    return {
        "match":
            {
                f"{field}" : {
                "query" : f"{value}",
                "fuzziness": "AUTO:2,4",
                "fuzzy_transpositions": True,
                "operator":  "or",
                "analyzer": "standard",
                "zero_terms_query": "none",
                "lenient": False,
                "prefix_length": 2,
                "max_expansions": 10,
                "boost": 100
                }
            }
        }


def greater(field, value):
    """
    Prepare query greater or equal query
    :param field:
    :param value:
    :return:
    """
    return {"range": {
        field: {
            "gt": value,
        },
    }}
