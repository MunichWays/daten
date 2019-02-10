import fastkml

# fastkml usage examples https://github.com/cleder/fastkml/tree/master/examples


class KMLTranslator:
    """
    Reads in RadlVorrangnetz KML from Google MyMaps, processes it and produces KML files that can be read in by uMap
    """
    def __init__(self, input_file='RadlVorrangnetz-Master.kml'):
        self.input_file = input_file
        self.k = fastkml.kml.KML()
        self.features = None
        self.layers = None

        # Read in RadlVorrangnetz KML file from Google MyMaps
        print(f'Reading in file {self.input_file}')
        with open(self.input_file, "r", encoding="utf-8") as fp:
            doc = fp.read().encode('utf-8')
            self.k.from_string(doc)

    def extract_layers(self):
        """Extract features from KML"""
        self.features = list(self.k.features())
        self.layers = list(self.features[0].features())  # Layers are KML folder objects
        print(f'Extracted {len(self.layers)} layers from input file')

    def write_split_layers(self):
        """Write each single layer to separate KML file"""
        # Loop over the layers
        for layer in self.layers:
            print(f'Processing layer {layer.name}...')

            # Create the root KML object
            k_out = fastkml.kml.KML()
            ns = '{http://www.opengis.net/kml/2.2}'

            # Create a KML Document and add it to the KML root object
            doc = fastkml.kml.Document(ns, 'docid', 'doc name', 'doc description')
            k_out.append(doc)
            doc.append(layer)

            # Write each layer to separate KML file
            with open(u"{}.kml".format(layer.name), "w") as fp:
                fp.write(k_out.to_string(prettyprint=True))


if __name__ == '__main__':
    bla = KMLTranslator()
    bla.extract_layers()
    bla.write_split_layers()
