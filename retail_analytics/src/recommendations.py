import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from surprise import accuracy
from surprise.model_selection import train_test_split
from logging_utils import get_logger, log_structured

logger = get_logger(__name__)

def build_collaborative_filtering_model(df: pd.DataFrame):
    # Surprise expects 'user', 'item', 'rating' columns
    # We'll treat 'PurchaseAmount' as the rating
    reader = Reader(rating_scale=(0, 5000))  # or min/max range of your amounts
    data = Dataset.load_from_df(df[["CustomerID", "ProductID", "PurchaseAmount"]], reader)
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
    
    algo = KNNBasic()
    algo.fit(trainset)
    
    predictions = algo.test(testset)
    rmse = accuracy.rmse(predictions, verbose=False)
    log_structured(logger, "info", f"Collaborative Filtering Model trained, RMSE={rmse:.4f}")
    
    return algo

def recommend_for_customer(algo, customer_id, df: pd.DataFrame, top_n=5):
    # Potential items to recommend: items the user hasn't purchased
    user_purchases = df[df["CustomerID"] == customer_id]["ProductID"].unique()
    unique_items = df["ProductID"].unique()

    predictions = []
    for item_id in unique_items:
        if item_id not in user_purchases:
            pred = algo.predict(uid=customer_id, iid=item_id)
            predictions.append((item_id, pred.est))

    # Sort by estimated rating (purchase amount)
    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:top_n]

def explain_recommendation(customer_id, recommendations):
    explanation = (
        f"Recommendations for Customer {customer_id} based on similar users' purchasing amounts. "
        f"These items are predicted to have high purchase ratings for this customer."
    )
    return explanation
