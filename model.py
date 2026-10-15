# ==========================================
# WOMEN SAFETY PREDICTION - FULL PIPELINE
# ==========================================

# Install (Colab me mostly already hota hai)
# !pip install pandas scikit-learn

# ------------------------------------------
# 1. Import Libraries
# ------------------------------------------
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ------------------------------------------
# 2. Generate 250 Rows Dataset
# ------------------------------------------
data = []

for _ in range(250):
    crime_count = random.randint(1, 10)
    population_density = random.randint(3000, 10000)
    police_presence = random.randint(0, 1)
    latitude = round(random.uniform(18.90, 19.15), 2)
    longitude = round(random.uniform(72.80, 72.90), 2)

    data.append([
        crime_count,
        population_density,
        police_presence,
        latitude,
        longitude
    ])

df = pd.DataFrame(data, columns=[
    "crime_count",
    "population_density",
    "police_presence",
    "latitude",
    "longitude"
])

# ------------------------------------------
# 3. Create Target Column (Safe/Unsafe)
# ------------------------------------------
df["safe"] = df["crime_count"].apply(lambda x: 0 if x > 5 else 1)

print("Dataset Ready ✅")
print(df.head())

# ------------------------------------------
# 4. Split Data
# ------------------------------------------
X = df.drop("safe", axis=1)
y = df["safe"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------------------------------
# 5. Train Model
# ------------------------------------------
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

print("\nModel Trained ✅")

# ------------------------------------------
# 6. Accuracy Check
# ------------------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy*100:.2f}%")

# ------------------------------------------
# 7. Test Prediction (Custom Input)
# ------------------------------------------
# Example: (tum change kar sakti ho)
test_data = [[4, 6000, 1, 19.07, 72.87]]

prediction = model.predict(test_data)[0]
probability = model.predict_proba(test_data)[0][1]

print("\n--- Prediction Result ---")

if prediction == 1:
    print("Area is SAFE ✅")
else:
    print("Area is UNSAFE ⚠️")

print(f"Safety Score: {probability*100:.2f}%")

# ------------------------------------------
# 8. Save Model (optional)
# ------------------------------------------
import pickle

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nModel saved as model.pkl 💾")