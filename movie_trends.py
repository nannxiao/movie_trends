import requests
from bokeh.charts import Line, output_file, show
from bokeh.palettes import brewer
import pandas as pd
apikeys = open('apikeys.py')
from apikeys import TMDB_KEY

# 1. Genre Trends Part
# Create a function for determining the number of releases for a single genre for a single month
def release_num(genre_id, month_id):
    '''This function takes two parameters: genre_id (int value), month_id (int value)
    then requests the movie list of the wanted genre id and month id, and reads the json file,
    and takes the 'total_results' of releases in that specific month in the year of 2016, 
    and returns this number'''
    if month_id in [1,3,5,7,8,10,12]:
        response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key='+TMDB_KEY+'&sort_by=popularity.desc&primary_release_date.gte=2016-'+str(month_id)+'-01&primary_release_date.lte=2016-'+str(month_id)+'-31&with_genres='+str(genre_id))
    elif month_id in [4,6,9,11]:
        response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key='+TMDB_KEY+'&sort_by=popularity.desc&primary_release_date.gte=2016-'+str(month_id)+'-01&primary_release_date.lte=2016-'+str(month_id)+'-30&with_genres='+str(genre_id))
    else:
        response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key='+TMDB_KEY+'&sort_by=popularity.desc&primary_release_date.gte=2016-'+str(month_id)+'-01&primary_release_date.lte=2016-'+str(month_id)+'-29&with_genres='+str(genre_id))
    movies = response.json()
    release_num = movies['total_results']
    return release_num

# Create another function that calls the first for each month and genre, compiling and returning the results
def compile_result(genre_id_list):
    '''This function takes one parameter: a list of genre ids, 
    then it creates an empty dictionary, and calls the first function 12 times for each genre id 
    in this list, to get the number of releases of this genre in each month in 2016
    finally it returns this dictionary for visualization use'''
    res = {}
    for genre_id in genre_id_list:
        # provide the user feedback by printing out a sentence for each genre-month processed
        for item in genres:
            if item['id'] == genre_id:
                namehah = item['name']
                print('Requesting data for genre:', namehah, '...')
        res[genre_id] = []
        for i in range(1, 13):
            res[genre_id].append(release_num(genre_id, i))
    return res

# Generate the line chart visualization from these results
def line_chart(results):
    '''This functoin takes one parameter: a dictionary, which is returned by the second function,
    then it creates a pandas DataFrame, which uses the genre names as column names, 
    and uses the 12 months as row indexes, and uses the lists of releases numbers of 
    each genre as dataframe values. Then we use this DataFrame to generate a line chart
    using Bokeh Line()'''
    x_values = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    y_values = {}
    colors = brewer['Dark2'][5]
    for item in results:
        for genre in genres:
            if genre['id'] == item:
                y_values[genre['name']] = results[item]
    
    # convert results to pandas DataFrame
    xyvalues = pd.DataFrame(y_values, index = x_values)
    
    # include appropriate color palettes, labels, title, and tick marks
    line = Line(xyvalues, title= 'Releases by Genre: 2016', legend = 'top_right', xlabel = 'Month', ylabel = 'Releases', color = colors)
    output_file('genre_by_season.html')
    show(line)

if __name__ == "__main__":
    # prompt the user for which of the two analyses to run
    analyze_type = input('Which of the two analyses do you want to run? (1 / 2)')

    if analyze_type == '1':
        # Genre by Season analysis:
        # Download the ids of each genre from the API, and store them in a list of dictionaries
        response = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key='+TMDB_KEY+'&language=en-US')
        genres = response.json()
        genres = genres['genres']

        # Save the genre names in a single variable that can be passed into a download function
        genre_list = []
        for item in genres:
            genre_list.append(item['name'])

        # create empty lists that store wanted genre ids and names
        genre_name_list = []
        genre_id_list = []
    
        # prompt the user for a list of genres to consider, and let user choose 5 genres to analyze
        print('\n1-Action, 2-Adventure, 3-Animation, 4-Comedy, 5-Crime, 6-Documentary, 7-Drama, 8-Family, 9-Fantasy, 10-History, 11-Horror, 12-Music, 13-Mystery, 14-Romance, 15-Science Fiction, 16-TV Movie, 17-Thriller, 18-War, 19-Western\n')
        for i in range(1, 6):
            genre_no = input('Enter the '+str(i)+'/5 genre number you want to analyze:\n')
            genre_name_list.append(genre_list[int(genre_no) - 1])
    
        for genre_name in genre_name_list:
            for item in genres:
                if item['name'] == genre_name:
                    genre_id_list.append(item['id'])

        results = compile_result(genre_id_list)
        line_chart(results)