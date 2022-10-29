# https://blogboard.io/blog/knowledge/python-sorted-lambda/

def bubble_sort(array: list, key):
    new_array = [e for e in array] # Create a copy of array to work on

    print('xxx', new_array, key(new_array[0]))
    while True:
        swapped = False
        for i in range(0, len(new_array) - 1):
            if key(new_array[i+1]) < key(new_array[i]):
                new_array[i],new_array[i+1] = new_array[i+1],new_array[i] 
                swapped = True

        if not swapped:
            break
    return new_array

movies = [
        (1994, 'The Shawshank Redemption', 9.2),
        (1999, 'Fight Club', 8.8),
        (1994, 'Pulp Fiction', 8.9),
        (1972, 'The Godfather', 9.2),
        (2008, 'The Dark Knight', 9.0)
]

movies = bubble_sort(movies, key=lambda movie: -movie[2])

for movie in movies:
    print(movie)
