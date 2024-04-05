// Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Polish Serial No Update', {
	on_submit:function(frm) {
	        $.each(frm.doc.polish_item || [], function(i, d) {
            var serial = d.slab_no;
            var batch_no = d.batch;
            var weight = d.net_weight;
            var length = d.length;
            var width = d.width;
            var grade = d.qc_grade;
            var polish_date_ = d.polish_date_;
            var thickness_in_mm_1 = d.thickness_in_mm_1;
            var thickness_in_mm_2 = d.thickness_in_mm_2;
            var thickness_in_mm_3 = d.thickness_in_mm_3 ;
            var thickness_in_mm_4 = d.thickness_in_mm_4;
            var thickness_in_mm_5 = d.thickness_in_mm_5;
            var shift = d.custom_qc_shift;
            var repair = d.repair;
            var remarks_qc = d.remarks_qc;
            var thickness_1 = d.thickness_1;
            var thickness_2 = d.thickness_2 ;
            var thickness_3 = d.thickness_3 ;
            var thickness_4 =  d.thickness_1;
            var thickness_5 = d.thickness_4 ;
            var thickness_6 = d.thickness_6 ;
            var back__repairr = d.custom_back_repair_by;
            var repolish_reason = d.repolish_reason;
            var w_final_size = d.w_final_size;
            var qc_date = d.qc_date;
            var unloading_operator_name = d.unloading_operator_name;
            var remarks = d.custom_remarks_other;
            var raw_slab_weight = d.raw_slab_weight;
            var bend = d.bend;
            var rp_1 = d.rp_1;
            var qc_name_supervisor = d.qc_name_supervisor;
            var gloss_value__ = d.gloss_value__;
            var l_final_size = d.l_final_size;
            var repair_con = d.repair_contact_name;
            
		  frappe.db.set_value('Serial No',serial, {
                'gross_weight': weight,
                'quality':grade,
                'custom_batch_no':batch_no,
                'length':length,
                'width':width,
                'serial_type':"Finish",
                'polish_date_' : polish_date_,
                'thickness_in_mm_1' : thickness_in_mm_1,
                'thickness_in_mm_2' : thickness_in_mm_2,
                'thickness_in_mm_3' : thickness_in_mm_3,
                'thickness_in_mm_4' : thickness_in_mm_4,
                'thickness_in_mm_5' : thickness_in_mm_5,
                'shift' : shift,
                'repair' : repair,
                'remarks_qc' : remarks_qc,
                'thickness_1' : thickness_1,
                'thickness_2' : thickness_2 ,
                'thickness_3' : thickness_3 ,
               'thickness_4' :  thickness_1,
                'thickness_5' : thickness_4 ,
                'thickness_6' : thickness_6 ,
                'back__repairr' : back__repairr,
                'repolish_reason' : repolish_reason,
                'w_final_size' : w_final_size,
                'qc_date' : qc_date,
                'unloading_operator_name' : unloading_operator_name,
                'remarks' : remarks,
                'raw_slab_weight' : raw_slab_weight,
                'bend' : bend,
                'rp_1' : rp_1,
                'qc_name_supervisor' : qc_name_supervisor,
                'gloss_value__' : gloss_value__,
                'l_final_size ': l_final_size,
                'repair_contact_name':repair_con
                

            });
	    }); 
	    
	}
})
cur_frm.cscript.onload = function(frm) {
    cur_frm.set_query("slab_no", "polish_item", function(doc, cdt, cdn) {
        var child = locals[cdt][cdn]; 
        var itemcode = child.item_code;
        return {
            "filters": {
                "item_code": itemcode,
                "status":"Active"
            }
        };
    });
    
};


