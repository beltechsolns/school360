from odoo import models, fields


class School360ThreadMixin(models.AbstractModel):
    _name = 'school360.thread.mixin'
    _description = 'School360 Logging & Activity Mixin'
    _inherit = ['mail.thread', 'mail.activity.mixin']
