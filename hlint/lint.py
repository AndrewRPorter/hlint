#!/usr/bin/python

# Copyright (c) 2007-2008 Mozilla Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from __future__ import print_function, with_statement

import sys
import re
import string
import gzip

# Several "try" blocks for python2/3 differences (@secretrobotron)
try:
    import httplib
except ImportError:
    import http.client as httplib

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO

try:
    maketrans = str.maketrans
except AttributeError:
    maketrans = string.maketrans


class Result(object):
    def __init__(self):
        self.dirty = 0


def valid(fileName):
    #
    # Begin
    #
    extPat = re.compile(r"^.*\.([A-Za-z]+)$")
    extDict = {
        "html": "text/html",
        "htm": "text/html",
        "xhtml": "application/xhtml+xml",
        "xht": "application/xhtml+xml",
        "xml": "application/xml",
    }

    forceXml = False
    forceHtml = False
    gnu = False
    errorsOnly = False
    encoding = None
    contentType = None
    inputHandle = None
    service = "https://html5.validator.nu/"

    #
    # Ensure a maximum of one forced output type
    #
    if forceXml and forceHtml:
        sys.stderr.write("Cannot force HTML and XHTML at the same time.\n")
        return False

    #
    # Set contentType
    #
    if forceXml:
        contentType = "application/xhtml+xml"
    elif forceHtml:
        contentType = "text/html"
    elif fileName:
        m = extPat.match(fileName)
        if m:
            ext = m.group(1)
            ext = ext.translate(
                maketrans(string.ascii_uppercase, string.ascii_lowercase)
            )
            if ext in extDict:
                contentType = extDict[ext]
            else:
                sys.stderr.write(
                    "Unable to guess Content-Type from file name. Please force the type.\n"
                )
                return False
        else:
            sys.stderr.write(
                "Could not extract a filename extension. Please force the type.\n"
            )
            return False
    else:
        sys.stderr.write("Need to force HTML or XHTML when reading from stdin.\n")
        return False

    if encoding:
        contentType = "%s; charset=%s" % (contentType, encoding)

    #
    # Read the file argument (or STDIN)
    #
    if fileName:
        inputHandle = fileName
    else:
        inputHandle = sys.stdin

    with open(inputHandle, mode="rb") as inFile:
        data = inFile.read()
        with BytesIO() as buf:
            # we could use another with block here, but it requires Python 2.7+
            zipFile = gzip.GzipFile(fileobj=buf, mode="wb")
            zipFile.write(data)
            zipFile.close()
            gzippeddata = buf.getvalue()

    #
    # Prepare the request
    #
    url = service

    if gnu:
        url = url + "?out=gnu"
    else:
        url = url + "?out=text"

    if errorsOnly:
        url = url + "&level=error"

    connection = None
    response = None
    status = 302
    redirectCount = 0

    #
    # Make the request
    #
    while status in (302, 301, 307) and redirectCount < 10:
        if redirectCount > 0:
            url = response.getheader("Location")
        parsed = urlparse.urlsplit(url)

        if redirectCount > 5:
            sys.stdout.write("Failed to make connection!")
            return False

        if parsed.scheme == "https":
            connection = httplib.HTTPSConnection(parsed[1])
        else:
            connection = httplib.HTTPConnection(parsed[1])

        headers = {
            "Accept-Encoding": "gzip",
            "Content-Type": contentType,
            "Content-Encoding": "gzip",
            "Content-Length": len(gzippeddata),
            "User-Agent": "html5check",
        }
        urlSuffix = "%s?%s" % (parsed[2], parsed[3])

        connection.connect()
        connection.request("POST", urlSuffix, body=gzippeddata, headers=headers)

        response = connection.getresponse()
        status = response.status

        redirectCount += 1

    #
    # Handle the response
    #
    if status != 200:
        sys.stderr.write("%s %s\n" % (status, response.reason))
        return False

    if response.getheader("Content-Encoding", "identity").lower() == "gzip":
        response = gzip.GzipFile(fileobj=BytesIO(response.read()))

    if fileName and gnu:
        quotedName = '"%s"' % fileName.replace("'", "\\042")
        for line in response.read().split("\n"):
            if line:
                sys.stdout.write(quotedName)
                sys.stdout.write(line + "\n")
    else:
        output = response.read()
        # python2/3 difference in output's type
        if not isinstance(output, str):
            output = output.decode("utf-8")

        if (
            output.strip()
            == "The document is valid HTML5 + ARIA + SVG 1.1 + MathML 2.0 (subject to the utter previewness of this service)."
        ):
            connection.close()
            return True
        else:
            sys.stdout.write("\n" + fileName + "\n===============\n")
            sys.stdout.write(output)
            connection.close()
            return False


def check(file):
    flag = valid(file)
    return flag
    

def check_files(file_list):
    results = {}

    for f in file_list:
        flag = valid(f)
        
        if not flag:
            results[f] = flag

    if results:
        for key, value in results.items():
            print(key, value)

    return results
