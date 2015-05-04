# -*- coding: utf-8 -*-
from openerp import fields, models


class survey_question(models.Model):
    _inherit = 'survey.question'

    conditional = fields.Boolean(
        'Conditional Question',
        copy=False,
        # we add copy = false to avoid wrong link on survey copy,
        # should be improoved
    )
    question_conditional_id = fields.Many2one(
        'survey.question',
        'Question',
        copy=False,
        help="In order to edit this field you should first save the question"
    )
    answer_id = fields.Many2one(
        'survey.label',
        'Answer',
        copy=False,
    )

    # NO HACEMOS ESTA MOD GENERICA PORQUE DA ERROR AL ALMACENAR LOS CHOICE
    # def validate_question(
    #         self, cr, uid, question, post, answer_tag, context=None):
    #     """We add answer_tag if not in post because it gets an error in this
    #     method, this happens when question is not display so the answer_tag
    #     value is no on post dictionary"""
    #     if answer_tag not in post:
    #         post[answer_tag] = ''
    #     return super(survey_question, self).validate_question(
    #          cr, uid, question, post, answer_tag, context=context)
    def validate_free_text(
            self, cr, uid, question, post, answer_tag, context=None):
        """We add answer_tag if not in post because it gets an error in this
        method, this happens when question is not display so the answer_tag
        value is no on post dictionary"""
        if answer_tag not in post:
            post[answer_tag] = ''
        return super(survey_question, self).validate_free_text(
             cr, uid, question, post, answer_tag, context=context)

    def validate_textbox(
            self, cr, uid, question, post, answer_tag, context=None):
        """We add answer_tag if not in post because it gets an error in this
        method, this happens when question is not display so the answer_tag
        value is no on post dictionary"""
        if answer_tag not in post:
            post[answer_tag] = ''
        return super(survey_question, self).validate_textbox(
             cr, uid, question, post, answer_tag, context=context)

    def validate_numerical_box(
            self, cr, uid, question, post, answer_tag, context=None):
        """We add answer_tag if not in post because it gets an error in this
        method, this happens when question is not display so the answer_tag
        value is no on post dictionary"""
        if answer_tag not in post:
            post[answer_tag] = ''
        return super(survey_question, self).validate_numerical_box(
             cr, uid, question, post, answer_tag, context=context)

    def validate_datetime(
            self, cr, uid, question, post, answer_tag, context=None):
        """We add answer_tag if not in post because it gets an error in this
        method, this happens when question is not display so the answer_tag
        value is no on post dictionary"""
        if answer_tag not in post:
            post[answer_tag] = ''
        return super(survey_question, self).validate_datetime(
             cr, uid, question, post, answer_tag, context=context)


class survey_user_input(models.Model):
    _inherit = 'survey.user_input'

    def get_list_questions(self, cr, uid, survey, user_input_id):

        obj_questions = self.pool['survey.question']
        obj_user_input_line = self.pool['survey.user_input_line']
        questions_to_hide = []
        question_ids = obj_questions.search(
            cr,
            uid,
            [('survey_id', '=', survey.id)])
        for question in obj_questions.browse(cr, uid, question_ids):
            if question.conditional:
                for question2 in obj_questions.browse(cr, uid, question_ids):
                    if question2 == question.question_conditional_id:
                        input_answer_id = obj_user_input_line.search(
                            cr,
                            uid,
                            [('user_input_id', '=', user_input_id),
                             ('question_id', '=', question2.id)])
                        if question.answer_id != obj_user_input_line.browse(
                                cr,
                                uid,
                                input_answer_id).value_suggested:
                            questions_to_hide.append(question.id)
        return questions_to_hide
