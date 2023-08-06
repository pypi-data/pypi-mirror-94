# Release notes

# 2.0.4
- Asynchronous compression + decompress only once per pipeline
- Refactoring

# 2.0.3
- Fix incorrect bound checking for error_rate in CutadaptPatternTrimmer operation
- Added more parameter checking in CutadaptPatternTrimmer.

# 2.0.2
- Added documentation

# 2.0.1
- Fixed a bug with the detection of paired-end .fastq files.

# 1.0.0
- Fix a bug with output files in merging using PEAR.
- Add docstrings and improve code style.
- Rename program to 'gbprocess'.

## 0.2.0
- Fix splitting paired-end files when there are differences in read lengths between forward and reverse files
- Prevented operations to be performed while files are empty.
- Fix a bug where samples would not be processed further after being split.
- Removed unused variable in pattern trimming.
- Fix searching for patterns when non-palindromic sequences are used as a cut-site.
- Dont't allow for usage of format specifiers in output file name templates.
- Allow duplicate operations

## 0.1.3
- Fix multiprocessing bug.

## 0.1.2
- Add versioning to release archives.
- Add tests for older code.
- Improved regex parsing of file names.
- Better parsing of command line options.

## 0.1.1
- Fix running from command line.
- Re-add PEAR option next to fastq-join and fastp for merging.
- Add more tests.
- Files with only whitespace characters are now considered empty.
- Fix problem with joining files that end with new line characters.

## 0.1.0
- Replace PEAR with fastq-join

## 0.0.3
- Code syntax changes
- Added more tests to code

## 0.0.2
- Improved input checking for fasta files (containing barcodes).
- Fix bug in CutadaptPositionalTrimmer.
- Print version at start of program.
- Clean exit when not arguments are passed.

## 0.0.1
- Initial release.