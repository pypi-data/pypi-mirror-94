""" md
## Usage

Once this plugin is [installed](../README.md#installation), just replace
the plugin name `simple` with `semiliterate` in your `mkdocs.yml` file.
It accepts all of the same parameters, so `mkdocs` will still work as before,
and you will have immediate access to all of the following extensions.
(Note that this documentation assumes a familiarity with the
[usage](https://athackst.github.io/mkdocs-simple-plugin/mkdocs_simple_plugin/plugin/)
of the `simple` plugin.)
"""

from mkdocs import utils
from mkdocs.config import config_options
from mkdocs_simple_plugin.plugin import SimplePlugin, StreamExtract

import os
import re
import subprocess
import tempfile
import yaml


class StreamInclusion(StreamExtract):
    r""" md  An extension of the StreamExtract class which adds

### Inclusion syntax

While extracting content from a file (because it matches one of the
`semiliterate` patterns, rather than just one of the `include_extensions`),
an unescaped expression of the form

`{! FILENAME YAML !}`

(which may span multiple lines) will trigger file inclusion. The FILENAME may
be a bare word, in which case it cannot contain whitespace, or it may be
enclosed in single or double quotes. Note that FILENAME is interpreted relative
to the directory in which the file containing the `{! .. !}` expression
resides. The YAML is interpreted exactly as the extraction options to a
`semiliterate` item as
[documented](https://athackst.github.io/mkdocs-simple-plugin/mkdocs_simple_plugin/plugin/index.html#semiliterate)
for the `simple` extension. The text extracted from FILENAME
is interpolated at the current location in the file currently being written.
Recursive inclusion is supported.

The simplest example of such an inclusion directive is just
`{! boilerplate.md !}`, which (because of the conventions for extraction
parameters) simply interpolates the entire contents of `boilerplate.md`
at the current location.

For an example that uses more of the extraction parameters, the current
version number of mkdocs-semiliterate is extracted into the
[Overview](../README.md) of this documentation via

` {! ../README.md extract: { start: 'repo:.*(\{!.*!\})' }
terminate: Rationale
!}`

to take advantage of the beginning of the `setup.cfg` file:
```
{! ../setup.cfg terminate: long !}...
```

(and of course both of the code snippets just above are extracted into this
page with `{! ... !}`, as you can see in the
[source code](https://code.studioinfinity.org/glen/mkdocs-semiliterate/src/branch/main/mkdocs_semiliterate/plugin.py)
for the plugin.)

Note that a `{! ... !}` directive must be in a line that semiliterate would
normally copy. That is, semiliterate does not examine lines after
the `terminate` regexp, or when no mode of extraction is active.
It also doesn't check any text written from lines that match these
special expressions, including `start` and `stop`.
Moreover, on such normally-transcribed lines,
it's the text **after** the application of any semiliterate `replace`ments that
is checked for `{! ... !}`.
     """  # noqa: E501

    include_open = re.compile(r'''(?<![`\\])(\{\!\s*)([\s'"])''')
    include_quoted_file = re.compile(
        r'''(['"])(?P<fn>.*?)\1\s+(?P<yml>[\s\S]*?)\s?\!\}''')
    include_bare_file = re.compile(r'\s(?P<fn>.*?)\s+(?P<yml>[\s\S]*?)\s?\!\}')

    def extract_line(self, line):
        """Copy line to the output stream, applying all specified replacements
           and handling inclusion syntax.
        """
        line = self.replace_line(line)
        include_match = StreamInclusion.include_open.search(line)
        if not include_match:
            self.transcribe(line)
            return
        # OK, we have found (the start of) an inclusion and must process it
        preamble = line[:include_match.start()]
        remainder = line[include_match.end(1):]
        doublequoted = False
        body_pattern = StreamInclusion.include_quoted_file
        if include_match[2].isspace():
            body_pattern = StreamInclusion.include_bare_file
        elif include_match[2] == '"':
            doublequoted = True
        body_match = body_pattern.search(remainder)
        if not body_match:
            for extra_line in self.input_stream:
                remainder += self.replace_line(extra_line)
                body_match = body_pattern.search(remainder)
                if body_match:
                    break
        if not body_match:
            errmsg = "semiliterate: End of file while scanning for `!}`"
            utils.log.error(errmsg)
            raise EOFError(errmsg)
        filename = body_match['fn']
        gitextract = False
        r""" md
### Double-quoted filenames and Git extraction

Standard Python escape sequences in double-quoted filenames are interpreted
as usual; for example you can write
```
{! ../tests/fixtures/quoted-filename/README.md extract:
  start: '(.*!.*)'
  stop: '\s'
!}
```
to include a file whose name (`snippet/Say "Don't"`, in this case) has both
double and single quotes.

Further, `semiliterate` supports a special escape to extract a file from the
Git archive of the project (presuming it is under Git version control) and then
include content from that file. For example, you could write
```
{! ../tests/fixtures/git-inclusion/README.md extract:
  start: '(.*!.*)'
  stop: '\s'
!}
```

to extract content starting after the `### install` line from the
`mkdocs.yml` file in the Git commit of this repository
tagged `0.1.0`. This feature is primarily useful if you are documenting the
development or changes to a project over time, or are documenting a feature
in a specific past release of your project, and want to be sure that
material included in your documentation does _not_ change as the project
progresses. (This behavior is as opposed to the usual case, in which you want
your documentation to incorporate the most up-to-date version of extracted
content.)

The precise behavior for a FILENAME argument in a `{! ... !}` inclusion of the
form

`"\git SPECIFIER"`

is that the output of `git show SPECIFIER` is written to a temporary file,
and that file is extracted from.
"""
        if doublequoted:
            if filename[:5] == r'\git ':
                gitextract = True
                filename = filename[5:]
            filename = (filename.encode('latin-1', 'backslashreplace')
                                .decode('unicode-escape'))
        include_path = self.include_root + '/' + filename
        if gitextract:
            (write_handle, include_path) = tempfile.mkstemp()
            utils.log.info(
                f"semiliterate: extracting {filename} to {include_path}")
            contents = subprocess.check_output(['git', 'show', filename])
            os.write(write_handle, contents)
            os.close(write_handle)
        new_root = re.match(r'(.*)/', include_path)[1]
        try:
            include_parameters = yaml.safe_load(body_match['yml'])
        except Exception as err:
            newmsg = (f"While attempting to include '{include_path}', could"
                      + f" not parse yaml '{body_match['yml']}'.")
            if hasattr(err, 'message'):
                raise SyntaxError(
                    f"{newmsg} YAML parser reports: {err.message}")
            raise SyntaxError(f"{newmsg} Caught exception: {str(err)}")
        if not include_parameters:
            include_parameters = {}
        with open(include_path) as include_file:
            self.transcribe(preamble)
            inclusion = StreamInclusion(
                include_file, self.output_stream, include_root=new_root,
                **include_parameters)
            if inclusion.extract():
                self.wrote_something = True
        self.transcribe(remainder[body_match.end():])


