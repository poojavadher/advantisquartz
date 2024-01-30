// Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Serial No Update', {
	on_submit:function(frm) {
	        $.each(frm.doc.press_item || [], function(i, d) {
            var serial = d.serial_no;
            var batch_no = d.batch_no;
            var select_type = d.select_type;
            var length = d.length;
            var width = d.width;
            var  distributor_slab_time_in = d.distributor_slab_time_in;
            var distributor_slab_time_out = d.distributor_slab_time_out;
            var fram_no = d.fram_no;
            var hopper_opening_ = d.hopper_opening_;
            var distributor_operator_name = d.distributor_operator_name;
            var press_operator_name = d.press_operator_name;
            var slab_out_temp = d.slab_out_temp;
            var set_weight = d.set_weight;
            var hopper_weight = d.hopper_weight;
            var press_bar_weight = d.press_bar_weight;
            var actual_or_laying_weight = d.actual_or_laying_weight;
            var total_weight = d.total_weight;
            var floor_ = d.floor_;
            var operator_name = d.operator_name;
            var dv_dry_vein = d.dv_dry_vein;
            var mould_no = d.mould_no;
            var hopper_belt_speed_ = d.hopper_belt_speed_;
            var press_bar_belt = d.press_bar_belt;
            var mobile_station = d.mobile_station;
            var slab_in_time = d.slab_in_time;
            var top_temp = d.top_temp;
            var press_slab_in_time = d.press_slab_in_time;
            var press_slab_out_time = d.press_slab_out_time;
            var vaccum_delay = d.vaccum_delay;
            var vaccum_ = d.vaccum_;
            var stage_iv = d.stage_iv;
            var slab_out_time = d.slab_out_time;
            var slab_in_temp = d.slab_in_temp;
            var stage_i = d.stage_i;
            var stage_ii = d.stage_ii;
            var stage_iii = d.stage_iii;
            var stage__iv = d.stage__iv;
            var stage_v = d.stage_v;
            var bottemp = d.bottemp;
            var oven_operator_name = d.oven_operator_name
            var remarks = d.remarks;
            var manu_con_name = d.manufacturing_contractor_name;
		  frappe.db.set_value('Serial No',serial, {
                'serial_no_type': select_type,
                'custom_batch_no':batch_no,
                'length':length,
                'width':width,
                'serial_type':"Polish",
                'distributor_slab_time_in':distributor_slab_time_in,
                'distributor_slab_time_out':distributor_slab_time_out,
                'fram_no':fram_no,
                'hopper_opening_':hopper_opening_,
                'distributor_operator_name':distributor_operator_name,
                'press_operator_name':press_operator_name,
                'slab_out_temp':slab_out_temp,
                'set_weight':set_weight,
                'hopper_weight':hopper_weight,
                'press_bar_weight':press_bar_weight,
                'actual_or_laying_weight':actual_or_laying_weight,
                'total_weight':total_weight,
                'floor_':floor_,
                'operator_name':operator_name,
                'dv_dry_vein':dv_dry_vein,
                'mould_no':mould_no,
                'hopper_belt_speed_':hopper_belt_speed_,
                'press_bar_belt':press_bar_belt,
                "mobile_station":mobile_station,
                'slab_in_time':slab_in_time,
                'top_temp':top_temp,
                'press_slab_in_time':press_slab_in_time,
                'press_slab_out_time':press_slab_out_time,
                'vaccum_delay':vaccum_delay,
                'vaccum_':vaccum_,
                'stage_iv':stage_iv,
                'slab_out_time':slab_out_time,
                'slab_in_temp':slab_in_temp,
                'stage_i':stage_i,
                'stage_ii':stage_ii,
                'stage_iii':stage_iii,
                'stage__iv':stage__iv,
                'stage_v':stage_v,
                'bottemp':bottemp,
                'oven_operator_name':oven_operator_name,
                'press_remarks':remarks,
                'manufacturing_contact_name':manu_con_name,
                'press_date':cur_frm.doc.press_date,
            });
	    }); 
	    
	   
	  
	}
})
cur_frm.cscript.onload = function(frm) {
    cur_frm.set_query("serial_no", "press_item", function(doc, cdt, cdn) {
        var child = locals[cdt][cdn]; 
        return {
            "filters": {
                "status": "Active"  
            }
        };
    });
    
};

