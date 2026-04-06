from apscheduler.schedulers.background import BackgroundScheduler
from database1 import initialize_db


def keepLive():
    print("Running every 1 hour")
    conn = None
    cursor = None
    try:
        conn = initialize_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products1")
        result = cursor.fetchone()
        print("Total products:", result[0])
    except Exception as e:
        print("ERROR:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()   

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=keepLive,
    trigger="interval",
    hours=1  
)
scheduler.start()
