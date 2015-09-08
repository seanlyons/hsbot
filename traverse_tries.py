import MySQLdb as sql
import re, string, sys, praw, pprint, json, time, calendar

pattern = re.compile('[\W_]+')
table_name = 'cards_trie'
logging_table = 'cards_explained'
opt_in = ['link_title', 'body', 'id', 'link_id', 'parent_id', 'name', 'link_url']
contraction_suffixes = ['ll', 's', 'd', 've']
subreddit_name = 'competitivehs'
footer = "###### I'm a bot! PM me for questions, concerns, etc! ######"

#secrets
secret_file = open('hsbot.secret', 'r')
secrets = secret_file.read().split('\n')
mysql_u = secrets[0]
mysql_p = secrets[1]
mysql_db = secrets[2]
reddit_u = secrets[3]
reddit_p = secrets[4]

def sanitize_word(word):
    word = word.lower()
    sanitized = ''
    for i in range(len(word)):
        if word[i].isspace():
            continue
        elif word[i].isalpha():
            sanitized += word[i]
        else:
            return sanitized
            
    return sanitized

#if 
def get_activity(thread_id, post_id):
    #the bot cannot comment on a post_id more than once, period
    statement = "select count(*) as count from "+logging_table+" where post_id='"+post_id+"'"
    print statement    
    cur.execute(statement)
    rows = cur.fetchall()[0]
    print rows
    print rows['count']
    #it already has a post_id recorded: fail out
    if rows['count'] > 0:
        print 'returning on 42'
        return False
        
    statement = "select card_ids_json from "+logging_table+" where thread_id='"+thread_id+"'"
    print statement    
    cur.execute(statement)
    rows = cur.fetchall()
    
    if not rows:
        return []
    
    card_ids = json.loads(rows[0]['card_ids_json'])
    
    return card_ids

        
def log_activity(bInsert, thread_id, post_id, last_update, card_ids_json, url):
    now = int(calendar.timegm(time.gmtime()))
    
    if bInsert:
        statement = "insert into "+logging_table+" (thread_id, post_id, card_ids_json, last_update, url) values ('"+thread_id+"', '"+post_id+"', '"+card_ids_json+"', "+now+", '"+url+"')"
    else:
        statement = "update "+logging_table+" set post_id='"+post_id+"', last_update='"+now+"', card_ids_json='"+card_ids_json+"'where thread_id='"+thread_id
        
    cur.execute(statement)
    return
    
def sql_to_name(rows):
    return (rows[0]["word1"]+' '+rows[0]["word2"]+' '+rows[0]["word3"]+' '+rows[0]["word4"]).rstrip()
        
def parse_post(title, comment):
    # comment = '''No, that would be Paletress. "She sees into your past and makes you face your fears. Most common fear: getting Majordomo out of Sneed's Old Shredder."'''
    new_comment = ''
    cards_linked_to = []
    words_in_name = 0
    
    for string in [title, comment]:
        split_string = string.split(' ')
        len_split_string = len(split_string)
        
        for i in range(len_split_string):
            if words_in_name > 0:
                words_in_name -= 1;
                continue
                
            #var initialization
            clean_word = clean_word2 = clean_word3 = ''

            #var assignment, if valid
            clean_word = sanitize_word(split_string[i])
            if i + 1 < len_split_string:
                clean_word2 = sanitize_word(split_string[i + 1])
            if i + 2 < len_split_string:
                clean_word3 = sanitize_word(split_string[i + 2])
            
            statement = 'SELECT * FROM '+ table_name + ' where ((word1 = "'+clean_word+'" and word2 = "") or (word1 = "'+clean_word+'" and word2 = "'+clean_word2+'" and word3 = "") or (word1 = "'+clean_word+'" and word2 = "'+clean_word2+'" and word3 = "'+clean_word3+'")) and disabled = 0;'
            
            # print statement
            
            cur.execute(statement)

            rows = cur.fetchall()

            if len(rows) == 0: 
                continue
            elif len(rows) == 1 and rows[0]["id"] not in cards_linked_to:
                cards_linked_to.append(rows[0]["id"])
                print "cards_linked_to: " + str(cards_linked_to)
                url = rows[0]["url"]
                full_name = sql_to_name(rows)
                words_in_name = full_name.count(' ') + 1
                print str(full_name)+' has '+str(words_in_name)+' words in its name.'
                #new_comment += '<a href="'+url+'">('+words+')</a><br/>'
                new_comment += '[('+full_name.strip().title()+')]('+url+')  \n'
            # else:
                # for row in rows:
                    # print "MULTISHOT ::: "
                    # print row

    # if new_comment:
        # print 'TITLE'
        # print title
        # print 'COMMENT'
        # print comment
        # print 'NEW_COMMENT'
        # print new_comment
    
    return new_comment
   
    
#init reddit
r = praw.Reddit(user_agent='Test Script by /u/bboe')
r.login(reddit_u, reddit_p)
hs = r.get_subreddit(subreddit_name)
posts = hs.get_comments()

#init sql
# try:
con = sql.connect('localhost', mysql_u, mysql_p, mysql_db);
cur = con.cursor(sql.cursors.DictCursor)

# print get_activity('cu9b3jtnnn', 't3_3hp3ft')
# sys.exit()

#iterate over reddit posts
for op in posts:
    selected = { k: vars(op)[k] for k in opt_in }
    new_comment = parse_post(selected['link_title'].strip(), selected['body'].strip())
    if new_comment:
        # name t1_cu92sm2           - 
        # link_id t3_3ho4yo         - this is something like a direct link to the comment itself- the initial t# is how deeply it's nested. 1 is OP, 2 is main comment, 3 is grandchild, etc.
        # parent_id t1_cu92msa      - 

        print selected['link_url'] + selected['id']
        
        
        
        # for s in selected:
            # print s, selected[s]
        # print str(selected['id']).strip()+' -> '+new_comment
        print new_comment
    # for s in selected:
        # try:
            # print s+' -> '+str(selected[s])
        # except Err:
            # print '[[ Unicode! ]]'

    print '---'
    # for s in selected:
        # print s+' -> '+str(selected[s])

        
