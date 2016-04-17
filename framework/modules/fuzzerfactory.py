from framework.modules.kindle_fire.gallery_fuzzer import KindleFireGalleryFuzzer
from framework.modules.asus_zenfone_2e.gallery_fuzzer import ASUSZenFoneGalleryFuzzer
from framework.modules.asus_zenfone_2e.video_fuzzer import ASUSZenFoneVideoFuzzer
from framework.modules.samsung_core_prime.document_viewer_fuzzer import DocumentViewerFuzzer
from framework.modules.thinkdroid.document_viewer import ThinkfreeDocumentFuzzer


class FuzzerFactory(object):

    def __init__(self):
        super(FuzzerFactory, self).__init__()

        self.samsung_core_prime_document_viewer_fuzzer = DocumentViewerFuzzer()
        self.kindle_fire_gallery_viewer_fuzzer = KindleFireGalleryFuzzer()
        self.asus_zenfone_2e_gallery_fuzzer = ASUSZenFoneGalleryFuzzer()
        self.asus_zenfone_2e_video_fuzzer = ASUSZenFoneVideoFuzzer()
        self.thinkfree_document_fuzzer = ThinkfreeDocumentFuzzer()

        self.fuzzers = [f for f in self.samsung_core_prime_document_viewer_fuzzer,
                        self.kindle_fire_gallery_viewer_fuzzer,
                        self.asus_zenfone_2e_gallery_fuzzer,
                        self.asus_zenfone_2e_video_fuzzer,
                        self.thinkfree_document_fuzzer
                        ]

    def get_fuzzer(self, selection):
        for fuzzer in self.fuzzers:
            if fuzzer.__getattribute__("label") == selection:
                return fuzzer
