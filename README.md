# Transaction Classification Based on NN built by TensorFlow

1. Build words vocabulary list based on the training and testing data
2. Transform the description of the transaction into vetor
3. Transform the labeled category into vector
4. Build Neural Network
5. Trainning
6. Use the testing data in test.json to predict the category

# How to execute
1. python restService.py Start the server
2. Query the category:
   POST request to localhost:5000/getCategory with JSON data like {"title":"PTV"}
   Input new training data:
   POST request to localhost:5000/inputCategory with JSON data like {"title":"PTV", "category":"Transport"}
