# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"
    _track = {
        "type": {},
    }

    credit_limit = fields.Float(
        track_visibility="onchange",
    )
