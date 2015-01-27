# -*- coding: utf-8 -*-
from openerp import models


class task(models.Model):
    _inherit = 'project.task'

    def create(self, cr, uid, vals, context=None):

        task_id = super(task, self).create(cr, uid, vals, context=context)

        partner_to_unfollow_ids = []
        for partner in self.browse(
                cr, uid, task_id, context=context).message_follower_ids:
            if partner.user_ids:
                for user in partner.user_ids:
                    if not self.pool['res.users'].has_group(
                            cr, user.id, 'base.group_user'):
                        partner_to_unfollow_ids.append(partner.id)
                        continue
            else:
                partner_to_unfollow_ids.append(partner.id)
        self.message_unsubscribe(
            cr, uid, [task_id], partner_to_unfollow_ids, context=None)
        return task_id
