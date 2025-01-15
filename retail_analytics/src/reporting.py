import os
import pdfkit
from html import escape
from logging_utils import get_logger, log_structured

logger = get_logger(__name__)

def generate_pdf_report(analysis_results, cluster_df, recommendations, output_dir="reports"):
    """
    Generate a PDF report based on the analysis results.

    :param analysis_results: Results of the analysis (top products, category sales, customer segments)
    :type analysis_results: dict
    :param cluster_df: DataFrame with customer segments
    :type cluster_df: pd.DataFrame
    :param recommendations: HTML content of the recommendations
    :type recommendations: str
    :param output_dir: Directory to store the report files (default: "reports")
    :type output_dir: str
    """
    REPORT_TEMPLATE = """
    <html>
    <head>
        <title>Retail Analytics Report</title>
        <link rel = "stylesheet" type = "text/css" href = "RetailAnalyticsReportStyle.css" />
    </head>
    <body>
        <h1>Retail Analytics Summary</h1>
        <div class="dashboardBody">
        <img src="../data/top_products.png" alt="Top Products Chart" width="500"/>
        <div>
        
            <p>Top Products:</p>
            <ul>{top_products}</ul>
        </div>
        </div>

        <h1>Data Analysis Insights</h1>
        
        <p class="number">Average Spending per Customer: ${avg_spend_per_customer:.2f}</p>
        <div class="insightSection">
       
         <div  class="insights">
         <h2>Category Sales: {category_sales}</h2>
        </div>
        <div class="insightsBox">
        <h2>Customer Segments</h2>
        <ul>
        {customer_segments}
        </ul>
        </div>
        </div>
        <div class="recommendations">
        <h2>Example Recommendations</h2>
        <p>{recommendations}</p>
        </div>
        
        
     
    </body>
    </html>
    """

    try:
        # Prepare data for the report
        top_products = "<table border='1' cellpadding='10'><thead><tr><th>Product ID</th><th>Purchase Amount</th></tr></thead><tbody>"
        for product_id, sales in analysis_results["top_products"].items():
            top_products += f"<tr><td>{escape(product_id)}</td><td>${sales:,.2f}</td></tr>"
        top_products += "</tbody></table>"
        #top_products = escape(str(analysis_results["top_products"]))
        #print(top_products)
        
        category_sales = "<table border='1' cellpadding='10'><thead><tr><th>Category</th><th>Purchase Amount</th></tr></thead><tbody>"
        for category, sales in analysis_results["category_sales"].items():
            category_sales += f"<tr><td>{escape(category)}</td><td>${sales:,.2f}</td></tr>"
        category_sales += "</tbody></table>"
        #category_sales = escape(str(analysis_results["category_sales"]))
        avg_spend_per_customer = analysis_results["avg_spend_per_customer"]

        # Summarize clusters
        segment_info = []
        for cluster_label, group in cluster_df.groupby("ClusterLabel"):
            segment_info.append(f"<li><strong>{cluster_label}</strong>: {len(group)} customers</li>")
        segment_html = "\n".join(segment_info)

        # Paths for output files
        os.makedirs(output_dir, exist_ok=True)
        html_file_path = os.path.join(output_dir, "RetailAnalyticsReport.html")
        pdf_file_path = os.path.join(output_dir, "RetailAnalyticsReport.pdf")
        img_path = os.path.abspath("../data/top_products.png")

        # Render the HTML content
        rendered_html = REPORT_TEMPLATE.format(
            top_products=top_products,
            category_sales=category_sales,
            avg_spend_per_customer=avg_spend_per_customer,
            customer_segments=segment_html,
            recommendations=recommendations,
            img_path=img_path
        )

        # Save the HTML content to a file (optional for debugging)
        with open(html_file_path, "w") as html_file:
            html_file.write(rendered_html)

        # PDFKit options
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'enable-local-file-access': None,  # Allow local resources like images
        }

        # Convert HTML to PDF
        #pdfkit.from_file(html_file_path, pdf_file_path, options=options)

        #log_structured(logger, "info", "PDF report generated successfully", report_file=pdf_file_path)

    except KeyError as e:
        log_structured(logger, "error", "Missing key in analysis results", missing_key=str(e))
    except OSError as e:
        log_structured(logger, "error", "wkhtmltopdf binary not found", error=str(e))
    except Exception as e:
        log_structured(logger, "error", "Failed to generate PDF report", error=str(e))
