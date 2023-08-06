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
Data model for "delete product" batches
"""

from __future__ import unicode_literals, absolute_import

from rattail.db.model import Base, BatchMixin, ProductBatchRowMixin


class DeleteProductBatch(BatchMixin, Base):
    """
    Primary data model for "delete product" batches.
    """
    __tablename__ = 'batch_delproduct'
    __batchrow_class__ = 'DeleteProductBatchRow'
    batch_key = 'delproduct'
    model_title = "Delete Product Batch"
    model_title_plural = "Delete Product Batches"


class DeleteProductBatchRow(ProductBatchRowMixin, Base):
    """
    Row of data within a new product batch.
    """
    __tablename__ = 'batch_delproduct_row'
    __batch_class__ = DeleteProductBatch

    STATUS_OK                           = 1
    STATUS_PRODUCT_NOT_FOUND            = 2
    STATUS_DEPARTMENT_NOT_ALLOWED       = 3
    STATUS_RECENT_ACTIVITY              = 4

    STATUS = {
        STATUS_OK                       : "ok",
        STATUS_PRODUCT_NOT_FOUND        : "product not found",
        STATUS_DEPARTMENT_NOT_ALLOWED   : "delete not allowed for department",
        STATUS_RECENT_ACTIVITY          : "has recent activity",
    }
