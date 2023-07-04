# Copyright (c) 2023, Sandeep Kakde and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class GymLockerBooking(Document):
    def before_save(self):
        booking_start_date = self.booking_start_date
        booking_end_date = self.booking_end_date

        existing_bookings = frappe.db.count(
            "Gym Locker Booking",
            filters={
                "docstatus": DocStatus.submitted(),
                "name": ["!=", self.name],
                "booking_start_date": ["<=", booking_end_date],
                "booking_end_date": [">=", booking_start_date],
            },
        )

        no_of_lockers = frappe.db.get_value("Gym Settings", "Gym Settings", "no_of_lockers")

        if existing_bookings >= int(no_of_lockers):
            frappe.throw("All lockers are currently booked.")
