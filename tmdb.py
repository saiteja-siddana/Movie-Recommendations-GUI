import requests,json,re

tmdb = '2f9a8302c5eac8e31c367cc077e9c854'

print('Enter name of a movie: ')
title = input("> ")
name = title[:-6]
year = title[-5:-1:]

result = re.sub(r'\([^)]*\)', '', name) ## Removing any paranthesis 

head,sep,tail = result.partition(',') 

## Removing article 'the' after ',' if any
## head is the name of a movie

url3 = 'http://api.themoviedb.org/3/search/movie?api_key=' + tmdb + '&query=' + head + '&year=' + year

request = requests.get(url3)
data = request.json()

print(head+tail)
print(year)
print("----------------------------------")

if data['results']:
    if data['results'][0]['poster_path']!='None':
        image = 'https://image.tmdb.org/t/p/original' + str(data['results'][0]['poster_path'])
        print(image)
