# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from openerp import api
from openerp import fields as new_fields

class survey_question_score_range(osv.Model):
    _name = 'survey.question.score.range'
    # _rec_name = 'value'
    # _order = 'sequence'
    _description = 'Survey Question Score Range'

    _columns = {
        'from': fields.integer('From (included)', required=True,),
        'to': fields.integer('To (included)', required=True,),
        'score': fields.integer('Score', required=True,),
        'survey_question_id': fields.many2one('survey.question', 'Question', required=True,),
    }

    defaults = {
    }


class survey_question(osv.Model):

    _inherit = 'survey.question'

    @api.one
    @api.depends(
        'score_ranges_ids',
        'score_ranges_ids.score',
        'score_calc_method',
        'copy_labels_ids',
        'copy_labels_ids.score',
        'matrix_subtype',
        'labels_ids_2',
        'labels_ids_2.matrix_answer_score_ids',
        'labels_ids_2.matrix_answer_score_ids.score',
        'type',)
    def _get_max_score(self):
        # TODO mejorar esto y ver porque se llama varias veces a esta funcion *hay que cambiarlo tambien en academic_reports que sobreescribimos esta funcion
        max_score = 0
        question = self 
        if question.type == 'simple_choice':
            scores = [answer.score for answer in question.copy_labels_ids]
            max_score = max(scores if scores else [0])

        elif question.type == 'multiple_choice' and question.score_calc_method == 'direct_sum':
            max_score = sum([answer.score for answer in question.copy_labels_ids if answer.score > 0])
        elif question.type == 'multiple_choice' and question.score_calc_method == 'ranges':
            scores = [score_range.score for score_range in question.score_ranges_ids]
            max_score = max(scores if scores else [0])
        
        elif question.type == 'numerical_box' and question.score_calc_method == 'direct_sum':
            max_score = question.validation_max_float_value
        elif question.type == 'numerical_box' and question.score_calc_method == 'ranges':
            scores = [score_range.score for score_range in question.score_ranges_ids]
            max_score = max(scores if scores else [0])              
        
        elif question.type == 'matrix' and question.matrix_subtype == 'simple' and question.score_calc_method == 'direct_sum':
            for matrix_question in question.labels_ids_2:
                scores = [matrix_score.score for matrix_score in matrix_question.matrix_answer_score_ids]
                max_score += max(scores if scores else [0])
        elif question.type == 'matrix' and question.matrix_subtype == 'multiple' and question.score_calc_method == 'direct_sum':
            for matrix_question in question.labels_ids_2:
                max_score += sum([matrix_score.score for matrix_score in matrix_question.matrix_answer_score_ids if matrix_score.score > 0])
        elif question.type == 'matrix' and question.score_calc_method == 'ranges':
            scores = [score_range.score for score_range in question.score_ranges_ids]
            max_score = max(scores if scores else [0])
        print 'Changing max_score', self.id, self.survey_id.id
        self.max_score = max_score

    
    max_score = new_fields.Integer(compute='_get_max_score', string='Max Score', help='Max score an answer of this question can get', store=True)

    _columns = {
        'objective_id': fields.many2one('survey.question.objective', string='Objective', ),
        'level_id': fields.many2one('survey.question.level', string='Level', ),
        'content_id': fields.many2one('survey.question.content', string='Content', ),
        # 'max_score': fields.function(_get_max_score, type='integer', string='Max Score', help='Max score an answer of this question can get',),
        'score_calc_method': fields.selection([('direct_sum','Direct Sum'),('ranges', 'Ranges')], 
                string='Score Method', 
                help="Choose"\
                     "-Direct Sum if you want to sum the values assigned to questions answers." \
                     "-Ranges if you want to define ranges for correct answers.",),
        'score_ranges_ids': fields.one2many('survey.question.score.range' ,'survey_question_id', string='Ranges',), 
        'copy_labels_ids': fields.related('labels_ids', relation='survey.label', 
            type='one2many', string='Suggested answers',),
    }

    _defaults = {
        'score_calc_method': 'direct_sum',
    }
