import numpy as np 

array = np.genfromtxt(r'QuestionsBaseOne.txt', dtype=str, delimiter=",")

selectedQuestionDiff = array[0][2:12]

print (selectedQuestionDiff)

print (array[0][2:12])
