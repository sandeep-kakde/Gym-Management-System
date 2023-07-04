# Copyright (c) 2023, Sandeep Kakde and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class GroupClassBooking(Document):
    def before_save(self):
        existing_bookings = frappe.db.count(
            "Group Class Booking",
            filters={
                "class_name": self.class_name,
                "docstatus": DocStatus.submitted(),
            },
        )

        class_maximum_capacity = frappe.db.get_value(
            "Group Class", self.class_name, "maximum_capacity"
        )

        if existing_bookings >= int(class_maximum_capacity):
            frappe.throw("Class is full!")
