"""
OmniCorp System Execution Module
Used by Foundry Agent Code Interpreter for Transactional and Personal Data Actions
"""
import datetime
import random

# Corporate baseline entitlements
POLICY_ENTITLEMENTS = {
    "annual_leave_days": 18,
    "sick_leave_days": 10,
    "paternity_leave_days": 10,  # 10 working days
    "maternity_leave_weeks": 26, # 26 weeks
}

EMPLOYEES = {
    "EMP101": {
        "name": "Piyush",
        "role": "Software Engineer",
        "department": "Engineering",
        "annual_leave_total": 18,
        "annual_leave_used": 7,
        "sick_leave_total": 10,
        "sick_leave_used": 2,
        "device": "HP Pavilion Plus 14 (RTX 3050)",
        "asset_tag": "ASSET-IND-8821"
    }
}

def get_leave_balance(emp_id="EMP101"):
    emp = EMPLOYEES.get(emp_id)
    if not emp:
        return {"error": "Employee not found"}
    return {
        "employee_id": emp_id,
        "employee_name": emp["name"],
        "annual_leave_total": emp["annual_leave_total"],
        "annual_leave_used": emp["annual_leave_used"],
        "annual_leave_remaining": emp["annual_leave_total"] - emp["annual_leave_used"],
        "sick_leave_total": emp["sick_leave_total"],
        "sick_leave_used": emp["sick_leave_used"],
        "sick_leave_remaining": emp["sick_leave_total"] - emp["sick_leave_used"],
        "paternity_leave_entitlement_days": POLICY_ENTITLEMENTS["paternity_leave_days"]
    }

def get_device_info(emp_id="EMP101"):
    emp = EMPLOYEES.get(emp_id)
    if not emp:
        return {"error": "Employee not found"}
    return {
        "employee_name": emp["name"],
        "assigned_device": emp["device"],
        "asset_tag": emp["asset_tag"]
    }

def create_it_ticket(issue_summary, category="Hardware", priority="P2"):
    ticket_id = f"INC-2026-{random.randint(1000, 9999)}"
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "status": "Ticket Created Successfully",
        "ticket_id": ticket_id,
        "timestamp": created_at,
        "category": category,
        "priority": priority,
        "summary": issue_summary,
        "sla_resolution_window": "12 hours (per IT SOP P2 standard)"
    }

def submit_expense_claim(amount_inr, category, description, emp_id="EMP101"):
    claim_id = f"EXP-2026-{random.randint(100, 999)}"
    return {
        "claim_status": "Submitted for Approval",
        "claim_id": claim_id,
        "employee_id": emp_id,
        "amount_inr": amount_inr,
        "category": category,
        "description": description,
        "policy_check": "Pending Finance Audit"
    }