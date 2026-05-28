from database.DB_connect import DBConnect
from model.arco import Arco
from model.pilota import Pilota

class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(annoI, annoF):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.*
            from drivers d, results r, races ra
            where d.driverId = r.driverId and r.raceId = ra.raceId 
            and ra.`year`  between %s and %s
            and r.`position` is not null
            order by d.driverId """

        cursor.execute(query, (annoI, annoF))

        for row in cursor:
            results.append(Pilota(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArchi(annoI, annoF, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.driverId as d1, r2.driverId as d2, count(*) as peso
                    from results r1, results r2, races ra
                    where ra.raceId = r1.raceId and ra.raceId = r2.raceId 
                    and r1.constructorId = r2.constructorId
                    and ra.`year` between %s and %s
                    and r1.driverId > r2.driverId 
                    and r1.`position` is not null 
                    and r2.`position` is not null
                    group by r1.driverId, r2.driverId
                    order by peso desc """

        cursor.execute(query, (annoI, annoF))

        for row in cursor:
            results.append(Arco(idMap[row["d1"]], idMap[row["d2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results