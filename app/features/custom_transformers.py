import numpy as np
import pandas as pd
import h3
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA

# -------------------------
# ColumnSelector
# -------------------------
class ColumnSelector(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cols_to_keep = [col for col in numeric_cols if col not in ['id', 'trip_duration']]
        return X[cols_to_keep].copy()

# -------------------------
# Feature Engineer
# -------------------------
class EnhancedNYCFeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self, n_clusters=30, random_state=42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans = None
        self.pca = None
    
    def fit(self, X, y=None):
        coords = np.vstack((
            X[['pickup_latitude', 'pickup_longitude']].values,
            X[['dropoff_latitude', 'dropoff_longitude']].values
        ))

        self.kmeans = MiniBatchKMeans(
            n_clusters=self.n_clusters,
            batch_size=10000,
            random_state=self.random_state,
            n_init=20
        ).fit(coords)

        self.pca = PCA(n_components=2, random_state=self.random_state)
        self.pca.fit(coords)

        return self
    
    def transform(self, X):
        X = X.copy()

        X['pickup_datetime'] = pd.to_datetime(X['pickup_datetime'])
        X['pickup_hour'] = X['pickup_datetime'].dt.hour
        X['pickup_minute'] = X['pickup_datetime'].dt.minute
        X['pickup_day'] = X['pickup_datetime'].dt.dayofweek
        X['pickup_month'] = X['pickup_datetime'].dt.month
        X['is_weekend'] = X['pickup_day'].isin([5, 6]).astype(int)

        X["distance"] = X.apply(lambda row: h3.great_circle_distance(
            (row["pickup_latitude"], row["pickup_longitude"]),
            (row["dropoff_latitude"], row["dropoff_longitude"]), unit="km"), axis=1)

        X['manhattan_distance'] = (
            abs(X['pickup_latitude'] - X['dropoff_latitude']) +
            abs(X['pickup_longitude'] - X['dropoff_longitude'])
        )

        X['pickup_cluster'] = self.kmeans.predict(
            X[['pickup_latitude', 'pickup_longitude']].values
        )
        X['dropoff_cluster'] = self.kmeans.predict(
            X[['dropoff_latitude', 'dropoff_longitude']].values
        )

        coords_p = X[['pickup_latitude', 'pickup_longitude']].values
        coords_d = X[['dropoff_latitude', 'dropoff_longitude']].values

        X[['pca_pickup1', 'pca_pickup2']] = self.pca.transform(coords_p)
        X[['pca_dropoff1', 'pca_dropoff2']] = self.pca.transform(coords_d)

        X.drop(['pickup_datetime','pickup_latitude','pickup_longitude',
                'dropoff_latitude','dropoff_longitude','id'], axis=1, errors='ignore', inplace=True)

        return X

# -------------------------
# LogTransformer
# -------------------------
class LogTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        for col in ['distance', 'manhattan_distance', 'passenger_count']:
            if col in X.columns:
                X[col] = np.log1p(X[col].clip(lower=0))
        return X