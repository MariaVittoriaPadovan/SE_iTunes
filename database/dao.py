from database.DB_connect import DBConnect
from model.album import Album


class DAO:

    @staticmethod
    def get_all_album(durata):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT a.id, a.title, a.artist_id, SUM(t.milliseconds)/60000 AS durata
                FROM album a, track t 
                WHERE a.id = t.album_id
                GROUP BY a.id, a.title, a.artist_id
                HAVING durata > %s
                """

        try:
            cursor.execute(query, (durata,))
            for row in cursor:
                result.append(Album(id=row['id'], title=row['title'], artist_id=row['artist_id'], durata=row['durata']))

        except Exception as e:
            print("Errore durante la query album")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista di oggetti Album con durata totale maggiore di quella passata come parametro

    @staticmethod
    def get_album_playlist_map(albums): #albums è una lista di oggetti Album
        cnx = DBConnect.get_connection()
        result = {a: set() for a in albums} #dizionario con chiave: oggetto album e valore: insieme vuoto
        #il set servirà per memorizzare gli ID delle playlist (senza duplicati)
        album_ids= tuple(a.id for a in albums) #estrae gli id degli album e li mette in una tupla(lista immutabile)
        if not album_ids:
            return result

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = f"""
                SELECT t.album_id, pt.playlist_id
                FROM track t, playlist_track pt
                WHERE t.id = pt.track_id AND t.album_id IN {album_ids}
                """

        try:
            cursor.execute(query)
            for row in cursor:
                album= next((a for a in albums if a.id == row['album_id']), None)
                #cerca nella lista albums l'oggetto album con id uguale a album_id, se non lo trova restituisce none
                if album:
                    result[album].add(row['playlist_id']) #aggiunge l’ID della playlist al set dell’album

        except Exception as e:
            print("Errore durante la query album playlist map")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # dizionario con chiave: oggetto Album e valore: set di playlist_id in cui compaiono i brani di quell’album
        #indica in quali playlist compaiono i brani di ogni album

