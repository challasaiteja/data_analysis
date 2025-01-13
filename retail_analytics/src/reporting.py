import pdfkit
import os
from logging_utils import get_logger, log_structured

logger = get_logger(__name__)

REPORT_TEMPLATE = """
<html>
<head><title>Retail Analytics Report</title></head>
<body>
    <h1>Retail Analytics Summary</h1>
    <h2>Data Analysis Insights</h2>
    <p>Top Products: {top_products}</p>
    <p>Category Sales: {category_sales}</p>
    <p>Average Spending per Customer: {avg_spend_per_customer:.2f}</p>
    
    <h2>Customer Segments</h2>
    <ul>
    {customer_segments}
    </ul>

    <h2>Example Recommendations</h2>
    <p>{recommendations}</p>

    <img src="../data/top_products.png" alt="Top Products Chart" width="500"/>
</body>
</html>
"""

def generate_pdf_report(analysis_results, cluster_df, recommendations):
    top_products = analysis_results["top_products"].to_dict()
    category_sales = analysis_results["category_sales"].to_dict()
    avg_spend_per_customer = analysis_results["avg_spend_per_customer"]

    # Summarize clusters
    segment_info = []
    for cluster_label, group in cluster_df.groupby("ClusterLabel"):
        segment_info.append(f"<li><strong>{cluster_label}</strong>: {len(group)} customers</li>")
    segment_html = "\n".join(segment_info)

    rendered_html = REPORT_TEMPLATE.format(
        top_products=top_products,
        category_sales=category_sales,
        avg_spend_per_customer=avg_spend_per_customer,
        customer_segments=segment_html,
        recommendations=recommendations
    )
    
    # Convert HTML to PDF
    pdfkit.from_string(rendered_html, "RetailAnalyticsReport.pdf")
    log_structured(logger, "info", "PDF report generated", report_file="RetailAnalyticsReport.pdf")
