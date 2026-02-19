// Copyright (c) 2025, neemus and contributors
// For license information, please see license.txt

frappe.ui.form.on('SRN Request Item', {
    component: function(frm, cdt, cdn) {
        // Auto-fill acquisition_date when component is selected
        let row = locals[cdt][cdn];
        if (row.component) {
            // Call server-side method to get component details
            frappe.call({
                method: 'ursc_cms_app.isro_cms.doctype.srn_request_item.srn_request_item.get_component_details',
                args: {
                    component: row.component
                },
                callback: function(r) {
                    if (r.message && r.message.acquisition_date) {
                        frappe.model.set_value(cdt, cdn, 'acquisition_date', r.message.acquisition_date);
                        
                        // If manufacture_date is not set, use acquisition_date
                        if (!row.manufacture_date) {
                            frappe.model.set_value(cdt, cdn, 'manufacture_date', r.message.acquisition_date);
                        }
                        
                        // Trigger age calculation
                        frappe.model.trigger('manufacture_date', cdt, cdn);
                    }
                }
            });
        }
    },
    
    acquisition_date: function(frm, cdt, cdn) {
        // If manufacture_date is not set, use acquisition_date
        let row = locals[cdt][cdn];
        if (row.acquisition_date && !row.manufacture_date) {
            frappe.model.set_value(cdt, cdn, 'manufacture_date', row.acquisition_date);
        }
    },
    
    manufacture_date: function(frm, cdt, cdn) {
        // Calculate component age when manufacture_date changes
        let row = locals[cdt][cdn];
        
        if (!row.manufacture_date) {
            // Clear values if no manufacture date
            frappe.model.set_value(cdt, cdn, 'component_age', 0);
            frappe.model.set_value(cdt, cdn, 'requires_testing', 0);
            return;
        }
        
        try {
            // Convert manufacture date to proper format
            let manufactureDate;
            if (typeof row.manufacture_date === 'string') {
                manufactureDate = frappe.datetime.str_to_obj(row.manufacture_date);
            } else {
                manufactureDate = row.manufacture_date;
            }
            
            const today = frappe.datetime.now_date();
            const todayDate = frappe.datetime.str_to_obj(today);
            
            // Check if manufacture date is in the future
            if (manufactureDate > todayDate) {
                frappe.msgprint(__('⚠️ Manufacture date cannot be in the future.'));
                frappe.model.set_value(cdt, cdn, 'component_age', 0);
                frappe.model.set_value(cdt, cdn, 'requires_testing', 0);
                return;
            }
            
            // Calculate difference in years using more accurate method
            const diffTime = todayDate - manufactureDate;
            const diffYears = diffTime / (1000 * 60 * 60 * 24 * 365.25); // Using 365.25 for leap years
            
            // Calculate component age and round to 2 decimal places
            const componentAge = Math.round(diffYears * 100) / 100;
            
            // Set the component age
            frappe.model.set_value(cdt, cdn, 'component_age', componentAge);
            
            // Auto mark for testing if more than 5 years old
            if (diffYears > 5) {
                frappe.model.set_value(cdt, cdn, 'requires_testing', 1);
                frappe.msgprint(__('⚠️ Component is older than 5 years — requires testing.'));
            } else {
                frappe.model.set_value(cdt, cdn, 'requires_testing', 0);
            }
            
        } catch (error) {
            console.error('Error calculating component age:', error);
            frappe.msgprint(__('Error calculating component age. Please check the manufacture date.'));
        }
    },
    
    requires_testing: function(frm, cdt, cdn) {
        // Optional: Add any additional logic when requires_testing is manually changed
        let row = locals[cdt][cdn];
        if (row.requires_testing && row.component_age <= 5) {
            frappe.msgprint(__('Note: Component is not older than 5 years but testing is still required.'));
        }
    }
});
