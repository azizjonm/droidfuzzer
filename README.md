#DroidFuzzer

## BETA

DroidFuzzer is a Android fuzzing toolkit that is mean to target devices and their mechanisms for parsing things like images and documents.  DroidFuzzer is meant to be modular allowing the support for multiple devices, image parsers, document viewers, media, and much more

```
______           _     _______
|  _  \         (_)   | |  ___|
| | | |_ __ ___  _  __| | |_ _   _ ___________ _ __
| | | | '__/ _ \| |/ _` |  _| | | |_  /_  / _ \ '__|
| |/ /| | | (_) | | (_| | | | |_| |/ / / /  __/ |
|___/ |_|  \___/|_|\__,_\_|  \__,_/___/___\___|_|



(DroidFuzzer) fuzzers show
2016-02-13 01:53:41,672 - DEBUG - Available modules : Samsung Core Prime : document_viewer_fuzzer
```
```
(DroidFuzzer) generate /Users/rotlogix/Downloads/demo.docx 100
2016-02-13 01:54:32,949 - DEBUG - Extension already exists (!)
2016-02-13 01:54:32,949 - DEBUG - Generating test-cases (!)
Random seed: 332976857100687300216904
 - /Users/rotlogix/Tools/android/droidfuzzer/test-cases/docx/test-case-1.docx: 1M
 - /Users/rotlogix/Tools/android/droidfuzzer/test-cases/docx/test-case-2.docx: 1M
 - /Users/rotlogix/Tools/android/droidfuzzer/test-cases/docx/test-case-3.docx: 1M
 - /Users/rotlogix/Tools/android/droidfuzzer/test-cases/docx/test-case-4.docx: 1M
 - /Users/rotlogix/Tools/android/droidfuzzer/test-cases/docx/test-case-5.docx: 1M
 ...
 ..
 .
```
