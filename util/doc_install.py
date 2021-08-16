#!/usr/bin/env python3

# doc_install.py [OPTION]... [-T] SOURCE DEST
# doc_install.py [OPTION]... SOURCE... DIRECTORY
# doc_install.py [OPTION]... -t DIRECTORY SOURCE...

# Copy SOURCE to DEST or multiple SOURCE files to the existing DIRECTORY,
# while setting permission modes. For HTML files, translate references to
# external documentation.

# Mandatory arguments to long options are mandatory for short options, too.
#       --book-base=BASEPATH          use reference BASEPATH for Devhelp book
#   -l, --tag-base=TAGFILE\@BASEPATH   use BASEPATH for references from TAGFILE (Doxygen <= 1.8.15)
#   -l, --tag-base=s\@BASEPUB\@BASEPATH substitute BASEPATH for BASEPUB (Doxygen >= 1.8.16)
#   -m, --mode=MODE                   override file permission MODE (octal)
#   -t, --target-directory=DIRECTORY  copy all SOURCE arguments into DIRECTORY
#   -T, --no-target-directory         treat DEST as normal file
#       --glob                        expand SOURCE as filename glob pattern
#   -v, --verbose                     enable informational messages
#   -h, --help                        display help and exit

import os
import sys
import re
import glob

# Globals
g_verbose = False
tags_dict = {}
subst_dict = {}
perm_mode = 0o644
g_book_base = None
html_doxygen_count = 0

message_prefix = os.path.basename(__file__) + ':'

# The installed files are read and written in binary mode.
# All regular expressions and replacement strings must be bytes objects.
html_start_pattern = re.compile(rb'\s*(?:<[?!][^<]+)*<html[>\s]')
html_split1_pattern = re.compile(rb'''
  \bdoxygen="([^:"]+):([^"]*)"  # doxygen="(TAGFILE):(BASEPATH)"
  \s+((?:href|src)=")\2([^"]*") # (href="|src=")BASEPATH(RELPATH")
  ''', re.VERBOSE)
html_split2_pattern = re.compile(rb'''
  \b((?:href|src)=")([^"]+") # (href="|src=")(BASEPUB RELPATH")
  ''', re.VERBOSE)

devhelp_start_pattern = re.compile(rb'\s*(?:<[?!][^<]+)*<book\s')
devhelp_subst_pattern = re.compile(rb'(<book\s+[^<>]*?\bbase=")[^"]*(?=")')

def notice(*msg):
  if g_verbose:
    print(message_prefix, ''.join(msg))

def error(*msg):
  print(message_prefix, 'Error:', ''.join(msg), file=sys.stderr)
  raise RuntimeError(''.join(msg))

def html_split1_func(group1, group2):
  global html_doxygen_count
  if group1 in tags_dict:
    html_doxygen_count += 1
    return tags_dict[group1]
  return group2

def html_split2_func(group2):
  for key in subst_dict:
    # Don't use regular expressions here. key may contain characters
    # that are special in regular expressions.
    if group2.startswith(key):
      return subst_dict[key] + group2[len(key):]
  return None

