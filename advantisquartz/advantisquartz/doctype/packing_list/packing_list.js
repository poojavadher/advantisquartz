// Copyright (c) 2023, pooja@sanskartechnolab.com and contributors
// For license information, please see license.txt

cur_frm.cscript.onload = function (frm) {
    cur_frm.set_query("serial_no", "items", function (doc, cdt, cdn) {
        var child = locals[cdt][cdn];
        var itemcode = child.item_code;
        return {
            "filters": {
                "item_code": itemcode,
                "status": "Active",
                "serial_type": "Finish"
            }
        };
    });
};

frappe.ui.form.on('Packing list', {
    container_no: function (frm) {
        $.each(frm.doc.items || [], function (i, d) {
            d.container_no = cur_frm.doc.container_no;
        });
    }
});


frappe.ui.form.on('Packing list', {
    refresh: function (frm) {
        frm.add_custom_button(__('Get Serial No.'), function () {
            var d = new frappe.ui.form.MultiSelectDialog({
                doctype: "Serial No",
                target: frm,
                setters: {
                    status: "Active",
                    serial_type: "Finish",
                    item_code: null,
                    quality: null,
                    sales_order:cur_frm.doc.sales_order

                },
                add_filters_group: 1,
                size: 'extra-large',
                action(selections) {
                    // console.log(selections);
                    d.dialog.hide();

                    var child_table = frm.doc.items || [];
                    // frm.clear_table("items");

                    selections.forEach(function (d) {
                        frappe.call({
                            method: "serial",
                            args: {
                                "serial_name": d
                            },
                            callback: function (data) {
                                var row = frm.add_child("items");
                                row.serial_no = d;
                                row.item_code = data.item_code;
                                row.production_weight = data.gross_weight;
                                row.production_length = data.length;
                                row.production_width = data.width;
                                row.production_grade = data.quality; // Make sure 'quality' is set properly
                                frm.refresh_field("items"); // Refresh the data table to display the updated 'Quality' value
                            }
                        });
                    });
                }
            });
        }).css({"color":"white", "background-color": "#14141f", "font-weight": "800"});
    }
});

frappe.ui.form.on('Packing list', {
    refresh: function (frm) {
        frm.add_custom_button(__('Get Serial No.'), function () {
            var d = new frappe.ui.form.MultiSelectDialog({
                doctype: "Serial No",
                target: frm,
                setters: {
                    status: "Active",
                },
                add_filters_group: 1,
                action(selections) {
                    // console.log(selections);
                    d.dialog.hide();

                    // Display a "Hello" message after hiding the dialog
                    frappe.msgprint("Hello");
                },
            });

            // Set the width of the dialog box using !important
            d.$wrapper.find('.modal-dialog').css("width", "800px !important");

            d.show();
        });
    }
});


frappe.ui.form.on('Packing list', {
    refresh(frm) {
        frm.fields_dict["items"].grid.add_custom_button(__('Download'), function () {
            // Fetch child table data
            const childTableData = frm.doc.items;
            const fieldMapping = {};

            // Define a mapping of custom field names to child table field names
            frm.fields_dict["items"].grid.docfields.forEach(childField => {
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
            anchor.download = 'packing_list.csv';
            anchor.click();
        });

        // Change button style to match the primary color
        frm.fields_dict["items"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
    }
});

frappe.ui.form.on('Packing list', {
    refresh(frm) {
        frm.fields_dict["items"].grid.add_custom_button(__('Upload'), function () {
            // Create a file input element dynamically
            var fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = '.csv,.xlsx';

            // Trigger the file selection when the file input changes
            fileInput.addEventListener('change', function (event) {
                handleFileUpload(event.target.files[0]);
            });

            // Trigger the file input click event
            fileInput.click();
        });

        // Change button style to match the primary color
        frm.fields_dict["items"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
    }
});
function handleFileUpload(file) {
    if (!file) {
        frappe.msgprint(__('No file selected.'));
        return;
    }

    var reader = new FileReader();
    reader.onload = function (event) {
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
    frm.clear_table('items');

    // Add new child table rows based on the CSV data
    for (var k = 0; k < pressItems.length; k++) {
        var child = frm.add_child('items', pressItems[k]);
    }

    // Refresh the child table to display the newly added rows
    frm.refresh_field('items');

    frappe.msgprint(__('CSV data has been successfully loaded into the child table.'));
}
frappe.ui.form.on('Packing list', {
    after_cancel: function (frm) {
        $.each(frm.doc.items || [], function (i, d) {
            var serial = d.serial_no;
            frappe.db.set_value('Serial No', serial, {
                'status': "Active",
                "serial_type": "Finish",
                "packing_list" : " ",
                "custom_sales_grade":"",
                "custom_sales_weight":"",
                "custom_saleable_measurement":"",
                "custom_sales_width":"",
                "custom_sales_length":""
            });
        });
    },
})

frappe.ui.form.on('Packing List Item', {
    before_items_remove(frm, cdt, cdn) {
        var child = frappe.get_doc(cdt, cdn);
        var serialNo = child.serial_no;
        if (serialNo) {
            // Update the 'status' field in the 'Serial Number' DocType
            frappe.db.set_value('Serial No', serialNo, {
                'status': "Active",
                "packing_list": "",
                "custom_sales_grade":"",
                "custom_sales_weight":"",
                "custom_saleable_measurement":"",
                "custom_sales_width":"",
                "custom_sales_length":""
            });
        }
        frm.save()
    }
});
    
