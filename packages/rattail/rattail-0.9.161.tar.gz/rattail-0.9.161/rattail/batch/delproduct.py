# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Handler for "delete product" batches
"""

from __future__ import unicode_literals, absolute_import

from sqlalchemy import orm

from rattail.db import model
from rattail.batch import BatchHandler


class DeleteProductBatchHandler(BatchHandler):
    """
    Handler for delete product batches.
    """
    batch_model_class = model.DeleteProductBatch

    def should_populate(self, batch):
        if hasattr(batch, 'products'):
            return True
        return False

    def populate(self, batch, progress=None):
        if hasattr(batch, 'products'):
            return self.populate_from_query(batch, progress=progress)

    def populate_from_query(self, batch, progress=None):
        session = orm.object_session(batch)

        def append(product, i):
            row = self.make_row()
            row.item_entry = product.uuid
            row.product = product
            self.add_row(batch, row)
            if i % 200 == 0:
                session.flush()

        self.progress_loop(append, batch.products, progress,
                           message="Adding products to batch")

    def refresh_row(self, row):
        if not row.product:
            row.status_code = row.STATUS_PRODUCT_NOT_FOUND
            return

        self.refresh_product_basics(row)
        row.status_code = row.STATUS_OK
