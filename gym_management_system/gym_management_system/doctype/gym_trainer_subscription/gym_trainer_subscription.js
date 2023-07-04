// Copyright (c) 2023, Sandeep Kakde and contributors
// For license information, please see license.txt

frappe.ui.form.on("Gym Trainer Subscription", {
	refresh: async function(frm) {
		if (!frappe.user_roles.includes("Gym Admin")) {
			memberDocName = (await frappe.db.get_value("Gym Member", {"email": frappe.session.user}, "name")).message.name
			frm.set_query("member", function () {
				return {
					filters: {
						name: memberDocName,
					},
				};
			});
		}
	}
});
