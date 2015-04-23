 #-*- coding: utf-8 -*-
from openerp import fields, models


class survey_question(models.Model):
    _inherit = 'survey.question'

    conditional = fields.Boolean(
        'Conditional Question')
    question_conditional_id = fields.Many2one(
        'survey.question',
        'Question',
        help="In order to edit this field you should first save the question")
    answer_id = fields.Many2one(
        'survey.label',
        'Answer'
    )


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
