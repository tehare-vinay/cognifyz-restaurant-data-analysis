"""
Cognifyz Data Analysis Internship - Level 1 & Level 2 Tasks
Author: Vinay Tehare
Dataset: Zomato-style restaurant dataset (Dataset.csv)
"""

import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
df = pd.read_csv("Dataset.csv")
results = []  # collect text output for results.md

def log(title, text):
    print(f"\n=== {title} ===\n{text}")
    results.append(f"## {title}\n\n{text}\n")


# ===========================================================
# LEVEL 1
# ===========================================================

# --- Task 1: Top Cuisines ---
cuisine_series = df["Cuisines"].dropna().str.split(", ")
all_cuisines = cuisine_series.explode()
top_cuisines = all_cuisines.value_counts().head(3)
pct_top = (top_cuisines / len(df) * 100).round(2)
text = ""
for c, cnt in top_cuisines.items():
    text += f"- {c}: {cnt} restaurants ({pct_top[c]}% of all restaurants)\n"
log("Level 1 - Task 1: Top 3 Cuisines", text)

# --- Task 2: City Analysis ---
city_counts = df["City"].value_counts()
top_city = city_counts.idxmax()
avg_rating_by_city = df.groupby("City")["Aggregate rating"].mean().sort_values(ascending=False)
best_rated_city = avg_rating_by_city.idxmax()
text = (
    f"- City with most restaurants: **{top_city}** ({city_counts.max()} restaurants)\n"
    f"- City with highest average rating: **{best_rated_city}** "
    f"(avg rating {avg_rating_by_city.max():.2f})\n"
)
log("Level 1 - Task 2: City Analysis", text)

# --- Task 3: Price Range Distribution ---
price_counts = df["Price range"].value_counts().sort_index()
price_pct = (price_counts / len(df) * 100).round(2)
plt.figure(figsize=(6, 4))
price_counts.plot(kind="bar", color="#4C72B0")
plt.title("Distribution of Price Ranges")
plt.xlabel("Price Range (1=Low, 4=High)")
plt.ylabel("Number of Restaurants")
plt.tight_layout()
plt.savefig("outputs/price_range_distribution.png")
plt.close()
text = "".join(f"- Price range {p}: {price_counts[p]} restaurants ({price_pct[p]}%)\n" for p in price_counts.index)
text += "\nChart saved: outputs/price_range_distribution.png\n"
log("Level 1 - Task 3: Price Range Distribution", text)

# --- Task 4: Online Delivery ---
delivery_pct = (df["Has Online delivery"].value_counts(normalize=True) * 100).round(2)
avg_rating_delivery = df.groupby("Has Online delivery")["Aggregate rating"].mean().round(2)
text = (
    f"- Restaurants offering online delivery: {delivery_pct.get('Yes', 0)}%\n"
    f"- Avg rating WITH online delivery: {avg_rating_delivery.get('Yes', 'N/A')}\n"
    f"- Avg rating WITHOUT online delivery: {avg_rating_delivery.get('No', 'N/A')}\n"
)
log("Level 1 - Task 4: Online Delivery", text)


# ===========================================================
# LEVEL 2
# ===========================================================

# --- Task 1: Restaurant Ratings distribution ---
rating_bins = pd.cut(df["Aggregate rating"], bins=[-0.1, 1, 2, 3, 4, 5],
                      labels=["0-1", "1-2", "2-3", "3-4", "4-5"])
rating_dist = rating_bins.value_counts().sort_index()
avg_votes = df["Votes"].mean()
plt.figure(figsize=(6, 4))
rating_dist.plot(kind="bar", color="#55A868")
plt.title("Aggregate Rating Distribution")
plt.xlabel("Rating Range")
plt.ylabel("Number of Restaurants")
plt.tight_layout()
plt.savefig("outputs/rating_distribution.png")
plt.close()
text = (
    f"- Most common rating range: **{rating_dist.idxmax()}** ({rating_dist.max()} restaurants)\n"
    f"- Average number of votes per restaurant: {avg_votes:.2f}\n"
    "\nChart saved: outputs/rating_distribution.png\n"
)
log("Level 2 - Task 1: Restaurant Ratings", text)

# --- Task 2: Cuisine Combinations ---
combo_counts = df["Cuisines"].value_counts().head(5)
combo_avg_rating = df.groupby("Cuisines")["Aggregate rating"].mean()
text = "Top 5 most common cuisine combinations:\n"
for combo, cnt in combo_counts.items():
    text += f"- {combo}: {cnt} restaurants, avg rating {combo_avg_rating[combo]:.2f}\n"
log("Level 2 - Task 2: Cuisine Combinations", text)

# --- Task 3: Geographic Analysis ---
plt.figure(figsize=(6, 5))
plt.scatter(df["Longitude"], df["Latitude"], s=3, alpha=0.4, color="#C44E52")
plt.title("Restaurant Locations (Longitude vs Latitude)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.savefig("outputs/geographic_distribution.png")
plt.close()
cluster_city = df["City"].value_counts().head(5)
text = "Restaurant location scatter plot saved: outputs/geographic_distribution.png\n\n"
text += "Top 5 cities by restaurant count (visible clusters):\n"
for c, cnt in cluster_city.items():
    text += f"- {c}: {cnt} restaurants\n"
log("Level 2 - Task 3: Geographic Analysis", text)

# --- Task 4: Restaurant Chains ---
chain_counts = df["Restaurant Name"].value_counts()
chains = chain_counts[chain_counts > 1].head(10)
chain_ratings = df[df["Restaurant Name"].isin(chains.index)].groupby("Restaurant Name")["Aggregate rating"].mean().round(2)
text = "Top restaurant chains (name appears in multiple locations):\n"
for name, cnt in chains.items():
    text += f"- {name}: {cnt} outlets, avg rating {chain_ratings[name]}\n"
log("Level 2 - Task 4: Restaurant Chains", text)


# ---------------------------------------------------------
# Save consolidated results
# ---------------------------------------------------------
with open("results.md", "w", encoding="utf-8") as f:
    f.write("# Cognifyz Data Analysis Internship - Results\n\n")
    f.write("\n".join(results))

print("\n\nAll tasks completed. See results.md and outputs/ folder for charts.")
