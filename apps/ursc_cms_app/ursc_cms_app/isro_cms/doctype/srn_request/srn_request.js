// Copyright (c) 2025, neemus and contributors
// For license information, please see license.txt

frappe.ui.form.on('SRN Request', {
    refresh(frm) {
        // Set default request date to today if creating new document
        if (frm.is_new() && !frm.doc.request_date) {
            frm.set_value('request_date', frappe.datetime.get_today());
        }
        
        // Calculate component age for all existing rows when form loads
        if (frm.doc.table_pdia && frm.doc.table_pdia.length > 0) {
            frm.doc.table_pdia.forEach((row, index) => {
                if (row.manufacture_date && (!row.component_age || row.component_age === 0)) {
                    calculate_component_age(frm, 'SRN Request Item', row.name);
                }
            });
        }
        
        // Add a manual button to recalculate all component ages
        frm.add_custom_button(__('Recalculate Component Ages'), function() {
            if (frm.doc.table_pdia && frm.doc.table_pdia.length > 0) {
                frm.doc.table_pdia.forEach((row, index) => {
                    if (row.manufacture_date) {
                        calculate_component_age(frm, 'SRN Request Item', row.name);
                    }
                });
                frappe.msgprint(__('Component ages recalculated successfully.'));
            }
        });
    }
});

frappe.ui.form.on('SRN Request Item', {
    manufacture_date(frm, cdt, cdn) {
        calculate_component_age(frm, cdt, cdn);
    },
    
    // Trigger calculation when row is added
    items_add(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.manufacture_date) {
            calculate_component_age(frm, cdt, cdn);
        }
    },
    
    // Trigger calculation when row is refreshed
    form_render(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.manufacture_date && (!row.component_age || row.component_age === 0)) {
            calculate_component_age(frm, cdt, cdn);
        }
    }
});

// Function to calculate component age
function calculate_component_age(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    
    if (!row.manufacture_date) {
        // Clear values if no manufacture date
        frappe.model.set_value(cdt, cdn, 'component_age', 0);
        frappe.model.set_value(cdt, cdn, 'requires_testing', 0);
        frm.refresh_field('table_pdia');
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
        
        // Debug logging
        console.log('Manufacture Date:', row.manufacture_date, 'Parsed:', manufactureDate);
        console.log('Today:', today, 'Parsed:', todayDate);
        
        // Check if manufacture date is in the future
        if (manufactureDate > todayDate) {
            frappe.msgprint(__('⚠️ Manufacture date cannot be in the future.'));
            frappe.model.set_value(cdt, cdn, 'component_age', 0);
            frappe.model.set_value(cdt, cdn, 'requires_testing', 0);
            frm.refresh_field('table_pdia');
            return;
        }
        
        // Calculate difference in years using more accurate method
        const diffTime = todayDate - manufactureDate;
        const diffYears = diffTime / (1000 * 60 * 60 * 24 * 365.25); // Using 365.25 for leap years
        
        // Calculate component age and round to 2 decimal places
        const componentAge = Math.round(diffYears * 100) / 100;
        
        console.log('Calculated component age:', componentAge, 'years');
        
        // Set the component age
        frappe.model.set_value(cdt, cdn, 'component_age', componentAge);
        
        // Auto mark for testing if more than 5 years old
        if (diffYears > 5) {
            frappe.model.set_value(cdt, cdn, 'requires_testing', 1);
            // Only show message if it's a new calculation (not on form load)
            if (frm.doc.__islocal) {
                frappe.msgprint(__('⚠️ Component is older than 5 years — send for testing.'));
            }
        } else {
            frappe.model.set_value(cdt, cdn, 'requires_testing', 0);
        }
        
        // Refresh the field to show updated values
        frm.refresh_field('table_pdia');
        
    } catch (error) {
        console.error('Error calculating component age:', error);
        frappe.msgprint(__('Error calculating component age. Please check the manufacture date.'));
    }
}
