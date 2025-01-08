import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import joblib

class Modelos:
    def __init__(self):
        self.model = None
        self.vectorizer = None

    def entrenar_gradient_boosted(self, df, nombre_modelo):
        limpiar_columnas = ['Calorias', 'Grasas', 'Proteínas', 'Carbohidratos']
        for column in limpiar_columnas:
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)

        self.vectorizer = TfidfVectorizer(max_features=1000)
        text_features = self.vectorizer.fit_transform(df['Subcategoria'].astype(str)).toarray()
        numerical_features = df[limpiar_columnas]
        X = pd.concat([numerical_features.reset_index(drop=True), pd.DataFrame(text_features)], axis=1)
        X.columns = X.columns.astype(str)
        y = df['Categoria']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        self.model.fit(X_train, y_train)

        model_and_vectorizer = {'model': self.model, 'vectorizer': self.vectorizer}
        joblib.dump(model_and_vectorizer, nombre_modelo + '.pkl')

        y_pred = self.model.predict(X_test)
        return accuracy_score(y_test, y_pred)

    def entrenar_k_nn(self, df, nombre_modelo):
        columns_to_clean = ['Calorias', 'Grasas', 'Proteínas', 'Carbohidratos']
        for column in columns_to_clean:
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)

        self.vectorizer = TfidfVectorizer(max_features=1000)
        text_features = self.vectorizer.fit_transform(df['Subcategoria'].astype(str)).toarray()
        numerical_features = df[columns_to_clean]
        X = pd.concat([numerical_features.reset_index(drop=True), pd.DataFrame(text_features)], axis=1)
        X.columns = X.columns.astype(str)
        y = df['Categoria']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = KNeighborsClassifier(n_neighbors=5, weights='distance', algorithm='auto', metric='minkowski', p=2)
        self.model.fit(X_train, y_train)

        model_and_vectorizer = {'model': self.model, 'vectorizer': self.vectorizer}
        joblib.dump(model_and_vectorizer, nombre_modelo + '.pkl')

        y_pred = self.model.predict(X_test)
        return accuracy_score(y_test, y_pred)

    def entrenar_naive_bayes(self, df, nombre_modelo):
        columns_to_clean = ['Calorias', 'Grasas', 'Proteínas', 'Carbohidratos']
        for column in columns_to_clean:
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)

        self.vectorizer = TfidfVectorizer(max_features=1000)
        text_features = self.vectorizer.fit_transform(df['Subcategoria'].astype(str)).toarray()
        numerical_features = df[columns_to_clean]
        X = pd.concat([numerical_features.reset_index(drop=True), pd.DataFrame(text_features)], axis=1)
        X.columns = X.columns.astype(str)
        y = df['Categoria']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = MultinomialNB()
        self.model.fit(X_train, y_train)

        model_and_vectorizer = {'model': self.model, 'vectorizer': self.vectorizer}
        joblib.dump(model_and_vectorizer, nombre_modelo + '.pkl')

        y_pred = self.model.predict(X_test)
        return accuracy_score(y_test, y_pred)

    def predecir(self, ruta_modelo, ruta_csv):
        model_and_vectorizer = joblib.load(ruta_modelo)
        self.model = model_and_vectorizer['model']
        self.vectorizer = model_and_vectorizer['vectorizer']

        df_nuevos = pd.read_csv(ruta_csv)
        columns_to_clean = ['Calorias', 'Grasas', 'Proteínas', 'Carbohidratos']
        for column in columns_to_clean:
            df_nuevos[column] = pd.to_numeric(df_nuevos[column].str.replace(r'[^\d.]+', '', regex=True),
                                              errors='coerce').fillna(0)

        text_features_nuevos = self.vectorizer.transform(df_nuevos['Subcategoria'].astype(str)).toarray()
        numerical_features_nuevos = df_nuevos[columns_to_clean]
        X_nuevos = pd.concat([numerical_features_nuevos.reset_index(drop=True), pd.DataFrame(text_features_nuevos)],
                             axis=1)
        X_nuevos.columns = X_nuevos.columns.astype(str)

        y_pred_nuevos = self.model.predict(X_nuevos)
        df_nuevos['Categoria_Predicha'] = y_pred_nuevos
        return df_nuevos[['Nombre', 'Categoria_Predicha']]