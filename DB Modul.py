import sqlite3

# Підключення до бази даних
conn = sqlite3.connect('football_db.sqlite3')
cursor = conn.cursor()

# Створення таблиць
def create_team_table(team_name):
    query = f'''
    CREATE TABLE IF NOT EXISTS {team_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        player_name TEXT,
        age INTEGER,
        goals INTEGER
    );
    '''
    cursor.execute(query)
    conn.commit()

def create_tournament_table():
    query = '''
    CREATE TABLE IF NOT EXISTS tournaments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER,
        team_name TEXT,
        position INTEGER,
        points INTEGER
    );
    '''
    cursor.execute(query)
    conn.commit()

# Заповнення даних в таблицях
def populate_team_data(team_name, players_data):
    for player_data in players_data:
        cursor.execute(f"INSERT INTO {team_name} (player_name, age, goals) VALUES (?, ?, ?);", player_data)
    conn.commit()

def populate_tournament_data(tournament_data):
    for data in tournament_data:
        cursor.execute("INSERT INTO tournaments (team_id, team_name, position, points) VALUES (?, ?, ?, ?);", data)
    conn.commit()

# Зміна очок команди
def update_team_points(team_name, new_points):
    cursor.execute("UPDATE tournaments SET points = ? WHERE team_name = ?;", (new_points, team_name))
    conn.commit()

# Зміна позиції команди
def update_team_position(team_name, new_position):
    cursor.execute("UPDATE tournaments SET position = ? WHERE team_name = ?;", (new_position, team_name))
    conn.commit()

# Виведення меню
def print_menu():
    print("1. Змінити очки команди")
    print("2. Змінити позицію команди")
    print("3. Вийти")

# Приклад використання
teams = {
    'Arsenal': [('Player1', 25, 10), ('Player2', 22, 8), ('Player3', 28, 12), ('Player4', 24, 9), ('Player5', 27, 11)],
    'ManCity': [('Player6', 26, 11), ('Player7', 24, 9), ('Player8', 27, 13), ('Player9', 23, 8), ('Player10', 28, 10)],
    'MU': [('Player11', 23, 9), ('Player12', 26, 14), ('Player13', 24, 7), ('Player14', 27, 12), ('Player15', 22, 11)],
    'Chelsea': [('Player16', 28, 10), ('Player17', 25, 13), ('Player18', 23, 8), ('Player19', 26, 12), ('Player20', 24, 9)]
}

for team, players_data in teams.items():
    create_team_table(team)
    populate_team_data(team, players_data)

create_tournament_table()

tournament_data = [(1, 'Arsenal', 1, 3),
                   (2, 'ManCity', 2, 6),
                   (3, 'MU', 3, 1),
                   (4, 'Chelsea', 4, 0)]

# Сортування таблиці турнірів за очками
sorted_tournament_data = sorted(tournament_data, key=lambda x: x[3], reverse=True)
populate_tournament_data(sorted_tournament_data)

while True:
    print("\n-------- МЕНЮ ДОСТУПУ --------")
    print_menu()
    choice = input("Виберіть опцію (1-3): ")

    if choice == '1':
        team_name = input("Введіть назву команди для зміни очок: ")
        new_points = int(input("Введіть нову кількість очок: "))
        update_team_points(team_name, new_points)
        print(f"Очки команди {team_name} змінені на {new_points}.")
    elif choice == '2':
        team_name = input("Введіть назву команди для зміни позиції: ")
        new_position = int(input("Введіть нову позицію: "))
        update_team_position(team_name, new_position)
        print(f"Позиція команди {team_name} змінена на {new_position}.")
    elif choice == '3':
        print("Дякую за використання меню. Програма завершена.")
        break
    else:
        print("Невірний вибір. Спробуйте ще раз.")

# Закриття підключення до бази даних
conn.close()