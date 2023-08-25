import frappe

@frappe.whitelist()
def get_child_for_parent(doc_name,child_table):
    parent = doc_name
    child = child_table
    # frappe.msgprint(parent)

    query = f"SELECT * FROM `{child}` WHERE parent = %s"
    result = frappe.db.sql(query, (parent,), as_dict=True)
    # frappe.msgprint(result[0].item_name)

    frappe.response['result'] = result 