# Copyright (c) 2023, Sandeep Kakde and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe.utils import add_to_date


class GymMembershipSubscription(Document):
    def before_save(self):
        duration_in_months = frappe.db.get_value(
            "Gym Membership", self.gym_membership, "duration_in_months"
        )
        self.subscription_end_date = add_to_date(
            self.subscription_start_date, months=duration_in_months
        )

        filters = [
            ["member", "=", self.member],
            ["docstatus", "=", DocStatus.submitted()],
        ]
        or_filters = [
            [
                "subscription_start_date",
                "Between",
                [self.subscription_start_date, self.subscription_end_date],
            ],
            [
                "subscription_end_date",
                "Between",
                [self.subscription_start_date, self.subscription_end_date],
            ],
        ]

        exists = frappe.db.get_all(
            "Gym Membership Subscription",
            filters=filters,
            or_filters=or_filters,
            pluck="name",
        )

        if exists:
            duplicate_membership_link = frappe.utils.get_link_to_form(
                "Gym Membership Subscription", exists[0]
            )
            frappe.throw(
                f"Another active membership exists for the user with name {duplicate_membership_link}"
            )
