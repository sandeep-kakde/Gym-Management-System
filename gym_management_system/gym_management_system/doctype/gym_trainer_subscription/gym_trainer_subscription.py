# Copyright (c) 2023, Sandeep Kakde and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class GymTrainerSubscription(Document):
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
            "Gym Trainer", self.trainer, "ratings", total_rating / len(trainer_ratings)
        )
