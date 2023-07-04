# Copyright (c) 2023, Sandeep Kakde and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    chart = get_chart_data(data)
    return columns, data, None, chart


def get_data(filters=None):
    return frappe.db.sql(
        f"""
        SELECT
            member.full_name,
            metric.date,
            metric.weight_kgs,
            metric.exercise_duration,
            metric.calories_intake,
            metric.heart_rate
        FROM
            `tabFitness Metrics` metric
        INNER JOIN
            `tabGym Member` member
        ON
            metric.member = member.name
        WHERE
            metric.member = '{filters.member_name}'
        ORDER BY
            metric.date
        """,
        as_dict=1,
    )


def get_columns():
    return [
        {
            "fieldname": "full_name",
            "label": "Customer Name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "date",
            "label": "Date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "fieldname": "exercise_duration",
            "label": "Exercise Duration",
            "fieldtype": "Duration",
            "width": 120,
        },
        {
            "fieldname": "weight_kgs",
            "label": "Weight (Kgs)",
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "fieldname": "calories_intake",
            "label": "Calories Intake",
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "fieldname": "heart_rate",
            "label": "Hear Rate",
            "fieldtype": "Int",
            "width": 120,
        },
    ]


def get_chart_data(data):
    labels = [d.get("date") for d in data]
    datasets = [
        {
            "name": "Weight (Kgs)",
            "chartType": "line",
            "values": [d.get("weight_kgs") for d in data],
        },
        {
            "name": "Calories Intake",
            "chartType": "line",
            "values": [d.get("calories_intake") for d in data],
        },
        {
            "name": "Heart Rate",
            "chartType": "line",
            "values": [d.get("heart_rate") for d in data],
        }
    ]

    chart = {"data": {"labels": labels, "datasets": datasets}}
    chart["type"] = "line"

    return chart
