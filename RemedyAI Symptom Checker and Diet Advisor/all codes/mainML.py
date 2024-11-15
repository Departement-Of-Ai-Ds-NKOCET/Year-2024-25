# Import necessary libraries (Main)
import pandas as pd
import numpy as np
import pickle  # For saving models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, f1_score, confusion_matrix, classification_report,
    precision_recall_curve, roc_curve, roc_auc_score
)
from sklearn.ensemble import VotingClassifier
import seaborn as sns
import matplotlib.pyplot as plt

# Function to provide remedies based on input features and predicted risk
def get_remedies(features, predicted_risk):
    remedies = []

    if predicted_risk > 0.5:  # High risk
        remedies.append("Consult a healthcare professional immediately for a thorough evaluation.")
    
    if features['age'] > 50:  # Use the correct column name for age
        remedies.append("Schedule regular check-ups with your doctor.")
    
    if features['chol'] > 200:  # Use the correct column name for cholesterol
        remedies.append("Consider adopting a heart-healthy diet low in saturated fats and high in fruits, vegetables, and whole grains.")
    
    if features['trestbps'] > 130:  # Use the correct column name for resting blood pressure
        remedies.append("Monitor your blood pressure regularly and consider lifestyle changes to lower it.")
    
    if features['thalach'] < 120:  # Use the correct column name for max heart rate achieved
        remedies.append("Improve your cardiovascular fitness through regular aerobic exercise.")
    
    if features['oldpeak'] > 1:  # Use the correct column name for ST depression (old peak)
        remedies.append("Discuss stress test results with your doctor and consider cardiac rehabilitation if recommended.")
    
    remedies.append("Maintain a healthy weight through a balanced diet and regular exercise.")
    remedies.append("If you smoke, quit smoking or seek support to help you quit.")
    remedies.append("Limit alcohol consumption to no more than one drink per day for women and two for men.")
    remedies.append("Aim for at least 150 minutes of moderate-intensity exercise per week.")
    remedies.append("Manage stress through relaxation techniques like meditation or yoga.")
    remedies.append("Ensure you're getting 7-9 hours of quality sleep each night.")
    
    return remedies


# Step 1: Load the dataset
df = pd.read_csv(r'C:\Users\priti\OneDrive\Desktop\project\heart.csv')

# Print column names
print("Column names:", df.columns.tolist())

# Step 2: Explore the dataset
print("Dataset Head:\n", df.head())  
print("\nDataset Info:\n", df.info())  
print("\nChecking for missing values:\n", df.isnull().sum())  

# Step 3: Data Preprocessing
# Handling missing values (if necessary)
df.fillna(df.median(), inplace=True)  # Fill missing values with median

# Define features (X) and target (y)
target_column = 'target'  
X = df.drop(columns=[target_column])
y = df[target_column]

# Standardize the features (scaling)
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Number of epochs to simulate
epochs = 5

# Step 4: Define the Models
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
lr_model = LogisticRegression(random_state=42)

# Combine the two models using VotingClassifier
voting_clf = VotingClassifier(estimators=[
    ('random_forest', rf_model), 
    ('logistic_regression', lr_model)
], voting='soft')  # Use 'soft' voting to get predict_proba

# Function to plot confusion matrices
def plot_confusion_matrices(models, cm_list, epoch):
    plt.figure(figsize=(18, 6))
    for i, (model_name, cm) in enumerate(zip(models, cm_list)):
        plt.subplot(1, len(models), i + 1)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues' if model_name == 'Random Forest' else 'Greens' if model_name == 'Logistic Regression' else 'Reds')
        plt.title(f'{model_name} Confusion Matrix - Epoch {epoch + 1}')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
    plt.tight_layout()
    plt.show()

