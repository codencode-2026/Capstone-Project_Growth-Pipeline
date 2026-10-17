import os
import json
import matplotlib.pyplot as plt

def generate_visualizations():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    findings_path = os.path.join(project_root, "narrator", "findings.json")
    visualizations_dir = os.path.join(project_root, "visualizations")
    os.makedirs(visualizations_dir, exist_ok=True)

    with open(findings_path, "r") as f:
        findings = json.load(f)

    return_rates = findings["return_rate_by_payment"]
    sorted_rates = dict(sorted(return_rates.items(), key=lambda item: item[1], reverse=True))

    methods = list(sorted_rates.keys())
    rates = list(sorted_rates.values())

    plt.figure(figsize=(8, 5))
    bars = plt.bar(methods, rates, color=['#d9534f', '#5bc0de', '#5cb85c'])
    
    plt.title("COD Returns at 44.4% — 3x Card & UPI Rate", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Payment Method", fontsize=12)
    plt.ylabel("Return Rate (%)", fontsize=12)
    plt.ylim(0, 60)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0, 
            height + 1.5, 
            f"{height:.1f}%", 
            ha='center', 
            va='bottom', 
            fontsize=11, 
            fontweight='bold'
        )

    plt.tight_layout()
    chart1_path = os.path.join(visualizations_dir, "return_rate_by_payment.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"[Chart 1] Saved: {chart1_path}")

    months = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]
    revenue = [11637.10, 13195.50, 20318.90, 9495.30, 13151.10, 11615.40]

    plt.figure(figsize=(9, 5))
    plt.plot(months, revenue, marker='o', color='#0275d8', linewidth=2.5, markersize=8)

    plt.title("Outlier-Corrected Monthly Revenue — March 2026 Peak (₹20,318.90)", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Revenue (INR ₹)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)

    march_idx = months.index("2026-03")
    march_val = revenue[march_idx]
    plt.annotate(
        f"Peak: ₹{march_val:,.2f}", 
        xy=(march_idx, march_val), 
        xytext=(march_idx - 0.5, march_val + 1500),
        arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
        fontsize=10, 
        fontweight='bold'
    )

    plt.tight_layout()
    chart2_path = os.path.join(visualizations_dir, "monthly_revenue_trend.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"[Chart 2] Saved: {chart2_path}")

if __name__ == "__main__":
    generate_visualizations()