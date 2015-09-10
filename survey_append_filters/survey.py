# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api


class survey_survey(models.Model):
    _inherit = 'survey.survey'

    append_filter = fields.Boolean(
        'Append filters in finished surveys',
        default=True)

    @api.model
    def filter_input_ids(self, survey, filters, finished=False):
        '''If user applies any filters, then this function returns list of
           filtered user_input_id and label's strings for display data in web.
           :param filters: list of dictionary (having: row_id, ansewr_id)
           :param finished: True for completely filled survey,Falser otherwise.
           :returns list of filtered user_input_ids.
        '''
        if survey.append_filter:
            if filters:
                input_lines = self.env['survey.user_input_line']
                filtered_inputs = input_lines.user_input_id
                for filter in filters:
                    row_id, answer_id = filter['row_id'], filter['answer_id']
                    if row_id == 0:
                        domain = [('value_suggested.id', '=', answer_id)]
                    else:
                        domain = [
                            '|',
                            ('value_suggested_row.id', '=', row_id),
                            ('value_suggested.id', '=', answer_id)]
                    if filtered_inputs:
                        domain.insert(
                            0,
                            ('user_input_id', 'in', filtered_inputs.ids))
                    lines = input_lines.search(domain)
                    filtered_inputs = lines.mapped('user_input_id')
            if finished:
                if not filtered_inputs:
                    user_inputs = self.env['survey.user_input'].search([
                        ('survey_id', '=', survey.id)])
                else:
                    user_inputs = filtered_inputs
                return user_inputs.filtered(lambda x: x.state == 'done').ids
            return filtered_inputs.ids
        else:
            return super(survey_survey, self).filter_input_ids(
                survey, filters, finished)
