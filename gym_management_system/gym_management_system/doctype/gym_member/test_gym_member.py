# Copyright (c) 2023, Sandeep Kakde and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe import MandatoryError


class TestGymMember(FrappeTestCase):
    def test_mandatory(self):
        gym_member = frappe.get_doc({
            "doctype": "Gym Member"
        })

        self.assertRaises(MandatoryError, gym_member.insert)
