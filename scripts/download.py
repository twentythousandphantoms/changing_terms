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


pdf_path = '../pdf/'
terms_path = '../terms/'

urls = [
    'https://donate.fbk.info/files/oferta.pdf',
    'https://acdn.tinkoff.ru/static/documents/627ee150-0276-4a81-9d0c-8be1e265ae87.pdf',
    'https://static.tinkoff.ru/documents/credit_cards/consumer_loan.pdf',
    'https://acdn.tinkoff.ru/static/documents/loyalty-program-target_rules.pdf',
    'https://acdn.tinkoff.ru/static/documents/9fd26052-7200-4593-aa8e-97ad4d5ccd06.pdf',
    'https://acdn.tinkoff.ru/static/documents/1b2a4c18-768a-4d0d-883c-bc43b56874bb.pdf',
    # TODO: Check pdf file another way
    'https://www.tinkoff.ru/api/tinsurance/document/static?fileId=8052e01b-7513-44ea-b7a0-cbb5400e56f4',
    'https://fs.moex.com/f/3499/agreement.pdf'
]


def download_doc(url, path=pdf_path):
    ext = tldextract.extract(url)
    domain_name = ext.domain
    parsed = urlparse(url)
    filename = domain_name + '__' + os.path.basename(parsed.path)

    response = requests.get(url, stream=True)

    with open(path + filename, 'wb') as f:
        f.write(response.content)

    return filename


def is_pdf(file, path=pdf_path):
    return file.endswith('.pdf')


def pdf_to_html(pdf, input_dir, output_dir=terms_path):
    print(f'{pdf} is pdf :) and gonna to be converted to html')
    output = BytesIO()
    html_file_name = f"{pdf}.html"

    with open(input_dir + pdf, 'rb') as pdf_file:
        extract_text_to_fp(pdf_file, output, laparams=LAParams(), output_type='html', codec='utf-8')
    with open(output_dir + html_file_name, 'wb') as html_file:
        html_file.write(output.getvalue())

    print('done.')
    return html_file_name


def html_to_md(html_file_name, path=terms_path):
    print(f'{html_file_name} is gonna be converted to markdown')

    md_file_name = f'{html_file_name}.md'

    html_content = open(path + html_file_name, "r").read()
    output = markdownify(html_content, heading_style="ATX")
    with open(path + md_file_name, 'w') as md_file:
        md_file.write(output)

    print('done.')
    return md_file_name


def main():
    while urls:
        url = urls.pop()
        terms = (download_doc(url))
        if is_pdf(terms):
            name = pdf_to_html(terms, pdf_path, terms_path)
            print(html_to_md(name, terms_path))
        else:
            print(terms + ' is NOT pdf :(')

if __name__ == '__main__':
    main()
