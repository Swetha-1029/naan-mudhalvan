# -*- coding: utf-8 -*-
"""Fake News Detection

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aRgZ7wovvP-IEd8Z9_YBVKeoTtMBN7gH

# Fake News Detection

## Importing Libraries
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import re
import string

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

"""## Importing Dataset"""

df_fake = pd.read_csv("Fake - Fake.csv")
df_true = pd.read_csv("True - True.csv")

df_fake.head()

df_true.head(5)

"""## Inserting a column "class" as target feature

---


"""

df_fake["class"] = 0
df_true["class"] = 1

df_fake.shape, df_true.shape

# Removing last 10 rows for manual testing
df_fake_manual_testing = df_fake.tail(10)
for i in range(23480,23470,-1):
    df_fake.drop([i], axis = 0, inplace = True)


df_true_manual_testing = df_true.tail(10)
for i in range(21416,21406,-1):
    df_true.drop([i], axis = 0, inplace = True)

df_fake.shape, df_true.shape

df_fake_manual_testing["class"] = 0
df_true_manual_testing["class"] = 1

df_fake_manual_testing.head(10)

df_true_manual_testing.head(10)

df_manual_testing = pd.concat([df_fake_manual_testing,df_true_manual_testing], axis = 0)
df_manual_testing.to_csv("manual_testing.csv")

"""## Merging True and Fake Dataframes

---


"""

df_merge = pd.concat([df_fake, df_true], axis =0 )
df_merge.head(10)
df_merge.to_csv('merged_dataset.csv', index=False)

df_merge.columns

"""## Removing columns which are not required"""

df = df_merge.drop(["title", "subject","date"], axis = 1)

df.isnull().sum()

"""## Random Shuffling the dataframe"""

df = df.sample(frac = 1)

df.head()

df.reset_index(inplace = True)
df.drop(["index"], axis = 1, inplace = True)

df.columns

df.head()

# (A) Check Missing Values Before Cleaning
print("Missing values BEFORE cleaning:\n", df_merge.isnull().sum())

# (B) Check Duplicate Rows Before Cleaning
print("Duplicate rows BEFORE cleaning:", df_merge.duplicated().sum())

# (C) Detect Outliers Based on Text Length Before Cleaning
df_merge["text_length"] = df_merge["text"].apply(len)

q1 = df_merge["text_length"].quantile(0.25)
q3 = df_merge["text_length"].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

print("\nOutlier Detection BEFORE cleaning:")
print("Q1 (25th percentile):", q1)
print("Q3 (75th percentile):", q3)
print("IQR:", iqr)
print("Lower bound:", lower_bound)
print("Upper bound:", upper_bound)

# Count number of outliers before removal
outliers_before = df_merge[(df_merge["text_length"] < lower_bound) | (df_merge["text_length"] > upper_bound)].shape[0]
print("Number of outliers BEFORE cleaning:", outliers_before)

# (D) Check Data Types Before Cleaning
print("\nData types BEFORE cleaning:\n", df_merge.dtypes)

# (A) Check Missing Values AFTER Cleaning
print("\nMissing values AFTER cleaning:\n", df_merge.isnull().sum())

# (B) Check Duplicate Rows AFTER Cleaning
print("Duplicate rows AFTER cleaning:", df_merge.duplicated().sum())

# (C) Detect Outliers Based on Text Length AFTER Cleaning
df_merge["text_length"] = df_merge["text"].apply(len)

q1 = df_merge["text_length"].quantile(0.25)
q3 = df_merge["text_length"].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

print("\nOutlier Detection AFTER cleaning:")
print("Q1 (25th percentile):", q1)
print("Q3 (75th percentile):", q3)
print("IQR:", iqr)
print("Lower bound:", lower_bound)
print("Upper bound:", upper_bound)

# Count number of outliers after removal
outliers_after = df_merge[(df_merge["text_length"] < lower_bound) | (df_merge["text_length"] > upper_bound)].shape[0]
print("Number of outliers AFTER cleaning:", outliers_after)

# (D) Check Data Types AFTER Cleaning
print("\nData types AFTER cleaning:\n", df_merge.dtypes)

# Drop text_length column (if no longer needed)
df_merge.drop("text_length", axis=1, inplace=True)

"""## Creating a function to process the texts"""

def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

df["text"] = df["text"].apply(wordopt)

"""## Defining dependent and independent variables"""

x = df["text"]
y = df["class"]

"""## Splitting Training and Testing"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

"""## Convert text to vectors"""

from sklearn.feature_extraction.text import TfidfVectorizer

vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)

"""## Logistic Regression"""

from sklearn.linear_model import LogisticRegression

LR = LogisticRegression()
LR.fit(xv_train,y_train)

pred_lr=LR.predict(xv_test)

LR.score(xv_test, y_test)

print(classification_report(y_test, pred_lr))

"""## Decision Tree Classification"""

from sklearn.tree import DecisionTreeClassifier

DT = DecisionTreeClassifier()
DT.fit(xv_train, y_train)

pred_dt = DT.predict(xv_test)

DT.score(xv_test, y_test)

print(classification_report(y_test, pred_dt))

"""## Gradient Boosting Classifier"""

from sklearn.ensemble import GradientBoostingClassifier

GBC = GradientBoostingClassifier(random_state=0)
GBC.fit(xv_train, y_train)

pred_gbc = GBC.predict(xv_test)

GBC.score(xv_test, y_test)

print(classification_report(y_test, pred_gbc))

"""## Random Forest Classifier"""

from sklearn.ensemble import RandomForestClassifier

RFC = RandomForestClassifier(random_state=0)
RFC.fit(xv_train, y_train)

pred_rfc = RFC.predict(xv_test)

RFC.score(xv_test, y_test)

