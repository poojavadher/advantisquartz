import frappe

def execute(filters=None):
    columns = [
        {"label": "Company", "fieldname": "company", "width": 200},
        {"label": "Warehouse", "fieldname": "warehouse", "width": 200},
        {"label": "Item Code", "fieldname": "item_code", "width": 220, "fieldtype": "Link", "options": "Item"},
        {"label": "Batch No", "fieldname": "batch_no", "width": 220, "fieldtype": "Link", "options": "Batch"},
        {"label": "Item Name", "fieldname": "item_name", "width": 230},
        {"label": "Status", "fieldname": "status", "width": 70},
        {"label": "P", "fieldname": "p", "width": 70},
        {"label": "A", "fieldname": "a", "width": 70},
        {"label": "B", "fieldname": "b", "width": 70},
        {"label": "C", "fieldname": "c", "width": 70},
        {"label": "Total", "fieldname": "total", "width": 100},
    ]

    # Dictionary to store counts for each combination of "company", "warehouse", "item_code", "quality", and "status"
    quality_counts = {}

    # Construct filters based on the presence of the "item" and "warehouse" filters
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
    if filters.get("batch_no"):
        base_filters["batch_no"] = filters.get("batch_no")
    # Fetch data from the "Serial No" doctype with dynamic filters
    serial_no_data = frappe.get_all(
        doctype="Serial No",
        filters=base_filters,
        fields=["company", "warehouse", "item_code", "quality", "status", "batch_no"]
    )

    for row in serial_no_data:
        if row.status in ["Active", "Hold"]:
            # Initialize counts for each combination if not present in the dictionary
            key = (row.company, row.warehouse, row.item_code, row.status, row.batch_no)
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
        company, warehouse, item_code, status, batch_no = key
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
            "batch_no": batch_no,
            **value,
            "total": value['p'] + value['a'] + value['b'] + value['c']
        })

    # Calculate totals for each quality and overall total
    total_p = sum(value["p"] for value in quality_counts.values())
    total_a = sum(value["a"] for value in quality_counts.values())
    total_b = sum(value["b"] for value in quality_counts.values())
    total_c = sum(value["c"] for value in quality_counts.values())
    total_all = total_p + total_a + total_b + total_c

    # Append the total row to data
    data.append({
        "company": "<b>Total</b>",
        "warehouse": "",
        "item_code": "",
        "item_name": "",
        "status": "",
        "batch_no": "",
        "p": "<b>{}</b>".format(total_p),
        "a": "<b>{}</b>".format(total_a),
        "b": "<b>{}</b>".format(total_b),
        "c": "<b>{}</b>".format(total_c),
        "total": "<b>{}</b>".format(total_all)
    })

    return columns, data
