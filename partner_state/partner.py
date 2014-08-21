# -*- coding: utf-8 -*-

from openerp import models, fields, api, _


class res_partner(models.Model):
    _inherit = 'res.partner'

    state = fields.Selection([
        ('potential', 'Potential'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved')],
        string='State',
        readonly=True,
        required=True,
        default='potencial')


    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list):
            ids = [ids]

        ret = super(res_partner, self).write(
            cr, uid, ids, vals, context=context)

        return_to_potential_fields = set(['name', 'property_account_position', 'vat', 'property_product_pricelist',
                                          'property_payment_term'])

        if return_to_potential_fields.intersection(set(vals.keys())) and 'state' not in vals:
            for partner in self.browse(cr, uid, ids, context=context):
                if partner.state and partner.state == 'pending':
                    wf_service = netsvc.LocalService("workflow")
                    wf_service.trg_validate(
                        uid, 'res.partner', partner.id, 'partner_pending_2_potential', cr)
                elif partner.state and partner.state == 'approved':
                    wf_service = netsvc.LocalService("workflow")
                    wf_ret = wf_service.trg_validate(
                        uid, 'res.partner', partner.id, 'partner_approved_2_potential', cr)

        return ret

    def partner_state_potential(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'potential'})
        return True

    def partner_state_pending(self, cr, uid, ids, context=None):
        self.check_fields(cr, uid, ids, 'Pendiente de Aprobación')
        self.write(cr, uid, ids, {'state': 'pending'})
        return True

    def partner_state_approved(self, cr, uid, ids, context=None):
        user_obj = self.pool.get('res.users')
        user = user_obj.browse(cr, uid, uid, context=context)
        if isinstance(user, list):
            user = user[0]

        user_can_approve_partners = False
        for group in user.groups_id:
            if group.name == 'Approve Partners':
                user_can_approve_partners = True
                break
        if not user_can_approve_partners:
            raise osv.except_osv('Permisos insuficientes',
                                 'No cuenta con los permisos indicados para Aprobar Partners.')

        self.check_fields(cr, uid, ids, 'Aprobado')
        self.write(cr, uid, ids, {'state': 'approved'})
        return True

    # Checkear los campos antes de realizar alguna transición
    def check_fields(self, cr, uid, ids, proximo_estado):
        titulo_alerta = 'No se puede pasa el Cliente al estado ' + \
            proximo_estado

        for partner in self.browse(cr, uid, ids):
            # Archivo adjunto 'constancia.pdf' definido
            attachment_ids = self.pool.get('ir.attachment').search(cr, uid,
                                                                   [('res_model', '=', 'res.partner'), ('res_id', '=', partner.id), ('datas_fname', '=', 'constancia.pdf')])
            if not attachment_ids:
                raise osv.except_osv(titulo_alerta,
                                     'El cliente no puede ser pasado al estado ' + proximo_estado +
                                     ' si no tiene adjunto el archivo \'constancia.pdf\'.')

            # Comercial definido
            if not partner.user_id:
                raise osv.except_osv(titulo_alerta,
                                     'El cliente no puede ser pasado al estado ' + proximo_estado + ' si no tiene definido el Comercial.')

            # Equipo de Venta definido
            if not partner.section_id:
                raise osv.except_osv(titulo_alerta,
                                     'El cliente no puede ser pasado al estado ' + proximo_estado + ' si no tiene definido el Equipo de Venta.')

            # Posición Fiscal definida
            if not partner.property_account_position:
                raise osv.except_osv(titulo_alerta,
                                     'El cliente no puede ser pasado al estado ' + proximo_estado + ' si no tiene definido la Posición Fiscal.')

            # CUIT definido
            if not partner.vat:
                raise osv.except_osv(titulo_alerta,
                                     'El cliente no puede ser pasado al estado ' + proximo_estado + ' si no tiene definido el CUIT (CIF/NIF).')

            # Al menos una Dirección por defecto o de facturación con
            # localidad, dirección y CP definida
            address_definido = False
            for address in partner.address:
                if address.type == "default" or address.type == "invoice":
                    if address.street and address.zip and address.city:
                        address_definido = True
                        break

            if not address_definido:
                raise osv.except_osv(titulo_alerta,
                                     'El cliente no puede ser pasado al estado ' + proximo_estado + ' si no tiene definido al menos ' +
                                     'una dirección por defecto o de facturación que contengan una calle, código postal y ciudad.')

            # Tarifa de Venta definido
            if not partner.property_product_pricelist:
                raise osv.except_osv(titulo_alerta,
                                     'El cliente no puede ser pasado al estado ' + proximo_estado + ' si no tiene definida la Tarifa de Venta.')

            # Al menos una Categoria definida
            if not partner.category_id:
                raise osv.except_osv(titulo_alerta,
                                     'El cliente no puede ser pasado al estado ' + proximo_estado +
                                     ' si no tiene asignada al menos una Categoría.')