class survey_label(osv.Model):
    
    _inherit = 'survey.label'
    
    _columns = {
        'score': fields.integer('Score'),
        'matrix_answer_score_ids': fields.one2many('survey.matrix_answer_score', 'question_id',
            'Matrix Answer Score'),
    }
    
    _defaults = {
        'score': 0,
    }

class survey_user_input(osv.Model):
    
    _inherit = 'survey.user_input'

    _columns = {
    # TODO: ver si usamos la funcion get_score, el tema es que hay que poner store=true para poder usarlo en la vista, habria que ver cuando hay que actualizar los valores
        # 'score': fields.function(_get_score,'Score'),
        'score': fields.integer('Score'),
        'input_question_score_ids': fields.one2many('survey.user_input_question_score', 'user_input_id', string='Question Scores', readonly=True,),
        # 'manual_score': fields.related('survey_id', 'manual_score', string="Survey Manual Score?", type="boolean", readonly=True),
        # 'without_questions': fields.related('survey_id', 'without_questions', string="Survey Without Questions?", type="boolean", readonly=True),
        'evaluation_type': fields.related('survey_id', 'evaluation_type', string="Evaluation Type", type="char", readonly=True),
        # This one was replaced by without_questions functionality
        # 'designed': fields.related('survey_id', 'designed', string="Survey Is designed?", type="boolean", readonly=True),
    }

    _defaults = {
        'score': 0,
    }

    def compute_score(self, cr, uid, ids, context=None):
        if not context:
            context={}
        question_obj = self.pool['survey.question']
        user_input_lines_obj = self.pool.get('survey.user_input_line')
        uiqs_obj = self.pool.get('survey.user_input_question_score')
        for user_input in self.browse(cr, uid, ids, context=context):
            computed_score = 0
            question_ids = question_obj.search(
                cr, uid,
                [('survey_id', '=', user_input.survey_id.id),
                 ('max_score', '!=', 0)])
            for question in question_obj.browse(cr, uid, question_ids, context=context):
                user_input_lines_ids = user_input_lines_obj.search(cr, uid,
                    [('question_id', '=', question.id), ('user_input_id', '=', user_input.id)],
                    context=context)
                user_input_lines = user_input_lines_obj.browse(cr, uid, user_input_lines_ids, context=context)

                if question.type == 'simple_choice' or question.score_calc_method == 'direct_sum':
                    question_score = sum([self.get_answer_score(user_input_line) for user_input_line in user_input_lines])
                elif question.score_calc_method == 'ranges':
                    pre_score = sum([self.get_answer_score(user_input_line) for user_input_line in user_input_lines])
                    question_score = self.get_ranged_score(cr, uid, question, pre_score, context=context)

                computed_score += question_score

                uiqs_ids = uiqs_obj.search(cr, uid,
                    [('question_id', '=', question.id), ('user_input_id', '=', user_input.id)],
                    context=context)

                # Calculte score_percentage
                score_percentage = question_score * 100.0 / question.max_score 

                if uiqs_ids:
                    uiqs_obj.write(cr, uid, uiqs_ids[0], {'score': question_score,'score_percentage': score_percentage}, context=context)
                else:
                    uiqs_obj.create(cr, uid, {
                        'score': question_score,
                        'score_percentage': score_percentage,
                        'question_id': question.id,
                        'user_input_id': user_input.id,
                        }, context=context)    
            if user_input.survey_id.max_score and user_input.survey_id.max_score != 0:
                computed_score = computed_score * 100.0 / user_input.survey_id.max_score
            else: 
                computed_score = False
            print 'User Input Computed Score', computed_score
            self.write(cr, uid, user_input.id, {'score': computed_score})
        return True

    # TODO: desde la pregunta, buscar el rango de acuerdo al pre_score y retornar el score asociado. Sino retornar 0
    def get_ranged_score(self, cr, uid, question, pre_score, context=None):
        question_score_range_obj = self.pool.get('survey.question.score.range')
        question_score_range_ids = question_score_range_obj.search(cr, uid,
            [('from', '<=', pre_score), ('to', '>=', pre_score), ('survey_question_id', '=', question.id)],
            context=context)
        if not question_score_range_ids:
            return 0
        else:
            return question_score_range_obj.browse(cr, uid, question_score_range_ids[0], context=context).score

    def get_answer_score(self, user_input_line):
        if user_input_line.question_id.type in ['simple_choice', 'multiple_choice'] and user_input_line.value_suggested:
            return user_input_line.value_suggested.score
        elif user_input_line.question_id.type == 'numerical_box':
            return int(user_input_line.value_number)
        elif user_input_line.question_id.type == 'matrix' and user_input_line.value_suggested:
            for given_answer_score in user_input_line.value_suggested_row.matrix_answer_score_ids:
                if user_input_line.value_suggested.id == given_answer_score.answer_id.id:
                    return given_answer_score.score
        return 0

    def write(self, cr, uid, ids, vals, context=None):
        write_res = super(survey_user_input, self).write(cr, uid, ids, vals, context=context)
        # If score in context then score is being writed
        if vals.get('state')=='done' and 'score' not in vals:
            if isinstance(ids, (int, long)):
                ids = [ids]            
            print 'cuidado!!!!!'
            self.compute_score(cr, uid, ids, context=context)
        return write_res