def install_file(in_name, out_name):
  '''
  Copy file to destination while translating references on the fly.
  '''
  global html_doxygen_count

  # Some installed files are binary (e.g. .png).
  # Read and write all files in binary mode, thus avoiding decoding/encoding errors.
  in_basename = os.path.basename(in_name)
  with open(in_name, mode='rb') as in_file:
    # Read the whole file into a string buffer.
    buf = in_file.read()

  if (tags_dict or subst_dict) and html_start_pattern.match(buf):
    # Probably an html file. Modify it, if appropriate.
    #
    # It would be possible to modify with a call to Pattern.sub() or Pattern.subn()
    # and let a function calculate the replacement string. Example:
    # (buf, number_of_subs) = html_split2_pattern.subn(html_subst2_func, buf)
    # A previous Perl script does just that. However, calling a function from
    # sub() or subn() is a slow operation. Installing doc files for a typical
    # module such as glibmm or gtkmm takes about 8 times as long as with the
    # present split+join solution. (Measured with python 3.9.5)
    html_doxygen_count = 0
    number_of_subs = 0
    change = 'no'
    if tags_dict and b'doxygen="' in buf:
      # Doxygen 1.8.15 and earlier stores the tag file name and BASEPATH in the html files.
      split_buf = html_split1_pattern.split(buf)
      for i in range(0, len(split_buf)-4, 5):
        basepath = html_split1_func(split_buf[i+1], split_buf[i+2])
        split_buf[i+1] = b''
        split_buf[i+2] = b''
        split_buf[i+3] += basepath
      number_of_subs = len(split_buf) // 5
      if number_of_subs > 0:
        buf = b''.join(split_buf)
        change = 'rewrote ' + str(html_doxygen_count) + ' of ' + str(number_of_subs)

    if number_of_subs == 0 and subst_dict:
      # Doxygen 1.8.16 and later does not store the tag file name and BASEPATH in the html files.
      # The previous html_split1_pattern.split() won't find anything to substitute.
      split_buf = html_split2_pattern.split(buf)
      for i in range(2, len(split_buf), 3):
        basepath = html_split2_func(split_buf[i])
        if basepath:
          split_buf[i] = basepath
          html_doxygen_count += 1
      number_of_subs = len(split_buf) // 3
      if html_doxygen_count > 0:
        buf = b''.join(split_buf)
      if number_of_subs > 0:
        change = 'rewrote ' + str(html_doxygen_count)
    notice('Translating ', in_basename, ' (', change, ' references)')

  elif g_book_base and devhelp_start_pattern.match(buf):
    # Probably a devhelp file.
    # Substitute new value for attribute "base" of element <book>.
    (buf, number_of_subs) = devhelp_subst_pattern.subn(rb'\1' + g_book_base, buf, 1)
    change = 'rewrote base path' if number_of_subs else 'base path not set'
    notice('Translating ', in_basename, ' (', change, ')')
  else:
    # A file that shall not be modified.
    notice('Copying ', in_basename)

  with open(out_name, mode='wb') as out_file:
    # Write the whole buffer into the target file.
    out_file.write(buf)

  os.chmod(out_name, perm_mode)

def split_key_value(mapping):
  '''
  Split TAGFILE@BASEPATH or s@BASEPUB@BASEPATH argument into key/value pair
  '''
  (name, path) = mapping.split('@', 1)
  if name != 's': # Doxygen 1.8.15 and earlier
    if not name:
      error('Invalid base path mapping: ', mapping)
    if path != None:
      return (name, path, False)
    notice('Not changing base path for tag file ', name);

  else: # name=='s', Doxygen 1.8.16 and later
    (name, path) = path.split('@', 1)
    if not name:
      error('Invalid base path mapping: ', mapping)
    if path != None:
      return (name, path, True)
    notice('Not changing base path for ', name);

  return (None, None, None)

def string_to_bytes(s):
  if isinstance(s, str):
    return s.encode('utf-8')
  return s # E.g. None

def make_dicts(tags):
  global tags_dict, subst_dict

  tags_dict = {}
  subst_dict = {}
  if not tags:
    return

  for tag in tags:
    (name, path, subst) = split_key_value(tag)
    if subst == None:
      continue
    # Translate a local absolute path to URI.
    path = path.replace('\\', '/').replace(' ', '%20')
    if path.startswith('/'):
      path = 'file://' + path
    path = re.sub(r'^([A-Za-z]:/)', r'file:///\1', path, count=1) # Windows: C:/path
    if not path.endswith('/'):
      path += '/'
    if subst:
      notice('Using base path ', path, ' for ', name)
      subst_dict[string_to_bytes(name)] = string_to_bytes(path)
    else:
      notice('Using base path ', path, ' for tag file ', name)
      tags_dict[string_to_bytes(name)] = string_to_bytes(path)

