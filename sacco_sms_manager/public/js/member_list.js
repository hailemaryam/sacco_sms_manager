// Copyright (c) 2025, Sacco SMS Manager and contributors
// License: MIT. See LICENSE

frappe.listview_settings["Member"] = {
	onload(listview) {
		listview.page.add_menu_item(__("Send Bulk SMS"), () => {
			const selected = listview.get_checked_items(true);
			if (selected.length === 0) {
				frappe.msgprint({
					title: __("No Selection"),
					message: __("Please select members to send SMS."),
					indicator: "orange",
				});
				return;
			}
			const d = new frappe.ui.Dialog({
				title: __("Send Bulk SMS"),
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
						method: "sacco_sms_manager.api.send_bulk_sms",
						args: {
							members: selected,
							message: values.message,
						},
						callback(r) {
							if (r.exc) {
								frappe.msgprint({
									title: __("Error"),
									message: r.message,
									indicator: "red",
								});
							} else {
								const res = r.message;
								frappe.msgprint({
									title: __("Bulk SMS Sent"),
									message: __(
										"Successfully sent to {0} of {1} members.",
										[res.success_count, res.success_count + res.failed_count]
									),
									indicator: "green",
								});
								d.hide();
								listview.refresh();
							}
						},
					});
				},
			});
			d.show();
		});
	},
};
