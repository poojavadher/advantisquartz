from frappe import _


def get_data():
    return {
        "non_standard_fieldnames": {
            "Stock Entry": "asset_maintenance",
            "Purchase Receipt": "machine_maintenance",
            "Purchase Invoice": "machine_maintenance"
        },
        "transactions": [
            {
                "label": _("Related"),
                "items": [
                    "Stock Entry",
                    "Purchase Receipt",
                    "Purchase Invoice",
                ],
            }
        ],
    }