import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score
import json
import numpy as np

# Set random seed
seed = 42

################################
########## DATA PREP ###########
################################

# Load in the data
df = pd.read_csv("wine_quality.csv")

# Split into train and test sections
X = df.drop('quality', axis=1)
y = df.quality
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

#################################
########## MODELLING ############
#################################

# Fit a model on the train section
regr = RandomForestClassifier(max_depth=7, random_state=seed)
regr.fit(X_train, y_train)

# Report training set score
predictions = regr.predict(X_test)
train_score = accuracy_score(predictions, y_test) * 100

# Write scores to a file
with open("metrics.json", 'w') as outfile:
    json.dump({"Accuracy of the Model is:" : train_score},outfile)

##########################################
##### PLOT FEATURE IMPORTANCE ############
##########################################
# Calculate feature importance in random forest
importances = regr.feature_importances_
labels = df.columns
feature_df = pd.DataFrame(list(zip(labels, importances)), columns=["feature", "importance"])
feature_df = feature_df.sort_values(by='importance', ascending=False, )

# image formatting
axis_fs = 18  # fontsize
title_fs = 22  # fontsize
sns.set(style="whitegrid")

ax = sns.barplot(x="importance", y="feature", data=feature_df)
ax.set_xlabel('Importance', fontsize=axis_fs)
ax.set_ylabel('Feature', fontsize=axis_fs)  # ylabel
ax.set_title('Random forest\nfeature importance', fontsize=title_fs)

plt.tight_layout()
plt.savefig("feature_importance.png", dpi=120)
plt.close()

###############################################
############ PLOT CONFUSION MATRIX #############
##########################################

from sklearn.metrics import plot_confusion_matrix
plot_confusion_matrix(regr,X_test,y_test)
plt.tight_layout()
plt.savefig("confusion_matrix.png",dpi=120)
plt.close()

