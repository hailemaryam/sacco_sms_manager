// Copyright (c) 2025, Sacco SMS Manager and contributors
// License: MIT. See LICENSE

frappe.ui.form.on("Loan Saving Payment", {
	refresh(frm) {
		console.log("Loan Saving Payment JS loaded", {
			status: frm.doc.payment_status
		});

		if (frm.doc.payment_status !== "Paid") {
			frm.add_custom_button(__("Mark as Paid"), () => {
				frm.set_value("payment_date", frappe.datetime.get_today());
				frm.save();
			}, __("Actions"));
		} else {
			frm.add_custom_button(__("Unmark as Paid"), () => {
				frm.set_value("payment_date", "");
				frm.save();
			}, __("Actions"));
		}

		if (frm.doc.payment_status === "Pending") {
			frm.add_custom_button(__("Send Reminder SMS"), () => {
				frappe.call({
					method: "sacco_sms_manager.api.send_loan_saving_payment_reminder",
					args: { payment_name: frm.doc.name },
					callback(r) {
						if (!r.exc) {
							frappe.show_alert({ message: __("Reminder SMS sent."), indicator: "green" });
						}
					},
				});
			}, __("Actions"));
		}
	},
});
