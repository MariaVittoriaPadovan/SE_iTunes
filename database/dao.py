from database.DB_connect import DBConnect
from model.album import Album


class DAO:

    @staticmethod
    def get_all_album(durata):
        cnx = DBConnect.get_connection()
        result = {}

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT a.id, a.title, SUM(t.milliseconds) AS durata
                FROM album a, track t 
                WHERE a.id = t.album_id
                GROUP BY a.id
                HAVING SUM(t.milliseconds) > %s
                """

        try:
            cursor.execute(query, (durata,))
            for row in cursor:
                result[row['id']] = Album(row['id'], row['title'], row['durata'])

        except Exception as e:
            print("Errore durante la query album")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # dizionario di oggetti Album con durata totale maggiore di quella passata come parametro

    @staticmethod
    def get_album_connessi():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT tr1.album_id AS a1, tr2.album_id AS a2
                FROM (SELECT pt1.track_id AS c1, pt2.track_id AS c2
                      FROM playlist_track pt1, playlist_track pt2
                      WHERE pt1.playlist_id = pt2.playlist_id
                            AND pt1.track_id < pt2.track_id) t1,
                      track tr1, track tr2
                WHERE t1.c1 <> t1.c2 
                      AND tr1.id = t1.c1 AND tr2.id = t1.c2
                      AND tr1.album_id <> tr2.album_id
                """

        try:
            cursor.execute(query)
            for row in cursor:
                result.append((row['a1'], row['a2']))

        except Exception as e:
            print("Errore durante la query album connessi")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista di coppie di id album connessi


