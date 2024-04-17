"""es curd operation"""
import logging
import math

from elasticsearch import helpers
import copy

from src.services.elastic_search.es_filter import match, filter_nested, wild_card_search, greater_or_equal, \
    smaller_or_equal, get_multiple_ids, filter_any_list, filter_nested_name, fuzzy_search_with_match, \
    fuzzy_search_with_match_email_domian, filter_any_list_dict, fuzzy_search_with_match_old, filter_range, \
    filter_nested_range, missing_filter, nested_sorting, get_fixed_records


class ElasticSearchUtility:
    """Es related operations"""

    def __init__(self, es, index_name):
        self.index_name = index_name
        self.e_s = es
        self.configuration = None
        self.id_field = None

    def create_index(self):
        """create new index"""
        if self.e_s.indices.exists(index=self.index_name):
            print(f"pass creation process of {self.index_name} index...")
        else:
            print(f"creating {self.index_name} index...")
            self.e_s.indices.create(index=self.index_name, body=self.configuration.idx_map)

    def delete_index(self):
        """
        Delete index on elastic search
        :return:
        """
        if self.e_s.indices.exists(index=self.index_name):
            print(f"Deleting {self.index_name} index...")
            self.e_s.indices.delete(index=self.index_name)
        else:
            print(f"Skipping {self.index_name} index deletion...")
            self.e_s.indices.create(index=self.index_name, body=self.configuration.idx_map)

        return None

    def bulk_insert(self, data: list):
        """
        Insert or Update data in bulk
        :param data: A list containing all the documents
        :return:
        """
        return helpers.bulk(self.e_s, data)

    def update_one(self, _id: int, updated_data: dict):
        """
        Update single data in elastic search with ID
        :param _id: Id of obj to be updated
        :param updated_data: Dict containing updated document
        :return:
        """
        data = {'doc': updated_data}
        res = self.e_s.update(
            index=self.index_name,
            id=_id,
            body=data
        )
        return res

    def refresh_index(self):
        """
        Refresh Index
        :return:
        """
        return self.e_s.indices.refresh(index=self.index_name)

    def delete_one(self, _id):
        """
        Delete obj from ES with ID
        :param _id: Id of objects which needs to be updated
        :return:
        """
        return self.e_s.delete(
            index=self.index_name,
            id=_id,
            ignore=404
        )

    def insert_one(self, document, _id):
        """
        Insert one element
        :param document:  document json
        :param _id:  id of object
        :return:
        """
        return self.e_s.index(index=self.index_name, body=document, id=_id)

    def does_exists(self, _id) -> bool:
        """
        check if element exists
        :param _id: id of object
        :return: bool
        """
        return self.e_s.exists(index=self.index_name, id=_id)

    def filters(self, payload: dict, page, size):
        """Controller for filter"""
        must_bool_filters = []
        must_not_bool_filters = []
        should_bool_filters = []
        fuzzy_queries = []
        filters = payload.get('filters', {})
        empty_fields = payload.get('filter_missing', []) or []
        query_string = copy.deepcopy(self.configuration.common_query_string)

        for key, value in filters.items():
            if value == None:
                continue
            if key in self.configuration.nested_fields:
                must_bool_filters += [filter_nested(key, self.configuration.nested_fields[key], value)]
            if key in self.configuration.search_fields:
                must_bool_filters.append(wild_card_search(key, value))
            if key in self.configuration.min_fields:
                must_bool_filters.append(greater_or_equal(key, filters.get(key)))
            if key in self.configuration.max_fields:
                must_bool_filters.append(smaller_or_equal(key, filters.get(key)))
            if key in self.configuration.exact_match:
                values = filters.get(key)
                if isinstance(values, list):
                    for _value in value:
                        must_bool_filters.append(match(key, _value))
                else:
                    must_bool_filters.append(match(key, filters.get(key)))

            if key in self.configuration.exact_not_match:
                base_key = key.replace("not_", "")
                values = filters.get(key)
                if isinstance(values, list):
                    for _value in value:
                        must_not_bool_filters.append(match(base_key, _value))
                else:
                    must_not_bool_filters.append(match(base_key, filters.get(key)))
            if key in self.configuration.list_fields:
                must_bool_filters.append(get_multiple_ids(key, filters.get(key)))
            if key in self.configuration.any_list:
                if isinstance(value, dict):
                    temp_should_list = []
                    for _key, _value in value.items():
                        if _key in self.configuration.list_fields:
                            temp_should_list.append(get_multiple_ids(_key, _value))
                        elif _key in self.configuration.nested_fields_name:
                            temp_should_list += [filter_nested_name(_key, self.configuration.nested_fields_name[_key], _value)]
                        elif _key in self.configuration.nested_fields:
                            temp_should_list += [filter_nested(_key, self.configuration.nested_fields[_key], _value)]
                        elif _key in self.configuration.fuzzy_search_fields:
                            temp_should_list.append(fuzzy_search_with_match(_key, _value)[0])
                    must_bool_filters.append(filter_any_list_dict(temp_should_list))
                else:
                    must_bool_filters.append(filter_any_list(key, value))
            if key in self.configuration.fuzzy_search_fields:
                must_bool_filters.append(fuzzy_search_with_match_old(key, filters.get(key)))
            if key in self.configuration.range_fields:
                if isinstance(value, list) and len(value) == 2:
                    must_bool_filters.append(filter_range(key, value[0], value[1]))
            if key in self.configuration.nested_range:
                if isinstance(value, list) and len(value) == 2:
                    must_bool_filters.append(filter_nested_range(key, self.configuration.nested_range[key], value[0], value[1]))
            if key in self.configuration.should_fields:
                if isinstance(value, list):
                    for _value in value:
                        should_bool_filters.append(match(key, _value))
                else:
                    should_bool_filters.append(match(key, value))

        for key in empty_fields:
            if key in self.configuration.missing_filter_fields:
                field_type = self.configuration.missing_filter_fields[key]
                if field_type == 'nested':
                    q = None
                    for queries in must_bool_filters:
                        if "nested" in queries and queries["nested"]["path"] == key:
                            q = queries["nested"]["query"]["bool"]["should"]
                            q.append(missing_filter(key))
                            break
                    if not q:
                        must_bool_filters.append(missing_filter(key, is_nested=True))
                else:
                    q = None
                    for queries in must_bool_filters or []:
                        if key in filters:
                            if "bool" in queries and "should" in queries["bool"]:
                                for should in queries["bool"]["should"] or []:
                                    if key in should.get("match", {}):
                                        q = queries["bool"]["should"]
                                        q.append(missing_filter(key))
                                        break
                                if q:
                                    break
                    if not q:
                        must_bool_filters.append(missing_filter(key))

        for key, value in payload.get('sort', {}).items():
            if key in self.configuration.sorting_fields and value in ["asc", "desc"]:
                if key in self.configuration.nested_fields:
                    query_string['sort'].append(nested_sorting(key, self.configuration.nested_fields[key], value))
                elif key in self.configuration.nested_range:
                    query_string['sort'].append(nested_sorting(key, self.configuration.nested_range[key], value))
                else:
                    query_string['sort'].append({key: {"order": value, "missing": "_last"}})
        if len(query_string["sort"]) > 1:
            score = query_string["sort"].pop(0)
            query_string["sort"] = query_string["sort"] + [score]
        query_string["query"]['function_score']['query']["bool"]["should"] += fuzzy_queries[0] if len(fuzzy_queries) > 0 else fuzzy_queries
        # query_string["query"]['function_score']['query']["bool"]["should"] += fuzzy_queries[0] if len(fuzzy_queries) > 0 else fuzzy_queries
        query_string["query"]['function_score']['query']['bool']['must'] += must_bool_filters
        query_string["query"]['function_score']['query']['bool']['must_not'] = must_not_bool_filters
        query_string["query"]['function_score']['query']['bool']['should'] += should_bool_filters
        query_string["query"]['function_score']['functions'] += get_fixed_records(self.id_field, payload.get('fixed_records', []))

        query_string['sort'].append({self.id_field: {"order": "desc"}})
        query_string['from'] = (size * page) - size
        query_string['size'] = size
        res = {}
        total_count = 0
        try:
            res = self.e_s.search(index=self.index_name, body=query_string) or {}
            total_count = res.get('hits', {}).get('total', {}).get('value') or 0 if res else 0
        except Exception as ex:
            logging.exception(ex)
        data = {
            "status": "success",
            "page": page,
            "total": total_count,
            "num_pages": int(math.ceil(total_count / size)) if total_count else 0,
            "data": [hit['_source'] for hit in res.get('hits', {}).get('hits', {})]
        }

        return data
