#!/usr/bin/env python3

# doc_postprocess.py [-h|--help] <pattern>...

# Post-process the Doxygen-generated HTML files matching pattern.

import os
import sys
import re
import glob

# Substitutions with regular expressions are somewhat slow in Python 3.9.5.
# Use str.replace() rather than re.sub() where possible.

# [search string, compiled regular expression or None, substitution string, count]
class_el_patterns = [
  # return value
  [ ' &amp;&nbsp;', re.compile(r' &amp;&nbsp; *'), '&amp;&#160;', 1],
  [ ' *&nbsp;', re.compile(r' \*&nbsp; *'), '*&#160;', 1],
  # parameters
  [ ' &amp;', None, '&amp;', 0],
  [ '&amp;', re.compile(r'&amp;\b'), '&amp; ', 0],
  [ ' *', None, '*', 0],
  [ '*', re.compile(r'\*\b'), '* ', 0],
  # templates
  [ 'template&lt;', re.compile(r'\btemplate&lt;'), 'template &lt;', 1]
]

class_md_patterns = [
  # left parenthesis
  [ '(&nbsp;', re.compile(r'\(&nbsp; *'), '(', 1],
  # return value
  [ ' &amp; ', None, '&amp; ', 0],
  [ ' * ', None, '* ', 0],
  # parameters
  [ ' &amp;&nbsp;', re.compile(r' &amp;&nbsp; *'), '&amp;&#160;', 0],
  [ ' *&nbsp;', re.compile(r' \*&nbsp; *'), '*&#160;', 0],
  # templates
  [ 'template&lt;', re.compile(r'\btemplate&lt;'), 'template &lt;', 1]
]

else_patterns = [
  # template decls
  [ 'template&lt;', re.compile(r'^(<h\d>|)template&lt;'), '\\1template &lt;', 1]
]

all_lines_patterns = [
  # For some reason, some versions of Doxygen output the full path to
  # referenced tag files. This is bad since it breaks doc_install.py,
  # and also because it leaks local path names into source tarballs.
  # Thus, strip the directory prefix here.
  [ ' doxygen="', re.compile(r' doxygen="[^":]*/([^":]+\.tag):'), ' doxygen="\\1:', 0],

  [ '&copy;', None, '&#169;', 0],
  [ '&mdash;', None, '&#8212;', 0],
  [ '&ndash;', None, '&#8211;', 0],
  [ '&nbsp;', re.compile(r' *&nbsp; *'), '&#160;', 0]
]

def doc_postprocess(patterns):
  if not (isinstance(patterns, list) or isinstance(patterns, tuple)):
    patterns = [] if patterns == None else [patterns]

  filepaths = []
  for pattern in patterns:
    filepaths += glob.glob(pattern)

  for filepath in filepaths:
    # Assume that the file is UTF-8 encoded.
    # If illegal UTF-8 bytes in the range 0x80..0xff are encountered, they are
    # replaced by Unicode Private Use characters in the range 0xdc80..0xdcff
    # and restored to their original values when the file is rewritten.
    with open(filepath, mode='r', encoding='utf-8', errors='surrogateescape') as file:
      # Read the whole file into a buffer, a list with one line per element.
      buf = file.readlines()

    for line_number in range(len(buf)):
      line = buf[line_number]

      # Substitute
      if '<a class="el"' in line:
        for subst in class_el_patterns:
          if subst[0] in line:
            if subst[1]:
              line = subst[1].sub(subst[2], line, count=subst[3])
            else:
              line = line.replace(subst[0], subst[2], subst[3])

      elif ('<td class="md"' in line) or ('<td class="mdname"' in line):
        for subst in class_md_patterns:
          if subst[0] in line:
            if subst[1]:
              line = subst[1].sub(subst[2], line, count=subst[3])
            else:
              line = line.replace(subst[0], subst[2], subst[3])

      else:
        for subst in else_patterns:
          if subst[0] in line:
            if subst[1]:
              line = subst[1].sub(subst[2], line, count=subst[3])
            else:
              line = line.replace(subst[0], subst[2], subst[3])

      for subst in all_lines_patterns:
        if subst[0] in line:
          if subst[1]:
            line = subst[1].sub(subst[2], line, count=subst[3])
          else:
            line = line.replace(subst[0], subst[2], subst[3])

      buf[line_number] = line

    with open(filepath, mode='w', encoding='utf-8', errors='surrogateescape') as file:
      # Write the whole buffer back into the file.
      file.writelines(buf)

  return 0

# ----- Main -----
if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(
    description='Post-process the Doxygen-generated HTML files matching pattern.')
  parser.add_argument('patterns', nargs='*', metavar='pattern', help='filename pattern')
  args = parser.parse_args()
  print(args.patterns)

  sys.exit(doc_postprocess(args.patterns))
