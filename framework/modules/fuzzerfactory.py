from framework.modules.kindle_fire.gallery_fuzzer import GalleryFuzzer
from framework.modules.samsung_core_prime.document_viewer_fuzzer import DocumentViewerFuzzer


class FuzzerFactory(object):

    def __init__(self):
        super(FuzzerFactory, self).__init__()

        self.samsung_core_prime_document_viewer_fuzzer = DocumentViewerFuzzer()
        self.kindle_fire_gallery_viewer_fuzzer = GalleryFuzzer()

        self.fuzzers = [f for f in self.samsung_core_prime_document_viewer_fuzzer,
                        self.kindle_fire_gallery_viewer_fuzzer
                        ]

    def get_fuzzer(self, selection):
        for fuzzer in self.fuzzers:
            if fuzzer.__getattribute__("label") == selection:
                return fuzzer
