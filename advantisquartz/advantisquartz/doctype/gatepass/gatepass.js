// Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('GatePass', {
	refresh: function(frm){
		// if (frm.doc.select_type == "Employee"){
		// 	frm.set_value('in_time',null)
		// }
		if (frm.doc.select_type == "Visitor" && frm.doc.workflow_state == "Pending"){
			frm.set_df_property('out_time',  'hidden', 1);
			frm.set_df_property('gate_out',  'hidden', 1);
			if(frm.doc.approver_email == frappe.session.user){
				frm.set_df_property('gate_out',  'hidden', 1);
			}
		}
		if (frm.doc.select_type == "Visitor" && frm.doc.workflow_state == "Approved"){
			if(frm.doc.approver_email == frappe.session.user){
				frm.set_df_property('gate_out',  'hidden', 1);
			}
			// else{
			// 	if (frm.doc.gate_out == 1){
			// 		frm.add_custom_button(__("Gate Out"), function() {
			// 			frm.set_value('out_time',frappe.datetime.now_time());
			// 			// frm.set_value('workflow_state','Gate Out');
			// 			frm.save('Update');
			// 			location.reload();
			// 		})
			// 	}
				
			// }
			frm.set_df_property('out_time',  'hidden', 1);
		}
		if (frm.doc.gate_out == 1){
			frm.add_custom_button(__("Gate Out"), function() {
				frm.set_value('out_time',frappe.datetime.now_time());
				// frm.set_value('workflow_state','Gate Out');
				frm.save('Update');
				location.reload();
			})
		}
		
	},
	empcode: function(frm) {
		if (frm.doc.select_type == "Employee"){
			frm.set_value('out_time',frappe.datetime.now_time())
			frm.set_value('to_meet_with',null);
		}
	},
	visitor_name: function(frm) {
		if (frm.doc.select_type == "Visitor"){
			frm.set_value('in_time',frappe.datetime.now_time())
		}
	}
});
