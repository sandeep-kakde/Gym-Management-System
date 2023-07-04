import frappe
from frappe.model.docstatus import DocStatus
from frappe.utils import today, get_fullname, date_diff, format_date, getdate


def get_context(context):
    DATE_FORMAT = "dd-mm-yyyy"
    current_date_str = today()
    current_date_obj = getdate()
    context.user_full_name = get_fullname()
    member_id = frappe.db.get_value(
        "Gym Member", {"email": frappe.session.user})

    active_membership_details = frappe.db.get_value(
        "Gym Membership Subscription",
        {
            "member": ["=", member_id],
            "subscription_start_date": ["<=", current_date_str],
            "subscription_end_date": [">=", current_date_str],
        },
        ["gym_membership", "subscription_start_date", "subscription_end_date"],
    )

    context.is_membership_active = False
    context.active_membership = (
        active_membership_details[0]
        if active_membership_details
        else "No active membership"
    )
    if active_membership_details:
        context.is_membership_active = True
        context.subscription_start_date = format_date(active_membership_details[1], format_string=DATE_FORMAT)
        context.subscription_end_date = format_date(active_membership_details[2], format_string=DATE_FORMAT)
        context.days_remaining = date_diff(active_membership_details[2], current_date_str)


    trainer_filters = {
        "member": ["=", member_id],
        "docstatus": DocStatus.submitted()
    }
    trainer_fields = ["trainer", "subscription_start_date", "subscription_end_date"]
    trainer_subscriptions = frappe.db.get_all("Gym Trainer Subscription", filters=trainer_filters, fields=trainer_fields)
    context.current_trainer = "No active trainer subscription found"
    for t in trainer_subscriptions:
        t.trainer = frappe.db.get_value("Gym Trainer", t.trainer, "full_name")

        if current_date_obj >= t.subscription_start_date and current_date_obj <= t.subscription_end_date:
            context.current_trainer = t.trainer

        t.subscription_start_date = format_date(t.subscription_start_date, format_string=DATE_FORMAT)
        t.subscription_end_date = format_date(t.subscription_end_date, format_string=DATE_FORMAT)

    context.trainer_subscriptions = trainer_subscriptions