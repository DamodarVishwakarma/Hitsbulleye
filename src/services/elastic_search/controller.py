"""controller for elastic"""
from src.configs.constants import config
from src.services.elastic_search.es_curd import ElasticSearchUtility
from src.services.elastic_search.mapping import QuestionEsConfig
from src.services.question.model import QuestionModel


class ElasticSearchController(ElasticSearchUtility):
    """controller for elastic"""

    def __init__(self, es):
        super().__init__(es, config.es_question_idx)
        self.e_s = es
        self.index_name = config.es_question_idx
        self.configuration = QuestionEsConfig
        self.id_field = 'question_id'
        self.elastic_utility = ElasticSearchUtility(self.e_s, index_name=self.index_name)

    def push_document_full(self):
        """
        Delete index and create new index with full data load
        """
        questions = QuestionModel.get_to_push_elastic(_id=None)
        if questions:
            self.delete_index()

        self.push_document_incremental()

    def push_document_incremental(self, _id=None):
        """Push insert update document in elastic search"""
        self.create_index()
        questions = QuestionModel.get_to_push_elastic(_id=None)
        for question in questions:
            try:
                if question.status:
                    data = {
                        'question_id': question.id,
                        'org_id': question.org_id,
                        'is_public': question.is_public,
                        'area_ids': question.area_ids,
                        'lod': question.lod,
                        'question_style': question.question_style,
                        'no_of_option': question.no_of_option,
                        'marking_range': question.marking_range,
                        'typable_text_type': question.typable_text_type,
                        'direction_id': question.direction_id,
                        'course_ids': question.course_ids,
                        'question_type': question.question_type,
                        'answer_type': question.answer_type,
                        'editor': question.editor,
                        'answer': question.answer,
                        'typable_answer': question.typable_answer,
                        'question': question.question,
                        'explanation': question.explanation,
                        'option1': question.option1,
                        'option2': question.option2,
                        'option3': question.option3,
                        'option4': question.option4,
                        'option5': question.option5,
                        'option6': question.option6,
                        'tags': question.tags,
                        'created_by': question.created_by,
                        'updated_by': question.updated_by,
                        'created_on': question.created_on,
                        'updated_on': question.updated_on,
                        'meta_data': question.meta_data
                    }
                    self.elastic_utility.insert_one(data, question.id)
                else:
                    self.elastic_utility.delete_one(question.id)
                QuestionModel.update_es_status(question.id)
            except Exception as EX:
                print(EX)
            finally:
                pass

    def delete_single_document(self, _id):
        """delete single document"""
        self.elastic_utility.delete_one(_id)
