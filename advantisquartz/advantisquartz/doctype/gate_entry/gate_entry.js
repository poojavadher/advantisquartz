// Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Entry', {
	validate: function (frm) {
		if (frm.doc.invoice_date > get_today()) {
			frappe.throw(__("Not Allowed To Select future dates"));
		}
	},
	is_weight_in: function (frm) {
		frm.set_value('weight_in_date', frappe.datetime.now_date());
		frm.set_value('weight_in_time', frappe.datetime.now_time());
	},
	is_unloaded: function (frm) {
		frm.set_value('unloading_date', frappe.datetime.now_date());
		frm.set_value('unloading_time', frappe.datetime.now_time());
	},

	is_weight_out: function (frm) {
		frm.set_value('weight_out_date', frappe.datetime.now_date());
		frm.set_value('weight_out_time', frappe.datetime.now_time());
	},
	is_gate_out: function (frm) {
		frm.set_value('gate_out_date', frappe.datetime.now_date());
		frm.set_value('gate_out_time', frappe.datetime.now_time());
	},
	sampling_done: function (frm) {
		frm.set_value('sample_date', frappe.datetime.now_date());
		frm.set_value('sample_time', frappe.datetime.now_time());
	},
	weight_out: function (frm) {
		var gross_weight = frm.doc.weight_in;
		var tare_weight = frm.doc.weight_out;
		console.log(gross_weight + "\n\n" + tare_weight);
		frm.doc.net_weight = gross_weight - tare_weight;
		frm.refresh_field('net_weight');
	},
	before_submit(frm) {
		if (frm.doc.entry_type == "Inward" && frm.doc.grn === 0) {
			frappe.throw("Purchase Receipt is pending for this Gate Entry");
		}
		var asset_repair = frm.doc.asset_repair_entry;
		if (asset_repair) {
			frappe.db.set_value("Asset Repair", asset_repair, 'gate_out_entry', frm.doc.name);
		}
	},
	before_cancel(frm) {
		if (frm.doc.purpose == "Raw Material") {
			frm.clear_table('qc_details');
		}
		var asset_repair = frm.doc.asset_repair_entry;
		if (asset_repair) {
			frappe.db.set_value("Asset Repair", asset_repair, 'gate_out_entry', ' ');
		}
	},
	outward_for(frm) {
		if (frm.doc.outward_for == "Purchase Receipt") {
			frm.set_query("outward_entry", function () {
				return {
					filters: {
						'is_return': 1,
						'docstatus': 1
					}
				};
			});
		}
		if (frm.doc.outward_for == "Delivery Note") {
			frm.set_query("outward_entry", function () {
				return {
					filters: {
						'status': "To Bill"
					}
				};
			});
		}
	},
	get_data: function (frm) {
		var doc_name = frm.doc.outward_entry;
		var row;
		if (frm.doc.outward_for == "Delivery Note") {
			frappe.call({
				method: "advantisquartz.advantisquartz.doctype.gate_entry.api.get_child_for_parent",
				args: {
					'doc_name': doc_name,
					'child_table': 'tabDelivery Note Item'
				},
				callback: function (r) {
					// console.log(r.result[0].item_code);
					for (var i = 0; i < r.result.length; i++) {
						row = frm.add_child('stock_item_tab');
						row.item = r.result[i].item_code;
						row.item_name = r.result[i].item_code;
						row.qty = r.result[i].qty;
						row.uom = r.result[i].uom;
						row.parent_doctype = r.result[i].parenttype;
						row.parentdoc = r.result[i].parent;
					}
					frm.refresh_field('stock_item_tab');
					frm.doc.outward_entry = null;
					frm.refresh_field('outward_entry');
				}
			});
		}
		if (frm.doc.outward_for == "Purchase Receipt") {
			frappe.call({
				method: "advantisquartz.advantisquartz.doctype.gate_entry.api.get_child_for_parent",
				args: {
					'doc_name': doc_name,
					'child_table': 'tabPurchase Receipt Item'
				},
				callback: function (r) {
					// console.log(r.result[0].item_code);
					for (var i = 0; i < r.result.length; i++) {
						row = frm.add_child('stock_item_tab');
						row.item = r.result[i].item_code;
						row.item_name = r.result[i].item_code;
						row.qty = r.result[i].qty;
						row.uom = r.result[i].uom;
						row.parent_doctype = r.result[i].parenttype;
						row.parentdoc = r.result[i].parent;
					}
					frm.refresh_field('stock_item_tab');
					frm.doc.outward_entry = null;
					frm.refresh_field('outward_entry');
				}
			});
		}
		if (frm.doc.outward_for == "Machine Maintenance") {
			frappe.call({
				method: "advantisquartz.advantisquartz.doctype.gate_entry.api.get_child_for_parent",
				args: {
					'doc_name': doc_name,
					'child_table': 'tabMachine Maintenance Item'
				},
				callback: function (r) {
					// console.log(r.result[0].item_code);
					for (var i = 0; i < r.result.length; i++) {
						row = frm.add_child('stock_item_tab');
						row.item = r.result[i].description_of_goods;
						row.item_name = r.result[i].item_name;
						row.qty = r.result[i].qty;
						row.uom = r.result[i].uom;
						row.parent_doctype = r.result[i].parenttype;
						row.parentdoc = r.result[i].parent;
					}
					frm.refresh_field('stock_item_tab');
					frm.doc.outward_entry = null;
					frm.refresh_field('outward_entry');
				}
			});
		}
	},
	outward_for(frm) {
		if (frm.doc.outward_for == 'Machine Maintenance') {
			var supplier = frm.doc.supplier;
			if (supplier) {
				frappe.call({
					method: "frappe.client.get_list",
					args: {
						doctype: "Machine Maintenance",
						filters: {
							supplier: supplier,
							docstatus: 1
						},
						fields: ["name"],
					},
					callback: function (response) {
						var machineMaintenanceOptions = response.message.map(function (item) {
							return item.name;
						});

						frm.fields_dict.outward_entry.get_query = function () {
							return {
								filters: [
									['Machine Maintenance', 'name', 'in', machineMaintenanceOptions]
								]
							};
						};

						frm.refresh_field('outward_entry');
					}
				});
			}
		}
	},

	// outward_for(frm) {
	// 	if (outward_for == 'Machine Maintenance') {
	// 		var supplier = cur_frm.doc.supplier;
	// 		// console.log(supplier);
	// 		frappe.call({
	// 			method: "frappe.client.get_list",
	// 			args: {
	// 				doctype: "Machine Maintenance",
	// 				filters: {
	// 					supplier: supplier,
	// 				},
	// 				fields: ["name"],
	// 			},
	// 			callback: function (response) {
	// 				console.log(response);
	// 				var machineMaintenanceOptions = response.message.map(function (item) {
	// 					return item.name;
	// 				});
	// 				console.log(machineMaintenanceOptions);
	// 				frm.fields_dict.outward_entry.get_query = function () {
	// 					return {
	// 						filters: [
	// 							['Machine Maintenance', 'name', 'in', machineMaintenanceOptions]
	// 						]
	// 					};
	// 				};
	// 				frm.refresh_field('outward_entry');
	// 			}
	// 		});
	// 	}
	// },
	/* for Lock fields functionality start */
	onload(frm) {
		frm.set_query("party_type", function () {
			return {
				filters: {
					'name': ["in", ["Customer", "Supplier"]]
				}
			};
		});

		checkLock(frm);
		toggleWeightLock(frm);
		toggleSamplingLock(frm);
		toggleunloadLock(frm);
		toggleWeightOutLock(frm);
		toggleQualityLock(frm);
	},

	lock_fields(frm) {
		checkLock(frm);
	},

	entry_type(frm) {
		checkLock(frm);
	},

	purpose(frm) {
		if (frm.doc.entry_type == "Outward") {
			frm.set_query("outward_for", function () {
				return {
					filters: {
						// 'name': ["in", ["Delivery Note", "Purchase Receipt", "Asset Repair"]]
						'name': ["in", ["Delivery Note", "Purchase Receipt", "Machine Maintenance"]]
					}
				};
			});
		}
		checkLock(frm);
	},

	truck_no(frm) {
		checkLock(frm);
	},

	is_weight_in(frm) {
		toggleWeightLock(frm);

		if (!frm.doc.is_weight_in) {
			frm.set_value('lock_weight', false);
		} else {
			frm.set_value('lock_weight', false);
		}
	},

	lock_weight(frm) {
		toggleWeightLock(frm);
	},

	refresh(frm) {
		if (!frm.is_new() && (!frm.doc.invoice_no || !frm.doc.invoice_date)) {
			var form = frm;
			frm.add_custom_button(__('Update Invoice Details'), function () {
				let dl = new frappe.ui.Dialog({
					title: 'Enter Details',
					fields: [{
						label: 'Invoice No.',
						fieldname: 'invoice_no',
						fieldtype: 'Data',
						reqd: 1
					},
					{
						label: 'Invoice Data',
						fieldname: 'inv_date',
						fieldtype: 'Date',
						reqd: 1
					}
					],
					primary_action_label: 'Update',
					primary_action(values) {
						frappe.db.set_value('Gate Entry', frm.doc.name, {
							'invoice_no': values.invoice_no,
							'invoice_date': values.inv_date
						})
						dl.hide();
						location.reload();
					}
				});
				dl.show();
			})
		}
		if (!frm.is_new() && (!frm.doc.challan_no || !frm.doc.challan_date)) {
			frm.add_custom_button(__('Update challan Details'), function () {
				let dl = new frappe.ui.Dialog({
					title: 'Enter Details',
					fields: [{
						label: 'Challan No.',
						fieldname: 'challan_no',
						fieldtype: 'Data',
						reqd: 1
					},
					{
						label: 'Challan Data',
						fieldname: 'challan_date',
						fieldtype: 'Date',
						reqd: 1
					}
					],
					primary_action_label: 'Update',
					primary_action(values) {
						frappe.db.set_value('Gate Entry', frm.doc.name, {
							'challan_no': values.challan_no,
							'challan_date': values.challan_date
						})
						dl.hide();
						location.reload();
					}
				});
				dl.show();
			})
		}

		checkLock(frm);

		if (!frm.is_new() && (!frappe.user.has_role('System Manager') || !frappe.user.has_role('Accounts Manager'))) {
			frm.set_df_property('lock_fields', 'read_only', true);
			frm.set_df_property('is_weight_in', 'read_only', frm.doc.lock_weight);
			frm.set_df_property('lock_weight', 'read_only', frm.doc.lock_weight);
			frm.set_df_property('sampling_done', 'read_only', frm.doc.lock_sampling);
			frm.set_df_property('lock_sampling', 'read_only', frm.doc.lock_sampling);
			frm.set_df_property('is_unloaded', 'read_only', frm.doc.lock_unload_details);
			frm.set_df_property('lock_unload_details', 'read_only', frm.doc.lock_unload_details);
			frm.set_df_property('is_weight_out', 'read_only', frm.doc.lock_weight_out_details);
			frm.set_df_property('lock_weight_out_details', 'read_only', frm.doc.lock_weight_out_details);
			frm.set_df_property('lock_quality_inspection', 'read_only', frm.doc.lock_quality_inspection);
		}
	},

	sampling_done(frm) {
		toggleSamplingLock(frm);
	},

	lock_sampling(frm) {
		toggleSamplingLock(frm);
	},

	is_unloaded(frm) {
		toggleunloadLock(frm);
	},

	lock_unload_details(frm) {
		toggleunloadLock(frm);
	},

	lock_weight_out_details(frm) {
		toggleWeightOutLock(frm);
	},

	is_unloaded(frm) {
		toggleWeightOutLock(frm);
	},

	lock_quality_inspection(frm) {
		toggleQualityLock(frm);
	},

	after_save(frm) {
		if (frappe.user.has_role('System Manager') || frappe.user.has_role('Accounts Manager')) {
			frm.set_df_property('lock_fields', 'read_only', false);
			frm.set_df_property('lock_weight', 'read_only', false);
			frm.set_df_property('lock_sampling', 'read_only', false);
			frm.set_df_property('lock_unload_details', 'read_only', false);
			frm.set_df_property('lock_weight_out_details', 'read_only', false);
			frm.set_df_property('lock_quality_inspection', 'read_only', false);
		} else {
			frm.set_df_property('lock_fields', 'read_only', true);
			frm.set_df_property('is_weight_in', 'read_only', frm.doc.lock_weight);
			frm.set_df_property('lock_weight', 'read_only', true);
			frm.set_df_property('sampling_done', 'read_only', frm.doc.lock_sampling);
			frm.set_df_property('lock_sampling', 'read_only', true);
			frm.set_df_property('is_unloaded', 'read_only', frm.doc.lock_unload_details);
			frm.set_df_property('lock_unload_details', 'read_only', true);
			frm.set_df_property('is_weight_out', 'read_only', frm.doc.lock_weight_out_details);
			frm.set_df_property('lock_weight_out_details', 'read_only', true);
			frm.set_df_property('lock_quality_inspection', 'read_only', frm.doc.lock_quality_inspection);
		}

	},

	before_save(frm) {
		if (frm.fields_dict.lock_fields && frm.fields_dict.lock_fields.$wrapper.is(':visible')) {
			if (!frm.doc.lock_fields) {
				if (!frappe.user.has_role('System Manager') || !frappe.user.has_role('Accounts Manager')) {
					frappe.throw('Cannot save when "Lock Fields" is unchecked. Please select the checkbox.');
				}
			}
		}
		if (!frappe.user.has_role('System Manager') && !frappe.user.has_role('Accounts Manager')) {
			if (!frm.doc.lock_weight && (frm.doc.uom || frm.doc.weight_in)) {
				frappe.msgprint('Cannot save when "Lock Weight" is unchecked. Please select the checkbox.');
				frappe.validated = false;
			}
			else if (!frm.doc.lock_sampling && frm.doc.sampling_person_name) {
				frappe.msgprint('Cannot save when "Lock Sampling" is unchecked. Please select the checkbox.');
				frappe.validated = false;
			}
			// else  if (!frm.doc.lock_quality_inspection && (frm.doc.qc_details || frm.doc.grn)) {
			//   frappe.msgprint('Cannot save when "Lock Quality Inspection" is unchecked. Please select the checkbox.');
			//   frappe.validated = false; 
			// }
			else if (!frm.doc.lock_unload_details && frm.doc.unloading_person) {
				frappe.msgprint('Cannot save when "Lock Unload Details" is unchecked. Please select the checkbox.');
				frappe.validated = false;
			}
			else if (!frm.doc.lock_weight_out_details && (frm.doc.weight_out || frm.doc.net_weight)) {
				frappe.msgprint('Cannot save when "Lock Weight Out Details" is unchecked. Please select the checkbox.');
				frappe.validated = false;
			}
		}/* for Lock fields functionality end */
	}
});