class survey_user_input_question_score(osv.Model):
    _name = 'survey.user_input_question_score'
    _description = 'Score of a User Input by Question'
    _rec_name = 'score'

    _columns = {
        'question_id': fields.many2one('survey.question', 'Question', ondelete='cascade', required=True,),
        'user_input_id': fields.many2one('survey.user_input', 'User Input', ondelete='cascade', required=True,),
        'score': fields.integer('Score', required=True,),
        'score_percentage': fields.integer('Score %', required=True,),
    }

class survey_matrix_answer_score(osv.Model):
    _name = 'survey.matrix_answer_score'
    _description = 'Matrix Answer Score'
    _rec_name = 'score'

    _columns = {
        'score': fields.integer('Score', required=True,),
        'question_id': fields.many2one('survey.label', 'Question'),
        'answer_id': fields.many2one('survey.label', 'Answer', required=True,),
    }

    _defaults = {
        'score': 0,
    }

class survey_question_level(osv.Model):
    
    _name = 'survey.question.level'
    _description = 'Question Level'
    
    _columns = {
        'name': fields.char(string="Name", required=True, translate=True),
    }

class survey_level(osv.Model):
    
    _name = 'survey.level'
    _description = 'Survey Level'

    def name_get(self, cr, uid, ids, context=None):
        # always return the full hierarchical name
        res = self._complete_name(cr, uid, ids, 'complete_name', None, context=context)
        return res.items()

    def _complete_name(self, cr, uid, ids, name, args, context=None):
        """ Forms complete name of location from parent location to child location.
        @return: Dictionary of values
        """
        res = {}
        for line in self.browse(cr, uid, ids):
            name = line.level_id.name 
            res[line.id] = name
        return res 
    
    def _get_score(self, cr, uid, ids, name, args, context=None):
        ret = dict()
        for level in self.browse(cr, uid, ids, context=context):
            ret[level.id] = sum([question.max_score for question in level.question_ids])
        return ret

    _columns = {
        'level_id': fields.many2one('survey.question.level', string="Level", required=True, translate=True),
        'score': fields.function(_get_score, type='integer', string='Score', readonly=True,),
        'survey_id': fields.many2one('survey.survey', string='Survey', required=True,),
    }

    @api.one
    @api.depends('survey_id.page_ids.question_ids.level_id')
    def get_question_ids(self):
        self.question_ids = self.env['survey.question'].search(
            [('page_id.survey_id', '=', self.survey_id.id),
             ('level_id', '=', self.level_id.id)])

    question_ids = new_fields.One2many(
        'survey.question',
        compute='get_question_ids',
        string='Questions',)

class survey_question_content(osv.Model):
    
    _name = 'survey.question.content'
    _description = 'Question Content'
    
    _columns = {
        'name': fields.char(string="Name", required=True, translate=True),
    }

