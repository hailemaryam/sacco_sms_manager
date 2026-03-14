// Copyright (c) 2025, Sacco SMS Manager and contributors
// License: MIT. See LICENSE

frappe.ui.form.on("Member", {
	refresh(frm) {
		if (!frm.doc.__islocal && frm.doc.phone) {
			frm.add_custom_button(__("Send SMS"), () => {
				const d = new frappe.ui.Dialog({
					title: __("Send SMS"),
					fields: [
						{
							fieldname: "message",
							fieldtype: "Small Text",
							label: __("Message"),
							reqd: 1,
						},
					],
					primary_action_label: __("Send"),
					primary_action(values) {
						frappe.call({
							method: "sacco_sms_manager.api.send_sms_to_member",
							args: { member: frm.doc.name, message: values.message },
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
										message: __("SMS sent successfully."),
										indicator: "green",
									});
									d.hide();
								}
							},
						});
					},
				});
				d.show();
			}, __("Actions"));
		}
	},
});