function checkLock(frm) {
	const allFields = ['naming_series', 'entry_type', 'purpose', 'party_type', "supplier", 'invoice_no', 'challan_no', 'challan_date', 'outward_for', 'outward_entry', 'invoice_date', 'stock_item_tab', 'driver_name', 'driver_mobile_no', 'truck_no', 'remarks'];

	const isLocked = frm.doc.lock_fields;
	for (const field of allFields) {
		frm.set_df_property(field, 'read_only', isLocked);
	}

	if (frm.doc.entry_type === 'Inward') {
		frm.set_df_property('purpose', 'reqd', !isLocked);
		frm.set_df_property('driver_name', 'reqd', !isLocked);
		frm.set_df_property('driver_mobile_no', 'reqd', !isLocked);
		frm.set_df_property('truck_no', 'reqd', !isLocked);
		frm.set_df_property('supplier', 'reqd', !isLocked);
		frm.set_df_property('party_type', 'reqd', !isLocked);
	} else if (frm.doc.entry_type === 'Outward') {
		frm.set_df_property('purpose', 'reqd', !isLocked);
		frm.set_df_property('driver_name', 'reqd', !isLocked);
		frm.set_df_property('driver_mobile_no', 'reqd', !isLocked);
		frm.set_df_property('truck_no', 'reqd', !isLocked);
	} else {
		frm.set_df_property('entry_type', 'reqd', !isLocked);
	}
}

