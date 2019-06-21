import string


def normalize(txt):
    txt = txt.replace('ي', 'ی')
    txt = txt.replace('ة', 'ه')
    txt = txt.replace('ئ', 'ی')
    return txt


def clean(txt):
    for d in string.digits:
        txt = txt.replace(d, '')
    punctuation = ('"', "'", ')', '(', '!', '.', ',', '،', '>', '<',
    '«', '»', '\\', '/', 'ˈ', '-', '_', '*', ']', '[', '|', 'ـ')
    for c in punctuation:
        txt = txt.replace(c, '')
    farsi_digits = '۰۱۲۳۴۵۶۷۸۹'
    for d in farsi_digits:
        txt = txt.replace(d, '')
    blacklist = ('', '\r', '	')
    for c in blacklist:
        txt = txt.replace(c, '')
    txt = txt.replace('\t', ' ')
    return txt

