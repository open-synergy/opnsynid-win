# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from openerp.tools import float_is_zero


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _get_invoice_line_vals(self, move, partner, inv_type):
        _super = super(StockMove, self)
        res = _super._get_invoice_line_vals(move, partner, inv_type)
        if inv_type in ('out_invoice', 'out_refund') and \
                move.procurement_id and move.procurement_id.move_dest_id and \
                move.procurement_id.move_dest_id.procurement_id and \
                move.procurement_id.move_dest_id.procurement_id.sale_line_id:
            sale_line = move.procurement_id.move_dest_id.\
                procurement_id.sale_line_id
            res['invoice_line_tax_id'] = [
                (6, 0, [x.id for x in sale_line.tax_id])]
            res['account_analytic_id'] = sale_line.order_id.project_id and \
                sale_line.order_id.project_id.id or False
            res['discount'] = sale_line.discount
            cust = sale_line.order_id.partner_id
            if move.product_id.id != sale_line.product_id.id:
                precision = self.env[
                    'decimal.precision'].precision_get('Discount')
                if float_is_zero(
                        sale_line.discount,
                        precision_digits=precision):
                    pricelist = sale_line.order_id.pricelist_id
                    res['price_unit'] = pricelist.price_get(
                        move.product_id.id, move.product_uom_qty or 1.0,
                        cust)[sale_line.order_id.pricelist_id.id]
                else:
                    res['price_unit'] = move.product_id.lst_price
            else:
                res['price_unit'] = sale_line.price_unit
            uos_coeff = move.product_uom_qty and move.product_uos_qty / \
                move.product_uom_qty or 1.0
            res['price_unit'] = res['price_unit'] / uos_coeff
        return res

    @api.model
    def _create_invoice_line_from_vals(self, move, invoice_line_vals):
        _super = super(StockMove, self)
        invoice_line_id = _super._create_invoice_line_from_vals(
            move, invoice_line_vals)
        context = self.env.context
        if context.get("inv_type") in ("out_invoice", "out_refund") and \
                move.procurement_id and move.procurement_id.move_dest_id and \
                move.procurement_id.move_dest_id.procurement_id and \
                move.procurement_id.move_dest_id.procurement_id.sale_line_id:
            sale_line = move.procurement_id.move_dest_id.\
                procurement_id.sale_line_id
            sale_line.write({
                "invoice_lines": [(4, invoice_line_id)]
            })
            sale_line.order_id.write({
                'invoice_ids': [(4, invoice_line_vals['invoice_id'])],
            })

        return invoice_line_id
