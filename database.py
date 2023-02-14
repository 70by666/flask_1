import datetime
import psycopg2


class PgDataBase:
    def __init__(self, db):
        self._db = db
        self._cursor = db.cursor()
    
    def ver(self):
        self._cursor.execute(
            "SELECT version()"
        )

        return self._cursor.fetchone()
    
    # profile
    def add_user(self, name, email, password):
        try:
            self._cursor.execute(f"SELECT COUNT(*) FROM users WHERE email LIKE '{email}'")
            result = self._cursor.fetchone()
            if result[0] > 0:
                print("Error email")
                return False
            
            now = datetime.datetime.now()
            tm = now.strftime('%Y-%m-%d %H:%M:%S')
            query = f"INSERT INTO users (name, email, password, time) VALUES('{name}', '{email}', '{password}', '{tm}')"
            self._cursor.execute(query)
            self._db.commit()
        except Exception as Ex:
            print(Ex)
            return False
        
        return True

    def get_user(self, user_id):
        try:
            self._cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
            result = self._cursor.fetchone()
            if not result:
                return False
            
            return result
        except Exception as Ex:
            print(Ex)
        
        return False

    def get_user_by_email(self, email):
        try:
            self._cursor.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            result = self._cursor.fetchone()
            if not result:
                return False
            
            return result
        except Exception as Ex:
            print(Ex)
        
        return False

    def update_ava(self, img, id):
        if not img:
            return False
        
        try:
            binary = psycopg2.Binary(img)
            self._cursor.execute(f"UPDATE users SET ava = {binary} WHERE id = {id}")
            self._db.commit()
        except Exception as Ex:
            print(Ex)
            return False
        
        return True

    # news
    def add_post(self, titlepost, img, text):
        if not img:
            return False
        
        try:
            binary = psycopg2.Binary(img)
            tm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = f"INSERT INTO posts (titlepost, img, text, time) VALUES('{titlepost}', {binary}, '{text}', '{tm}')"
            self._cursor.execute(query)
            self._db.commit()
        except Exception as Ex:
            print(Ex)
            return False

        return True

    def get_post_list(self):
        try:
            self._cursor.execute(f"SELECT id, titlepost, time FROM posts")
            result = self._cursor.fetchall()            
        except Exception as Ex:
            print(Ex)
            
        return result

    def get_post(self, id_post):
        try:
            self._cursor.execute(f"SELECT id, titlepost, text, time FROM posts WHERE id = '{id_post}' LIMIT 1")
            result = self._cursor.fetchone()
        except Exception as Ex:
            print(Ex)
        
        return result

    def get_post_img(self, id_post):
        try:
            self._cursor.execute(f"SELECT img FROM posts WHERE id = '{id_post}' LIMIT 1")
            result = self._cursor.fetchone()
        except Exception as Ex:
            print(Ex)
        
        return result
    
    # dogs
    # def add_dog(self, img):
    #     if not img:
    #         return False
        
    #     try:
    #         binary = psycopg2.Binary(img)
    #         query = f"INSERT INTO dogs (img) VALUES({binary})"
    #         self._cursor.execute(query)
    #         self._db.commit()
    #     except Exception as Ex:
    #         print(Ex)
    #         return False

    #     return True

    # def get_dog(self, dog_id):
    #     try:
    #         self._cursor.execute(f"SELECT img FROM dogs WHERE id = {dog_id} LIMIT 1")
    #         result = self._cursor.fetchone()
    #     except Exception as Ex:
    #         print(Ex)

    #     return result
    
    # def get_dog_id(self):
    #     try:
    #         self._cursor.execute(f"SELECT id FROM dogs")
    #         result = self._cursor.fetchall()
    #     except Exception as Ex:
    #         print(Ex)
        
    #     return result
