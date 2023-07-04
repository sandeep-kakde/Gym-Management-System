import frappe


def execute():
    group_class_types = [
        "Yoga",
        "Power Yoga",
        "Zumba",
        "Cross Fit",
        "Cardio",
    ]
    records = [
        {"doctype": "Group Class Type", "group_class_type": d}
        for d in group_class_types
    ]
    for record in records:
        frappe.get_doc(record).insert(
            ignore_permissions=True,
            ignore_if_duplicate=True,
        )
