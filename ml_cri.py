import pandas as pd
import numpy as np
import pickle
from typing import Dict, Tuple, Optional
from sklearn.base import BaseEstimator
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from yellowbrick.classifier import ConfusionMatrix
import matplotlib.pyplot as plt
import os
import warnings 

warnings.filterwarnings("ignore")


class CRIModelEvaluator:
    def __init__(self, data_frame: pd.DataFrame, target_index: int = 0):

        if data_frame.empty:
            raise ValueError("The provided DataFrame is empty.")
            
        self.X = data_frame.drop(data_frame.columns[target_index], axis=1)
        self.y = data_frame.iloc[:, target_index]
        
        self.models: Dict[str, BaseEstimator] = {}
        self.results: Dict[str, Dict] = {}
        
        self.X_train: Optional[np.ndarray] = None
        self.X_test: Optional[np.ndarray] = None
        self.y_train: Optional[np.ndarray] = None
        self.y_test: Optional[np.ndarray] = None
        
        # Yellowbrick class labels mapping
        # Classes: 0: 'Não se aplica', 1: 'Baixo', 2: 'Médio', 3: 'Alto'
        self.class_labels: Dict[int, str] = {
            0: 'Não se aplica', 
            1: 'Baixa', 
            2: 'Média', 
            3: 'Alta'}

        print(f"Evaluator initialized. Total samples: {len(self.y)}")

    def add_model(self, model: BaseEstimator, name: str) -> None:
        self.models[name] = model
        print(f"'{name}' model added.")

    def split_data(
            self, test_size: float = 0.3, random_state: int = 0) -> None:
        
        if self.X is None or self.y is None:
            raise AttributeError(
                "X and Y data not defined during initialization.")

        X_train, X_test, y_train, y_test = train_test_split(
            self.X.values, self.y.values, 
            test_size=test_size, 
            random_state=random_state
        )
        
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        
        print(f"Data split (Holdout): Train={len(X_train)}, Test={len(X_test)}")


    def train_model(self, name: str) -> None:
        
        if self.X_train is None:
            raise AttributeError("Not data split. Call 'split_data' first.")
            
        if name not in self.models:
            raise ValueError(f"Model '{name}' not found.")

        print(f"\n--- Training Model: {name} ---")
        model = self.models[name]
        
        model.fit(self.X_train, self.y_train)

        # Prediction
        predictions = model.predict(self.X_test)

        # Metric Calculation
        accuracy = accuracy_score(self.y_test, predictions)

        # Storing results
        self.results[name] = {
            'model': model,
            'predictions': predictions,
            'accuracy': accuracy,
            'confusion_matrix': confusion_matrix(self.y_test, predictions)
        }

        print(f"Accuracy of {name}: {accuracy:.4f}")

    def train_all_models(self) -> None:
        for name in self.models.keys():
            self.train_model(name)

    def evaluate_model(self, name: str) -> None:
        
        if name not in self.results:
            raise ValueError(
                f"Model '{name}' not trained. Call 'train_model' first.")
            
        results = self.results[name]
        model = results['model']
        predictions = results['predictions']

        # 1. Classification Report
        print(f"\n--- Classification Report for {name} ---")
        target_names = list(self.class_labels.values())
        print(classification_report(
            self.y_test, predictions, target_names=target_names))

        # 2. Confusion Matrix (Yellowbrick)
        plt.figure(figsize=(10, 7))
        mc_plot = ConfusionMatrix(
            model,
            classes=target_names,
            encoder=self.class_labels,
            percent=False,
            title=f"Confusion Matrix - {name} (Accuracy: {results['accuracy']:.2f})"
        )
        
        mc_plot.fit(self.X_train, self.y_train)
        mc_plot.score(self.X_test, self.y_test)
        
        # Save the confusion matrix plot
        confusion_matrix_file: str = {
            'DecisionTree': 'dt', 'KNN': 'knn',
            'SVM': 'svm','RandomForest': 'rf',
            'NaiveBayes': 'nb'}
        output_dir = 'imagens_ml'
        os.makedirs(output_dir, exist_ok=True)
        mc_plot.show(
            outpath=os.path.join(
            output_dir,
            f'matriz_confusao_{confusion_matrix_file[name]}_cri.png'))
        plt.close()

    def compare_models(
            self, metric: str = 'accuracy') -> Tuple[str, BaseEstimator]:
    
        if not self.results:
            raise ValueError("No models trained for comparison.")
            
        best_name = max(self.results,
                        key=lambda k: self.results[k].get(metric, -1))
        best_model = self.results[best_name]['model']
        best_score = self.results[best_name][metric]
        
        print("\n--- Model Comparison Results ---")
        for name, res in self.results.items():
            print(f"- {name}: {res[metric]:.4f}")

        print(f"\nThe best model is: {best_name} with {metric} of {best_score:.4f}")
        return best_name, best_model

    def save_best_model(
            self, output_path: str = 'classificador_ml_cri.pkl') -> None:

        if not self.results:
            raise ValueError("No models trained for serialization.")
            
        try:
            best_name, best_model = self.compare_models(metric='accuracy')
            
            with open(output_path, 'wb') as file:
                pickle.dump(best_model, file)

            print(f"\nThe best model ({best_name}) was saved via pickle "
                  f"at: {output_path}")

        except Exception as e:
            print(f"Error saving the model with pickle: {e}")


if __name__ == "__main__":
    from pre_processamento_cri import PipelineCRI
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.svm import SVC
    
    data_cri = PipelineCRI('data/barragens.csv')
    evaluator_cri = CRIModelEvaluator(
        data_cri.run_full_cri_pipeline('data/barragens.csv'), target_index=0)
    
    evaluator_cri.split_data(test_size=0.3, random_state=0)
    
    # Example usage with models (assuming models are defined elsewhere)
    evaluator_cri.add_model(DecisionTreeClassifier(), 'DecisionTree')
    evaluator_cri.add_model(RandomForestClassifier(), 'RandomForest')
    evaluator_cri.add_model(KNeighborsClassifier(), 'KNN')
    evaluator_cri.add_model(GaussianNB(), 'NaiveBayes')
    evaluator_cri.add_model(SVC(), 'SVM')

    evaluator_cri.train_all_models()
    for model_name in evaluator_cri.models.keys():
        evaluator_cri.evaluate_model(model_name)
    
    #evaluator_cri.save_best_model()