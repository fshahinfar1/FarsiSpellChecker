import string


def normalize_chars(txt):
    """
    convert some arabic characters to farsi
    """
    txt = txt.replace('ي', 'ی')
    txt = txt.replace('ة', 'ه')
    txt = txt.replace('ئ', 'ی')
    return txt


def clean_punctuation(txt):
    punctuation = ('"', "'", ')', '(', '!', '.', ',', '،',
    '«', '»', '\\', '/', 'ˈ', '-', '_', '*', ']', '[', '|', 'ـ')
    for c in punctuation:
        txt = txt.replace(c, '')
    return txt


def clean_numbers(txt):
    for d in string.digits:
        txt = txt.replace(d, '')
    farsi_digits = '۰۱۲۳۴۵۶۷۸۹'
    for d in farsi_digits:
        txt = txt.replace(d, '')
    return txt


def clean_blacklist(txt):
    blacklist = ('', '\r', '	')
    for c in blacklist:
        txt = txt.replace(c, '')
    txt = txt.replace('\t', ' ')
    return txt

