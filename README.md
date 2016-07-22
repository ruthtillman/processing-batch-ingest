# Basic Information and Description

Run this script after performing a successful batch ingest. It will need two directory paths--one to the local working directory where original metadata-n.csv files are stored, etc., and one to the appropriate directory within /success/ on the batch ingester. It backs up original files and creates appropriate files for updating the objects in future through the batch ingester.

## Problem Statement

When updating something in the batch ingester, one needs two things:

1. A copy of the original submission CSV with the addition of the field "curate_id". (Also with any files removed, see **Necessary follow-up steps**)
2. The metadata-n.rof file(s) and a JOB file which re-add the properties field including the thumbnails to the object.

One then submits the two as two separate ingests in order.

## Script Process

The script does the following:

1. Creates directory `/originals` in local working directory if doesn't already exist.
2. Retrieves successful ROFs from remote directory into working directory and renames them with prefix `original-`.
3. Copies original CSVs from the working directory into directory `/originals`, renames them with prefix `original-`. This means we'll always have a copy of the original even as we make updates.
4. Walks through the ROF files and extracts all non-GenericFile PIDs as a CSV with the header `curate_id` in a file named `pid-n.csv`. `n` in `pid-n` refers to the original CSV/ROF ingest and all PIDs are in the same order as objects in the CSV and can simply be added to `metadata-n.csv` as a new column.
5. Walks through the ROF files and creates ROFs without the prefix `original-` that have the necessary information to update thumbnails. Creates directory called `/update-thumbnails` if it doesn't exist, and moves these there.
6. Moves the `original-metadata-n.rof` files to the `/originals` directory.

## Necessary follow-up steps

1. Open `metadata-n.csv` and `pid-n.csv` files.
2. Remove files column from `metadata-n.csv` (this is one reason we kept a copy of the originals).
3. Add column `curate_id` from `pid-n.csv` to `metadata-n.csv` and save. The ordering of the two is the same and thus no extra reconciliation is needed.

## Dependencies

Runs on Python 2.7.11. Requires installation of Python jq library (possible via [Homebrew](http://brew.sh/)) before it can be run.

## BUG?

JOB file may be in the wrong order.

## Future Work

Add support for this being the second or third ingest, running only the process to copy the mid-process CSV files into a directory and keep the most recent copy of the CSV in the main file.
