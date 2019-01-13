import sys
from fastkml import kml

# reconfigure default encoding to utf8 for python2
if sys.version_info.major < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')


doc = None
with open("RadlVorrangnetz-Master.kml", "r") as fp:
    doc = fp.read()

k = kml.KML()
k.from_string(doc)

features = list(k.features())

for folder in list(features[0].features()):
    print(folder.name)

    # Create the root KML object
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'

    # Create a KML Document and add it to the KML root object
    d = kml.Document(ns, 'docid', 'doc name', 'doc description')
    k.append(d)

    d.append(folder)

    with open(u"{}.kml".format(folder.name), "w") as fp:
        fp.write(k.to_string(prettyprint=True))