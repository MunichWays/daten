import munichways_data.kmltranslate
import kml2geojson

translator = munichways_data.kmltranslate.KMLTranslator()
translator.extract_layers()
translator.color_placemarks()
translator.write_split_layers()

kml2geojson.main.convert(kml_path='output/D_gelb_rot_Gesamtnetz.kml',
                         output_dir='geojson_output/')
