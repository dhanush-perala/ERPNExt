import oracledb
 
try:

    conn = oracledb.connect(

        user="system",

        password="oracle",

        dsn="localhost/XEPDB1"

    )

    print("✅ Connected successfully to Oracle Database!")

    print("Database version:", conn.version)
 
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM dual")

    for row in cursor:

        print("Test query output:", row)
 
    cursor.close()

    conn.close()
 
except Exception as e:

    print("❌ Connection failed:", e)

 
