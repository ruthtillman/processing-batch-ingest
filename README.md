# Basic Information and description

Useful for matching PIDs to files after an ingest. Works best when titles are distinct. Order ingest metadata file and this file alphabetically on Title. Should match, but should be checked at some levels. Once column with PIDs has been added to spreadsheet, we'll have the tools to update in the future.

## Dependencies

Runs on Python 2.7.11. Requires installation of Python jq library (possible via [Homebrew](http://brew.sh/)) before it can be run.

## Possible Future Work

- Currently only handles single ingest file, single output file.
- Ingest file and output file defined by user, may be useful to take in group of files and output matching filenames.
