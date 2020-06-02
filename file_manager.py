import pandas as pd

class FileManager:
    def __init__(self, filename):
        self.__df = pd.read_csv(filename)
        self.__df["Date"] = pd.to_datetime(self.__df["Date"])

    def countries(self):
        countries = self.__df['Country/Region'].unique()
        return [{'label': country, 'value': country} for country in countries]

    def get_covid_df(self):
        return self.__df

    def get_last_information(self):
        covid_by_date = self.__df.groupby([self.__df["Date"], self.__df["Country/Region"]]).sum()
        covid_by_date.reset_index(level=['Country/Region'], inplace=True)
        return covid_by_date[covid_by_date.index == covid_by_date.index[-1]]