from sklearn.preprocessing import StandardScaler


class Scaler():
    non_scaled = ["weekday_is_monday", "weekday_is_tuesday", "weekday_is_wednesday", "weekday_is_thursday", "weekday_is_friday", "weekday_is_saturday", "weekday_is_sunday", "is_weekend", 'shares']

    def __init__(self, df):
        print(df.columns)
        df = df.drop('shares', axis=1)
        self.scaler = StandardScaler()
        self.feature_cols = [col for col in df.columns if col not in self.non_scaled]

        self.scaler.fit(df[self.feature_cols])
    
    def transform(self, df):
        df[self.feature_cols] = self.scaler.transform(df[self.feature_cols])

        return df
