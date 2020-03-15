import psycopg2

conn = psycopg2.connect('dbname=mydb user=postgres password=yT82Sb&n2mcuy')

crsr = conn.cursor()

crsr.execute("DROP TABLE IF EXISTS todos;")
crsr.execute("""
  CREATE TABLE todos (
    id serial PRIMARY KEY,
    description VARCHAR NOT NULL
  );
""")
crsr.execute("INSERT INTO todos (description) VALUES ('first'), ('second');")
crsr.execute("INSERT INTO todos (description) VALUES (%(desc)s);", {'desc': 'third?'})

# commit, so it does the executions on the db and persists in the db
conn.commit()

crsr.close()
conn.close()
