import discord
import datetime
import sqlite3
from werkzeug.security import generate_password_hash

TOKEN = "use_your_token"
LINK = '*not available*'
con = sqlite3.connect('db/library.sqlite')
CUR = con.cursor()


class BotLibrarian(discord.Client):
    async def on_ready(self):
        print('Bot-Librarian connected to Discord and ready to work!')

    def help_bot(self):
        """
        Current function must respond to the command "$bot_help" and return the 'help text'
        """
        text = 'Commands:\n' \
               '"$link" - Link to our website\n' \
               '"$register [email] [password] [about]" - register your account on the site\n\n' \
               'If you are not registered on our website, you will not be able to use the commands below\n' \
               '"$new_book [Title] [Author] [Mark] [Content]" - Make a new book and add it to the library\n' \
               'For example: $new_book Greenlights McConaughey 4 ...\n' \
               '"$find_book [Title]" - Find the book by the title\n' \
               '"$edit_book Old_Title Title, author, mark, content" - After finding a book by Old_Title, ' \
               'you replace Title, author, mark and content of a book\n' \
               '"$find_similar Title" - Find books with the similar titles'
        return text

    def send_link(self):
        """
        Current function must respond to the command "$link" and return the link of Library website
        """
        text = f'Link to our website - {LINK}\n'
        return text

    def register(self, email, password, nickname, about=''):
        if '@' not in email and '.' not in email:
            return 'Field "email" filled in incorrectly'
        about = ' '.join(about)
        hashed_password = generate_password_hash(password)
        created_date = datetime.datetime.now()
        status = 'DONE! If you want edit your library account, contact to ClayMix#0467'
        request = f"""INSERT INTO users (name, about, email, hashed_password, created_date) 
        VALUES ('{nickname}', '{about}', '{email}', '{hashed_password}', '{created_date}')"""
        result = CUR.execute(f"""SELECT ALL FROM users
                                WHERE name IN ('{nickname}')""").fetchall()
        if result:
            status = 'This user is already exists'

        else:
            result = CUR.execute(request).fetchall()
            con.commit()
            con.close()

        return status

    def new_book(self, nickname, title, author, mark, content=''):
        content = ' '.join(content)
        user_id = CUR.execute(f"""SELECT id FROM users
                                    Where name IN ('{nickname}')""")
        user_id = user_id[0][0]
        created_date = datetime.datetime.now()
        status = 'DONE!'
        request = f"""INSERT INTO books (title, author, mark, content, created_date, is_private)
                  VALUES ('{title}', '{author}', '{mark}', '{content}', '{created_date}', 0,
                      '{user_id}')"""
        result = CUR.execute(f"""SELECT title, author FROM books
                                WHERE title IN ('{title}') AND author IN ('{author}')""").fetchall()

        if result:
            status = 'This book is already exists!'

        else:
            result = CUR.execute(request).fetchall()
            con.commit()
            con.close()

        return status

    def find_book(self, title):
        text = ''
        result = CUR.execute(f"""SELECT title, author, mark FROM books
                                WHERE '{title}' IN title""").fetchall()

        if result:
            book = result[0]
            text += f'Название - {book[0]}\nАвтор - {book[1]}\n Оценка на сайте - {book[2]}'

        else:
            text = 'Search for book failed. But you can create a new book!'

        return text

    def find_similar(self, title):
        text = ''
        result = CUR.execute(f"""SELECT title, author, mark FROM books
                                        WHERE title LIKE '%{title}%'""").fetchall()

        if result:
            for i in result:
                text += f'Название - {i[0]}\nАвтор - {i[1]}\n Оценка на сайте - {i[2]}\n\n'

        else:
            text = 'Search for books failed. But you can create a new book!'

        return text

    def change_link(self, link):
        LINK = link

    async def on_message(self, message):
        if message.author == self.user:
            return

        elif '$' in message.content.lower() and message.content.lower()[0] == '$':
            mcl = message.content.lower()
            if '$link' in mcl:
                await message.channel.send(self.send_link())

            elif '$register' in mcl:
                line = mcl.split()
                line.pop(0)
                nickname = message.author
                nickname = nickname.split('#')[0]
                email = line[0]
                password = line[1]
                line.pop(0)
                line.pop(0)

                await message.channel.send(self.register(email, password, nickname, line))

            elif '$bot_help' in mcl:
                await message.channel.send(self.help_bot())

            else:
                nickname = message.author
                nickname = nickname.split('#')[0]
                result = CUR.execute(f"""SELECT id FROM users
                                        WHERE name IN ('{nickname}')""").fetchall()

                if not result:
                    await message.channel.send('Register the account before using the library!')

                else:
                    line = mcl.split()

                    if '$new_book' in mcl:
                        line.pop(0)
                        title = line[0]
                        author = line[1]
                        mark = line[2]
                        line.pop(0)
                        line.pop(0)
                        line.pop(0)

                        await message.channel.send(self.new_book(nickname, title, author, mark, line))

                    elif '$find_book' in mcl:
                        line.pop(0)
                        title = line[0]

                        await message.channel.send(self.find_book(title))

                    elif '$find_similar' in mcl:
                        line.pop(0)
                        title = line[0]

                        await message.channel.send(self.find_similar(title))

                    elif message.author == 'ClayMix#0467':
                        if '$change_link' in mcl:
                            link = line[1]

                            await self.change_link(link)


def main():
    client = BotLibrarian()
    client.run(TOKEN)


if __name__ == "__main__":
    main()
