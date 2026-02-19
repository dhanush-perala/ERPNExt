import frappe
import os
import json

@frappe.whitelist(allow_guest=True)
def add_project_card_api():
    """
    Fetches all projects from 'ADD PROJECT CARD' doctype.
    """
    try:
        projects = frappe.get_all("ADD PROJECT CARD", fields=["project"])
        return {"status": "success", "message": projects}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "add_project_card_api")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def project_subsystem_api():
    """
    CRUD API for 'ADD PROJECT SUBSYSTEM' doctype
    """
    try:
        if frappe.request.method == "GET":
            # Read from local JSON file
            json_path = os.path.join(frappe.get_app_path('ursc_cms_app'), 'project_subsystem_api.py')
            with open(json_path, 'r') as file:
                data = json.load(file)
            return {"status": "success", "data": data}

        elif frappe.request.method == "POST":
            data = json.loads(frappe.request.data)
            action = data.get("action")

            if action == "get_projects":
                projects = frappe.get_all("Project", fields=["name as project"])
                return {"status": "success", "data": projects}

            elif action == "read":
                records = frappe.get_all("ADD PROJECT SUBSYSTEM", fields=["name", "project", "sub_system", "centre"])
                return {"status": "success", "data": records}

            elif action == "create":
                doc = frappe.get_doc({
                    "doctype": "ADD PROJECT SUBSYSTEM",
                    "project": data["project"],
                    "sub_system": data["sub_system"],
                    "centre": data["centre"]
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()
                return {"status": "success", "message": "Record added"}

            elif action == "update":
                name = data.get("name")
                if not name:
                    return {"status": "error", "message": "Name is required for update"}
                doc = frappe.get_doc("ADD PROJECT SUBSYSTEM", name)
                doc.project = data["project"]
                doc.sub_system = data["sub_system"]
                doc.centre = data["centre"]
                doc.save(ignore_permissions=True)
                frappe.db.commit()
                return {"status": "success", "message": "Record updated"}

            elif action == "delete":
                name = data.get("name")
                if not name:
                    return {"status": "error", "message": "Name is required to delete"}
                frappe.delete_doc("ADD PROJECT SUBSYSTEM", name, ignore_permissions=True)
                frappe.db.commit()
                return {"status": "success", "message": "Record deleted"}

            else:
                return {"status": "error", "message": "Invalid action"}

        else:
            return {"status": "error", "message": "Unsupported HTTP method"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "project_subsystem_api")
        return {"status": "error", "message": str(e)}
elif action == "read":
    records = frappe.get_all("Project Subsystem", fields=["name", "project", "sub_system", "centre"])
    return {"status": "success", "data": records}

