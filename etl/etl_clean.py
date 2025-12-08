import os
import pandas as pd
from datetime import datetime

# Resolve project root and data paths automatically
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data_raw")
CLEAN = os.path.join(RAW, "cleaned")

os.makedirs(CLEAN, exist_ok=True)

# Load raw CSVs
presc = pd.read_csv(
    os.path.join(RAW, "prescriptions.csv"),
    parse_dates=["date_received", "date_filled"]
)

inv = pd.read_csv(os.path.join(RAW, "inventory.csv"))

wf = pd.read_csv(
    os.path.join(RAW, "workflow.csv"),
    parse_dates=["entered_time", "label_start", "filled_time",
                 "checked_time", "pickup_time"]
)

staff = pd.read_csv(
    os.path.join(RAW, "staffing.csv"),
    parse_dates=["date"]
)

# Normalize drug names + join inventory information
presc = presc.merge(
    inv[["drug_name", "SKU", "cost_per_unit"]],
    on="drug_name",
    how="left"
)

# Compute derived metrics
presc["fill_hours"] = (
    (presc["date_filled"] - presc["date_received"])
    .dt.total_seconds() / 3600
)

# Workflow stage durations
wf["label_hours"] = (
    (wf["label_start"] - wf["entered_time"])
    .dt.total_seconds() / 3600
)
wf["check_hours"] = (
    (wf["checked_time"] - wf["filled_time"])
    .dt.total_seconds() / 3600
)
wf["pickup_hours"] = (
    (wf["pickup_time"] - wf["filled_time"])
    .dt.total_seconds() / 3600
)

# Save cleaned files
presc.to_csv(os.path.join(CLEAN, "prescriptions_cleaned.csv"), index=False)
inv.to_csv(os.path.join(CLEAN, "inventory_cleaned.csv"), index=False)
wf.to_csv(os.path.join(CLEAN, "workflow_cleaned.csv"), index=False)
staff.to_csv(os.path.join(CLEAN, "staffing_cleaned.csv"), index=False)

print(f"✔ Cleaned data written to: {CLEAN}")