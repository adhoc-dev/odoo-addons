# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class adhoc_base_configuration(models.TransientModel):
    _inherit = 'adhoc.base.config.settings'

    # Project
    module_project_issue_views_modifications = fields.Boolean(
        'Simplify issue views',
        help="""Installs the project_issue_views_modifications module.""")
    module_project_issue_solutions = fields.Boolean(
        'Project Issue Solutions',
        help="""Installs the project_issue_solutions module.""")
    module_project_alert_upcoming_tasks = fields.Boolean(
        'Alert upcoming task',
        help="""Installs the project_alert_upcoming_tasks module.""")
    module_project_description = fields.Boolean(
        'Use description on projects',
        help="""Installs the project_description module.""")
    module_project_issue_create_task_defaults = fields.Boolean(
        'Use issue task information on creating a task from an issue',
        help="""Installs the project_issue_create_task_defaults module.""")
    module_project_issue_product = fields.Boolean(
        'Relate issues to products (and viceversa)',
        help="""Installs the project_issue_product module.""")
    module_project_task_order = fields.Boolean(
        'Change default tasks order to "priority desc, sequence, date_deadline, planned_hours, date_start, create_date desc"',
        help="""Installs the project_task_order module.""")
    module_project_issue_order = fields.Boolean(
        'Add sequence field to issues and change default order to "priority desc, sequence, date_deadline, duration, create_date desc"',
        help="""Installs the project_issue_order module.""")
    module_project_task_issues = fields.Boolean(
        'Add Issue in to task view',
        help="""Installs the project_task_issues module.""")
    module_project_tags = fields.Boolean(
        'Add Tags on Projects',
        help="""Installs the project_tags module.""")
    module_project_task_desc_html = fields.Boolean(
        'Changes description type on tasks to html',
        help="""Installs the project_task_desc_html module.""")
    module_project_task_phase = fields.Boolean(
        'Add project phases to tasks',
        help="""Installs the project_task_phase module.""")
    module_project_task_portal_unfollow = fields.Boolean(
        'Add functionality "not add to the task supporters of the project that do not have the activated field employee"',
        help="""Installs the project_task_portal_unfollow module.""")
    module_project_task_phase = fields.Boolean(
        'Add project phases to tasks',
        help="""Installs the project_task_phase module.""")
    module_project_user_story = fields.Boolean(
        'Project User Stories.',
        help="""Installs the project_user_story module.""")
    module_project_stage = fields.Boolean(
        'Add stages to projects.',
        help="""Installs the project_stage module.""")
    module_project_kanban_open_project = fields.Boolean(
        'Open the form view of a project by clicking on the view KanBan.',
        help="""Installs the project_kanban_open_project module.""")
    module_project_category = fields.Boolean(
        'Add categories to projects.',
        help="""Installs the project_category module.""")
    module_project_task_activity = fields.Boolean(
        'Add Activities to task.',
        help="""Installs the project_task_activity module.""")
