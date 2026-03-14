// Copyright (c) 2025, Sacco SMS Manager and contributors
// License: MIT. See LICENSE

frappe.ui.form.on("Membership Fee Payment", {
	refresh(frm) {
		if (
			!frm.doc.__islocal &&
			!["Paid"].includes(frm.doc.payment_status)
		) {
			frm.add_custom_button(__("Send Reminder SMS"), () => {
				frappe.call({
					method: "sacco_sms_manager.api.send_membership_fee_reminder",
					args: { payment_name: frm.doc.name },
					callback(r) {
						if (r.exc) {
							frappe.msgprint({
								title: __("Error"),
								message: r.message,
								indicator: "red",
							});
						} else {
							frappe.msgprint({
								title: __("Success"),
								message: __("Reminder SMS sent."),
								indicator: "green",
							});
						}
					},
				});
			}, __("Actions"));
		}
	},
});
