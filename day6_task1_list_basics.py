movies = ['Матрица', 'Начало', 'Интерстеллар', 'Дюна', 'Оппенгеймер']

print(f"Все фильмы: {movies}")
print(f"Первый: {movies[0]}")
print(f"Последний: {movies[-1]}")
print(f"Всего: {len(movies)}")

for movie in movies:
    print(f"- {movie}")
