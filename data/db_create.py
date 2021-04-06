import sqlite3

conn = sqlite3.connect("db.db")
cursor = conn.cursor()


cursor.execute("""CREATE TABLE Car_Models
		        (
		    	 user_id int NOT NULL,
		    	 data text NOT NULL
		        )
		        """)


cursor.execute("""CREATE TABLE Car
		        (
		    	 user_id int NOT NULL,
		    	 link varchar(31),
		    	 ssd varchar(31),
		    	 data text
		        )
		        """)


cursor.execute("""CREATE TABLE Phone
		        (
		    	 user_id int NOT NULL,
		    	 phone varchar(31) NOT NULL,
		    	 password varchar(31)
		        )
		        """)