import os
import requests
from urllib.parse import urlparse
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from io import StringIO
from io import BytesIO
import codecs


import tldextract

from markdownify import markdownify


path = '../terms/'

urls = [
    'https://benjamins.com/catalog/term.4.1.08bes/fulltext/term.4.1.08bes.pdf',
    # 'https://nuzhnapomosh.ru/wp-content/themes/takiedela/assets/pdf/oferta_personal.pdf',
    # 'http://prostor-sklad.ru/docs/terms_of_use.pdf',
    # 'https://docs.github.com/en/free-pro-team@latest/github/site-policy/github-terms-of-service'
]


def download_doc(url, path='/tmp/'):
    ext = tldextract.extract(url)
    domain_name = ext.domain
    parsed = urlparse(url)
    filename = domain_name + '__' + os.path.basename(parsed.path)

    response = requests.get(url, stream=True)

    with open(path + filename, 'wb') as f:
        f.write(response.content)

    return path + filename


def is_pdf(file):
    return file.endswith('.pdf')


# TODO: fix this
# TypeError: string argument expected, got 'bytes'
def pdf_to_html(pdf):
    print(f'{pdf} is pdf :) and gonna to be converted to html')
    output = BytesIO()
    html_file_name = "intermediate.html"

    with open(pdf, 'rb') as pdf_file:
        extract_text_to_fp(pdf_file, output, laparams=LAParams(), output_type='html', codec='utf-8')
    with open(html_file_name, 'wb') as html_file:
        html_file.write(output.getvalue())

    print('done.')
    return html_file_name


def html_to_md(html_file_name):
    print(f'{html_file_name} is gonna be converted to markdown')

    md_file_name = f'{html_file_name}.md'

    html_content = open(html_file_name, "r").read()
    output = markdownify(html_content, heading_style="ATX")
    with open(md_file_name, 'w') as md_file:
        md_file.write(output)

    print('done.')
    return md_file_name


def main():
    while urls:
        url = urls.pop()
        terms = (download_doc(url))
        if is_pdf(terms):
            name = pdf_to_html(terms)
            print(html_to_md(name))
        else:
            print(terms + ' is NOT pdf :(')

if __name__ == '__main__':
    main()
