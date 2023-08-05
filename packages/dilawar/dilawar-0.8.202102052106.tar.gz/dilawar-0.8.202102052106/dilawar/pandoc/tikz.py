#!/usr/bin/env python3

"""
Pandoc filter to process raw latex tikz environments into images.
Assumes that pdflatex is in the path, and that the standalone
package is available.  Also assumes that ImageMagick's convert
is in the path. Images are put in the tikz-images directory.

CREDIT: Did I write this? Or downloaded it from somewhere? Oh the mystery.
"""

import os
import subprocess
import shutil
import sys
from subprocess import call
from tempfile import mkdtemp

from pandocfilters import (
    toJSONFilter,
    Para,
    Image,
    get_filename4code,
    get_extension,
    get_caption,
)


def print1(*args):
    print(*args, file=sys.stderr)


def tikz2image(tikz_src, filetype, outfile):
    tmpdir = mkdtemp()
    olddir = os.getcwd()
    os.chdir(tmpdir)
    f = open("tikz.tex", "w")
    f.write(
        """\\documentclass{standalone}
             \\usepackage{tikz}
             \\usetikzlibrary{positioning,calc,shapes,arrows,arrows.meta}
             \\begin{document}
             """
    )
    f.write(tikz_src)
    f.write("\n\\end{document}\n")
    f.close()
    call(["lualatex", "--shell-escape", "tikz.tex"], stdout=sys.stderr)
    os.chdir(olddir)
    if filetype == "pdf":
        shutil.copyfile(tmpdir + "/tikz.pdf", outfile + ".pdf")
    else:
        call(["convert", tmpdir + "/tikz.pdf", outfile + "." + filetype])
    shutil.rmtree(tmpdir)

def to_format(txt : str, fmt : str) -> str:
    cmd = f"pandoc -t {fmt}"
    s = subprocess.check_output(cmd.split(" "), input=txt, encoding='utf8')
    assert s, s
    return s

def _get_caption(item, fmt : str):
    captions, typef, keyvals = get_caption(item)
    #for caption in captions:
    #    if caption['c'] is None and caption['c']:
    #        continue
    #    caption['c'] = to_format(caption['c'], fmt)
    #    print1(caption)
    return captions, typef, keyvals


def tikz(key, value, format, _):
    if key == "CodeBlock":
        [[ident, classes, keyvals], code] = value
        if set(classes).intersection(set(["latex", "tex", "tikz"])):
            outfile = get_filename4code("tikz", code)
            filetype = get_extension(format, "png", html="png", latex="pdf")
            src = outfile + "." + filetype
            if not os.path.isfile(src):
                tikz2image(code, filetype, outfile)
                sys.stderr.write("Created image " + src + "\n")
            caption, typef, keyvals = _get_caption(keyvals, format)
            return Para([Image([ident, [], keyvals], caption, [src, typef])])

if __name__ == "__main__":
    toJSONFilter(tikz)