frappe.ui.form.on('Polish Serial No Update', {
    refresh(frm) {
        frm.fields_dict["polish_item"].grid.add_custom_button(__('Download'), function() {
            // Fetch child table data
            const childTableData = frm.doc.polish_item;
            const fieldMapping = {};
            
            // Define a mapping of custom field names to child table field names
            frm.fields_dict["polish_item"].grid.docfields.forEach(childField => {
                if (childField.fieldname !== 'name' && 
                    childField.fieldtype !== 'Column Break' && 
                    childField.fieldtype !== 'Section Break') {
                    fieldMapping[childField.fieldname] = childField.fieldname;
                }
            });

            // Create a CSV string with custom field names as the first row
            const csvContent = "data:text/csv;charset=utf-8," 
                + Object.keys(fieldMapping).join(',') + '\n'
                + childTableData.map(row => Object.keys(fieldMapping).map(customField => row[fieldMapping[customField]] || "").join(',')).join('\n');

            // Create a temporary anchor element to trigger the download
            const anchor = document.createElement('a');
            anchor.href = encodeURI(csvContent);
            anchor.target = '_blank';
            anchor.download = 'polish_serial_no_update.csv';
            anchor.click();
        });

        // Change button style to match the primary color
        frm.fields_dict["polish_item"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
    }
});


frappe.ui.form.on('Polish Serial No Update', {
    refresh(frm) {
        frm.fields_dict["polish_item"].grid.add_custom_button(__('Upload'), function() {
            // Create a file input element dynamically
            var fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = '.csv,.xlsx';
            
            // Trigger the file selection when the file input changes
            fileInput.addEventListener('change', function(event) {
                handleFileUpload(event.target.files[0]);
            });

            // Trigger the file input click event
            fileInput.click();
        });

        // Change button style to match the primary color
        frm.fields_dict["polish_item"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
    }  
});
function handleFileUpload(file) {
    if (!file) {
        frappe.msgprint(__('No file selected.'));
        return;
    }

    var reader = new FileReader();
    reader.onload = function(event) {
        var csvData = event.target.result;
        processData(csvData);
    };
    reader.readAsText(file);
}
function processData(csvData) {
    var lines = csvData.split('\n');
    var fieldNames = lines[0].split(','); // Assuming the first row contains field names

    // Remove the header line from the lines array
    lines.splice(0, 1);

    var pressItems = [];
    for (var i = 0; i < lines.length; i++) {
        var values = lines[i].split(',');

        // Skip empty lines
        if (values.length === 1 && values[0].trim() === '') {
            continue;
        }

        var pressItem = {};
        for (var j = 0; j < fieldNames.length; j++) {
            // Trim any leading/trailing spaces from field names and values
            var fieldName = fieldNames[j].trim();
            var value = values[j].trim();

            // Map the field name with its corresponding value
            pressItem[fieldName] = value;
        }

        pressItems.push(pressItem);
    }

    // Get the current form instance
    var frm = cur_frm;

    // Clear existing child table rows
    frm.clear_table('polish_item');

    // Add new child table rows based on the CSV data
    for (var k = 0; k < pressItems.length; k++) {
        var child = frm.add_child('polish_item', pressItems[k]);
    }

    // Refresh the child table to display the newly added rows
    frm.refresh_field('polish_item');

    frappe.msgprint(__('CSV data has been successfully loaded into the child table.'));
}

frappe.ui.form.on('Polish Serial No Update', {
    refresh: function(frm) {
        frm.add_custom_button(__('Get Serial No.'), function() {
            var d = new frappe.ui.form.MultiSelectDialog({
                doctype: "Serial No",
                target: me.frm,
                setters: {
                    status: "Active",
                    serial_type:"Polish",
                    item_code: null,
                },
                add_filters_group: 1,
                columns: ["status"],
                action(selections){
                    console.log(selections);
                    d.dialog.hide();

                    var child_table = cur_frm.doc.polish_item || [];
                    frm.clear_table("polish_item");
                    
                    selections.forEach(function(d){
                        
                            frappe.call({
                       method: "serial",
                       args: {
                           "serial_name": d
                           
                       }, 
                       callback: function(data)
                       {
                           
                           var row = frm.add_child("polish_item");
                            row.slab_no = d;
                            row.item_code = data.item_code
                            row.item_name = data.item_name
                            row.batch=data.custom_batch_no
                            row.weight=data.gross_weight
                            row.length = data.length
                            row.width=data.width
                          
 frm.refresh_field("polish_item");
                       }
                         })

  
                    })
                }
            });
        });
    }
});


