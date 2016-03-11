# -*- coding: utf-8 -*-
from openerp import models, api, fields
import time

class sale_order(models.Model):
    _inherit = "sale.order"

    @api.multi
    def debts_credit_limit_ok(self):
        self.ensure_one()
        if self.order_policy == 'prepaid':
            return True

        now = fields.Date.today()
        domain = [
            ('partner_id', '=', self.partner_id.id), ('state', '=', 'paid'),
            ('date_due', '>=', now,)]
        debts_invoices = self.env['account.invoice'].search(domain)
        available_debts = self.partner_id.credit

        if debts_invoices:
            if available_debts > 0:
                return False
        return True
