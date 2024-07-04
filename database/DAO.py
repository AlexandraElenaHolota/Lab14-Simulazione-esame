from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCromosomi():
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT g.Chromosome 
                    FROM genes g 
                    WHERE g.Chromosome != 0"""

        cursor.execute(query, )

        result = []
        for row in cursor:
            result.append(row['Chromosome'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllWeightEdges():
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.Chromosome1, t1.Chromosome2, SUM(t1.Expression_Corr) as somma 
                        FROM (SELECT DISTINCT t.*, g1.Chromosome as Chromosome2
                        FROM genes g1, (SELECT i.GeneID1, i.GeneID2, g.Chromosome as Chromosome1, i.Expression_Corr 
                        FROM interactions i, genes g 
                        WHERE i.GeneID1 = g.GeneID ) as t
                        WHERE t.GeneID2=g1.GeneID ) as t1
                        WHERE t1.Chromosome1!=t1.Chromosome2 and t1.Chromosome1!=0 
                        GROUP BY t1.Chromosome1, t1.Chromosome2
                        ORDER BY t1.Chromosome1, t1.Chromosome2"""

        cursor.execute(query, )

        result = []
        for row in cursor:
            result.append((row["Chromosome1"], row["Chromosome2"], row["somma"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getMaxMin():
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT MIN(n.somma) as min, Max(n.somma) as max 
                    FROM (SELECT t1.Chromosome1, t1.Chromosome2, SUM(t1.Expression_Corr) as somma
                    FROM (SELECT DISTINCT t.*, g1.Chromosome as Chromosome2
                    FROM genes g1, (SELECT i.GeneID1, i.GeneID2, g.Chromosome as Chromosome1, i.Expression_Corr 
                    FROM interactions i, genes g 
                    WHERE i.GeneID1 = g.GeneID ) as t
                    WHERE t.GeneID2=g1.GeneID ) as t1
                    WHERE t1.Chromosome1!=t1.Chromosome2 and t1.Chromosome1!=0 
                    GROUP BY t1.Chromosome1, t1.Chromosome2
                    ORDER BY t1.Chromosome1, t1.Chromosome2) as n"""

        cursor.execute(query, )

        result = []
        for row in cursor:
            result.append((row["min"], row["max"]))

        cursor.close()
        conn.close()
        return result
