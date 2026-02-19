import frappe

@frappe.whitelist()
def get_project_list():
    data = frappe.get_all("ADD PROJECT CARD", fields=["project"])
    return {
        "message": data
    }
