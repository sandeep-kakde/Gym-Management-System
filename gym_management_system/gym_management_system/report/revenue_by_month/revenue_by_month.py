# Copyright (c) 2023, Sandeep Kakde and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):

    columns, data = get_columns(), get_data()
    chart = get_chart_data(data)
    return columns, data, None, chart


def get_data():
    results = frappe.db.sql(
        """
        SELECT
            s.subscription_start_date,
            s.subscription_end_date,
            m.price,
            m.membership_plan_name
        FROM
            `tabGym Membership Subscription` s
        INNER JOIN
            `tabGym Membership` m
        ON
            s.gym_membership = m.name
        WHERE
            s.docstatus = 1
        ORDER BY
            s.subscription_start_date
        """,
        as_dict=1,
    )

    revenue_by_month = {}
    for r in results:
        month = r.subscription_start_date.strftime("%B-%Y")

        if month not in revenue_by_month:
            revenue_by_month[month] = 0

        revenue_by_month[month] += r.price

    data = []
    for month, revenue in revenue_by_month.items():
        data.append({
            "month": month,
            "revenue": revenue,
        })

    return data


def get_columns():
    return [
        {
            "fieldname": "month",
            "label": "Month",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "revenue",
            "label": "Revenue",
            "fieldtype": "Float",
            "width": 150,
        },
    ]


def get_chart_data(data):
    labels = [d.get("month") for d in data]
    datasets = [
        {
            "name": "Revenue",
            "chartType": "bar",
            "values": [d.get("revenue") for d in data],
        }
    ]

    chart = {"data": {"labels": labels, "datasets": datasets}}
    chart["type"] = "bar"

    return chart