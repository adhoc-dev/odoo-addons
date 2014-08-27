# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.osv import fields as old_fields
from openerp.exceptions import except_orm, Warning, RedirectWarning


class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_partner_states(self):
        return [
            ('potential', _('Potential')),
            ('pending', _('Pending Approval')),
            ('approved', _('Approved'))]

    # Usamos la api vieja porque si no da error en permisos
    # company_partner_state = fields.Boolean(
    #     related='company_id.partner_state',
    #     string="Company Partner State")
    _columns = {
        'company_partner_state': old_fields.related('company_id', 'partner_state', type='boolean'),
    }

    partner_state = fields.Selection(
        '_get_partner_states',
        string='Partner State',
        readonly=True,
        required=True,
        default='potential')

    def write(self, cr, uid, ids, vals, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.partner_state in ['approved', 'pending']:
                fields = self.check_fields(
                    cr, uid, partner.id, 'track', context=context)
                if fields:
                    fields_set = set(fields)
                    vals_set = set(vals)
                    if fields_set & vals_set:
                        partner.partner_state_potential()

        ret = super(res_partner, self).write(
            cr, uid, ids, vals, context=context)

        return ret

    @api.multi
    def partner_state_potential(self):
        self.partner_state = 'potential'

    @api.multi
    def partner_state_pending(self):
        fields = self.check_fields('approval')
        if fields:
            partners_read = self.read(fields)
            for partner_read in partners_read:
                for partner_field in partner_read:
                    if not partner_read[partner_field]:
                        raise Warning(
                            _("Can not request approval, \
                                required field %s empty on partner id %i!"
                                % (partner_field, partner_read['id'])))
        self.partner_state = 'pending'

    @api.multi
    def partner_state_approved(self):
        self.check_partner_approve()
        self.partner_state = 'approved'

    @api.multi
    def check_partner_approve(self):
        user_can_approve_partners = self.env[
            'res.users'].has_group('partner_state.approve_partners')
        print 'user_can_approve_partners', user_can_approve_partners
        if not user_can_approve_partners:
            raise Warning(
                _("User can't approve partners, \
                    please check user permissions!"))
        return True

    @api.multi
    def check_fields(self, field_type):
        ret = False
        if self.company_id.partner_state:
            company_field_ids = self.company_id.partner_state_field_ids
            if field_type == 'approval':
                ret = [field.field_id.name for field in company_field_ids if field.approval]
            elif field_type == 'track':
                ret = [field.field_id.name for field in company_field_ids if field.track]
        return ret