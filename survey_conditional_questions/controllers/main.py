# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

import logging
import werkzeug
import werkzeug.utils
from math import ceil
from openerp.addons.web import http
from openerp.addons.survey.controllers.main import WebsiteSurvey
from openerp.addons.web.http import request
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as DTF


_logger = logging.getLogger(__name__)


class SurveyConditional(WebsiteSurvey):

    @http.route()
    def fill_survey(self, survey, token, prev=None, **post):
        '''Display and validates a survey'''
        cr, uid, context = request.cr, request.uid, request.context
        survey_obj = request.registry['survey.survey']
        user_input_obj = request.registry['survey.user_input']

        # Controls if the survey can be displayed
        errpage = self._check_bad_cases(
            cr, uid, request, survey_obj, survey, user_input_obj, context=context)
        if errpage:
            return errpage

        # Load the user_input
        try:
            user_input_id = user_input_obj.search(
                cr, uid, [('token', '=', token)])[0]
        except IndexError:  # Invalid token
            return request.website.render("website.403")
        else:
            user_input = user_input_obj.browse(
                cr, uid, [user_input_id], context=context)[0]

        # Do not display expired survey (even if some pages have already been
        # displayed -- There's a time for everything!)
        errpage = self._check_deadline(
            cr, uid, user_input, context=context)
        if errpage:
            return errpage

        # Select the right page
        if user_input.state == 'new':  # First page
            page, page_nr, last = survey_obj.next_page(
                cr, uid, user_input, 0, go_back=False, context=context)
            data = {'survey': survey, 'page': page,
                    'page_nr': page_nr, 'token':  token}
            data['hide_question_ids'] = user_input_obj.get_list_questions(
                cr, uid, survey, user_input_id)
            if last:
                data.update({'last': True})
            return request.website.render('survey.survey', data)
        elif user_input.state == 'done':  # Display success message
            return request.website.render('survey.sfinished', {'survey': survey,
                                                               'token': token,
                                                               'user_input': user_input})
        elif user_input.state == 'skip':
            flag = (True if prev and prev == 'prev' else False)
            page, page_nr, last = survey_obj.next_page(
                cr, uid, user_input, user_input.last_displayed_page_id.id, go_back=flag, context=context)

            # special case if you click "previous" from the last page, then
                # leave the survey, then reopen it from the URL, avoid crash
            if not page:
                page, page_nr, last = survey_obj.next_page(
                    cr, uid, user_input, user_input.last_displayed_page_id.id, go_back=True, context=context)

            data = {'survey': survey, 'page': page,
                    'page_nr': page_nr, 'token': user_input.token}
            if last:
                data.update({'last': True})
            data['hide_question_ids'] = user_input_obj.get_list_questions(
                cr, uid, survey, user_input_id)
            return request.website.render('survey.survey', data)
        else:
            return request.website.render("website.403")
