from utils.dbconfig import dbconfig

db = dbconfig()
cursor = db.cursor()

def clearAllEntries():
    query = "DELETE FROM pm.entries"
    cursor.execute(query)
    db.commit()