def doc_install_funcargs(sources=[], target=None, book_base=None, tags=[],
  mode=0o644, target_is_dir=True, expand_glob=False, verbose=False):
  '''
  Copy source files to target files or target directory.
  '''
  global g_verbose, perm_mode, g_book_base

  g_verbose = verbose
  perm_mode = mode
  make_dicts(tags)
  g_book_base = string_to_bytes(book_base)

  if not target:
    error('Target file or directory required.')
  if book_base:
    notice('Using base path ', book_base, ' for Devhelp book')

  if not target_is_dir:
    if expand_glob:
      error('Filename globbing requires target directory.')
    if len(sources) != 1:
      error('Only one source file allowed when target is a filename.')

    install_file(sources[0], target)
    return 0

  if expand_glob:
    expanded_sources = []
    for source in sources:
      expanded_sources += glob.glob(source)
    sources = expanded_sources

  basename_set = set()
  for source in sources:
    basename = os.path.basename(source)

    # If there are multiple files with the same base name in the list, only
    # the first one will be installed. This behavior makes it very easy to
    # implement a VPATH search for each individual file.
    if basename not in basename_set:
      basename_set.add(basename)
      out_name = os.path.join(target, basename)
      install_file(source, out_name)
  return 0

def doc_install_cmdargs(args=None):
  '''
  Parse command line parameters, or a sequence of strings equal to
  command line parameters. Then copy source files to target file or
  target directory.
  '''
  import argparse

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    prog=os.path.basename(__file__),
    usage='''
      %(prog)s [OPTION]... [-T] SOURCE DEST
      %(prog)s [OPTION]... SOURCE... DIRECTORY
      %(prog)s [OPTION]... -t DIRECTORY SOURCE...''',
    description='''
      Copy SOURCE to DEST or multiple SOURCE files to the existing DIRECTORY,
      while setting permission modes. For HTML files, translate references to
      external documentation.'''
  )
  parser.add_argument('--book-base', dest='book_base', metavar='BASEPATH',
    help='use reference BASEPATH for Devhelp book')
  parser.add_argument('-l', '--tag-base', action='append', dest='tags', metavar='SUBST',
    help='''TAGFILE@BASEPATH   use BASEPATH for references from TAGFILE (Doxygen <= 1.8.15)
s@BASEPUB@BASEPATH substitute BASEPATH for BASEPUB (Doxygen >= 1.8.16)'''
  )
  parser.add_argument('-m', '--mode', dest='mode', metavar='MODE', default='0o644',
    help='override file permission MODE (octal)')

  group = parser.add_mutually_exclusive_group()
  group.add_argument('-t', '--target-directory', dest='target_dir', metavar='DIRECTORY',
    help='copy all SOURCE arguments into DIRECTORY')
  group.add_argument('-T', '--no-target-directory', action='store_false', dest='target_is_dir',
    help='treat DEST as normal file')

  parser.add_argument('--glob', action='store_true', dest='expand_glob',
    help='expand SOURCE as filename glob pattern')
  parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
    help='enable informational messages')
  parser.add_argument('source_dest', nargs='+',
    help='''SOURCE DEST
SOURCE... DIRECTORY
SOURCE...'''
  )
  parsed_args = parser.parse_args(args)

  if not parsed_args.target_is_dir:
    if len(parsed_args.source_dest) != 2:
      error('Source and destination filenames expected.')
    sources = [parsed_args.source_dest[0]]
    target = parsed_args.source_dest[1]
  else:
    target = parsed_args.target_dir
    if not target:
      if len(parsed_args.source_dest) < 2:
        error('At least one source file and destination directory expected.')
      target = parsed_args.source_dest[-1]
      sources = parsed_args.source_dest[0:-1]
    else:
      sources = parsed_args.source_dest

  return doc_install_funcargs(
    sources=sources,
    target=target,
    book_base=parsed_args.book_base,
    tags=parsed_args.tags,
    mode=int(parsed_args.mode, base=8),
    target_is_dir=parsed_args.target_is_dir,
    expand_glob=parsed_args.expand_glob,
    verbose=parsed_args.verbose
  )

# ----- Main -----
if __name__ == '__main__':
  sys.exit(doc_install_cmdargs())
