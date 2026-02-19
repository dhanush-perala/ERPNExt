import frappe

from erpnext.stock.doctype.item.item import Item
 
class ItemOverride(Item):

    @property

    def meta(self):

        meta = super().meta

        if not meta.title_field:

            meta.title_field = "item_name"

        return meta

 