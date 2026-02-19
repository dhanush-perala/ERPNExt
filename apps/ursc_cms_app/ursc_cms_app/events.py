from ursc_cms_app.api import delete_item_alternatives
 
def alternate_part_disable_on_submit(doc, method):

    """

    Triggered AFTER submit of Alternate Part Disable

    """
 
    if not doc.link_part_number:

        return
 
    if not doc.selected_alternatives:

        return
 
    delete_item_alternatives(

        item_code=doc.link_part_number,

        alternatives_json=doc.selected_alternatives

    )

 