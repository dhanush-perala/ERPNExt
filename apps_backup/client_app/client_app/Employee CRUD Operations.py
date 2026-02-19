import frappe

# Create Employee API
@frappe.whitelist(allow_guest=True)
def create_employee(emp_name, emp_mobile, time):
    # Check if an employee with the same mobile number already exists
    existing_employee = frappe.get_all("employee_doc", filters={"employeemobile": emp_mobile}, limit_page_length=1)
    if existing_employee:
        return {"status": "error", "message": "Employee with this mobile number already exists."}
    
    # Create a new employee document
    employee = frappe.get_doc({
        "doctype": "employee_doc",
        "employeename": emp_name,
        "employeemobile": emp_mobile,
        "time": time,
        "status": "active"  # New employee starts as active
    })
    employee.insert()
    return {"status": "success", "message": "Employee created successfully."}

# Get Employee API
@frappe.whitelist(allow_guest=True)
def get_employee(emp_id):
    employee = frappe.get_all("employee_doc", filters={"name": emp_id, "status": "active"}, fields=["name", "employeename", "employeemobile", "time"], limit_page_length=1)
    if employee:
        return {"status": "success", "data": employee[0]}
    else:
        return {"status": "error", "message": "Employee not found or inactive."}

# Update Employee API
@frappe.whitelist(allow_guest=True)
def update_employee(emp_id, emp_name, emp_mobile, time):
    employee = frappe.get_all("employee_doc", filters={"name": emp_id, "status": "active"}, limit_page_length=1)
    if not employee:
        return {"status": "error", "message": "Active employee not found."}

    employee_doc = frappe.get_doc("employee_doc", employee[0].name)
    employee_doc.employeename = emp_name
    employee_doc.employeemobile = emp_mobile
    employee_doc.time = time
    employee_doc.save()
    return {"status": "success", "message": "Employee updated successfully."}

# Soft Delete Employee (Set Status to Inactive)
@frappe.whitelist(allow_guest=True)
def delete_employee(emp_id):
    employee = frappe.get_all("employee_doc", filters={"name": emp_id,}, limit_page_length=1)
    if not employee:
        return {"status": "error", "message": "Active employee not found."}

    # Mark the employee as inactive (soft delete)
    employee_doc = frappe.get_doc("employee_doc", employee[0].name)
    employee_doc.status = "inactive"
    employee_doc.save()
    return {"status": "success", "message": "Employee marked as inactive successfully."}

