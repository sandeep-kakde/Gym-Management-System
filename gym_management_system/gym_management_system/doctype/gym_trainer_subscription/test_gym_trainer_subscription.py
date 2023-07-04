# Copyright (c) 2023, Sandeep Kakde and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestGymTrainerSubscription(FrappeTestCase):
    def create_gym_trainer(self):
        gym_trainer = frappe.get_doc({
            "doctype": "Gym Trainer"
        })
        gym_trainer.first_name = "John"
        gym_trainer.last_name = "Doe"
        gym_trainer.phone = "+91 1234567890"
        gym_trainer.email = "john@nomail.com"
        gym_trainer.insert()
        self.trainer_name = gym_trainer.name

    def create_gym_member(self):
        gym_member = frappe.get_doc({
            "doctype": "Gym Member"
        })
        gym_member.first_name = "Test"
        gym_member.date_of_birth = "2011-01-11"
        gym_member.weight = 56
        gym_member.last_name = "User"
        gym_member.phone = "+91 1234567890"
        gym_member.email = "test@nomail.com"
        gym_member.insert()
        self.member_name = gym_member.name

    def setUp(self):
        self.create_gym_trainer()
        self.create_gym_member()

    def test_update_trainer_ratings(self):
        subscription = frappe.get_doc({
            "doctype": "Gym Trainer Subscription"
        })
        subscription.trainer = self.trainer_name
        subscription.member = self.member_name
        subscription.trainer_rating = 4
        subscription.docstatus = 1
        subscription.subscription_start_date = "2023-06-01"
        subscription.subscription_end_date = "2023-06-10"
        subscription.insert()

        subscription.update_trainer_ratings()

        expected_ratings = 4
        actual_ratings = frappe.db.get_value("Gym Trainer", subscription.trainer, "ratings")
        self.assertEqual(expected_ratings, actual_ratings)
