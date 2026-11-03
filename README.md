# Real Estate Investment Advisor

A complete local project for the provided `india_housing_prices.csv`. Deployment is intentionally a later manual step. Run the app locally with `streamlit run app.py` after training.

## Quick start

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python scripts/run_all.py
.venv/bin/python scripts/eda.py
.venv/bin/streamlit run app.py
```

Outputs: cleaned data in `data/processed/`, EDA charts and findings in `reports/`, fitted models in `models/` (trained on a deterministic 50,000-row sample for laptop runtime), and MLflow runs/model registrations in local `mlflow.db` (launch UI with `.venv/bin/mlflow ui --backend-store-uri sqlite:///mlflow.db`).

## Target definitions and limits

The source has no observed five-year sale prices or investment outcome labels. `Good_Investment` is defined as price per sq ft at or below the city median. `Future_Price_5Y_Lakhs` is current price compounded at a deterministic city-specific annual rate spanning 5%–9%. These are assignment proxies; performance metrics evaluate agreement with the constructed labels, not real investment return or future market accuracy. See `reports/target_assumptions.json`.

The source contains 250,000 rows, no missing cells, and no exact duplicate rows. Price per sq ft is recomputed from price and area because the supplied column is inconsistent. Crime rate, infrastructure score, and RERA status are not present and are excluded.

## Structure

- `scripts/pipeline.py`: preprocessing, targets, model pipelines, evaluation, MLflow.
- `scripts/eda.py`: summary and assignment charts.
- `app.py`: local Streamlit prediction and insights UI.
- `data/processed/india_housing_processed.csv`: processed dataset with explicit proxy targets.
