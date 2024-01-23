# Copyright (c) 2024, pooja@sanskartechnolab.com and contributors
# For license information, please see license.txt

# import frappe

import frappe

def execute(filters=None):
    columns = [
        {"label": "Company", "fieldname": "company", "width": 200},
        {"label": "Warehouse", "fieldname": "warehouse", "width": 200},
        {"label": "Item Code", "fieldname": "item_code", "width": 220},
        {"label": "Item Name", "fieldname": "item_name", "width": 230},
        {"label": "Status", "fieldname": "status", "width": 70},
        {"label": "P", "fieldname": "p", "width": 70},
        {"label": "A", "fieldname": "a", "width": 70},
        {"label": "B", "fieldname": "b", "width": 70},
        {"label": "C", "fieldname": "c", "width": 70},
    ]

    # Dictionary to store counts for each combination of "company", "warehouse", "item_code", and "quality"
    quality_counts = {}

    # # Construct filters based on the presence of the "item" and "warehouse" filters
    base_filters = {
        "status": filters.get("status"),
    }

    # Check if "company" filter is present
    if filters.get("company"):
        base_filters["company"] = filters.get("company")

    if filters.get("item"):
        base_filters["item_code"] = filters.get("item")

    if filters.get("warehouse"):
        base_filters["warehouse"] = filters.get("warehouse")
    
    # Fetch data from the "Serial No" doctype with dynamic filters
    serial_no_data = frappe.get_all(
        doctype="Serial No",
        filters=base_filters,
        fields=["company", "warehouse", "item_code", "quality", "status"]
    )

    for row in serial_no_data:
        if row.status in ["Active", "Hold"]:
            # Initialize counts for each combination if not present in the dictionary
            key = (row.company, row.warehouse, row.item_code, row.status)
            if key not in quality_counts:
                quality_counts[key] = {"p": 0, "a": 0, "b": 0, "c": 0}

            # Increment the count based on the quality
            if row.quality == "P":
                quality_counts[key]["p"] += 1
            elif row.quality == "A":
                quality_counts[key]["a"] += 1
            elif row.quality == "B":
                quality_counts[key]["b"] += 1
            elif row.quality == "C":
                quality_counts[key]["c"] += 1

    # Fetch additional details like item name
    data = []
    for key, value in quality_counts.items():
        company, warehouse, item_code, status = key
        item_data = frappe.get_all(
            doctype="Item",
            filters={"item_code": item_code},
            fields=["item_name"]
        )

        # Append the row to data
        data.append({
            "company": company,
            "warehouse": warehouse,
            "item_code": item_code,
            "item_name": item_data[0].item_name if item_data else "",
            "status": status,
            **value
        })

    return columns, data
