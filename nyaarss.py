import pickle
import feedparser
import urllib
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
        self.to_download = dict()
        self.struct = (self.q, self.to_download)

    def save(self):
        pickle.dump(self.struct, open(self.q_filename, "wb"))
        print "Save success at " + self.q_filename

    def load(self):
        try:
            self.q, self.to_download = pickle.load(open(self.q_filename, "rb"))
            print "Load successful from " + self.q_filename
        except EOFError:
            print "Couldn't load " + self.q_filename + "PLEASE FIX!?"
            self.save()

    def add_query(self, query):
        qt = tuple(query)
        if qt in self.q:
            print repr(query)+" is already in here! Update?"
            return None
        self.q[qt] = dict()

    def update(self):
        for k,v in self.q.items():
            search = self.nyaa_parser(k)
            for title, link in search:
                print title + " " + link
                if title not in v:
                    v[title] = [0, link]
                    if title not in self.to_download:
                        self.to_download[title] = k

    def remove_download(self, title):
        if title in self.to_download:
            k = self.to_download[title]
            #Setting it to "Downloaded"
            self.q[k][title][0] = 1
            del self.to_download[title]
            if title not in self.to_download:
                print "Successfuly removed "+title
            else:
                print "wtf is going on?"

    def to_download_printed(self):
        for title, url in self.to_download.items():
            print title

    def download(self, title):
#Check if title is there
        if title in self.to_download:
            k = self.to_download[title]
#The url is localed in query's title's url
            url = self.q[k][title][1]
#Download sequence
            download_link = urllib.URLopener()
            download_link.retrieve(url, title+".torrent")
#Remove from your downloads
            self.remove_download(title)
            print "Downloaded "+title+".torrent from "+url
        else:
            print "Download failed for "+title

    def download_all(self):
#Temporary to_download for iterable
        temp = dict(self.to_download)
        for title, url in temp.items():
            self.download(title)

    def nyaa_parser(self, termlist):
        terms_q = '+'.join(termlist)
        nyaa_url = "http://www.nyaa.eu/?page=rss&term="

        nyaa_feed = feedparser.parse(nyaa_url+terms_q)
        print "Grabbing RSS feed from " + "nyaa_url+terms_q"

        parsed = list()
        for x in nyaa_feed['entries']:
            key = x['title']
            value = x['links'][0]['href']
            parsed.append((key,value))
        return parsed

    def printed(self):
        for k,v in self.q.items():
            print k
            for kk, vv in v.items():
                print '\t'+repr(kk)
                print '\t\t'+repr(vv)

#terms = sys.argv[1:]
downloader = SchedulerObject("anime.db")
downloader.load()
downloader.add_query(['horriblesubs','Dagashi','Kashi','720p'])
downloader.update()
downloader.printed()
downloader.save()
downloader.to_download_printed()
downloader.download_all()
downloader.save()

#nyaa_categories = dict()
#nyaa_categories["All categories"] = "0_0"
