# # Whitelist the original method
# import frappe
# from frappe import whitelist
# from india_compliance.gst_india.overrides.transaction import get_regional_round_off_accounts

# @whitelist()
# def my_whitelisted_method():
#     try:
#         return get_regional_round_off_accounts()
#     except Exception as e:
#         frappe.log_error(f"Error fetching regional round-off accounts: {e}")
#         return None


# import frappe
# from india_compliance.gst_india.overrides.transaction import get_regional_round_off_accounts as get_gst_round_off_accounts

# @frappe.whitelist()
# def my_whitelisted_method(company):
#     try:
#         # Call the built-in function within your custom logic
#         account_list = ["default_account"]  # Example default account list

#         # Invoke the built-in function
#         regional_accounts = get_gst_round_off_accounts(company, account_list)

#         # Add custom logic here if needed
#         # For example, modify the regional_accounts based on additional parameters

#         return regional_accounts

#     except Exception as e:
#         frappe.log_error(f"Error in custom API: {e}")
#         return None
import frappe

@frappe.whitelist()
def round_tax_amounts(docname):
    try:
        purchase_order = frappe.get_doc("Purchase Order", docname)

        for tax in purchase_order.get("taxes"):
            if tax.get("custom_rounded_amount"):
                # Round the tax_amount field to the nearest whole number
                rounded_tax_amount = round(tax.get("tax_amount"))

                # Update the tax_amount in the database
                frappe.db.set_value("Purchase Taxes and Charges", tax.name, "tax_amount", rounded_tax_amount)

        # Commit changes
        frappe.db.commit()

        return "Tax amounts rounded successfully."
    except Exception as e:
        frappe.log_error(f"Error rounding tax amounts: {e}")
        return "Failed to round tax amounts."
