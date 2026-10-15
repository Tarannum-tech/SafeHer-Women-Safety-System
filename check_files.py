import pandas as pd
import pickle
import os

print("=" * 50)
print("Training Women Safety ML Model")
print("=" * 50)

# Create crime dataset if it doesn't exist
if not os.path.exists("crime_dataset.csv"):
    print("\nCreating crime_dataset.csv...")
    data = {
        'area': ['Andheri', 'Bandra', 'Kurla', 'Powai', 'Dadar', 'Thane'],
        'crime_count': [18, 5, 22, 4, 10, 3],
        'night_risk': [1, 0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)
    df.to_csv("crime_dataset.csv", index=False)
    print("✅ Created crime_dataset.csv")
else:
    print("\nLoading existing crime_dataset.csv...")
    df = pd.read_csv("crime_dataset.csv")
    print(f"✅ Loaded {len(df)} records")

print("\nDataset preview:")
print(df)

# Train model
print("\nTraining Decision Tree Classifier...")
X = df[['crime_count', 'night_risk']]
y = [1 if c > 15 else 0 for c in df['crime_count']]

from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
print("✅ Model trained and saved as model.pkl")

print("\n" + "-" * 50)
print("Testing model predictions:")
print("-" * 50)

test_cases = [
    ('Andheri', 'night'),
    ('Bandra', 'day'),
    ('Kurla', 'night'),
    ('Powai', 'day'),
    ('Dadar', 'night'),
    ('Thane', 'day')
]

for area, time in test_cases:
    row = df[df['area'] == area]
    if not row.empty:
        crime = row['crime_count'].values[0]
        night = 1 if time == 'night' else 0
        result = model.predict([[crime, night]])
        risk = model.predict_proba([[crime, night]])[0][1] * 100
        status = "⚠️ UNSAFE" if result[0] == 1 else "✅ SAFE"
        print(f"  {area:10} ({time:5}): {status} - Risk: {risk:.1f}%")

print("\n" + "=" * 50)
print("✅ Model training complete!")
print("=" * 50)