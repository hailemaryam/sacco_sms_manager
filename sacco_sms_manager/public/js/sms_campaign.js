// Copyright (c) 2025, Sacco SMS Manager and contributors
// License: MIT. See LICENSE

frappe.ui.form.on("SMS Campaign", {
	refresh(frm) {
		if (!frm.doc.__islocal && frm.doc.status !== "Sent") {
			frm.add_custom_button(__("Send Now"), () => {
				frappe.confirm(
					__("Send SMS to all target members now?"),
					() => {
						frm.call({
							method: "send_now",
							doc: frm.doc,
							callback(r) {
								if (!r.exc) {
									frappe.msgprint({
										title: __("Campaign Sent"),
										message: __("SMS sent to {0} members.", [r.message.sent_count]),
										indicator: "green",
									});
									frm.reload_doc();
								}
							},
						});
					}
				);
			}, __("Actions"));
		}
	},
	send_to_all_members(frm) {
		if (frm.doc.send_to_all_members) {
			frm.set_value("target_members", []);
		}
	},
});
