# data/members.py

MEMBER_DB = {
    "SUP-987654": {
        "memberId": "SUP-987654",
        "name": "John Smith",
        "age": 42,
        "balance": 85000,
        "hardshipEligible": True,
        "retirementEligible": False
    },
    "SUP-111111": {
        "memberId": "SUP-111111",
        "name": "Alice Brown",
        "age": 60,
        "balance": 150000,
        "hardshipEligible": False,
        "retirementEligible": True
    }
}


def get_member(member_id: str):
    return MEMBER_DB.get(member_id)
