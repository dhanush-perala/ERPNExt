if frappe.request.method == "POST":
    data = frappe.request.get_json()

    # Create
    if data.get("action") == "create":
        doc = frappe.get_doc({
            "doctype": "ADD PROJECT CARD",
            "project": data.get("project"),
            "prog_name": data.get("prog_name"),
            "project_ref_no": data.get("project_ref_no"),
            "pd_staff_no": data.get("pd_staff_no"),
            "project_status": data.get("project_status")
        })
        doc.insert(ignore_permissions=True)
        frappe.response["message"] = {"status": "success", "msg": "Saved successfully"}

    # Read
    elif data.get("action") == "read":
        records = frappe.get_all("ADD PROJECT CARD", 
            fields=["name", "project", "prog_name", "project_ref_no", "pd_staff_no", "project_status"],
            order_by="creation desc")
        frappe.response["message"] = {"status": "success", "records": records}

    # Delete
    elif data.get("action") == "delete":
        name = data.get("name")
        if name:
            try:
                frappe.delete_doc("ADD PROJECT CARD", name, ignore_permissions=True)
                frappe.response["message"] = {"status": "success", "msg": "Deleted successfully"}
            except Exception as e:
                frappe.response["message"] = {"status": "error", "msg": str(e)}
        else:
            frappe.response["message"] = {"status": "error", "msg": "Missing document name for delete"}

    # Update
    elif data.get("action") == "update":
        name = data.get("name")
        if name:
            try:
                doc = frappe.get_doc("ADD PROJECT CARD", name)
                doc.project = data.get("project")
                doc.prog_name = data.get("prog_name")
                doc.project_ref_no = data.get("project_ref_no")
                doc.pd_staff_no = data.get("pd_staff_no")
                doc.project_status = data.get("project_status")
                doc.save(ignore_permissions=True)
                frappe.response["message"] = {"status": "success", "msg": "Updated successfully"}
            except Exception as e:
                frappe.response["message"] = {"status": "error", "msg": str(e)}
        else:
            frappe.response["message"] = {"status": "error", "msg": "Missing document name for update"}

