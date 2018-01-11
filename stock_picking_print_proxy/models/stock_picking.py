# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
import pytz
from datetime import datetime


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _convert_datetime_utc(self, dt):
        if dt:
            convert_dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            if self.env.user.tz:
                tz = pytz.timezone(self.env.user.tz)
            else:
                tz = pytz.utc
            convert_utc = pytz.utc.localize(convert_dt).astimezone(tz)
            format_utc = convert_utc.strftime("%d-%m-%Y %H:%M:%S")

            return format_utc
        else:
            return "-"

    @api.multi
    def export_for_printing(self):
        self.ensure_one()
        value = []
        picking_line = []
        for move in self.move_lines:
            res_move = {
                "product_code": move.product_id and move.product_id.code or "-",
                "product_name": move.product_id and move.product_id.name or "-",
                "product_qty": move.product_qty,
                "product_uom": move.product_uom and move.product_uom.name or "-"
            }
            picking_line.append(res_move)
        res_picking = {
            "id": self.id,
            "no_do": self.name,
            "no_so": self.sale_id.name or "-",
            "tanggal": self._convert_datetime_utc(self.date_done),
            "toko": self.delivery_address_id.commercial_partner_id.name or "-",
            "line": picking_line
        }
        value.append(res_picking)
        return value
