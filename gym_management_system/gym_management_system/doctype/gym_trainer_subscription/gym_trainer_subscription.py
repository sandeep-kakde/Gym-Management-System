# Copyright (c) 2023, Sandeep Kakde and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class GymTrainerSubscription(Document):
    def before_save(self):
        self.check_duplicate_entry()

    def on_submit(self):
        self.update_trainer_ratings

    def on_cancel(self):
        self.update_trainer_ratings()

    def update_trainer_ratings(self):
        filters = {"trainer": self.trainer, "docstatus": DocStatus.submitted()}
        trainer_ratings = frappe.db.get_all(
            "Gym Trainer Subscription", filters=filters, pluck="trainer_rating"
        )

        total_rating = 0
        for rating in trainer_ratings:
            total_rating += rating

        frappe.db.set_value(
            "Gym Trainer", self.trainer, "ratings", total_rating / (len(trainer_ratings) or 1)
        )

    def check_duplicate_entry(self):
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
            "Gym Trainer Subscription",
            filters=filters,
            or_filters=or_filters,
            pluck="name",
        )

        if exists:
            duplicate_membership_link = frappe.utils.get_link_to_form(
                "Gym Trainer Subscription", exists[0]
            )
            frappe.throw(
                f"Another active Trainer Subscription exists for the user with name {duplicate_membership_link}"
            )
