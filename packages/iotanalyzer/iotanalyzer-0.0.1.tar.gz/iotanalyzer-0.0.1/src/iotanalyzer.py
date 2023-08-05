import pandas as pd

# Import sklearn classification algorithms
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import RidgeClassifierCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

# Import sklearn evaluation functions
from sklearn.metrics import classification_report, confusion_matrix

# ??
from sklearn.preprocessing import MinMaxScaler

# Import sklearn datastructure
from sklearn import tree

# Import sklearn train/test splitter
from sklearn.model_selection import train_test_split

# ??
from joblib import dump, load

import math

class classifier():
    def __init__(self, DEBUG = False):
        self.DEBUG = DEBUG

    def __log(self, msg):
        if self.DEBUG:
            print(msg)
    
    def __naiveBayes(self, x_train, y_train):
        model = GaussianNB()
        model = model.fit(x_train, y_train)
        return (model)


    def __knn(self, x_train, y_train):
        model = KNeighborsClassifier()
        model = model.fit(x_train, y_train)
        return (model)

    def __decisionTree(self, x_train, y_train):
        model = tree.DecisionTreeClassifier(class_weight='balanced')
        model = model.fit(x_train, y_train)
        return (model)

    # SVM Classifier linear kernel
    def __svm_linear(self, x_train, y_train):
        model = SVC(kernel='linear', class_weight='balanced')
        model = model.fit(x_train, y_train)
        return (model)

    # SVM Classifier polynomial kernel e.g. 2-8
    def __svm_poly(self, x_train, y_train, polynomial_degree):
        model = SVC(kernel='poly',class_weight='balanced', degree=polynomial_degree, random_state=0)
        model = model.fit(x_train, y_train)
        return (model)

    # SVM Classifier rbf kernel
    def __svm_rbf(self, x_train, y_train):
        model = SVC(kernel='rbf',class_weight='balanced')
        model = model.fit(x_train, y_train)
        return (model)

    def __logisticRegression(self, x_train, y_train):
        model = LogisticRegression(class_weight = 'balanced')
        model = model.fit(x_train, y_train)
        return (model)

    def __passiveAggressiveClassifier(self, x_train, y_train):
        model =PassiveAggressiveClassifier(max_iter=1000, random_state=0,tol=1e-3,class_weight='balanced')
        model = model.fit(x_train, y_train)
        return (model)

    def __randomforest(self, x_train, y_train):
        model = RandomForestClassifier(max_depth=2, random_state=0, class_weight='balanced')
        model = model.fit(x_train, y_train)
        return (model)

    def __ridgeClassifierCV(self, x_train, y_train):
        model = RidgeClassifierCV(alphas=[1e-3, 1e-2, 1e-1, 1], class_weight='balanced')
        model = model.fit(x_train, y_train)
        return (model)
    
    def run(self, input_path, features, groundtruth_name, classifier_name, test_set_size=0.3, model_saved_dir=None, polynomial_degree=None):
        classifiers = {
            'naiveBayes': self.__naiveBayes,
            'knn': self.__knn,
            'decisionTree': self.__decisionTree,
            'svm_linear': self.__svm_linear,
            'svm_poly': self.__svm_poly,
            'svm_rbf': self.__svm_rbf,
            'logisticRegression': self.__logisticRegression,
            'passiveAggressiveClassifier': self.__passiveAggressiveClassifier,
            'randomforest': self.__randomforest,
            'ridgeClassifierCV': self.__ridgeClassifierCV
        }

        df = pd.read_csv(input_path)
        df = df.dropna()

        features = features

        x = df[features]

        scaler = MinMaxScaler()
        x = scaler.fit_transform(x)
        
        y = df[groundtruth_name]
        
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = test_set_size)

        if classifier_name != 'svm_poly':
            model = classifiers[classifier_name](x_train, y_train)
        elif polynomial_degree != None:
            model = classifiers[classifier_name](x_train, y_train, polynomial_degree)
        else:
            return 'Error: no polynomial degree is provided for SVM polynomial kernel.'

        # Save trained model
        if model_saved_dir != None:
            model_saved_path = model_saved_dir + classifier_name + '_model.joblib'
            dump(model, model_saved_path)

        y_pred = model.predict(x_test)

        cnf_matrix = confusion_matrix(y_test, y_pred)

        self.__log(classification_report(y_test, y_pred))

        self.__log(cnf_matrix)

        return cnf_matrix
    
    def run_all(self, input_path, features, groundtruth_name, test_set_size=0.3, model_saved_dir=None, svm_polynomial_degrees=None):
        classifier_list = ['naiveBayes', 'knn', 'decisionTree', 'svm_linear', 'svm_poly', 'svm_rbf', 'logisticRegression', 'passiveAggressiveClassifier', 'randomforest', 'ridgeClassifierCV']
        cnf_matrix = {}
        
        for classifier_name in classifier_list:
            if classifier_name != 'svm_poly':
                cnf_matrix[classifier_name] = self.run(input_path, features, groundtruth_name, classifier_name, test_set_size=test_set_size, model_saved_dir=model_saved_dir)
            elif svm_polynomial_degrees != None:
                for degree in svm_polynomial_degrees:
                    cnf_matrix[classifier_name+str(degree)] = self.run(input_path, features, groundtruth_name, classifier_name, test_set_size=test_set_size, model_saved_dir=model_saved_dir, polynomial_degree=degree)
            else:
                self.__log('No polynomial degrees are provided for SVM polynomial kernel. Skip...')
        
        return cnf_matrix
    
    def test(self, test_data_path, features,groundtruth_name, model_dir, classifier_name):
        # Load test data
        df = pd.read_csv(test_data_path)
        df = df.dropna()

        features = features

        x_test = df[features]

        scaler = MinMaxScaler()
        x_test = scaler.fit_transform(x_test)
        
        y_test = df[groundtruth_name]

        # Load saved model

        model = load(model_dir + classifier_name + '.joblib')
        
        y_pred = model.predict(x_test)

        cnf_matrix = confusion_matrix(y_test, y_pred)

        self.__log(classification_report(y_test, y_pred))

        self.__log(cnf_matrix)

        return cnf_matrix

