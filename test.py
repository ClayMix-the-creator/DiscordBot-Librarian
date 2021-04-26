import sqlite3

con = sqlite3.connect('db/library.sqlite')
cur = con.cursor()

result = cur.execute("""SELECT id FROM books
                        WHERE title LIKE '%1%'""").fetchall()

con.close()

print(result, len(result))

for elem in result:
    print(elem[0])