import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')))
from html import escape
from data_generation import main as generate_data
from data_loading import load_and_validate_purchases, filter_data
from data_analysis import analyze_data
from clustering import create_customer_clusters
from recommendations import build_collaborative_filtering_model, recommend_for_customer, explain_recommendation
from src.logging_utils import get_logger, log_structured
from src.reporting import generate_pdf_report
logger = get_logger(__name__)

def run_pipeline():
    
    # 1. Generate or Load Data
    if not os.path.exists("data/purchases.csv"):
        generate_data()  # only if needed

    # 2. Load & Validate
    df = load_and_validate_purchases("data/purchases.csv")

    # Example filter: last 6 months
    df = filter_data(df, start_date="2024-07-01", end_date="2025-01-01")

    # 3. Analyze Data
    analysis_results = analyze_data(df)
    print(analysis_results)

    # 4. Clustering
    cluster_df = create_customer_clusters(df)

    # 5. Recommendation
    algo = build_collaborative_filtering_model(df)
    sample_customer_id = df["CustomerID"].iloc[0]
    recs = recommend_for_customer(algo, sample_customer_id, df)
    explanation = explain_recommendation(sample_customer_id, recs)

    # 6. Report
    def format_recommendations(sample_customer_id, recs, explanation):
    # Convert the recommendations to an HTML table
        recommendations_html = f"<h3>Recommendations for Customer {escape(sample_customer_id)}</h3>"
        recommendations_html += "<table border='1' cellpadding='10'><thead><tr><th>Product ID</th><th>Predicted Purchase Amount</th></tr></thead><tbody>"
        
        for product_id, predicted_amount in recs:
            recommendations_html += f"<tr><td>{escape(product_id)}</td><td>${predicted_amount:,.2f}</td></tr>"
        
        recommendations_html += "</tbody></table>"
        recommendations_html += f"<p><strong>Explanation:</strong> {escape(explanation)}</p>"
        
        return recommendations_html


    recommendations_text = format_recommendations(sample_customer_id, recs, explanation)

    #recommendations_text = f"Customer {sample_customer_id} => Recommendations: {recs}\n, Explanation: {explanation}"
    generate_pdf_report(analysis_results, cluster_df, recommendations_text)

if __name__ == "__main__":
    run_pipeline()
