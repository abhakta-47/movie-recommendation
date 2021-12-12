import numpy as np
from numpy.core.fromnumeric import shape
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import pickle
import requests

api_key = "00112194220384db1f4e36062ac14246"
human_friendly_cols = ['id', 'title', 'overview', 'tagline']


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
        # self.human_friendly_cols = ['id', 'title', 'overview', 'tagline']

    def get_recommendations(self, title, cosine_sim, new_data=False):
        idx = 0 if new_data else self.indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
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


class Model_content_v2:
    def __init__(self) -> None:
        self.movies_df = pickle_read('./processed/obj_v2/movies_df.pk')
        self.indices = pickle_read('./processed/obj_v2/indices.pk')
        self.count_vector = pickle_read('./processed/obj_v2/count_vector.pk')
        self.count_matrix = pickle_read('./processed/obj_v2/count_matrix.pk')

    def get_recommendations(self, title, cosine_sim, new_data=False):
        idx = 0 if new_data else self.indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        movie_indices = [i[0] for i in sim_scores]
        return self.movies_df.iloc[movie_indices]['id'].tolist()

    def genre2sentence(self, item):
        if isinstance(item, list):
            genres = []
            for genre in item:
                genres.append('genre_' + str(genre))
            return str(genres)
        return []

    def get_director(self, x):
        for i in x:
            if i['department'] == 'Directing':
                return i['name']
        return np.nan

    def get_list(self, x):
        if isinstance(x, list):
            if len(x) == 0:
                return []
            names = [i['name'] for i in x]
            # Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
            if len(names) > 3:
                names = names[:3]
            return names

        # Return empty list in case of missing/malformed data
        return []

    def get_genre_list(self, x):
        if isinstance(x, list):
            if len(x) == 0:
                return []
            names = [('genre_'+str(i['id'])) for i in x]
            # Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
            if len(names) > 3:
                names = names[:3]
            return names

        # Return empty list in case of missing/malformed data
        return []

    def clean_data(self, x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        else:
            # Check if director exists. If not, return empty string
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''

    def get_credit(self, id):
        url = 'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}'.format(
            api_key=api_key, movie_id=id)
        try:
            res = requests.get(url)
        except:
            raise ('not connected to internet or movidb issue')

        if res.status_code != 200:
            print('error')
            return []

        res = res.json()

        if 'errors' in res.keys():
            print('api error !!!')
            return {}

        new_movie_credit = {'cast': [], 'crew': []}
        for credit in res['cast']:
            new_movie_credit['cast'].append({
                'cast_id': credit['id'],
                'name': credit['name'],
                'character': credit['character'],
            })
        for crew in res['crew']:
            new_movie_credit['crew'].append({
                'crew_id': crew['id'],
                'name': crew['name'],
                'department': crew['department'],
            })
        return new_movie_credit

    def get_keyword(self, id):
        url = 'https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={api_key}'.format(
            api_key=api_key, movie_id=id)
        try:
            res = requests.get(url)
        except:
            raise ('not connected to internet or movidb issue')

        if res.status_code != 200:
            print('error')
            return []

        res = res.json()

        if 'errors' in res.keys():
            return {}
        # print(res)
        return res['keywords']

    def get_movie(self, id):
        url = 'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'.format(
            movie_id=id, api_key=api_key)
        try:
            res = requests.get(url)
        except:
            raise ('not connected to internet or movidb issue')

        if res.status_code != 200:
            return {'status': 500, 'err': 'movie not found'}

        res = res.json()
        return res['genres']

    def create_soup(self, x):
        return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

    def new_movie(self, id):
        genres = self.get_movie(id)
        key_word = self.get_keyword(id)
        credit = self.get_credit(id)

        new_df = pd.DataFrame([[genres, key_word, credit['cast'], credit['crew']]], columns=[
            'genres', 'keywords', 'cast', 'crew'])

        new_df['director'] = new_df['crew'].apply(self.get_director)

        features = ['cast', 'keywords', ]
        for feature in features:
            new_df[feature] = new_df[feature].apply(self.get_list)
            # print(feature, end=' ')
        new_df['genres'] = new_df['genres'].apply(self.get_genre_list)

        features = ['cast', 'keywords', 'director', 'genres']

        for feature in features:
            # print(feature, end=" ")
            new_df[feature] = new_df[feature].apply(self.clean_data)

        new_df['soup'] = new_df.apply(self.create_soup, axis=1)

        new_count_matrix = self.count_vector.transform(new_df['soup'])
        # print(self.count_matrix.shape, new_count_matrix.shape)
        sub_cosine_sim = cosine_similarity(new_count_matrix, self.count_matrix)
        data = self.get_recommendations('Avengers: Age of Ultron',
                                        cosine_sim=sub_cosine_sim,
                                        new_data=True)
        return {'status': 200, 'data': data}


if __name__ == '__main__':
    # model = Model()
    # print(model.new_data(580489))
    model_content_v2 = Model_content_v2()
    print(model_content_v2.new_movie(580489))
