#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================== IMPORTS
import sys
import os
import bs4 as bs
import urllib.request as request
# =============================================== FUNCTIONS

SWITCH = {
    "plato.stanford.edu" : lambda soup: soup.find(
    #    'div', id="article-content"
    #).find(
        'div', id="aueditable"
    ),
    "towardsdatascience.com" : lambda soup: soup.find(
        'div', {"class" : "section-content"}
    ),
}

def print_usage():
    print('usage: minify.py <url> [<out_path>] [-o|--open]')

def main():
    args = sys.argv[1:]

    if not args or args[0] in ["-h", "--help"]:
        print_usage()
        sys.exit(1)
    # get arguments
    url = args[0]
    out_path = None if len(args) < 2 else os.path.abspath(args[1])
    if not len(args) < 3:
        if args[2] in ["-o", "--open"]:
            open_browser = True
        else:
            print("Could not parse arguments.")
            print_usage()
            sys.exit(1)
    else:
        open_browser = False

    # get base page url
    base_url = get_base_url(url)

    # Check wether page is covered, if so minify
    try:
        soup_filter_func = SWITCH[base_url]
    except KeyError:
        print(base_url + " not covered. ")
        sys.exit(1)
    minified_html = minify_html(url, soup_filter_func)

    # Return minified html
    if out_path is None:
        sys.stdout.write(minified_html)
    else:
        if os.path.isfile(out_path):
            if input("File exists. Overwrite? [y/n] ").lower() != "y":
                print("Aborted.")
                sys.exit(2)
        with open(out_path, "w") as f:
            f.write(minified_html)
            print("Written to " + out_path)
        if open_browser:
            import webbrowser
            webbrowser.open_new(out_path)
        sys.exit(0)


def get_base_url(url):
    url = url.replace(
        "https://", ''
    ).replace(
        "http://", ''
    )
    return url.split('/')[0]


def minify_html(url, soup_filter_func):
    r = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    source_html = request.urlopen(r).read()
    soup = bs.BeautifulSoup(source_html, 'html.parser')
    content = soup_filter_func(soup)

    template_html_1 = """
        <html>
            <head>
                <script type="text/x-mathjax-config">
                  MathJax.Hub.Config({
                    tex2jax: {
                      inlineMath: [ ['$','$'], ["\\\\(","\\\\)"] ],
                      processEscapes: true
                    }
                  });
                </script>
                <script type="text/javascript"
                    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
                </script>

                <!-- https://github.com/nicokant/readable-css -->
                <link href="https://unpkg.com/readable-css/css/readable.css" rel="stylesheet" />
            </head>
            <body>
                <div class="readable-content">
    """
    template_html_2 = """
                </div>
            </body>
        </html>
    """
    buffer_str = "\n" + " "*20
    minified_html = "\n".join([
        str(e) for e in content
    ])
    minified_html = minified_html.replace("\n", buffer_str)
    minified_html = buffer_str + template_html_1 + minified_html + template_html_2
    return minified_html

# =============================================== ENTRY
if __name__ == '__main__':
    main()


