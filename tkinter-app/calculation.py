import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

def process_inputs(inputs):
	# Process the inputs
	result = 1
	
	
	# Assuming you have a new input as a list
	new_input = [
	    inputs[0],
	    float(inputs[1]),
	    float(inputs[2]),
	    float(inputs[3]),
	    float(inputs[4])
	]
	

	# Load the CSV file into a DataFrame
	df3 = pd.read_csv("dataset.csv")

	# Handling outliers using IQR method
	Q1 = df3.quantile(0.25)
	Q3 = df3.quantile(0.75)
	IQR = Q3 - Q1
	df3 = df3[~((df3 < (Q1 - 1.5 * IQR)) | (df3 > (Q3 + 1.5 * IQR))).any(axis=1)]

	# Handling skewed distributions
	df3["precipitation"] = np.sqrt(df3["precipitation"])
	df3["wind"] = np.sqrt(df3["wind"])

	# Label encoding the "weather" column
	lc = LabelEncoder()
	df3["weather"] = lc.fit_transform(df3["weather"])

	# Convert "date" column to datetime format
	df3["date"] = pd.to_datetime(df3["date"])

	# Convert the "date" column to int64
	df3["date"] = df3["date"].apply(lambda x: int(x.timestamp()))

	# Create x_df3 by excluding "weather" column and converting remaining columns to int64
	x_df3 = df3.loc[:, df3.columns != "weather"].astype(np.int64).values

	# Create y_df3 by assigning the values of the "weather" column
	y_df3 = df3["weather"].values

	# Split the data into training and testing sets
	x_train_df3, x_test_df3, y_train_df3, y_test_df3 = train_test_split(x_df3, y_df3, test_size=0.1, random_state=2)

	# Create a decision tree classifier with the specified parameters
	dec_df3 = DecisionTreeClassifier(max_depth=4, max_leaf_nodes=15, random_state=0)

	# Train the decision tree model on the training data
	dec_df3.fit(x_train_df3, y_train_df3)


	# Convert the new input to a DataFrame
	df_new = pd.DataFrame([new_input], columns=["date", "precipitation", "high_temperature", "low_temperature", "wind"])

	# Handle outliers (using the same threshold values as during training)
	#df_new = df_new[~((df_new < (Q1 - 1.5 * IQR)) | (df_new > (Q3 + 1.5 * IQR))).any(axis=1)]

	# Transform skewed distributions (using the same transformations as during training)
	df_new["precipitation"] = np.sqrt(df_new["precipitation"])
	df_new["wind"] = np.sqrt(df_new["wind"])

	# Convert "date" column to datetime format
	df_new["date"] = pd.to_datetime(df_new["date"])

	# Convert the "date" column to int64
	df_new["date"] = df_new["date"].apply(lambda x: int(x.timestamp()))

	# Exclude the "weather" column and convert remaining columns to int64
	x_new = df_new.loc[:, df_new.columns != "weather"].astype(np.int64).values


	# Make predictions using the trained model
	predictions = dec_df3.predict(x_new)

	# Decode the predicted labels (if needed)
	predicted_weather = lc.inverse_transform(predictions)

	result= predicted_weather[0]

	

	return result