function toggleWeightLock(frm) {
	const isWeightInChecked = frm.doc.is_weight_in;
	const isLockWeightChecked = frm.doc.lock_weight;

	if (isWeightInChecked && isLockWeightChecked) {
		frm.set_df_property('uom', 'read_only', true);
		frm.set_df_property('weight_in', 'read_only', true);
		frm.set_df_property('is_weight_in', 'read_only', true);
	} else if (!isWeightInChecked && isLockWeightChecked) {
		frm.set_df_property('uom', 'read_only', true);
		frm.set_df_property('weight_in', 'read_only', false);
		frm.set_df_property('is_weight_in', 'read_only', true);
	} else {
		frm.set_df_property('uom', 'read_only', false);
		frm.set_df_property('weight_in', 'read_only', isLockWeightChecked);
		frm.set_df_property('is_weight_in', 'read_only', isLockWeightChecked);
	}
}

function toggleSamplingLock(frm) {
	const isSamplingDoneChecked = frm.doc.sampling_done;
	const isLockSamplingChecked = frm.doc.lock_sampling;
	const isSamplingPersonNameReadOnly = isSamplingDoneChecked && isLockSamplingChecked;
	frm.set_df_property('sampling_person_name', 'read_only', isSamplingPersonNameReadOnly);
	frm.set_df_property('sampling_done', 'read_only', isSamplingPersonNameReadOnly);
}


function toggleQualityLock(frm) {
	const isLockQualityInspectionChecked = frm.doc.lock_quality_inspection;
	frm.set_df_property('qc_details', 'read_only', isLockQualityInspectionChecked);
}


function toggleunloadLock(frm) {
	const isUnloadedChecked = frm.doc.is_unloaded;
	const isLockUnloadDetailsChecked = frm.doc.lock_unload_details;
	const isUnloadingPersonReadOnly = isUnloadedChecked && isLockUnloadDetailsChecked;
	frm.set_df_property('unloading_person', 'read_only', isUnloadingPersonReadOnly);
	frm.set_df_property('is_unloaded', 'read_only', isUnloadingPersonReadOnly);
}

function toggleWeightOutLock(frm) {
	const isWeightOutChecked = frm.doc.is_weight_out;
	const isLockWeightOutDetailsChecked = frm.doc.lock_weight_out_details;
	const isWeightOutReadOnly = isWeightOutChecked && isLockWeightOutDetailsChecked;
	frm.set_df_property('weight_out', 'read_only', isWeightOutReadOnly);
	frm.set_df_property('net_weight', 'read_only', isWeightOutReadOnly);
	frm.set_df_property('is_weight_out', 'read_only', isWeightOutReadOnly);
}
