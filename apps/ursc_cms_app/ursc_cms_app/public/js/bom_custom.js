frappe.ui.form.on('BOM', {

    refresh(frm) {

        frm.add_custom_button(__('Get Items From'), function () {

            get_items_from_cardwise_component(frm);

        }).addClass('btn-primary');

    },

});
 
// Dialog to select Cardwise Component List

function get_items_from_cardwise_component(frm) {

    frappe.prompt(

        [

            {

                fieldtype: 'Link',

                label: 'Cardwise Component List',

                fieldname: 'cardwise_component_list',

                options: 'Cardwise Component List Update and Approve - Designer',

                reqd: 1

            }

        ],

        function (values) {

            fetch_items_for_bom(frm, values.cardwise_component_list);

        },

        __('Select Cardwise Component List'),

        __('Get Items')

    );

}
 
// Fetch items and add to BOM

function fetch_items_for_bom(frm, cardwise_component_list) {

    frappe.call({

        method: "ursc_cms_app.api.get_components_for_bom",

        args: {

            cardwise_component_list: cardwise_component_list

        },

        callback: function (r) {

            const components = r.message || [];
 
            if (components.length) {

                components.forEach(component => {

                    frm.add_child('items', {

                        item_code: component.item_code,

                        qty: component.qty,
                             uom: component.uom,          // stock UOM

                        rate: component.rate         // last transaction rate'
 

                    });

                });
 
                frm.refresh_field('items');
 
                frappe.show_alert({

                    message: __('Items fetched successfully from Cardwise Component List'),

                    indicator: 'green'

                });

            } else {

                frappe.msgprint(__('No items found in the selected Cardwise Component List.'));

            }

        }

    });

}

 