class SemiliteratePlugin(SimplePlugin):
    r""" md   An extension of the mkdocs-simple-plugin

### Universal block-comment markdown

By default, `semiliterate` scans for block-comment markdown `/** md` ... `**/`
in all files with _any_ extension, as it's valid in so many disparate languages.
(As opposed to `simple`, which defaults to searching for such markdown in a
specific list of file types.)
    """

    super_sdict = dict(SimplePlugin.config_scheme)
    super_semi_dflt = super_sdict['semiliterate'].default
    semi_dflt = [b if 'js' not in b['pattern'] else dict(b, pattern=r'\.')
                 for b in super_semi_dflt]
    altered_config_scheme = dict(
        super_sdict,
        semiliterate=config_options.Type(list, default=semi_dflt)).items()

    add_param_doc = r""" md
### Additional plugin parameters

`semiliterate` adds a couple of new plugin parameters to further tailor its
behavior as compared to `simple`. They are described in this section, with
default values in parentheses at the beginning of each entry.

{! plugin.py extract:
  start: '[*]altered_config_scheme'
  replace:
  - ["\\('(.*)',\\s*$", '\1\n']
  - ['config_options.Type.*?default=([^\)]*)', ':  (\1)']
  - '^\s*#(.*\s*)$'
terminate: '^\s*\)'
!}
    """
    config_scheme = (
        # Note documentation of each new parameter **follows** the parameter.
        *altered_config_scheme,
        ('exclude_extensions',
         config_options.Type(list, default=['.o'])),
        # Files whose name contains a string in this list will not be processed
        #    by `semiliterate`, regardless of whether they might match
        #    `include_extensions`, the `semiliterate` patterns, or standard
        #    Markdown.
        ('copy_standard_markdown',
         config_options.Type(bool, default=False)),
        # Whether to add MkDocs' list of standard Markdown extensions to the
        #    `include_extensions` parameter so that Markdown files will be
        #    directly copied to the docsite. Note that the `simple` behavior
        #    corresponds to a _true_ value for `copy_standard_markdown`, but
        #    `semiliterate` still incorporates all standard Markdown files
        #    because of the following `extract_standard_markdown` parameter.
        ('extract_standard_markdown',
         config_options.Type(dict, default={}))
        # If the `enable` key of this dict parameter is true
        #    (it defaults to the opposite of `copy_standard_markdown`),
        #    it adds a semiliterate block causing extraction (and hence
        #    include-directive processing) from all standard Markdown files
        #    (as defined by MkDocs). The remaining keys of this parameter are
        #    included as parameters of that semiliterate block. Thus, the
        #    default values of the parameters arrange for Markdown files to be
        #    copied "as-is", except possibly for embedded inclusions.
        #    On the other hand, setting this parameter to `{enable: false}`
        #    (which is also the default when `copy_standard_markdown` is true)
        #    will prevent automatic extraction (and hence disable
        #    inclusion-directive processing) from standard Markdown files.
    )

    def build_docs(self):
        self.exclude_extensions = self.config['exclude_extensions']
        dflt_enable = False
        if not self.config['copy_standard_markdown']:
            self.include_extensions = self.config['include_extensions']
            dflt_enable = True
        if self.config['extract_standard_markdown'].get('enable', dflt_enable):
            ext_pat = '|'.join(re.escape(s) for s in utils.markdown_extensions)
            self.semiliterate.append(dict(
                pattern=re.compile(f"^(.*(?:{ext_pat}))$"),
                destination=r'\1',
                **self.config['extract_standard_markdown']))
        paths = []
        for root, directories, files in os.walk("."):
            if self.in_include_directory(root):
                document_root = self.build_docs_dir + root[1:]
                for f in files:
                    if any(ext in f for ext in self.exclude_extensions):
                        continue
                    paths.extend(self.copy_file(root, f, document_root))
                    paths.extend(self.extract_from(root, f, document_root))
            directories[:] = [d for d in directories
                              if self.in_search_directory(d, root)]
        return paths

    def try_extraction(self, original_file, root, new_file, **kwargs):
        extraction = StreamInclusion(
            original_file, new_file, include_root=root, **kwargs)
        return extraction.extract()
