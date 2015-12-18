# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models
import logging

_logger = logging.getLogger(__name__)


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

    def validate_question(
            self, cr, uid, question, post, answer_tag, context=None):
        ''' Validate question, depending on question type and parameters '''

        input_answer_id = self.pool['survey.user_input_line'].search(
            cr, uid,
            [('user_input_id.token', '=', post.get('token')),
             ('question_id', '=', question.question_conditional_id.id)])
        try:
            checker = getattr(self, 'validate_' + question.type)
        except AttributeError:
            _logger.warning(
                question.type + ": This type of question has no validation method")
            return {}
        else:
            for answers in self.pool['survey.user_input_line'].browse(cr, uid,input_answer_id):
                value_suggested = answers.value_suggested
                if question.conditional and question.answer_id != value_suggested:
                    return {}
                else:
                    return checker(cr, uid, question, post, answer_tag, context=context)


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
                        for answers in obj_user_input_line.browse( cr,uid,input_answer_id):
                            value_suggested = answers.value_suggested
                            if question.answer_id != value_suggested:
                                questions_to_hide.append(question.id)
        return questions_to_hide
