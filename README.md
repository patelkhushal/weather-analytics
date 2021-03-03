# Weather Analytics

## Problem


There are two csv files. `climate.csv` has climate information for a few weeks in early 2020 collected at weather stations around Canada. The second file `cities.csv` has demographic information about Canadian cities and includes the majority of Canada's urban population.

Your task is to provide a method that reads both files, accepts a date, and computes the mean and median daytime temperatures for urban Canadians on that day. A correct solution will incorporate attributes from both files such as temperature, location, population, etc. while carefully handling any data issues

Please track any assumptions or trade-offs that you make during the exercise and justify the decisions you made. Also, while it's not important for your solution to implement scaling to larger datasets, if time permits, please include a discussion about how that would change your approach (if at all).

## Solution

### How code works

First, I am getting all the city coordinates from cities.csv file and storing in a dictionary (city_to_coordinates) with city name as key and coordinates as value. Then, I am doing the same for stations (station_to_coordinates). After both dictionaries are populated, I compare distance between each station to all cities and associate station to closest city using "cities_to_stations" dictionary which has city name as the key and array of stations as a value.

Then we call in calculate_weather function that takes in a date passed to the program and passes an additional parameter cities_to_stations. The function will then calculate mean and median temperatures for each cities by looking into all the weather station associated to the city. calculate_weather function will print the city name and mean and median for that city on the stdout
<br>

### Assumption

I am trying to find which weather station belongs to which cities by computing the distance between the weather station coordinates and city coordinates. The city that is closest to a weather station is where that weather station is associated to

Problem with this assumption is, if weather station is located at the far end of the city (city A) and the neighbouring city (city B) happens to be close to that weather station than city A, then we classify the current weather station under city B. This is due to the fact that we're only given latitude and longitude of the weather station and not which city it belongs to. I found this out by testing my code and checked if the weather station province from climate.csv matches with the associated city's province in cities.csv
<br>

### Scaling

We can scale the solution by using no sql database like mongo or redis to save in the computed dictionaries (city_to_coordinates and cities_to_stations) so that repeated analytics on these data sets will take less time to compute the same information again.

If the data set increase in size then we can consider using distributed storage system like Hadoop file system (HDFS) to split the data into different nodes and running analytics on each node
