# -*- coding: utf-8 -*-
from openerp import fields, models, api


class partner(models.Model):

    """"""

    _inherit = 'res.partner'

    course_average_classrooms = fields.Integer(
        string='Average Classrooms per Course')
    classrooms_average_students = fields.Integer(
        string='Average Students per Classroom')
    course_ids = fields.Many2many(
        'res.partner.course',
        'res_partner_course_rel',
        'partner_id',
        'course_id',
        string='Courses')

    @api.one
    @api.depends(
        'course_ids',
        'classrooms_average_students',
        'course_average_classrooms')
    def _get_totals(self):
        courses_total = len(self.course_ids)
        classrooms_total = courses_total * self.course_average_classrooms or 0
        classrooms_average_students = self.classrooms_average_students
        students_total = classrooms_total * classrooms_average_students or 0
        self.courses_total = courses_total
        self.classrooms_total = classrooms_total
        self.students_total = students_total

    courses_total = fields.Integer(
        compute='_get_totals',
        string='Courses Total',
        readonly=True,
        store=True,)
    classrooms_total = fields.Integer(
        compute='_get_totals',
        string='Classrooms total',
        readonly=True,
        store=True)
    students_total = fields.Integer(
        compute='_get_totals',
        string='Students total',
        readonly=True,
        store=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