class survey_content(osv.Model):
    
    _name = 'survey.content'
    _description = 'Survey Content'

    def name_get(self, cr, uid, ids, context=None):
        # always return the full hierarchical name
        res = self._complete_name(cr, uid, ids, 'complete_name', None, context=context)
        return res.items()

    def _complete_name(self, cr, uid, ids, name, args, context=None):
        """ Forms complete name of location from parent location to child location.
        @return: Dictionary of values
        """
        res = {}
        for line in self.browse(cr, uid, ids):
            name = line.content_id.name 
            res[line.id] = name
        return res 

    def _get_score(self, cr, uid, ids, name, args, context=None):
        ret = dict()
        for level in self.browse(cr, uid, ids, context=context):
            ret[level.id] = sum([question.max_score for question in level.question_ids])
        return ret

    _columns = {
        'content_id': fields.many2one('survey.question.content', string="Content", required=True, translate=True),
        'score': fields.function(_get_score, type='integer', string='Score', readonly=True,),
        'survey_id': fields.many2one('survey.survey', string='Survey', required=True,),
    }

    @api.one
    @api.depends('survey_id.page_ids.question_ids.content_id')
    def get_question_ids(self):
        self.question_ids = self.env['survey.question'].search(
            [('page_id.survey_id', '=', self.survey_id.id),
             ('content_id', '=', self.content_id.id)])

    question_ids = new_fields.One2many(
        'survey.question',
        compute='get_question_ids',
        string='Questions',)


class survey_question_objective(osv.Model):
    
    _name = 'survey.question.objective'
    _description = 'Question Objective'
    
    _columns = {
        'name': fields.char(string="Name", required=True, translate=True),
    }

class survey_objective(osv.Model):
    
    _name = 'survey.objective'
    _description = 'Survey Objective'

    def name_get(self, cr, uid, ids, context=None):
        # always return the full hierarchical name
        res = self._complete_name(cr, uid, ids, 'complete_name', None, context=context)
        return res.items()

    def _complete_name(self, cr, uid, ids, name, args, context=None):
        """ Forms complete name of location from parent location to child location.
        @return: Dictionary of values
        """
        res = {}
        for line in self.browse(cr, uid, ids):
            name = line.objective_id.name 
            res[line.id] = name
        return res 
    
    def _get_score(self, cr, uid, ids, name, args, context=None):
        ret = dict()
        for objective in self.browse(cr, uid, ids, context=context):
            ret[objective.id] = sum([question.max_score for question in objective.question_ids])
        return ret

    _columns = {
        'objective_id': fields.many2one('survey.question.objective', string="Objective", required=True, translate=True),
        'score': fields.function(_get_score, type='integer', string='Score', readonly=True,),
        'survey_id': fields.many2one('survey.survey', string='Survey', required=True, ondelete='cascade'),
    }

    @api.one
    @api.depends('survey_id.page_ids.question_ids.objective_id')
    def get_question_ids(self):
        self.question_ids = self.env['survey.question'].search(
            [('page_id.survey_id', '=', self.survey_id.id),
             ('objective_id', '=', self.objective_id.id)])

    question_ids = new_fields.One2many(
        'survey.question',
        compute='get_question_ids',
        string='Questions',)

