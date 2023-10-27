// Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Machine Maintenance', {
	onload:function(frm){
		frm.set_query('description_of_goods', 'item', () => {
			return {
				filters: {
					'is_stock_item': 0,
				}
			}
		})
	},
	before_save: function (frm) {
		var item_table = cur_frm.doc.item;
		var totalSum = 0;
		var qty;
		var rate;
		var total;
		var description_of_goods;
		for (var i = 0; i < item_table.length; i++) {
			description_of_goods = item_table[i].description_of_goods;
			qty = item_table[i].qty;
			rate = item_table[i].rate;
			total = qty * rate;
			// console.log(qty);
			// console.log(rate);
			// console.log(total);
			cur_frm.doc.item[i].total = total;
			cur_frm.refresh_fields('item');
			totalSum += total;
			// console.log(totalSum);
			frm.set_value('challan_total_value', totalSum);
			frm.refresh_field('challan_total_value');
		}
	},

	// on_submit: function (frm) {
	// 	var id = cur_frm.doc.name;
	// 	var item_table = cur_frm.doc.item;

	// 	var newStockEntry = frappe.model.get_new_doc('Stock Entry');
	// 	newStockEntry.stock_entry_type = "Material Issue";
	// 	newStockEntry.asset_maintenance = id;
	// 	// newStockEntry.docstatus = 1;
	// 	newStockEntry.purpose_name = "Asset Maintenance"
	// 	newStockEntry.items = [];
	// 	for (var i = 0; i < item_table.length; i++) {
	// 		var description_of_goods = item_table[i].description_of_goods;
	// 		var qty = item_table[i].qty;
	// 		var rate = item_table[i].rate;
	// 		var source_warehouse = item_table[i].source_warehouse;
	// 		// console.log(description_of_goods, source_warehouse)
	// 		newStockEntry.items.push({
	// 			"qty": qty,
	// 			"basic_rate": rate,
	// 			"s_warehouse": source_warehouse,
	// 			"item_code": description_of_goods,
	// 		});
	// 	}

	// 	frappe.call({
	// 		method: 'frappe.client.save',
	// 		args: {
	// 			doc: newStockEntry
	// 		},
	// 		callback: function (response) {
	// 			console.log(response.message);
	// 			if (response.message) {
	// 				frappe.msgprint(__('New stock entry created'));
	// 				frm.reload_doc();
	// 			}
	// 		}
	// 	});
	// }
});

frappe.ui.form.on("Machine Maintenance Item", "description_of_goods", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	d.source_warehouse = frm.doc.warehouse;
	frm.refresh_field('item');
	// frappe.db.get_value("Item Default", {"parent": d.description_of_goods,'company':frm.doc.company}, "default_warehouse", function(value) {
	// 	d.source_warehouse = value.default_warehouse;
	// });
	// frm.refresh_field('item');
});