print(classification_report(y_test, pred_rfc))

"""## Model Testing"""

def output_lable(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "Not A Fake News"

def manual_testing(news):
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    pred_GBC = GBC.predict(new_xv_test)
    pred_RFC = RFC.predict(new_xv_test)

    return print("\n\nLR Prediction: {} \nDT Prediction: {} \nGBC Prediction: {} \nRFC Prediction: {}".format(output_lable(pred_LR[0]),                                                                                                       output_lable(pred_DT[0]),
                                                                                                              output_lable(pred_GBC[0]),
                                                                                                              output_lable(pred_RFC[0])))

news = str(input())
manual_testing(news)

news = str(input())
manual_testing(news)

# UNIVARIATE ANALYSIS


# Countplot for class distribution
sns.countplot(data=df, x='class')
plt.title('Distribution of Fake (0) and Real (1) News')
plt.xlabel('Class')
plt.ylabel('Count')
plt.show()

# Word count in each article
df["word_count"] = df["text"].apply(lambda x: len(str(x).split()))

# Histogram of word count
plt.hist(df["word_count"], bins=50, color='skyblue')
plt.title('Word Count Distribution')
plt.xlabel('Word Count')
plt.ylabel('Frequency')
plt.show()

# Boxplot of word count by class
sns.boxplot(data=df, x='class', y='word_count')
plt.title('Word Count by Class')
plt.show()

# BIVARIATE / MULTIVARIATE ANALYSIS

# Correlation matrix (only numerical)
corr = df[['word_count', 'class']].corr()

# Heatmap
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# Grouped bar plot of average word count per class
df.groupby("class")["word_count"].mean().plot(kind='bar', color=['red', 'green'])
plt.title("Average Word Count by Class")
plt.xlabel("Class")
plt.ylabel("Average Word Count")
plt.xticks(ticks=[0,1], labels=["Fake", "Real"], rotation=0)
plt.show()


# INSIGHTS SUMMARY


print("\n--- Insights Summary ---")
print("1. The dataset is balanced/unbalanced based on class counts.")
print("2. Fake news articles tend to have more/less words on average than real news.")
print("3. Word count is slightly correlated with the class label.")
print("4. Features like word count could help distinguish fake from real news.")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import roc_curve, auc
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import TfidfVectorizer # Import TfidfVectorizer

# Load Your Dataset
df = pd.read_csv('/content/merged_dataset.csv')

# Assuming the last column is the target and 'text' column contains text data
X = df[['text']]  # Select the 'text' column for feature extraction
y = df.iloc[:, -1]   # last column as label

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#  Feature Extraction using TfidfVectorizer
vectorizer = TfidfVectorizer() # Initialize TfidfVectorizer
X_train_vec = vectorizer.fit_transform(X_train['text']) # Fit and transform training data
X_test_vec = vectorizer.transform(X_test['text']) # Transform testing data

# Model Training
model = RandomForestClassifier(random_state=42)
model.fit(X_train_vec, y_train) # Train the model with vectorized data

#Confusion Matrix
y_pred = model.predict(X_test_vec) # Predict using vectorized testing data
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
disp.plot(cmap='Blues')
plt.title("Confusion Matrix")
plt.show()

# ROC Curve
if hasattr(model, "predict_proba"):
    y_prob = model.predict_proba(X_test_vec)[:, 1] # Use X_test_vec instead of X_test
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.grid()
    plt.show()

from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, mean_squared_error

# Predict using vectorized testing data
y_pred = model.predict(X_test_vec)

# (1) Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# (2) F1-Score (macro average for multi-class, binary you can use 'binary')
f1 = f1_score(y_test, y_pred, average='macro')
print(f"F1 Score (Macro): {f1:.4f}")

# (3) ROC-AUC
if hasattr(model, "predict_proba"):
    y_prob = model.predict_proba(X_test_vec)

    # If binary classification
    if len(model.classes_) == 2:
        roc_auc = roc_auc_score(y_test, y_prob[:, 1])
        print(f"ROC AUC Score: {roc_auc:.4f}")
    else:
        # Multi-class ROC AUC using One-vs-Rest
        roc_auc = roc_auc_score(y_test, y_prob, multi_class='ovr')
        print(f"ROC AUC Score (OvR Multi-class): {roc_auc:.4f}")

# (4) RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"RMSE: {rmse:.4f}")

#feature_importances
if hasattr(model, "feature_importances_"):

    importances = model.feature_importances_
    feature_names = vectorizer.get_feature_names_out()
    sorted_idx = np.argsort(importances)[::-1]
    top_n = 20
    # Create a bar plot for top N features
    sns.barplot(x=importances[sorted_idx[:top_n]],
                y=[feature_names[i] for i in sorted_idx[:top_n]])

    plt.title(f"Top {top_n} Feature Importances")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()
else:
    print("Model does not support feature_importances_. Skipping feature importance plot.")

#Residual plot
y_pred = model.predict(X_test_vec)  # Use X_test_vec (vectorized data) instead of X_test
residuals = np.array(y_test) - np.array(y_pred)
sns.scatterplot(x=y_pred, y=residuals)
plt.axhline(0, color='r', linestyle='--')
plt.xlabel("Predicted")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()

#Model Comparison Plot
def plot_model_comparison(model_scores):
    names = list(model_scores.keys())
    scores = list(model_scores.values())
    sns.barplot(x=scores, y=names)
    plt.title("Model Accuracy Comparison")
    plt.xlabel("Accuracy")
    plt.ylabel("Model")
    plt.xlim(0, 1)
    plt.grid(True)
    plt.show()
accuracy = model.score(X_test_vec, y_test) # Use X_test_vec instead of X_test
plot_model_comparison({'Random Forest': accuracy, 'Dummy Model': 0.5})
