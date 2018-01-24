import pandas as pd


class MovieLens:

    def get_data(self):
        uname = ['user_id', 'gender', 'age', 'occupation', 'postcode']
        users = pd.read_table('resource/movielens/users.dat', sep='::', header=None, names=uname)
        rname = ['user_id', 'movie_id', 'rating', 'timestamp']
        ratings = pd.read_table('resource/movielens/ratings.dat', sep='::', header=None, names=rname)
        mname = ['movie_id', 'title', 'category']
        movies = pd.read_table('resource/movielens/movies.dat', sep='::', header=None, names=mname)
        data = pd.merge(pd.merge(ratings, users), movies)
        return data

    def get_average_rating_by_condition(self, condition):
        data = self.get_data()
        mean_ratings = pd.pivot_table(data, 'rating', 'title', condition)
        return mean_ratings

    def filter_rating_number_by_title(self, size=0):
        data = self.get_data()
        rating_by_field = data.groupby('title').size()
        filtered_group = rating_by_field.index[rating_by_field >= size]
        return filtered_group

    def get_top_rated_movies_by_gender(self, gender='F'):
        popular_movies = self.filter_rating_number_by_title(300)
        rating_by_gender = self.get_average_rating_by_condition('gender')
        rating_by_gender = rating_by_gender.ix[popular_movies]
        top_rated_movies = rating_by_gender.sort_index(by=gender, ascending=False)
        return top_rated_movies

    def get_ratings_diff(self):
        rating_by_gender = self.get_average_rating_by_condition('gender')
        rating_by_gender['diff'] = rating_by_gender['F'] - rating_by_gender['M']
        sorted_rating = rating_by_gender.sort_index(by='diff')
        return sorted_rating

    def get_std_rating_by_title(self):
        movie_list = self.filter_rating_number_by_title(200)
        rating_std_by_title = self.get_data().groupby('title')['rating'].std()
        rating_std_by_title = rating_std_by_title.ix[movie_list]
        return rating_std_by_title.order(ascending=False)


if __name__ == '__main__':
    m = MovieLens()
    # print m.get_top_rated_movies_by_gender('M')[:5]
    print m.get_std_rating_by_title()[:5]
