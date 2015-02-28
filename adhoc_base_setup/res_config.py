# -*- coding: utf-8 -*-
from openerp import models, fields


class adhoc_base_configuration(models.TransientModel):
    _name = 'adhoc.base.config.settings'
    _inherit = 'res.config.settings'

    # Fixes
    module_mail_sender_patch = fields.Boolean(
        'Patch mail sender when using own smtp server instead of localhost',
        help="""Installs the mail_sender_patch module.""")
    module_portal_fix = fields.Boolean(
        'Fix company assigne on portal user creation from partner (assign partner company)',
        help="""Installs the portal_fix module.""")

    # Usability and tools modules
    module_web_recipients_uncheck = fields.Boolean(
        'Uncheck recipients on res.partner',
        help="""Installs the web_recipients_uncheck module.""")
    module_web_sheet_full_width = fields.Boolean(
        'Use the whole available screen width when displaying sheets',
        help="""Installs the web_sheet_full_width module.""")
    module_web_ckeditor4 = fields.Boolean(
        'Provides a widget for editing HTML fields using CKEditor 4.x',
        help="""Installs the module_web_ckeditor4 module.""")
    module_web_group_expand = fields.Boolean(
        'Allow group by lists to be expanded and collapased with buttons',
        help="""Installs the web_group_expand module.""")
    module_document_url = fields.Boolean(
        'Allow to attach an URL as a document.',
        help="""Installs the document_url module.""")
    module_help_doc = fields.Boolean(
        'Install Help Documentation',
        help="""Installs the help_doc module.""")
    module_mass_editing = fields.Boolean(
        'Mass Editing',
        help="""Installs the mass_editing module.""")
    module_help_online = fields.Boolean(
        'Allows the creation of an online help available from the lists and forms in Odoo.',
        help="""Installs the help_online module.""")
    module_web_m2x_options = fields.Boolean(
        'Modifies "many2one" and "many2manytags" form widgets so as to add some new display control options.',
        help="""Installs the web_m2x_options module.""")
    module_web_export_view = fields.Boolean(
        'Web Export View. Export to csv',
        help="""Installs the web_export_view module.""")
    module_attachment_preview = fields.Boolean(
        'The module adds a little print preview icon right of download links for attachments or binary fields',
        help="""Installs the attachment_preview module.""")
    module_document_url = fields.Boolean(
        'Module that allows to attach an URL as a document.',
        help="""Installs the document_url module.""")

    # Technical
    module_auth_admin_passkey = fields.Boolean(
        'Use admin password as a passkey for all active logins',
        help="""Installs the auth_admin_passkey module.""")
    module_adhoc_support = fields.Boolean(
        'Use ADHOC support',
        help="""Installs the adhoc_support module.""")
    module_cron_run_manually = fields.Boolean(
        'Enable Run Cron Manually',
        help="""Installs the cron_run_manually module.""")
    module_disable_openerp_online = fields.Boolean(
        'Disable OpenERP Online',
        help="""Installs the disable_openerp_online module.""")
    module_auth_server_admin_passwd_passkey = fields.Boolean(
        'Allow database login with instance admin password',
        help="""Installs the auth_server_admin_passwd_passkey module.""")

    # Partner modules
    module_partner_vat_unique = fields.Boolean(
        'Add a constraint on partners so that vat must be unique except in partner with parent/child relationship.',
        help="""Installs the partner_vat_unique module.""")
    module_partner_person = fields.Boolean(
        'Add person information to partners.',
        help="""Installs the partner_person module. Add firstname, lastname, birthdate, etc.""")
    module_partner_social_fields = fields.Boolean(
        'Add social fields to partners',
        help="""Installs the partner_social_fields module.""")
    module_base_state_active = fields.Boolean(
        'Hide USA states and add active field for states',
        help="""Installs the base_state_active module.""")
    module_partner_views_fields = fields.Boolean(
        'Add Fields on Partners Views',
        help="""Installs the partner_views_fields module.""")
    module_partner_search_by_ref = fields.Boolean(
        'Search Partners by Reference',
        help="""Installs the partner_search_by_ref module.""")
    module_partner_search_by_vat = fields.Boolean(
        'Search Partners by VAT',
        help="""Installs the partner_search_by_vat module.""")
    module_partner_state = fields.Boolean(
        'Manage different states on partners',
        help="""Installs the partner_state module.""")
    module_partner_school = fields.Boolean(
        'Manage School Data on partners',
        help="""Installs the partner_school module.""")
    module_partner_credit_limit = fields.Boolean(
        'Restrict credit limit edition on partners and restrict sale orders approval for partners without credit',
        help="""Installs the partner_credit_limit module.""")
