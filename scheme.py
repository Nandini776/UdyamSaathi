def get_eligible_schemes(net_profit_monthly, business_type="Kirana"):
    schemes = []

    # 1. PM MUDRA Loan (Shishu / Kishor)
    if net_profit_monthly > 2000:
        schemes.append({
            "name": "PM-MUDRA Scheme (Shishu / Kishor)",
            "ministry": "Ministry of Finance / MSME",
            "max_loan": "₹50,000 - ₹5,00,000",
            "interest": "8.5% - 10%",
            "purpose": "Working capital & stock procurement",
            "eligibility_match": "High"
        })

    # 2. NSFDC Micro-Credit Scheme (MoSJE Specific)
    if net_profit_monthly >= 1500:
        schemes.append({
            "name": "NSFDC Micro-Credit Scheme (MCC)",
            "ministry": "MoSJE (Ministry of Social Justice)",
            "max_loan": "Up to ₹1,40,000",
            "interest": "5% per annum (Concessional)",
            "purpose": "Small trade & rural retail expansion",
            "eligibility_match": "Very High"
        })

    # 3. NBCCFDC General Loan Scheme
    if net_profit_monthly >= 3000:
        schemes.append({
            "name": "NBCCFDC Term Loan",
            "ministry": "MoSJE",
            "max_loan": "Up to ₹5,00,000",
            "interest": "6% - 8%",
            "purpose": "Asset purchase & equipment setup",
            "eligibility_match": "Medium"
        })

    return schemes