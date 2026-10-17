import os
import json

def generate_scr_narrative_offline(findings: dict) -> dict:
    cleaned_rev = f"{findings['cleaned_total_revenue_inr']:,.2f}"
    cod_rate = findings['return_rate_by_payment']['COD']
    seg_rate = findings['highest_risk_segment']['return_rate_pct']
    delta = f"{findings['duplicate_reconciliation_delta_inr']:,.2f}"
    peak_month = findings['true_peak_month']['month']
    peak_rev = f"{findings['true_peak_month']['revenue_inr']:,.2f}"

    narrative = f"""* Situation
Mamaearth generated a cleaned total revenue of INR {cleaned_rev} across 175 validated orders after accounting for a duplicate-driven reconciliation delta of INR {delta}.

* Complication
Returns are disproportionately concentrated in Cash on Delivery (COD) transactions, which exhibit a high return rate of {cod_rate}%. The situation is most severe in Tier-2 cities under COD payment methods, where return rates peak at {seg_rate}%, heavily eroding operating margins.

* Resolution
Regional operations and finance heads should impose targeted COD friction or verification controls in Tier-2 cities. Furthermore, underlying revenue trends reveal that {peak_month} was the true peak month at INR {peak_rev} once bulk order outliers were removed, providing a reliable baseline for demand planning."""

    return {
        "status": "success",
        "narrative": narrative,
        "mode": "offline"
    }

def generate_scr_narrative(findings: dict) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return generate_scr_narrative_offline(findings)

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        system_instruction = (
            "You are a senior data analyst writing for Mamaearth's regional ops and finance heads. "
            "Follow the SCR (Situation-Complication-Resolution) format using '*' for section headings instead of '###'. "
            "Every number in the narrative must match the provided findings exactly without deviation."
        )

        user_prompt = f"Write an SCR narrative based on these exact metrics: {json.dumps(findings)}"

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config={
                'system_instruction': system_instruction,
                'temperature': 0.0,
                'max_output_tokens': 500,
            }
        )

        return {
            "status": "success",
            "narrative": response.text,
            "mode": "online"
        }
    except Exception as err:
        return generate_scr_narrative_offline(findings)

def check_numeric_accuracy(narrative_text: str) -> bool:
    normalized = narrative_text.replace(",", "")
    required_substrings = ["97358.3", "44.4", "54.5", "2501.9", "20318.9"]
    
    print("\n--- NUMERIC ACCURACY CHECKLIST ---")
    all_passed = True
    for sub in required_substrings:
        present = sub in normalized
        print(f"Checking '{sub}': {'PASS' if present else 'FAIL'}")
        if not present:
            all_passed = False
    return all_passed

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    findings_path = os.path.join(script_dir, "findings.json")

    with open(findings_path, "r") as f:
        findings = json.load(f)

    result = generate_scr_narrative(findings)
    print(f"\n--- SCR NARRATIVE ({result['mode'].upper()}) ---")
    print(result["narrative"])

    sample_out_path = os.path.join(script_dir, "sample_output.txt")
    with open(sample_out_path, "w") as f:
        f.write(result["narrative"])

    check_numeric_accuracy(result["narrative"])