from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pandas as pd
import os
from collections import defaultdict
from itertools import combinations

app = FastAPI(title="AI E-commerce Assistant - API")

class RecommendRequest(BaseModel):
    customer_id: Optional[str] = None
    product_id: Optional[str] = None
    top_k: int = 5

# --- Load data at startup ---
ROOT = os.getcwd()
PRODUCTS_CSV = os.path.join(ROOT, "data", "products.csv")
ORDERS_CSV = os.path.join(ROOT, "data", "orders.csv")

if not os.path.exists(PRODUCTS_CSV) or not os.path.exists(ORDERS_CSV):
    raise RuntimeError(f"Missing data files. Expected at: {PRODUCTS_CSV} and {ORDERS_CSV}")

products_df = pd.read_csv(PRODUCTS_CSV, dtype=str)
# Ensure numeric price
if "price" in products_df.columns:
    try:
        products_df["price"] = products_df["price"].astype(float)
    except Exception:
        products_df["price"] = products_df["price"].replace(',', '', regex=True).astype(float)

orders_df = pd.read_csv(ORDERS_CSV, dtype=str)

# --- Build co-purchase counts: co_counts[a][b] = count of orders containing both a and b ---
co_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
for order_id, group in orders_df.groupby("order_id"):
    prods = list(group["product_id"])
    # only count pairs if >=2 products in order
    for a, b in combinations(prods, 2):
        co_counts[a][b] += 1
        co_counts[b][a] += 1

# global popularity
global_popularity = orders_df["product_id"].value_counts().to_dict()

def product_info(pid: str) -> Dict[str, Any]:
    row = products_df.loc[products_df["product_id"] == pid]
    if row.empty:
        return {"product_id": pid, "name": None, "price": None}
    row = row.iloc[0]
    return {"product_id": pid, "name": row.get("name"), "price": float(row.get("price")) if row.get("price") is not None else None}

def recommend_for_product(product_id: str, top_k: int):
    if product_id not in products_df["product_id"].values:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    scores = co_counts.get(product_id, {})
    if not scores:
        # fallback: return top global items except the product itself
        items = [(pid, cnt) for pid, cnt in global_popularity.items() if pid != product_id]
        items = sorted(items, key=lambda x: x[1], reverse=True)[:top_k]
    else:
        items = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [dict(**product_info(pid), score=int(cnt)) for pid, cnt in items]

def recommend_for_customer(customer_id: str, top_k: int):
    cust_products = orders_df.loc[orders_df["customer_id"] == customer_id, "product_id"].unique().tolist()
    if not cust_products:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found or has no purchases")
    agg_scores = defaultdict(int)
    for pid in cust_products:
        for other_pid, cnt in co_counts.get(pid, {}).items():
            agg_scores[other_pid] += cnt
    # remove items customer already has
    for pid in cust_products:
        if pid in agg_scores:
            del agg_scores[pid]
    if not agg_scores:
        # fallback to global popular items the customer hasn't purchased
        candidates = [(pid, cnt) for pid, cnt in global_popularity.items() if pid not in cust_products]
        candidates = sorted(candidates, key=lambda x: x[1], reverse=True)[:top_k]
        return [dict(**product_info(pid), score=int(cnt)) for pid, cnt in candidates]
    items = sorted(agg_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [dict(**product_info(pid), score=int(cnt)) for pid, cnt in items]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(req: RecommendRequest):
    # Priority: if product_id provided -> product-based recommendations
    if req.product_id:
        recs = recommend_for_product(req.product_id, req.top_k)
        return {"source": "product_co_purchase", "product_id": req.product_id, "recommendations": recs}
    if req.customer_id:
        recs = recommend_for_customer(req.customer_id, req.top_k)
        return {"source": "customer_history", "customer_id": req.customer_id, "recommendations": recs}
    # fallback: top trending
    top = sorted(global_popularity.items(), key=lambda x: x[1], reverse=True)[:req.top_k]
    return {"source": "trending", "recommendations": [dict(**product_info(pid), score=int(cnt)) for pid, cnt in top]}
