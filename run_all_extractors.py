from deck_extractors.tempostorm import TempostormExtractor

all_extractors = [TempostormExtractor]

for extractor_class in all_extractors:
    extractor = extractor_class()
    extractor.run()