class evaluation():
    def __init__(self, model, sklearn_cnf_matrix=None, TP=None, TN=None, FN=None, FP=None):
        self.model = model
        if sklearn_cnf_matrix.any() != None:
            self.cnf_matrix = sklearn_cnf_matrix
            cnf_matrix_array = sklearn_cnf_matrix.tolist()
            self.TP = int(cnf_matrix_array[0][0])
            self.FP = int(cnf_matrix_array[0][1])
            self.FN = int(cnf_matrix_array[1][0])
            self.TN = int(cnf_matrix_array[1][1])
        elif TP != None and TN != None and FN != None and FP != None:
            self.TP = int(TP)
            self.FP = int(FP)
            self.FN = int(FN)
            self.TN = int(TN)

    def get_np_cnf_matrix(self):
        return self.cnf_matrix
    
    def get_cnf_matrix(self):
        return {
            'TP': self.TP,
            'FN': self.FN,
            'FP': self.FP,
            'TN': self.TN
        }

    def get_all_metrics(self):
        TP = self.TP
        FN = self.FN
        FP = self.FP
        TN = self.TN

        if ((int(TP + FP))) == 0 or (int((FN + TN)) == 0 ) or (int((FP + TN)) ==0)or (int((TP + FN))==0) :
            return 'Cannot calculate evaluation metrics.'
        else:
            metric = {}
            
            ACCURACY = float((TP + TN)/(TP + FP + FN + TN))
            PRECISION = float(TP/(TP + FP))
            RECALL = float(TP/(TP + FN))
            if ((PRECISION == 0) or (RECALL == 0)):
                return 'Cannot calculate PRECISION or RECALL.'
            else:
                metric['TP'] = TP
                metric['FN'] = FN
                metric['TN'] = TN
                metric['FP'] = FP
                F1 = float(2 * PRECISION*RECALL / (PRECISION + RECALL))
                MCC = float((TP * TN - FP * FN) / math.sqrt((TP + FP) * (FN + TN) * (FP + TN) * (TP + FN)))
                SPECIFICITY = float(TN / (TN + FP))
                metric['TPR'] = float(TP / (TP + FN))
                metric['FNR']  = float(FN / (TP + FN))
                metric['TNR'] = float(TN / (TN + FP))
                metric['FPR']  = float(FP / (TN + FP))
                metric['ACCURACY'] = ACCURACY
                metric['PRECISION'] =PRECISION
                metric['RECALL']= RECALL
                metric['F1'] = F1
                metric['MCC'] = MCC
                metric['Cohen_kappa'] = 2 * (TP * TN - FN * FP) / (TP * FN + TP * FP + 2 * TP * TN + FN^2 + FN * TN + FP^2 + FP * TN)
                metric['SPECIFICITY'] = SPECIFICITY
                metric['model'] = self.model
                return metric