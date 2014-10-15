# -*- coding: utf-8 -*-
from openerp import models
from openerp.osv import fields, osv
from openerp.tools.translate import _
import conversor


class Report(models.Model):
    _inherit = 'report'

    def get_html(self, cr, uid, ids, report_name, data=None, context=None):
        # TODO mejorar este metodo para que sea "heredado"
        """This method generates and returns html version of a report.
        """
        # If the report is using a custom model to render its html, we must use it.
        # Otherwise, fallback on the generic html rendering.
        try:
            report_model_name = 'report.%s' % report_name
            particularreport_obj = self.pool[report_model_name]
            return particularreport_obj.render_html(cr, uid, ids, data=data, context=context)
        except KeyError:
            def to_word(val):
                return conversor.to_word(val)
            report = self._get_report_from_name(cr, uid, report_name)
            report_obj = self.pool[report.model]
            docs = report_obj.browse(cr, uid, ids, context=context)
            docargs = {
                'doc_ids': ids,
                'doc_model': report.model,
                'docs': docs,
                'report': report,
                'to_word': to_word,
            }
            # We add all the key-value pairs of the report configuration
            for report_conf_line in report.line_ids:
                if report_conf_line.value_type == 'text':
                    docargs.update(
                        {report_conf_line.name: report_conf_line.value_text})
                elif report_conf_line.value_type == 'boolean':
                    docargs.update(
                        {report_conf_line.name: report_conf_line.value_boolean})
            return self.render(cr, uid, [], report.report_name, docargs, context=context)


class ir_actions_report(models.Model):
    _inherit = 'ir.actions.report.xml'

    _columns = {
        'sequence': fields.integer('Sequence', help="Used to order priority of reports"),
        'line_ids': fields.one2many('report.configuration.line', 'report_id',
                                    string='Configuration lines'),
        'print_logo': fields.selection([('no_logo', 'Do not print log'),
                                        ('company_logo', 'Company Logo'),
                                        ('specified_logo', 'Specified Logo')], 'Print Logo', required=True),
        'logo': fields.binary('Logo'),
        'use_background_image': fields.boolean('Use Background Image'),
        'background_image': fields.binary('Background Image'),
        'company_id': fields.many2one('res.company', 'Company', change_default=True),
    }

    _defaults = {
        'print_logo': 'no_logo',
        'company_id': False,
        'sequence': 10,
    }

    def get_report_name(self, cr, uid, model, model_ids, context=None):
        report = self.get_report(cr, uid, model, model_ids, context=context)
        return report.report_name

    def get_report(self, cr, uid, model, model_ids, context=None):
        record = self.pool[model].browse(cr, uid, model_ids, context=context)
        # TODO que pasa cuando se quieren imprimir varios invoice?
        if isinstance(record, list):
            record = record[0]
        domains = self.get_domains(cr, model, record, context=context)


        # TODO habria que mejorar esto porque se podria recibir un listado de
        # ids con distintas cias
        active_model_obj = self.pool.get(model)
        active_object = active_model_obj.browse(
            cr, uid, model_ids, context=context)
        if hasattr(active_object, 'company_id') and active_object[0].company_id:
            company = active_object.company_id
        else:
            company = self.pool['res.users'].browse(
                cr, uid, uid, context=context).company_id
        for domain in domains:
            domain.append(('model', '=', model))

            # Search for company specific
            domain_with_company = domain + [('company_id', '=', company.id)]
            report_ids = self.search(
                cr, uid, domain_with_company,
                order='sequence', context=context)
            if report_ids:
                break

            # If not company specific, then for any company (allowed to the user)
            report_ids = self.search(
                cr, uid, domain, order='sequence', context=context)
            if report_ids:
                break
        if report_ids:
            report = self.browse(cr, uid, report_ids[0], context=context)
        else:
            title = _('No report defined')
            message = _('There is no report defined for this conditions.')
            raise osv.except_osv(title, message)
        return report

    def get_domains(self, cr, model, record, context=None):
        return []

    def update_lines_that_apply(self, cr, uid, ids, context=None):
        key_value_obj = self.pool.get('report.configuration.default')
        conf_line_obj = self.pool.get('report.configuration.line')

        all_ids = key_value_obj.search(cr, uid, [], context=context)
        for report in self.browse(cr, uid, ids, context=context):
            conf_line_name_id = {}
            for line in report.line_ids:
                conf_line_name_id[line.name] = line.id

            for key_value in key_value_obj.browse(cr, uid, all_ids, context=context):
                if key_value.apply_to_all or key_value.apply_to_model_id.model == report.model:
                    vals = {'name': key_value.name, 'report_id': report.id}
                    if key_value.value_type == 'text':
                        vals['value_type'] = 'text'
                        vals['value_text'] = key_value.value_text
                    elif key_value.value_type == 'boolean':
                        vals['value_type'] = 'boolean'
                        vals['value_boolean'] = key_value.value_boolean

                    if conf_line_name_id.get(key_value.name, False):
                        if key_value.override_values:
                            line_id = conf_line_name_id[key_value.name]
                            conf_line_obj.write(
                                cr, uid, [line_id], vals, context=context)
                    else:
                        conf_line_obj.create(cr, uid, vals, context=context)

    def create(self, cr, uid, vals, context=None):
        '''
        When a Report is created, we add the default keys.
        '''
        id = super(ir_actions_report, self).create(
            cr, uid, vals, context=context)
        no_key_lines = context.get('no_key_lines', False)
        if not no_key_lines:
            self.update_lines_that_apply(cr, uid, [id], context=context)
        return id


