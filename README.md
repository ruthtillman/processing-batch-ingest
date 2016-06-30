# Basic Information and description

Useful for matching PIDs to files after an ingest. Should run in the same order as original ingest spreadsheet and thus PIDs should be in the right order to begin with. However, dc:title is extracted so we can always compare the two if there's concern.

## Dependencies

Runs on Python 2.7.11. Requires installation of Python jq library (possible via [Homebrew](http://brew.sh/)) before it can be run.

## Possible Future Work

- Currently only handles single ingest file, single output file.
- Ingest file and output file defined by user, may be useful to take in group of files and output matching filenames.
