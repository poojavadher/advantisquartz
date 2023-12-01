// Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lab Sample', {
	mesh_qc_template(frm) {
	    if (frm.doc.mesh_qc_template){
	       frappe.model.with_doc("Mesh QC Template", frm.doc.mesh_qc_template, function() {
                var tabletransfer= frappe.model.get_doc("Mesh QC Template", frm.doc.mesh_qc_template);
                $.each(tabletransfer.parameters, function(index, row){
                    var d = frm.add_child("lab_sections_and_mesh_no");
                    d.lab_section = row.lab_section;
                    d.mesh_no = row.mesh_no;
                    frm.refresh_field("lab_sections_and_mesh_no");
					cur_frm.set_value('inspected_by', frappe.session.user);
					cur_frm.refresh_field('inspected_by');
                });
            });
	    }
	    else{
	        frm.clear_table("lab_sections_and_mesh_no");
	        frm.refresh_field("lab_sections_and_mesh_no");
			cur_frm.set_value('inspected_by', "");
			cur_frm.refresh_field('inspected_by');
	    }

	},
	quality_inspection_template: function(frm) {
		if (frm.doc.quality_inspection_template) {
			return frm.call({
				method: "get_item_specification_details",
				doc: frm.doc,
				callback: function() {
					refresh_field('readings');
					cur_frm.set_value('inspected_by', frappe.session.user);
					cur_frm.refresh_field('inspected_by');
				}
			});
		}
		else{
	        frm.clear_table("readings");
	        frm.refresh_field("readings");
			cur_frm.set_value('inspected_by', "");
			cur_frm.refresh_field('inspected_by');
	    }
	},
});
