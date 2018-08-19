# Panzer configuration files #

These started as a clone of the [configuration
files](https://github.com/msprev/dot-panzer) provided by the
[author](https://github.com/msprev) of
[panzer](https://github.com/msprev/panzer).

Install to `$HOME/.config/panzer/`.

Custom styles have been added. These styles use custom filter and postflight
scripts, as well as custom metadata files.

## Custom styles ##

Standard

* Replacement base style
* Adds filter scripts: metadata_files,
  [pandoc-fignos](https://github.com/tomduck/pandoc-fignos),
  [pandoc-eqnos](https://github.com/tomduck/pandoc-eqnos), and
  [pandoc-tablenos](https://github.com/tomduck/pandoc-tablenos)
* Adds postflight script: createmobi


PaginateSections

* Add page break at the start of each H1 section
* Adds filter script: paginatesects

IncludeFiles

* Include content from other markdown files
* Adds filter script: includefiles

FlushSections

* Flush all floats at the end of each section
* Uses metadata file `m_latex_flush-sect.md` to add package `placeins` with option `section`

FlushSubsections

* Flush all floats at the end of each subsection
* Uses metadata file `m_latex_flush-subsect.md` to add package `placeins` with
  option `section`, and redefines internal commands to flush subsects instead
  of sects

Latex\[8|9|10|11|12|14|17|20\]pt

* Change font size to 8, 9, 10, 11, 12, 14, 17, or 20 pt
* Uses metadata files `m_latex_font-size-[8|9|10|11|12|14|17|20]pt` to change
  document class to `extarticle` and apply a font size

## Custom scripts ##

metadata_files

* Makes available an additional metadata field called `metadata-file`
    * This field can be used in the source markdown file or in the panzer style
      file as part of style definitions
* This field can hold a single inline value or a list of multiple values
* Each value is a path to a markdown file
    * Can be a full path or path relative to the current working directory
    * If file is not a valid path, look in current directory, then
      `$HOME/.config/panzer/custom`, and finally in `$HOME/.panzer/custom`
* The yaml metadata header in each markdown files is processed
    * These fields are additive in the sense used by
      [panzer](https://github.com/msprev/panzer)
    * If the same setting is specified in more than one metadata file, the
      last one processed will 'win', except for `header-includes` fields which
      are cumulative, except that a `header-includes` field in the source
      metadata file will completely replace all such fields in additional
      metadata files

createmobi

* Uses the cli utility `ebook-convert` from the `calibre` application to create
  an additional `mobi` output file when an `epub` file is output

paginatesects

* Add `\newpage` command before each level 1 header
* Adjusts page counter appropriately

includefiles

* Adds directive `INCLUDEFILE` which can be used to insert another document in
  the current document at the location of, and replacing, the directive
* The `INCLUDEPREFIX` directive can be used to supply a directory path which
  will be prefixed to all subsequent `INCLUDEFILE` paths
* Designed for markdown files; YMMV using this filter with other document
  types
