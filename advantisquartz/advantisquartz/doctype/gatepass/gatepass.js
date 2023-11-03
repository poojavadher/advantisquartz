// Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('GatePass', {
	refresh: function(frm){
		if (frm.doc.select_type == "Employee" && frm.doc.workflow_state == "Pending"){
			frm.set_df_property('in_time',  'hidden', 1);
			frm.set_df_property('out_time',  'hidden', 1);
		}
		if (frm.doc.select_type == "Employee" && frm.doc.workflow_state == "Approved"){	
			frm.set_df_property('in_time',  'hidden', 1);
			setTimeout(() => {
				frm.page.actions.find('[data-label="Gate%20In"]').parent().parent().remove();
			}, 500);
			if (frm.doc.gate_in == 0 && frappe.user.has_role("Gate Entry Operator")){
				frm.add_custom_button(__("Gate In"), function() {
					frm.set_value('gate_in',1);
					frm.set_value('in_time',frappe.datetime.now_time());
					frm.set_value('workflow_state','Gate In');
					frm.save('Update');
					location.reload();
				}).css({"color":"white", "background-color": "#14141f", "font-weight": "800"});
			}
		}
		if (frm.doc.select_type == "Visitor" && frm.doc.workflow_state == "Pending"){
			frm.set_df_property('out_time',  'hidden', 1);
			frm.set_df_property('gate_out',  'hidden', 1);
			// if(frm.doc.approver_email == frappe.session.user){
			// 	frm.set_df_property('gate_out',  'hidden', 1);
			// }
		}
		if (frm.doc.select_type == "Visitor" && frm.doc.workflow_state == "Approved"){
			if(frm.doc.approver_email == frappe.session.user){
				frm.set_df_property('gate_out',  'hidden', 1);
			}
			else{
				if (frm.doc.gate_out == 0){
					frm.add_custom_button(__("Gate Out"), function() {  	
						frm.set_value('gate_out',1);
						frm.set_value('out_time',frappe.datetime.now_time());
						frm.set_value('workflow_state','Gate Out');
						frm.save('Update');
						location.reload();
					}).css({"color":"white", "background-color": "#14141f", "font-weight": "800"});
				}
				
			}
			frm.set_df_property('out_time',  'hidden', 1);
		}
	},
	empcode: function(frm) {
		if (frm.doc.select_type == "Employee"){
			// frm.set_value('out_time',frappe.datetime.now_time())
			frm.set_value('to_meet_with',null);
		}
	},
	visitor_name: function(frm) {
		if (frm.doc.select_type == "Visitor"){
			frm.set_value('in_time',frappe.datetime.now_time())
		}
	},
	company_staff: function(frm){
		if(frm.doc.company_staff == 1){
			frm.set_value('company_labour',0);
			frm.set_value('contractor_labour',0);
		}
	},
	company_labour: function(frm){
		if(frm.doc.company_labour == 1){
			frm.set_value('company_staff',0);
			frm.set_value('contractor_labour',0);
		}
	},
	contractor_labour: function(frm){
		if(frm.doc.contractor_labour == 1){
			frm.set_value('company_labour',0);
			frm.set_value('company_staff',0);
		}
	},
});
