# 🛒 AI E-commerce Assistant
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)  
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-teal.svg)  
![SQLite](https://img.shields.io/badge/SQLite-DB-lightgrey.svg)  
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)  
![License](https://img.shields.io/badge/license-MIT-green.svg)  

An AI-powered recommendation system for e-commerce platforms.
Built with FastAPI + Python + ML, it provides:

* Collaborative filtering (co-purchase recommendations)
* Content-based filtering (TF-IDF on product tags & descriptions)
* Upcoming: Hybrid recommender (combines co-purchase + content)
* API-ready for Shopify, WooCommerce, or custom integration

Features

* `/products` → List all products
* `/customers` → List all customers
* `/recommend` → Get co-purchase recommendations
* `/recommend/content` → Get content-based recommendations
* Future: `/recommend/hybrid`

Project Structure
AI-E-commerce-Assistant/
│── data/
│   ├── products.csv
│   ├── transactions.csv
│── main.py                # FastAPI app
│── recommender.py          # Co-purchase logic
│── content_recommender.py  # TF-IDF recommender
│── requirements.txt
│── README.md

Installation

Clone the repo:

git clone https://github.com/Peterson-Muriuki/AI-E-commerce-Assistant.git
cd AI-Ecommerce-Assistant

Create & activate virtual environment:

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

Install dependencies:

pip install -r requirements.txt

Run API:

uvicorn main:app --reload


API Usage

1. List Products

GET /products

2. List Customers

GET /customers

Co-purchase Recommendations

GET /recommend?product_id=p1&top_k=5

4. Content-Based Recommendations

GET /recommend/content?product_id=p1&top_k=5

Example Response

{
  "recommendations": [
    {"product_id": "p3", "name": "Running Shoes", "similarity": 0.72},
    {"product_id": "p7", "name": "Sneakers", "similarity": 0.66}
  ]
}

---

Roadmap

* [x] Co-purchase recommender
* [x] Content-based recommender (TF-IDF + cosine similarity)
* [ ] Hybrid recommender (merge both methods)
* [ ] Dockerize app
* [ ] Shopify/WooCommerce webhook integration

Author

Peterson Muriuki
📧 [pitmuriuki@gmail.com](mailto:pitmuriuki@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/peterson-muriuki/)
🐙 [GitHub](https://github.com/Peterson-Muriuki)

⚡ Ready to deploy AI-powered recommendations into your e-commerce app!