# Step 5: Run the models over multiple epochs and gather metrics
for epoch in range(epochs):
    print(f"\nEpoch {epoch + 1} - Model Evaluation")

    # Split data into training and testing sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=epoch)

    # Train the models separately
    rf_model.fit(X_train, y_train)
    lr_model.fit(X_train, y_train)
    voting_clf.fit(X_train, y_train)

    # Model Predictions
    rf_pred = rf_model.predict(X_test)
    rf_pred_prob = rf_model.predict_proba(X_test)[:, 1]

    lr_pred = lr_model.predict(X_test)
    lr_pred_prob = lr_model.predict_proba(X_test)[:, 1]

    voting_pred = voting_clf.predict(X_test)
    voting_pred_prob = voting_clf.predict_proba(X_test)[:, 1]

    # Save the models using pickle
    with open(f'random_forest_model_epoch_{epoch + 1}.pkl', 'wb') as rf_file:
        pickle.dump(rf_model, rf_file)

    with open(f'logistic_regression_model_epoch_{epoch + 1}.pkl', 'wb') as lr_file:
        pickle.dump(lr_model, lr_file)

    with open(f'voting_classifier_model_epoch_{epoch + 1}.pkl', 'wb') as voting_file:
        pickle.dump(voting_clf, voting_file)

    # Calculate Metrics for Random Forest
    rf_accuracy = accuracy_score(y_test, rf_pred)
    rf_f1 = f1_score(y_test, rf_pred, average='weighted')
    rf_cm = confusion_matrix(y_test, rf_pred)
    rf_report = classification_report(y_test, rf_pred, output_dict=True)
    rf_auc = roc_auc_score(y_test, rf_pred_prob)

    # Calculate Metrics for Logistic Regression
    lr_accuracy = accuracy_score(y_test, lr_pred)
    lr_f1 = f1_score(y_test, lr_pred, average='weighted')
    lr_cm = confusion_matrix(y_test, lr_pred)
    lr_report = classification_report(y_test, lr_pred, output_dict=True)
    lr_auc = roc_auc_score(y_test, lr_pred_prob)

    # Calculate Metrics for Voting Classifier (Combined Algorithm)
    voting_accuracy = accuracy_score(y_test, voting_pred)
    voting_f1 = f1_score(y_test, voting_pred, average='weighted')
    voting_cm = confusion_matrix(y_test, voting_pred)
    voting_report = classification_report(y_test, voting_pred, output_dict=True)
    voting_auc = roc_auc_score(y_test, voting_pred_prob)

    # Step 6: Display Metrics for All Models
    print(f"\nRandom Forest - Epoch {epoch + 1}")
    print(f"Accuracy: {rf_accuracy * 100:.2f}%, F1-Score: {rf_f1:.2f}, AUC: {rf_auc:.2f}")
    print(f"Precision: {rf_report['weighted avg']['precision']:.2f}, Recall: {rf_report['weighted avg']['recall']:.2f}, Support: {rf_report['weighted avg']['support']}")
    
    print(f"\nLogistic Regression - Epoch {epoch + 1}")
    print(f"Accuracy: {lr_accuracy * 100:.2f}%, F1-Score: {lr_f1:.2f}, AUC: {lr_auc:.2f}")
    print(f"Precision: {lr_report['weighted avg']['precision']:.2f}, Recall: {lr_report['weighted avg']['recall']:.2f}, Support: {lr_report['weighted avg']['support']}")
    
    print(f"\nVoting Classifier (Combined) - Epoch {epoch + 1}")
    print(f"Accuracy: {voting_accuracy * 100:.2f}%, F1-Score: {voting_f1:.2f}, AUC: {voting_auc:.2f}")
    print(f"Precision: {voting_report['weighted avg']['precision']:.2f}, Recall: {voting_report['weighted avg']['recall']:.2f}, Support: {voting_report['weighted avg']['support']}")

    # Step 7: Plot ROC Curves for All Models
    fpr_rf, tpr_rf, _ = roc_curve(y_test, rf_pred_prob)
    fpr_lr, tpr_lr, _ = roc_curve(y_test, lr_pred_prob)
    fpr_voting, tpr_voting, _ = roc_curve(y_test, voting_pred_prob)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr_rf, tpr_rf, color='blue', label=f'Random Forest (AUC = {rf_auc:.2f})')
    plt.plot(fpr_lr, tpr_lr, color='green', label=f'Logistic Regression (AUC = {lr_auc:.2f})')
    plt.plot(fpr_voting, tpr_voting, color='red', label=f'Voting Classifier (AUC = {voting_auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - Epoch {epoch + 1}')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.show()

    # Plot Confusion Matrices for all models
    plot_confusion_matrices(
        ['Random Forest', 'Logistic Regression', 'Voting Classifier'], 
        [rf_cm, lr_cm, voting_cm], epoch
    )

    # Step 8: Generate remedies for selected test samples
    sample_indices = np.random.choice(range(len(X_test)), size=3, replace=False)  # Randomly choose 3 samples

    for idx in sample_indices:
        sample_features = dict(zip(df.columns[:-1], X_test[idx]))  # Convert to dictionary for easier interpretation
        predicted_risk = voting_pred_prob[idx]
        remedies = get_remedies(sample_features, predicted_risk)

        print(f"\nSample {idx + 1}:")
        print(f"Features: {sample_features}")
        print(f"Predicted Risk: {predicted_risk:.2f}")
        print(f"Recommended Remedies: {', '.join(remedies)}")
