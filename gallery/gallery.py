import os
from pelican import signals
from ConfigParser import SafeConfigParser
import codecs

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.gif', '.bmp']

class galleryimage:
    def __init__(self, src, alt, title):
        self.src = src
        self.alt = alt
        self.title = title
    def __repr__(self):
        return repr((self.src, self.alt, self.title))

def add_gallery_post(generator):

    contentpath = generator.settings.get('PATH')
    gallerycontentpath = os.path.join(contentpath,'images/gallery')
    parser = SafeConfigParser();

    for article in generator.articles:
        if 'gallery' in article.metadata.keys():
            album = article.metadata.get('gallery')
            galleryimages = []

            albumpath=os.path.join(gallerycontentpath, album)

            if(os.path.isdir(albumpath)):
                texts = os.path.join(albumpath, album+".txt")
                if os.path.isfile(texts):
                    #todo: use user defined encoding
                    parser.readfp(codecs.open(texts, "r", "utf8"))              
                        
                for i in os.listdir(albumpath):
                    if os.path.isfile(os.path.join(albumpath, i)):
                        alt   = " "
                        title = " "
                        iName, iExt = os.path.splitext(i)
                        if iExt.lower() in IMAGE_EXTENSIONS: 
                            if parser.has_option(iName, "alt"):
                                alt = parser.get(iName, "alt")
                            if parser.has_option(iName, "title"):
                                title = parser.get(iName, "title")
                            
                            galleryimages.append(galleryimage(i, alt, title))

            article.album = album
            article.galleryimages = sorted(galleryimages, key=lambda galleryimage: galleryimage.src)


def generate_gallery_page(generator):

    contentpath = generator.settings.get('PATH')
    gallerycontentpath = os.path.join(contentpath,'images/gallery')

    for page in generator.pages:
        if page.metadata.get('template') == 'gallery':
            gallery = dict()

            for a in os.listdir(gallerycontentpath):
                if os.path.isdir(os.path.join(gallerycontentpath, a)):

                    for i in os.listdir(os.path.join(gallerycontentpath, a)):
                        if os.path.isfile(os.path.join(os.path.join(gallerycontentpath, a), i)):
                            gallery.setdefault(a, []).append(i)
                    gallery[a].sort()

            page.gallery=gallery


def register():
    signals.article_generator_finalized.connect(add_gallery_post)
    signals.page_generator_finalized.connect(generate_gallery_page)
