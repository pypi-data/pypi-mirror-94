import numpy as np

def calculate_accuracy(model, x_test, y_test):
	result = model.predict(x_test);
	
	test_acc = np.sum(result == y_test) / len(y_test);
	print(f"Accuracy of the model: {test_acc}%")
	
def calculate_confusion(model, x_test, y_test):
	result = model.predict(x_test);
	
	print("Classes |TP     |FP     |FN     |TN     |")
	for i in model.classes:
		
		from_true = np.where(y_test == model.classes[i])[0]
		from_pred = np.where(result == model.classes[i])[0]
		
		intersect = np.intersect1d(from_true, from_pred)
		TP = intersect.size
		FN = from_true.size - TP
		FP = from_pred.size - TP
		TN = len(result) - (TP + FN + FP)
		
		print("_________________________________________")
		print(f"{model.classes[i]}\t|{TP}\t|{FP}\t|{FN}\t|{TN}\t|")