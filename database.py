import sqlite3

conn = sqlite3.connect("games.db")

# Create a cursor
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE games (
                game_name text,
                game_console text,
                game_publisher text,
                year_released integer
                )''')

conn.commit()

conn.close()