frappe.ui.form.on('Serial No Update', {
    refresh(frm) {
        frm.fields_dict["press_item"].grid.add_custom_button(__('Download'), function() {
            // Fetch child table data
            const childTableData = frm.doc.press_item;
            const fieldMapping = {};
            
            // Define a mapping of custom field names to child table field names
            frm.fields_dict["press_item"].grid.docfields.forEach(childField => {
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
            anchor.download = 'serial_no_update.csv';
            anchor.click();
        });

        // Change button style to match the primary color
        frm.fields_dict["press_item"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
    }
});


frappe.ui.form.on('Serial No Update', {
    refresh(frm) {
        frm.fields_dict["press_item"].grid.add_custom_button(__('Upload'), function() {
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
        frm.fields_dict["press_item"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
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
    frm.clear_table('press_item');

    // Add new child table rows based on the CSV data
    for (var k = 0; k < pressItems.length; k++) {
        var child = frm.add_child('press_item', pressItems[k]);
    }

    // Refresh the child table to display the newly added rows
    frm.refresh_field('press_item');

    frappe.msgprint(__('Data has been successfully loaded into the child table.'));
}



frappe.ui.form.on('Serial No Update', {
    refresh: function (frm) {
        frm.add_custom_button(__('Get Serial No.'), function () {
            var d = new frappe.ui.form.MultiSelectDialog({
                doctype: "Serial No",
                target: frm,
                setters: {
                    status: "Active",
                    item_code: null,
                    serial_type: "Press"
                },
                add_filters_group: 1,
                columns: ["status"],
                action(selections) {
                    console.log(selections);
                    d.dialog.hide();

                    selections.sort(compareSerialNumbers);

                    var child_table = frm.doc.press_item || [];
                    frm.clear_table("press_item");

                    selections.forEach(function (d) {
                        frappe.call({
                            method: "serial",
                            args: {
                                "serial_name": d
                            },
                            callback: function (data) {
                                var row = frm.add_child("press_item");
                                row.serial_no = d;
                                console.log(row.serial_no)
                                row.batch_no = data.custom_batch_no;

                                frm.refresh_field("press_item");
                            }
                        })
                    })
                }
            });
        });
    }
});

function compareSerialNumbers(a, b) {
    var partsA = a.match(/([a-zA-Z-]+)([0-9-]+)/);
    var partsB = b.match(/([a-zA-Z-]+)([0-9-]+)/);

    var alphanumericComparison = partsA[1].toLowerCase().localeCompare(partsB[1].toLowerCase());

    if (alphanumericComparison === 0) {
        var numA = parseInt(partsA[2]);
        var numB = parseInt(partsB[2]);

        return numA - numB;
    }

    return alphanumericComparison;
}






// frappe.ui.form.on('Serial No Update', {
//     refresh: function(frm) {
//         frm.add_custom_button(__('Get Serial No.'), function() {
//             var d = new frappe.ui.form.MultiSelectDialog({
//                 doctype: "Serial No",
//                 target: me.frm,
//                 setters: {
//                     status: "Active",
//                     item_code: null,
//                     serial_type:"Press"
//                 },
//                 add_filters_group: 1,
//                 columns: ["status"],
//                 action(selections){
//                     console.log(selections);
//                     d.dialog.hide();

//                     var child_table = cur_frm.doc.press_item || [];
//                     frm.clear_table("press_item");
                    
//                     selections.forEach(function(d){
                        
//                             frappe.call({
//                       method: "serial",
//                       args: {
//                           "serial_name": d
                           
//                       }, 
//                       callback: function(data)
//                       {
                           
//                           var row = frm.add_child("press_item");
//                             row.serial_no = d;
//                             console.log(row.serial_no)
//                             row.batch_no=data.custom_batch_no;
                          
//                             frm.refresh_field("press_item");
//                       }
//                          })

  
//                     })
//                 }
//             });
//         });
//     }
// });
