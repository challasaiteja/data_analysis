import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')))
import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from surprise import accuracy
from surprise.model_selection import train_test_split
from src.logging_utils import get_logger, log_structured

logger = get_logger(__name__)

def build_collaborative_filtering_model(df: pd.DataFrame):
    """
    Builds a collaborative filtering model using the Surprise library.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with at least 'CustomerID', 'ProductID', 'PurchaseAmount' columns.

    Returns
    -------
    algo : Surprise Algorithm
        Trained algorithm instance.
    """
    # Surprise expects 'user', 'item', 'rating' columns
    # We'll treat 'PurchaseAmount' as the rating
    reader = Reader(rating_scale=(0, 5000))  # or min/max range of your amounts
    data = Dataset.load_from_df(df[["CustomerID", "ProductID", "PurchaseAmount"]], reader)
    
    # Split data into training and test sets
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
    
    # Build a K-NN Baseline algorithm
    algo = KNNBasic()
    algo.fit(trainset)
    
    # Evaluate the model
    predictions = algo.test(testset)
    rmse = accuracy.rmse(predictions, verbose=False)
    log_structured(logger, "info", f"Collaborative Filtering Model trained, RMSE={rmse:.4f}")
    
    return algo

def recommend_for_customer(algo, customer_id, df: pd.DataFrame, top_n=5):
    """
    Recommend items for a given customer by predicting their purchase amounts.

    Parameters
    ----------
    algo : Surprise Algorithm
        Trained algorithm instance.
    customer_id : str
        Customer ID to generate recommendations for.
    df : pd.DataFrame
        DataFrame with 'CustomerID', 'ProductID', 'PurchaseAmount' columns.
    top_n : int
        Number of recommendations to return.

    Returns
    -------
    recommendations : list of tuples
        List of tuples containing the item ID and the estimated purchase amount.
    """
    # Potential items to recommend: items the user hasn't purchased
    user_purchases = df[df["CustomerID"] == customer_id]["ProductID"].unique()
    unique_items = df["ProductID"].unique()

    predictions = []
    for item_id in unique_items:
        if item_id not in user_purchases:
            # Predict the purchase amount for the item
            pred = algo.predict(uid=customer_id, iid=item_id)
            predictions.append((item_id, pred.est))

    # Sort by estimated rating (purchase amount)
    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:top_n]

def explain_recommendation(customer_id, recommendations):
    """
    Generate a string explaining the recommendations for a given customer.

    The explanation is a simple sentence stating that the recommendations are based on similar users'
    purchasing amounts, and that the items are predicted to have high purchase ratings for this customer.

    Parameters
    ----------
    customer_id : str
        Customer ID to generate the explanation for.
    recommendations : list of tuples
        List of tuples containing the item ID and the estimated purchase amount.

    Returns
    -------
    explanation : str
        String explaining the recommendations for the customer.
    """
    explanation = (
        f"Recommendations for Customer {customer_id} based on similar users' purchasing amounts. "
        f"These items are predicted to have high purchase ratings for this customer."
    )
    return explanation
