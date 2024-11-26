import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

# Load the dataset
file_path = r"C:\Users\swapn\OneDrive\Desktop\infosys\human stress\stress_detection _dataset.csv"
df = pd.read_csv(file_path)

# Check for NaN or Infinite values in the dataset
if df.isnull().any().any():
    print("Dataset contains NaN values. Filling them with the column mean.")
    df = df.fillna(df.mean())  # Replace NaN with column means

if np.isinf(df.values).any():
    print("Dataset contains infinite values. Replacing them with NaN.")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.fillna(df.mean())  # Replace any remaining NaN values

# Separate features and target variable
X = df.drop('Stress', axis=1)  
y = df['Stress']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the features
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create the Logistic Regression model
model = LogisticRegression()

# Train the model
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f'Accuracy: {accuracy:.2f}')
print(f'Precision: {precision:.2f}')
print(f'Recall: {recall:.2f}')
print(f'F1-Score: {f1:.2f}')

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

# Plot confusion matrix
plt.figure(figsize=(6, 4))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ['Not Stressed', 'Stressed'])
plt.yticks(tick_marks, ['Not Stressed', 'Stressed'])

thresh = cm.max() / 2
for i, j in np.ndindex(cm.shape):
    plt.text(j, i, cm[i, j], horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")

plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.tight_layout()
plt.show()

# Save the trained model to a file
joblib.dump(model, 'stress_detection_model.pkl')
