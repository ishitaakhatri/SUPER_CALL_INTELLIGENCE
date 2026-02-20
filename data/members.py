# data/members.py

MEMBER_DB = {

    "SUP-987654": {
        "memberId": "SUP-987654",
        "personalInfo": {
            "firstName": "John",
            "lastName": "Smith",
            "dateOfBirth": "1983-05-14",
            "age": 42,
            "contactNumber": "+61-400-123-456",
            "email": "john.smith@email.com"
        },
        "accountInfo": {
            "accountStatus": "Active",
            "memberSince": "2015-03-12",
            "balance": 85000,
            "currency": "AUD",
            "contributionType": "Employer + Voluntary"
        },
        "eligibilityFlags": {
            "hardshipEligible": True,
            "retirementEligible": False,
            "earlyReleaseEligible": True
        },
        "withdrawalHistory": [
            {
                "date": "2023-02-11",
                "amount": 5000,
                "reason": "Financial Hardship"
            }
        ],
        "riskProfile": {
            "vulnerableCustomer": False,
            "fraudFlag": False
        }
    },

    "SUP-111111": {
        "memberId": "SUP-111111",
        "personalInfo": {
            "firstName": "Alice",
            "lastName": "Brown",
            "dateOfBirth": "1965-08-22",
            "age": 60,
            "contactNumber": "+61-401-222-333",
            "email": "alice.brown@email.com"
        },
        "accountInfo": {
            "accountStatus": "Active",
            "memberSince": "2001-06-18",
            "balance": 150000,
            "currency": "AUD",
            "contributionType": "Employer"
        },
        "eligibilityFlags": {
            "hardshipEligible": False,
            "retirementEligible": True,
            "earlyReleaseEligible": False
        },
        "withdrawalHistory": [],
        "riskProfile": {
            "vulnerableCustomer": False,
            "fraudFlag": False
        }
    },

    "SUP-222222": {
        "memberId": "SUP-222222",
        "personalInfo": {
            "firstName": "Michael",
            "lastName": "Lee",
            "dateOfBirth": "1990-11-03",
            "age": 35,
            "contactNumber": "+61-402-444-555",
            "email": "michael.lee@email.com"
        },
        "accountInfo": {
            "accountStatus": "Active",
            "memberSince": "2017-01-10",
            "balance": 42000,
            "currency": "AUD",
            "contributionType": "Employer + Voluntary"
        },
        "eligibilityFlags": {
            "hardshipEligible": False,
            "retirementEligible": False,
            "earlyReleaseEligible": False
        },
        "withdrawalHistory": [],
        "riskProfile": {
            "vulnerableCustomer": True,
            "fraudFlag": False
        }
    },

    "SUP-333333": {
        "memberId": "SUP-333333",
        "personalInfo": {
            "firstName": "Emma",
            "lastName": "Davis",
            "dateOfBirth": "1978-02-19",
            "age": 47,
            "contactNumber": "+61-403-666-777",
            "email": "emma.davis@email.com"
        },
        "accountInfo": {
            "accountStatus": "Suspended",
            "memberSince": "2010-09-25",
            "balance": 98000,
            "currency": "AUD",
            "contributionType": "Employer"
        },
        "eligibilityFlags": {
            "hardshipEligible": True,
            "retirementEligible": False,
            "earlyReleaseEligible": True
        },
        "withdrawalHistory": [
            {
                "date": "2024-05-01",
                "amount": 10000,
                "reason": "Medical Hardship"
            }
        ],
        "riskProfile": {
            "vulnerableCustomer": False,
            "fraudFlag": True
        }
    },

    "SUP-444444": {
        "memberId": "SUP-444444",
        "personalInfo": {
            "firstName": "Daniel",
            "lastName": "Wilson",
            "dateOfBirth": "1988-07-09",
            "age": 37,
            "contactNumber": "+61-404-888-999",
            "email": "daniel.wilson@email.com"
        },
        "accountInfo": {
            "accountStatus": "Active",
            "memberSince": "2018-04-14",
            "balance": 67000,
            "currency": "AUD",
            "contributionType": "Employer + Voluntary"
        },
        "eligibilityFlags": {
            "hardshipEligible": False,
            "retirementEligible": False,
            "earlyReleaseEligible": True
        },
        "withdrawalHistory": [],
        "riskProfile": {
            "vulnerableCustomer": False,
            "fraudFlag": False
        }
    }
}


def get_member(member_id: str):
    return MEMBER_DB.get(member_id)
