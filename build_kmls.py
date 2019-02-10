import munichways_data.kmltranslate

translator = munichways_data.kmltranslate.KMLTranslator()
translator.extract_layers()
translator.write_split_layers()
