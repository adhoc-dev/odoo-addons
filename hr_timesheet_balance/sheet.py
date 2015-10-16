from openerp import fields, models, api


class sheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    theoretical_hours = fields.Float(
        'Theoretical hours',
        store=True
    )
    theoretical_difference = fields.Float(
        'Theoretical difference',
        compute='_get_theoretical_difference',
        store=True
    )

    @api.one
    @api.depends(
        'theoretical_hours',
        'total_timesheet',
        'timesheet_ids.unit_amount')
    def _get_theoretical_difference(self):
        self.theoretical_difference = self.total_timesheet - \
            self.theoretical_hours