class survey_survey(osv.Model):

    _inherit = 'survey.survey'

    def _get_scores(self, cr, uid, ids, names, arg, context=None):
        res = dict([(id, {'max_score':0, 
            'obj_questions_score':0, 
            'level_questions_score':0,
            'non_obj_questions_score':0,
            'non_level_questions_score':0,
            }) for id in ids])
        for survey in self.browse(cr, uid, ids, context=context):
            content_questions_score = sum([content.score for content in survey.question_content_ids])
            res[survey.id]['content_questions_score'] = content_questions_score
            non_content_questions_ids = self.pool.get('survey.question').search(cr, uid, [('survey_id','=',survey.id),('content_id','=',False)],context=context)
            non_content_questions = self.pool.get('survey.question').browse(cr, uid, non_content_questions_ids, context=context)
            non_content_questions_score = sum([question.max_score for question in non_content_questions])
            res[survey.id]['non_content_questions_score'] = non_content_questions_score
                        
            obj_questions_score = sum([objective.score for objective in survey.question_objective_ids])
            res[survey.id]['obj_questions_score'] = obj_questions_score
            non_obj_questions_ids = self.pool.get('survey.question').search(cr, uid, [('survey_id','=',survey.id),('objective_id','=',False)],context=context)
            non_obj_questions = self.pool.get('survey.question').browse(cr, uid, non_obj_questions_ids, context=context)
            non_obj_questions_score = sum([question.max_score for question in non_obj_questions])
            res[survey.id]['non_obj_questions_score'] = non_obj_questions_score
            
            level_questions_score = sum([level.score for level in survey.question_level_ids])
            res[survey.id]['level_questions_score'] = level_questions_score
            non_level_questions_ids = self.pool.get('survey.question').search(cr, uid, [('survey_id','=',survey.id),('level_id','=',False)],context=context)            
            non_level_questions = self.pool.get('survey.question').browse(cr, uid, non_level_questions_ids, context=context)
            non_level_questions_score = sum([question.max_score for question in non_level_questions])
            res[survey.id]['non_level_questions_score'] = non_level_questions_score
            
            res[survey.id]['max_score'] = obj_questions_score + non_obj_questions_score
        return res

    _columns = {
        'time_allocated': fields.float("Time Allocated?",),
        'is_evaluation': fields.boolean("Is Evaluation?",),
        'evaluation_type': fields.selection([('automatically_evaluated', 'Automatically Evaluated'),
            ('manually_evaluated','Manually Evaluated'),],
            string="Evaluation Type",
            help="-Automattically Evaluated: you have to set espected question results and the evaluation will be evaluated automatically.\
                \n-Manually Evaluated: someone will need to correct the evaluation and complete with the score."),
        # 'evaluation_type': fields.selection([('automatically_evaluated', 'Automatically Evaluated'),
        #     ('manually_evaluated','Manually Evaluated'),
        #     ('only_score', 'Only Score')],
        #     string="Evaluation Type",
        #     help="-Automattically Evaluated: you have to set espected question results and the evaluation will be evaluated automatically.\
        #         \n-Manually Evaluated: someone will need to correct the evaluation and complete with the score.\
        #         \n-Only Score: Evaluations without questions and that should be manually evaluated. For example, you can make evaluations without questions just to enter results from evaluations make outside this system."),
        'question_objective_ids': fields.one2many('survey.objective', 'survey_id',
            string='Questions Objectives', copy=True),
        'question_level_ids': fields.one2many('survey.level', 'survey_id',
            string='Questions Levels', copy=True),
        'question_content_ids': fields.one2many('survey.content', 'survey_id',
            string='Questions Contents', copy=True),
        'obj_questions_score': fields.function(_get_scores, type='integer', string='Objetives Score', help='Score for questions with objetive defined', multi='_get_scores', ),
        'non_obj_questions_score': fields.function(_get_scores, type='integer', string='Other Questions Score', help='Score for questions without objetive defined', multi='_get_scores', ),
        'content_questions_score': fields.function(_get_scores, type='integer', string='Contents Score', help='Score for questions with content defined', multi='_get_scores', ),
        'non_content_questions_score': fields.function(_get_scores, type='integer', string='Other Questions Score', help='Score for questions without content defined', multi='_get_scores', ),
        'level_questions_score': fields.function(_get_scores, type='integer', string='Levels Score', help='Score for questions with level defined', multi='_get_scores', ),
        'non_level_questions_score': fields.function(_get_scores, type='integer', string='Other Questions Score', help='Score for questions without level defined', multi='_get_scores', ),
        'max_score': fields.function(_get_scores, type='integer', string='Max Score',
            help='Maximum score that can be obtained in this evaluation', multi='_get_scores', ),
    }

    _defaults = {
        'evaluation_type': 'automatically_evaluated',
    }
    # Metodo por si queremos recalcular todos los score
    def compute_score(self, cr, uid, ids, context=None):    
        user_input_obj = self.pool['survey.user_input']
        total_user_input_ids = user_input_obj.search(
            cr, uid, [('survey_id', 'in', ids)], order='id', context=context)
        print 'len total_user_input_ids', len(total_user_input_ids)
        user_input_obj.compute_score(cr, uid, total_user_input_ids, context=context)
        return total_user_input_ids