import pickle
import feedparser
import sys

#DATA STRUCTURE OF NYAA's RSS FEED @ ['entries']
#
#summary_detail
#published_parsed
#links
#tags
#title
#summary
#guidislink
#title_detail
#link
#published
#id

class SchedulerObject(object):
    """This object is creates a pickle that allows for retention of your Queries.
    WORKS SPECIFICALLY FOR NYAA.SE
    It can also reload those queries.
    It can also Schedule download of those queries

    Attributes:
        q_filename: This is the filename that saves your queries and previously downloaded torrents
        q_pickle: this is your query pickel
        q: the actual object
    """

    def __init__(self, q_filename):
        """Instantiates the object based on the filename  q_filename
        q_file MUST be file object that can be read and written
        """
        self.q_filename = q_filename
        self.q = dict()

    def save(self):
        pickle.dump(self.q, open(self.q_filename, "wb"))
        print "Save success at " + self.q_filename

    def load(self):
        try:
            self.q = pickle.load(self.q_filename, "rb")
            print "Load successful from " + self.q_filename
        except EOFError:
            print "Couldn't load " + self.q_filename

    def add_query(self, query):
        qt = tuple(query)
        if qt in self.q:
            print query+" is already in here! Update?"
            return None
        self.q[qt] = dict()

    def update_all(self):
        for k,v in self.q.items():
            search = self.nyaa_parser(k)
            for title, link in search:
                if title not in v:
                    v[title] = (0, link)

    def nyaa_parser(self, termlist):
        terms_q = '+'.join(termlist)
        nyaa_url = "http://www.nyaa.eu/?page=rss&term="

        nyaa_feed = feedparser.parse(nyaa_url+terms_q)
        print nyaa_url+terms_q

        parsed = list()
        for x in nyaa_feed['entries']:
            key = x['title']
            value = x['links'][0]['href']
            parsed.append((key,value))
        return parsed

    def printed(self):
        for k,v in self.q.items:
            print k
            for status, link in v:
                print '\t'+str(status)+" "+link

#terms = sys.argv[1:]
downloader = SchedulerObject("test")

downloader.add_query(['horriblesubs','Dagashi','Kashi','720p'])
downloader.update_all()
downloader.printed()
downloader.save()

downloader2 = SchedulerObject("test")
downloader2.load()
downloader2.printed()

#nyaa_categories = dict()
#nyaa_categories["All categories"] = "0_0"
