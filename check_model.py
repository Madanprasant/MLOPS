import pickle
import numpy as np

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# Test cases
# 2, 2, 2, 2
test_1 = np.array([[2, 2, 2, 2]])
prob_1 = model.predict_proba(test_1)[0, 1]
print(f"Prob for [2,2,2,2]: {prob_1}")

# 3, 3, 3, 3
test_2 = np.array([[3, 3, 3, 3]])
prob_2 = model.predict_proba(test_2)[0, 1]
print(f"Prob for [3,3,3,3]: {prob_2}")

# 7, 1, 3, 7 (Near decision boundary area)
test_3 = np.array([[7, 1, 3, 7]])
prob_3 = model.predict_proba(test_3)[0, 1]
print(f"Prob for [7,1,3,7]: {prob_3}")
