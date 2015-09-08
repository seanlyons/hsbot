import MySQLdb as sql

table_name = 'cards_trie'

#secrets
secret_file = open('hsbot.secret', 'r')
secrets = secret_file.read().split('\n')
mysql_u = secrets[0]
mysql_p = secrets[1]
mysql_db = secrets[2]

try:
    con = sql.connect('localhost', mysql_u, mysql_p, mysql_db)

    cur = con.cursor()
    statement = "INSERT INTO "+table_name+"(Name, ) VALUES('Jack London')"
    cur.execute()


    ver = cur.fetchone()
    
    print "Database version : %s " % ver
    
except sql.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()
    
