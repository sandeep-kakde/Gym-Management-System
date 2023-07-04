// Copyright (c) 2023, Sandeep Kakde and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Fitness Metrics"] = {
	"filters": [
		{
			fieldname: "member_name",
			label: __("Customer Name"),
			fieldtype: "Link",
			options: "Gym Member",
			reqd: 1
		}
	]
};
