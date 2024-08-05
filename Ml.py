from sklearn import tree
import csv
import numpy as np

def preprocess_value(value):
    try:
        return float(value.replace(',', '').replace(' miles', ''))
    except ValueError:
        return 0.0  
x = []
y = []

with open('car_res copy.csv', 'r') as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        x.append(list(map(preprocess_value, row[1:6])))
        y.append(row[6])

# تبدیل لیست‌ها به آرایه‌های numpy
x = np.array(x)
y = np.array(y)

# ایجاد و آموزش مدل Decision Tree Classifier
clf = tree.DecisionTreeClassifier()
clf.fit(x, y)
new_data=['Ford Fusion','7,142 miles','Duluth, GA','Gray interior','Blue exterior','8 accident reported']
new_data_features = list(map(preprocess_value, new_data[1:6]))
prediction = clf.predict([np.array(new_data_features)])

print(prediction)
print(new_data[1:6])