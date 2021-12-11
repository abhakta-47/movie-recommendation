import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import pickle
import requests

api_key = "00112194220384db1f4e36062ac14246"


def pickle_read(fileName):
    with open(fileName, 'rb') as file_opened:
        return pickle.load(file=file_opened)


def pickle_write(fileName, obj):
    with open(fileName, 'wb') as file_opened:
        pickle.dump(obj=obj, file=file_opened)


class Model:
    def __init__(self) -> None:
        self.movies_df = pickle_read('./processed/obj/movies_df.pk')
        self.indices = pickle_read('./processed/obj/indices.pk')
        self.tf = pickle_read('./processed/obj/tf.pk')
        self.description_matrix = pickle_read(
            './processed/obj/description_matrix.pk')
        # self.cosine_sim = pickle_read('./processed/obj/cosine_sim.pk')
        self.human_friendly_cols = ['id', 'title', 'overview', 'tagline']

    def get_recommendations(self, title, cosine_sim, new_data=False):
        idx = 0 if new_data else self.indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:31]
        movie_indices = [i[0] for i in sim_scores]
        return self.movies_df.iloc[movie_indices]['id'].tolist()
        # return self.movies_df.iloc[movie_indices][self.human_friendly_cols]

    # def get_recommendations(self, title, cosine_sim, new_data=False):
    #     idx = 0 if new_data else self.indices[title]
    #     sim_scores = list(enumerate(cosine_sim[idx]))
    #     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #     sim_scores = sim_scores[1:31]
    #     movie_indices = [i[0] for i in sim_scores]
    #     return self.movies_df.iloc[movie_indices][self.human_friendly_cols]

    def new_data(self, new_id):
        url = 'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'.format(
            movie_id=new_id, api_key=api_key)
        try:
            res = requests.get(url)
        except:
            raise ('not connected to internet or movidb issue')

        if res.status_code != 200:
            return {'status': 500, 'err': 'movie not found'}

        res = res.json()
        title = res['title']
        tagline = res['tagline']
        overview = res['overview']

        sub_df = pd.DataFrame([[title, tagline, overview]], columns=[
                              'title', 'tagline', 'overview'])
        sub_df['description'] = sub_df['tagline'] + sub_df['overview']
        sub_des_matrix = self.tf.transform(sub_df['description'])
        sub_cosine_sim = linear_kernel(sub_des_matrix, self.description_matrix)
        data = self.get_recommendations('Avengers: Age of Ultron',
                                        cosine_sim=sub_cosine_sim,
                                        new_data=True)
        return {'status': 200, 'data': data}


if __name__ == '__main__':
    model = Model()
    print(model.new_data(580489))
