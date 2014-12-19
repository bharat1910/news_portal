import nltk
import os
import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="123", # your password
                      db="NewsExplorer") # name of the data base

cur = db.cursor()

person_dict = {}
organization_dict = {}
location_dict = {}
file_id = 0
article_id = 0
person_id = 0
organization_id = 0
location_id = 0
article_person_id = 0
article_organization_id = 0
article_location_id = 0

base_dir = '/Users/bharat/Desktop/crawler/data/'
year = 2013
for month in range(1,13):
    dir_path = base_dir + str(year) + '/' + str(month)
    news_files = [f for f in os.listdir(dir_path) if f.endswith('.news')]

    for file in news_files:
        file_id = file_id + 1
        file_path = dir_path + '/' + file
        date = file.split('.')[0]
        try:
            cur.execute("INSERT INTO news_explorer_file (id, path_file, published_date, name, source, published_location) VALUES (%s, %s, %s, %s, %s, %s)", (file_id, file_path, date, 'dummy', 'dummy', 'dummy'))
        except:
            continue;
        with open(file_path) as f:
            for line in f:
                article_id = article_id + 1
                tkens = line.split("$###$")
                title = tkens[0]
                news = tkens[1]
                cur.execute("INSERT INTO news_explorer_article (id, file_id, headline, content, number, clicks, category) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                       , (article_id, file_id, title, news, 1, 0, 'dummy'))

                news = unicode(news, 'utf-8')
                title = unicode(title, 'utf-8')
                tokens = nltk.tokenize.word_tokenize(news)
                #print tokens
                pos = nltk.pos_tag(tokens)
                sentt = nltk.ne_chunk(pos, binary = False)
                for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
                    article_person_id = article_person_id + 1
                    leaves = subtree.leaves()
                    person = ''
                    for leave in leaves:
                        person = person + leave[0] + ' '
                    person = person.strip().upper()
                    person = person.encode('latin-1', 'ignore')
                    if not person_dict.has_key(person):
                        person_id = person_id + 1
                        person_dict[person] = person_id

                        print person
                        try:
                            #person = unicode(person, 'ignore')
                            cur.execute("INSERT INTO news_explorer_person (id, name) VALUES (%s, %s)"
                            ,(person_id, person.replace('?', '')))
                        except:
                            continue


                    per_id = person_dict[person]
                    try:
                        cur.execute("INSERT INTO news_explorer_articlebyperson (id, person_id, article_id, count) VALUES (%s, %s, %s, %s)",(article_person_id,per_id, article_id, 1))
                    except:
                        continue;

                for subtree in sentt.subtrees(filter=lambda t: t.label() == 'ORGANIZATION'):
                    article_organization_id = article_organization_id + 1
                    leaves = subtree.leaves()
                    organization = ''
                    for leave in leaves:
                        organization = organization + leave[0] + ' '
                    organization = organization.strip().upper()
                    organization = organization.encode('latin-1','ignore')
                    if not organization_dict.has_key(organization):
                        organization_id = organization_id + 1
                        organization_dict[organization] = organization_id

                        print organization
                        try:
                            cur.execute("INSERT INTO news_explorer_organization (id, name) VALUES (%s, %s)",(organization_id, organization))
                        except:
                            continue

                    org_id = organization_dict[organization]
                    try:
                        cur.execute("INSERT INTO news_explorer_articlebyorganization (id, organization_id, article_id, count) VALUES (%s, %s, %s, %s)",(article_organization_id,org_id, article_id, 1))
                    except:
                        continue;

                for subtree in sentt.subtrees(filter=lambda t: t.label() == 'LOCATION'):
                    article_location_id = article_location_id + 1
                    leaves = subtree.leaves()
                    location = ''
                    for leave in leaves:
                        location = location + leave[0] + ' '
                    location = location.strip().upper()
                    location = location.encode('latin-1', 'ignore')
                    if not location_dict.has_key(location):
                        location_id = location_id + 1
                        location_dict[location] = location_id
                        #location = location.encode('latin-1', 'ignore')
                        print location
                        try:
                            cur.execute("INSERT INTO news_explorer_location (id, name, parentlocation_id) VALUES (%s, %s, %s)"
                            ,(location_id, location, -1))
                        except:
                            continue;

                    loc_id = location_dict[location]
                    try:
                        cur.execute("INSERT INTO news_explorer_articlebylocation (id, location_id, article_id, count) VALUES (%s, %s, %s, %s)",(article_location_id,loc_id, article_id, 1))
                    except:
                        continue

db.commit()
cur.close()
db.close()
