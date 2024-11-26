import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

# Loading the dataset
file_path = r"C:\Users\swapn\OneDrive\Desktop\infosys\human stress\stress_detection _dataset.csv"
df = pd.read_csv(file_path)

# Preprocessing
X = df.drop('Stress', axis=1)
y = df['Stress']

# Check for NaN or infinite values
if X.isnull().sum().any() or (X == float('inf')).sum().any() or (X == float('-inf')).sum().any():
    # Handle NaN values: replace with the mean of each column
    X.fillna(X.mean(), inplace=True)
    
    # Handle infinite values: replace with a large number
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.fillna(X.mean(), inplace=True)

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizing the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Creating the model
model = DecisionTreeClassifier(random_state=42)

# Training the model
model.fit(X_train_scaled, y_train)

# Making the prediction
y_pred = model.predict(X_test_scaled)

# Evaluating the model
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
plt.figure(figsize=(6, 4))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()

# Adding text annotations
thresh = cm.max() / 2
for i, j in np.ndindex(cm.shape):
    plt.text(j, i, cm[i, j], horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")

# Displaying the plot
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.tight_layout()
plt.show()

# Saving the model
joblib.dump(model, 'stress_detection_dt_model.pkl')
