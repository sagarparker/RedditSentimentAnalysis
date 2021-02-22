import warnings
import os
import pandas as pd 
import matplotlib.pyplot as plt
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score

warnings.filterwarnings('ignore')
dir_Path = 'D:\\College\\NLP\\SentimentAnalysis'
os.chdir(dir_Path)
Postdata = pd.read_csv('RedditData.csv')
print(Postdata.shape)

### Checking Missing values in the csv file

count = Postdata.isnull().sum().sort_values(ascending=False)
percentage = ((Postdata.isnull().sum()/len(Postdata)*100)).sort_values(ascending=False)
missing_data = pd.concat([count, percentage], axis=1,
keys=['Count','Percentage'])

print('Count and percentage of missing values for the columns:\n')

print(missing_data)

#This function converts to lower-case, removes square bracket, removes numbers and punctuation
def text_clean_1(text):
    
    #Convert the text to lower
    text = text.lower()
    
    #Remove the brackets
    text = re.sub('\[.*?\]', '', text)
    
    #Remove the punctuations
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    
    #Remove the digits
    text = re.sub('\w*\d\w*', '', text)
    
    return text

cleaned1 = lambda x: text_clean_1(x)

# Updated text
Postdata['cleaned_post_data'] = pd.DataFrame(Postdata.redditpost.apply(cleaned1))
Postdata.head(10)

# Apply a second round of cleaning
def text_clean_2(text):
    
    #Replacing quotes with blanks
    text = re.sub('[‘’“”…]', '', text)
    
    #Replacing new lines with blank
    text = re.sub('\n', '', text)
    return text

cleaned2 = lambda x: text_clean_2(x)

# Let's take a look at the updated text
Postdata['cleaned_data'] = pd.DataFrame(Postdata['cleaned_post_data'].apply(cleaned2))
Postdata.head(10)


#Independent variable
Independent_var = Postdata.cleaned_data

#Target variable
Dependent_var = Postdata.category

IV_train, IV_test, DV_train, DV_test = train_test_split(Independent_var, Dependent_var, test_size = 0.1, random_state = 225)

print('IV_train :', len(IV_train))
print('IV_test  :', len(IV_test))
print('DV_train :', len(DV_train))
print('DV_test  :', len(DV_test))


tvec = TfidfVectorizer()
clf2 = LogisticRegression(solver = "lbfgs")


model = Pipeline([('vectorizer',tvec),('classifier',clf2)])

model.fit(IV_train, DV_train)

predictions = model.predict(IV_test)

confusion_matrix(predictions, DV_test)


print("Accuracy : ", accuracy_score(predictions, DV_test))
print("Precision : ", precision_score(predictions, DV_test, average = 'weighted'))
print("Recall : ", recall_score(predictions, DV_test, average = 'weighted'))


example = ["I am angry"]
result = model.predict(example)

print(result)

