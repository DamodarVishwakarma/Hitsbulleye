class BaseConfig:
    common_query_string = {
        "sort": [{
            "_score": {
                "order": "desc"
            }
        }],
        "query": {
            "function_score": {
                "query": {'bool': {'must': [], 'should': [], "minimum_should_match": "50%"}},
                "boost": "5",
                "functions": [],
                "score_mode": "max",
                "boost_mode": "replace"
            }
        }
    }

    index_setting = {
            'search': {
                'slowlog': {
                    'threshold': {
                        'query': {
                            'warn': '800ms',
                            'info': '600ms',
                        },
                        'fetch': {
                            'warn': '500ms',
                            'info': '300ms',
                        }
                    }
                }},
            'indexing': {
                'slowlog': {
                    'threshold': {
                        'index': {
                            'warn': '1s'
                        }
                    }
                }
            },
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "bigram_combiner": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "custom_shingle",
                            "my_char_filter"
                        ]
                    },
                    "autocomplete_edge_ngram_word": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "autocomplete_filter"]
                    }
                },
                "filter": {
                    "custom_shingle": {
                        "type": "shingle",
                        "min_shingle_size": 2,
                        "max_shingle_size": 3,
                        "output_unigrams": True
                    },
                    "my_char_filter": {
                        "type": "pattern_replace",
                        "pattern": " ",
                        "replacement": ""
                    },
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 20
                    }
                }
            }
        }


class QuestionEsConfig(BaseConfig):
    idx_map = {
        "settings": BaseConfig.index_setting,
        "mappings": {
            "properties": {
                'question_id': {'type': 'integer'},
                'org_id': {'type': 'integer'},
                'is_public': {'type': 'boolean'},
                'area_ids': {'type': 'integer'},
                'lod': {'type': 'integer'},
                'question_style': {'type': 'integer'},
                'no_of_option': {'type': 'integer'},
                'marking_range': {'type': 'integer'},
                'typable_text_type': {'type': 'integer'},
                'direction_id': {'type': 'integer'},
                'course_ids': {'type': 'integer'},
                'question_type': {'type': 'integer'},
                'answer_type': {'type': 'integer'},
                'editor': {'type': 'integer'},
                'answer': {'type': 'integer'},
                'typable_answer': {'type': 'keyword'},
                'question': {'type': 'text'},
                'explanation': {'type': 'text'},
                'option1': {'type': 'text'},
                'option2': {'type': 'text'},
                'option3': {'type': 'text'},
                'option4': {'type': 'text'},
                'option5': {'type': 'text'},
                'option6': {'type': 'text'},
                'tags': {"type": 'keyword'},
                'created_by': {'type': 'keyword'},
                'updated_by': {'type': 'keyword'},
                'created_on': {'type': 'date'},
                'updated_on': {'type': 'date'},
                'meta_data': {'type': 'object'},
            },
            "dynamic_templates": [
                {
                    "text_indexed_template": {
                        "match_mapping_type": "string",
                        "match": 'reversed_text_*',
                        "mapping": {
                            "type": "text"
                        }
                    }
                },
                {
                    "keyword_indexed_template": {
                        "match_mapping_type": "string",
                        "match": 'reversed_keyword_*',
                        "mapping": {
                            "type": "keyword"
                        }
                    }
                },
                {
                    "integer_indexed_template": {
                        "match_mapping_type": "long",
                        "match": 'reversed_integer_*',
                        "mapping": {
                            "type": "integer"
                        }
                    }
                },
                {
                    "float_indexed_template": {
                        "match_mapping_type": "double",
                        "match": 'reversed_float_*',
                        "mapping": {
                            "type": "float"
                        }
                    }
                },
                {
                    "date_indexed_template": {
                        "match_mapping_type": "date",
                        "match": 'reversed_date_*',
                        "mapping": {
                            "type": "date"
                        }
                    }
                },
                {
                    "nested_indexed_template": {
                        "match": 'reversed_nested_*',
                        "mapping": {
                            "type": "nested"
                        }
                    }
                }
            ]

        }
    }
    sorting_fields = []
    nested_fields = {'course_ids':  'id', 'area_ids': 'id'}
    nested_fields_name = {}
    nested_range = {}
    max_fields = []
    min_fields = []
    fuzzy_search_fields = []
    search_fields = []
    exact_match = []

    should_fields = []
    range_fields = []
    list_fields = []
    any_list = ["question_id"]
    exact_not_match = []
    any_list_exactmatch = []
    missing_filter_fields = {}
