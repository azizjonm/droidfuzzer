from framework.modules.kindle_fire.gallery_fuzzer import KindleFireGalleryFuzzer
from framework.modules.asus_zenfone_2e.gallery_fuzzer import ASUSZenFoneGalleryFuzzer
from framework.modules.asus_zenfone_2e.video_fuzzer import ASUSZenFoneVideoFuzzer
from framework.modules.asus_zenfone_2e.document_fuzzer import ASUSZenFoneDocumentFuzzer
from framework.modules.samsung_core_prime.document_viewer_fuzzer import DocumentViewerFuzzer
from framework.modules.samsung_core_prime.media_scanner_fuzzer import MediaScannerFuzzer as SamsungCorePrimeMediaScannerFuzzer
from framework.modules.lg_gpad_7.polaris_office_fuzzer import PolarisOfficeFuzzer
from framework.modules.lg_gpad_7.media_scanner import MediaScannerFuzzer as LGGPad7MediaScannerFuzzer
from framework.modules.lg_gpad_7.gallery_fuzzer import GalleryFuzzer


class FuzzerFactory(object):

    def __init__(self):
        super(FuzzerFactory, self).__init__()

        self.samsung_core_prime_document_viewer_fuzzer = DocumentViewerFuzzer()
        self.samsung_core_prime_media_scanner_fuzzers = SamsungCorePrimeMediaScannerFuzzer()
        self.kindle_fire_gallery_viewer_fuzzer = KindleFireGalleryFuzzer()
        self.asus_zenfone_2e_gallery_fuzzer = ASUSZenFoneGalleryFuzzer()
        self.asus_zenfone_2e_video_fuzzer = ASUSZenFoneVideoFuzzer()
        self.asus_zenfone_2e_document_fuzzer = ASUSZenFoneDocumentFuzzer()
        self.lg_gpad_7_polaris_office_fuzzer = PolarisOfficeFuzzer()
        self.lg_gpad_7_media_scanner_fuzzer = LGGPad7MediaScannerFuzzer()
        self.lg_gpad_7_gallery_fuzzer = GalleryFuzzer()

        self.fuzzers = [f for f in self.samsung_core_prime_document_viewer_fuzzer,
                        self.samsung_core_prime_media_scanner_fuzzers,
                        self.kindle_fire_gallery_viewer_fuzzer,
                        self.asus_zenfone_2e_gallery_fuzzer,
                        self.asus_zenfone_2e_video_fuzzer,
                        self.asus_zenfone_2e_document_fuzzer,
                        self.lg_gpad_7_polaris_office_fuzzer,
                        self.lg_gpad_7_media_scanner_fuzzer,
                        self.lg_gpad_7_gallery_fuzzer
                        ]

    def get_fuzzer(self, selection):
        for fuzzer in self.fuzzers:
            if fuzzer.__getattribute__("label") == selection:
                return fuzzer