class report_configuration_line(models.Model):
    _name = 'report.configuration.line'
    _description = 'Line of the configuration information'

    _columns = {
        'name': fields.char('Key', size=256, required=True),
        'value_type': fields.selection([('text', 'Text'), ('boolean', 'Boolean')], 'Value Type', required=True),
        'value_text': fields.text('Value', required=False, translate=False),
        # 'value_text': fields.text('Value', required=False, translate=True),
        'value_boolean': fields.boolean('Value', required=False),
        'report_id': fields.many2one('ir.actions.report.xml', 'Report', required=True, ondelete='cascade'),
    }


class configuration_default(models.Model):
    _name = 'report.configuration.default'
    _description = 'Default Keys For Reports'

    _columns = {
        'name': fields.char('Key', size=256, required=True),
        'apply_to_all': fields.boolean(string='Apply To All Models',),
        'apply_to_model_id': fields.many2one('ir.model', string='Apply To Model', required=False),
        'override_values': fields.boolean('Override Values', help='If true, override values in already created Aeroo Report Configuration when saved.'),
        'value_type': fields.selection([('text', 'Text'), ('boolean', 'Boolean')], 'Value Type', required=True),
        'value_text': fields.text('Value', required=False, translate=False),
        # 'value_text': fields.text('Value', required=False, translate=True),
        'value_boolean': fields.boolean('Value', required=False),
    }

    _defaults = {
        'override_values': False,
        'apply_to_all': True,
    }

    # def create(self, cr, uid, vals, context=None):
    #     ids = super(configuration_default, self).create(cr, uid, vals, context=context)

    #     configuration_obj = self.pool.get('ir.actions.report.xml')
    # configuration_obj = self.pool.get('report.configuration')
    #     conf_ids = False
    #     if vals['apply_to_all'] == True:
    #         conf_ids = configuration_obj.search(cr, uid, [], context=context)
    #     else:
    #         conf_ids = configuration_obj.search(cr, uid, [('model', '=', vals['apply_to_model_id'])], context=context)

    #     configuration_obj.update_lines_that_apply(cr, uid, conf_ids, context=context)

    #     return ids

    # def write(self, cr, uid, ids, vals, context=None):
    #     super(configuration_default, self).write(cr, uid, ids, vals, context=context)

    #     for default_vk in self.browse(cr, uid, ids, context=context):
    #         configuration_obj = self.pool.get('ir.actions.report.xml')
    #         conf_ids = False
    #         if default_vk.apply_to_all == True:
    #             conf_ids = configuration_obj.search(cr, uid, [], context=context)
    #         else:
    #             conf_ids = configuration_obj.search(cr, uid, [('report_model_id', '=', default_vk.apply_to_model_id)], context=context)

    #         configuration_obj.update_lines_that_apply(cr, uid, conf_ids, context=context)

    #     return ids
