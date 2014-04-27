from news_explorer.models import Article

def indexDocumentsForSolr():
    A = Article.objects.values('id', 'headline', 'content')

    file = open('solr-4.1.0/xml/docs.xml', 'w+')
    file.write('<add>\n')

    for a in A:
        file.write('<doc>\n')
        file.write('<field name="id">' + str(a['id']) + '</field>\n')
        file.write('<field name="cat"></field>\n')
        file.write('<field name="url"></field>\n')
        file.write('<field name="title">' + str(a['headline']) + '</field>\n')
        file.write('<field name="content">' + str(a['content']) + '</field>\n')
        file.write('</doc>\n')

    file.write('</add>')
    file.close()