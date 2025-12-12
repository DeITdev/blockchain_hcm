// Copyright (c) 2025, Danar IT and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Credential", {
  refresh: function (frm) {
    // Add custom buttons
    if (frm.doc.verification_status === "Pending") {
      frm.add_custom_button(__("Verify Credential"), function () {
        frappe.call({
          method: "blockchain_hcm.blockchain_hcm.doctype.employee_credential.employee_credential.verify_credential",
          args: {
            credential_name: frm.doc.name
          },
          callback: function (r) {
            if (r.message) {
              frm.reload_doc();
            }
          }
        });
      }).addClass("btn-primary");
    }

    if (frm.doc.verification_status === "Verified") {
      frm.add_custom_button(__("Revoke Credential"), function () {
        frappe.confirm(
          __("Are you sure you want to revoke this credential?"),
          function () {
            frappe.call({
              method: "blockchain_hcm.blockchain_hcm.doctype.employee_credential.employee_credential.revoke_credential",
              args: {
                credential_name: frm.doc.name
              },
              callback: function (r) {
                if (r.message) {
                  frm.reload_doc();
                }
              }
            });
          }
        );
      }).addClass("btn-danger");
    }

    // Set color indicator based on status
    if (frm.doc.verification_status) {
      frm.set_indicator_color(frm.doc.verification_status);
    }
  },

  employee: function (frm) {
    // Auto-fetch employee name
    if (frm.doc.employee) {
      frappe.db.get_value("Employee", frm.doc.employee, "employee_name", function (r) {
        if (r && r.employee_name) {
          frm.set_value("employee_name", r.employee_name);
        }
      });
    }
  },

  set_indicator_color: function (status) {
    let color_map = {
      "Pending": "orange",
      "Verified": "green",
      "Expired": "red",
      "Revoked": "darkgrey"
    };

    frappe.show_alert({
      message: __("Status: {0}", [status]),
      indicator: color_map[status] || "blue"
    });
  }
});
