import sys
import MySQLdb as sql

txt = open('scraped.txt', 'r')
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

    for line in txt:
        if line[0] != '/':
            continue
        
        split = line.split(' ')
        img = split[2].strip('\n')
        
        dirty_url = split[0][7:]
        num = dirty_url.find('-')
        number = dirty_url[0:num]
        name = dirty_url[num + 1:]
        
        # print dirty_url+', '+number+', '+name+' ||| '+ img
        broken_names = name.split('-')
        
        keys = ""
        vals = ""
        
        for r in range(len(broken_names)):
            if r > 0:
                vals += ", "
                keys += ", "
            vals += "'"+broken_names[r]+"'"
            r += 1
            keys += 'word'+str(r)
                
        keys += ', url'
        vals += ", '"+img+"'"
        
        statement = "INSERT INTO "+table_name+"("+keys+") VALUES("+vals+")"
        wrapper = 'mysql -u'+mysql_u+' -p'+mysql_p+' -e "' + statement + '"'
        # cur.execute(statement)
        print wrapper
        # sys.exit()
    
except sql.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    # sys.exit(1)
finally:    
    if con:    
        con.close()
    
