# -*- coding: utf-8 -*-


import openerp.tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

from datetime import datetime, timedelta

date_format = '%Y-%m-%d'
#date_format = '%Y-%m-%d %H:%M:%S'

class res_users(osv.Model):
    _inherit = 'res.users'
    
    def send_project_alert_upcomming_tasks_from_button(self, cr, uid, ids, context=None):
        all_user_ids = self.search(cr, uid, [], context=context)
        self.send_project_alert_upcomming_tasks_to_users(cr, uid, all_user_ids, 7, context=context)
        return True
        
    
    def send_project_alert_upcomming_tasks(self, cr, uid, upcoming_days, context=None):
        all_user_ids = self.search(cr, uid, [], context=context)
        self.send_project_alert_upcomming_tasks_to_users(cr, uid, all_user_ids, upcoming_days, context=context)
        return True
        
    def send_project_alert_upcomming_tasks_to_users(self, cr, uid, ids, upcoming_days, context=None):
        task_obj = self.pool.get('project.task')
        
        for user in self.browse(cr, 1, ids, context=context):
            filters = [('user_id', '=', user.id), ('state', 'in', ('open', 'pending'))]
            task_ids = task_obj.search(cr, 1, filters, order='date_late_finish', context=context)
            
            task_due = []
            overdue_tasks = []
            
            for task in task_obj.browse(cr, 1, task_ids, context=context):
                if not task.date_late_finish:
                    continue
                
                now = datetime.now()
                date_late_finish = datetime.strptime(task.date_late_finish, "%Y-%m-%d")
                now_plus_upcoming_days = now + timedelta(days=upcoming_days)
                
                if date_late_finish <= now:
                    overdue_tasks.append(task)
                elif now < date_late_finish and date_late_finish <= now_plus_upcoming_days:
                    task_due.append(task)
            
            if not task_due and not overdue_tasks:
                continue
            
            base_url = self.pool.get('ir.config_parameter').get_param(cr, 1, 'web.base.url')
            action_id = self.pool.get('ir.model.data').get_object_reference(cr, 1, 'project', 'action_view_task')[1]
            
            subject = 'Tasks coming due'
            body = ''
            
            if task_due:
                body += '<ul>'
                body += '<li>Tasks due in ' + str(upcoming_days) + ' days</li>'
                body += '<ul>'
                for task in task_due:
                    body += '<li>'
                    
                    body += '<a href="' + base_url + '/#action=' + str(action_id) + '&id=' + str(task.id) + '&view_type=form">'
                    body += task.name
                    body += '</a>'
                    
                    if task.project_id:
                        body += ' - ' + task.project_id.name
                    body += ' - ' + datetime.strptime(task.date_late_finish, "%Y-%m-%d").strftime("%Y/%m/%d")
                    body += '</li>'
                
                body += '</ul>'
                body += '</ul>'
            
            if overdue_tasks:
                body += '<ul>'
                body += '<li>Overdue tasks</li>'
                body += '<ul>'
                for task in overdue_tasks:
                    body += '<li>'
                    
                    body += '<a href="' + base_url + '/#action=' + str(action_id) + '&id=' + str(task.id) + '&view_type=form">'
                    body += task.name
                    body += '</a>'
                    
                    if task.project_id:
                        body += ' - ' + task.project_id.name
                    body += ' - ' + datetime.strptime(task.date_late_finish, "%Y-%m-%d").strftime("%Y/%m/%d")
                    body += '</li>'
                
                body += '</ul>'
                body += '</ul>'
            
            post_values = {
                'subject': subject,
                'body': body,
                'partner_ids': [user.partner_id.id]}

            subtype = 'mail.mt_comment'
            
            thread_obj = self.pool.get('mail.thread')
            thread_obj.message_post(cr, 1, [0], type='comment', subtype=subtype, context=context, **post_values)
        return True
    
res_users()



