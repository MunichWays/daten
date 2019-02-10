import fastkml

# fastkml usage examples https://github.com/cleder/fastkml/tree/master/examples

k = fastkml.kml.KML()

# Read in RadlVorrangnetz KML file from Google MyMaps
with open("RadlVorrangnetz-Master.kml", "r", encoding="utf-8") as fp:
    doc = fp.read().encode('utf-8')
    k.from_string(doc)

# Extract features from KML
features = list(k.features())
layers = list(features[0].features())  # Layers are KML folder objects

# Loop over the layers
for layer in layers:
    print(f'Processing layer {layer.name}...')

    # Create the root KML object
    k = fastkml.kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'

    # Create a KML Document and add it to the KML root object
    d = fastkml.kml.Document(ns, 'docid', 'doc name', 'doc description')
    k.append(d)
    d.append(layer)

    # Write each layer to separate KML file
    with open(u"{}.kml".format(layer.name), "w") as fp:
        fp.write(k.to_string(prettyprint=True))
