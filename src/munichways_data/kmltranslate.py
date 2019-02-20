import fastkml
import re


class KMLTranslator:
    """
    Reads in RadlVorrangnetz KML from Google MyMaps, processes it and produces KML files that can be read in by uMap
    """
    def __init__(self,
                 input_file='RadlVorrangnetz-Master.kml',
                 output_dir='output/'):
        self.input_file = input_file
        self.output_dir = output_dir
        self.k = fastkml.kml.KML()
        self.features = None
        self.layers = None
        self.styles = self._define_styles()

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

    @staticmethod
    def _define_styles():
        """Define line styles that represent the cycling conditions"""
        yellow_line = fastkml.Style(id='gelb', styles=[fastkml.LineStyle(color='ffff00', width=2)])
        red_line = fastkml.Style(id='rot', styles=[fastkml.LineStyle(color='ff0000', width=2)])
        green_line = fastkml.Style(id='grün', styles=[fastkml.LineStyle(color='00ff00', width=2)])
        black_line = fastkml.Style(id='schwarz', styles=[fastkml.LineStyle(color='000000', width=2)])
        grey_line = fastkml.Style(id='grau', styles=[fastkml.LineStyle(color='888888', width=2)])
        return [green_line, yellow_line, red_line, black_line, grey_line]

    def color_placemarks(self):
        """
        Add color line style to each placemark based on its name:
        gelb_ -> yellow_line
        rot_ -> red_line
        grün_ -> green_line
        schwarz_ -> black_line
        anything else -> grey_line
        """
        processed_layers = []
        for layer in self.layers:
            processed_layer = fastkml.Folder(ns=layer.ns,
                                             id=layer.id,
                                             name=layer.name,
                                             description=layer.description)
            placemarks = list(layer.features())
            for placemark in placemarks:
                processed_placemark = self._set_styleurl_by_color_prefix(placemark)
                processed_layer.append(processed_placemark)
            processed_layers.append(processed_layer)

        self.layers = processed_layers

    @staticmethod
    def _set_styleurl_by_color_prefix(placemark):
        """Sets style url of placemark depending on its color prefix"""
        color_pattern = re.compile('^(\w+)_.*')
        match = re.match(color_pattern, placemark.name)
        if match:
            color = match[1]
            if color not in ['gelb', 'grün', 'rot', 'schwarz']:
                color = 'grau'
        else:
            color = 'grau'
        placemark.styleUrl = color
        return placemark

    def write_split_layers(self):
        """Write each single layer to separate KML file"""
        # Loop over the layers
        for layer in self.layers:
            print(f'Processing layer {layer.name}...')

            # Create the root KML object
            k_out = fastkml.kml.KML()
            ns = '{http://www.opengis.net/kml/2.2}'

            # Create a KML document and add it to the KML root object
            doc = fastkml.kml.Document(ns=ns,
                                       id='docid',
                                       name='doc name',
                                       description='doc description',
                                       styles=self.styles)
            k_out.append(doc)

            # Add layer to KML document
            doc.append(layer)

            # Write KML object for this layer to KML file
            with open(u"{}{}.kml".format(self.output_dir, layer.name), "w") as fp:
                fp.write(k_out.to_string(prettyprint=True))
