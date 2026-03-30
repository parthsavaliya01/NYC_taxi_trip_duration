"""
Mnemonic tools using phonemes
"""

rooturl = 'http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/'
url_term_and_phones = rooturl + 'cmudict-0.7b'
url_phones = rooturl + 'cmudict-0.7b.phones'
url_symbols = rooturl + 'cmudict-0.7b.symbols'


def term_and_phones():
    return _text_to_term_and_phones(_get_cmu_raw_data_text())


def _get_cmu_raw_data_text(url=url_term_and_phones, encoding='latin1'):
    from pyckup import grab

    return grab(url).decode(encoding)


def _text_to_term_and_phones(text):
    for term, phones in map(
        methodcaller('split', sep=' ' * 2),
        filter(lambda x: not x.startswith(';;;'), text.splitlines()),
    ):
        yield term.lower(), phones.split(' ')


from functools import cached_property
from operator import methodcaller
from itertools import chain, product
from collections import Counter, defaultdict


class Phone:
    rooturl = 'http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/'
    url_term_and_phones = rooturl + 'cmudict-0.7b'
    url_phones = rooturl + 'cmudict-0.7b.phones'
    url_symbols = rooturl + 'cmudict-0.7b.symbols'
    encoding = 'latin1'

    def __init__(self, url_term_and_phones=None):
        self.url_term_and_phones = url_term_and_phones or self.url_term_and_phones

    @cached_property
    def tp(self):
        return dict(
            _text_to_term_and_phones(
                _get_cmu_raw_data_text(self.url_term_and_phones, self.encoding)
            )
        )

    def term_to_phones(self, sentence):
        terms = map(str.lower, sentence.split())
        phones = chain.from_iterable(map(self.tp.get, terms))
        return list(phones)

    @cached_property
    def phone_class(self):
        lines = _get_cmu_raw_data_text(self.url_phones).splitlines()
        return dict(map(methodcaller('split', sep='\t'), lines))

    @cached_property
    def phone_counts(self):
        return dict(Counter(chain.from_iterable(self.tp.values())).most_common())

    @cached_property
    def phones(self):
        # Note: url_phones contains
        return sorted(self.phone_counts)


def keys_for_value(d: dict):
    """An inverse of dict ``d``.
    If ``d`` is a mapping of ``(key, value)``, ``keys_for_value`` will return
    a dict of ``(unique_value, group_of_key)`` items.
    """
    inverse_d = defaultdict(list)

    for key, value in d.items():
        inverse_d[value].append(key)

    return dict(inverse_d)


class MajorSystem(Phone):
    """
    See:    https://en.wikipedia.org/wiki/Mnemonic_major_system

    >>> m = MajorSystem()

    The "Mnemonic Major System" (https://en.wikipedia.org/wiki/Mnemonic_major_system)
    assigns a set of similar phonemes to each digit:

    >>> assert m.phones_for_num == {
    ...     0: {'S', 'Z'},
    ...     1: {'D', 'DH', 'T', 'TH'},
    ...     2: {'N'},
    ...     3: {'M'},
    ...     4: {'R'},
    ...     5: {'L'},
    ...     6: {'CH', 'JH', 'SH'},
    ...     7: {'G', 'K'},
    ...     8: {'F', 'V'},
    ...     9: {'B', 'P'}
    ... }

    As a consequence these phonemes are mapped to numbers:

    >>> assert m.num_of_phone == {
    ...     'B': 9,
    ...     'CH': 6,
    ...     'D': 1,
    ...     'DH': 1,
    ...     'F': 8,
    ...     'G': 7,
    ...     'JH': 6,
    ...     'K': 7,
    ...     'L': 5,
    ...     'M': 3,
    ...     'N': 2,
    ...     'P': 9,
    ...     'R': 4,
    ...     'S': 0,
    ...     'SH': 6,
    ...     'T': 1,
    ...     'TH': 1,
    ...     'V': 8,
    ...     'Z': 0
    ... }

    Any sentence has a corresponding phoneme sequence:

    >>> m.term_to_phones('wild cat')
    ['W', 'AY1', 'L', 'D', 'K', 'AE1', 'T']

    The system doesn't contain all phonemes; only some of the consonant phonemes.
    So if we only keep those phonemes that the system covers, we get:

    >>> m.term_to_mst_sequence('wild cat')
    ['L', 'D', 'K', 'T']

    Which corresponds to a number.

    >>> m.term_to_nums('wild cat')
    [5, 1, 7, 1]

    But really, the system is used to be able to create words (therefore images)
    that correspond to a sequence of numbers, so that one can remember them:

    >>> m.terms_of_numstr['3214']  # doctest: +NORMALIZE_WHITESPACE
    ['hammontree', 'mahindra', 'manteer', 'mantra', 'mentor', 'minteer', 'mondry',
    'monetary', 'monteiro', 'monterey', 'montero', 'monterrey', 'montrouis',
    'montroy', 'montuori', 'omohundro']
    """

    phones_for_num = {
        0: {'Z', 'S'},
        1: {'T', 'D', 'TH', 'DH'},
        2: {'N'},
        3: {'M'},
        4: {'R'},
        5: {'L'},
        6: {'CH', 'SH', 'JH'},
        7: {'K', 'G'},
        8: {'F', 'V'},
        9: {'P', 'B'},
    }

    @cached_property
    def num_of_phone(self):
        def gen():
            for num, v in self.phones_for_num.items():
                for phone in v:
                    yield phone, num

        return dict(sorted(gen()))

    @cached_property
    def mst_phones(self):
        return set(self.num_of_phone)

    def term_to_mst_sequence(self, sentence):
        terms = map(str.lower, sentence.split())
        phones = chain.from_iterable(map(self.tp.get, terms))
        return list(filter(self.mst_phones.__contains__, phones))

    def term_to_nums(self, sentence):
        return list(map(self.num_of_phone.get, self.term_to_mst_sequence(sentence)))

    @property
    def nums_of_term(self):
        return {term: self.term_to_nums(term) for term in self.tp}

    @cached_property
    def numstr_of_term(self):
        return {
            term: ''.join(map(str, nums)) for term, nums in self.nums_of_term.items()
        }

    @cached_property
    def terms_of_numstr(self):
        return keys_for_value(self.numstr_of_term)

    def num_to_terms(self, num):
        def _middle_out_sort(a):
            return sorted(a, key=lambda x: abs(x - len(a) / 2))

        if not isinstance(num, str):
            num = str(num)
        if num in self.terms_of_numstr:
            yield from self.terms_of_numstr[num]
        for i in _middle_out_sort(range(0, len(num))):
            if 0 < i < len(num) - 1:
                first_half, second_half = num[:i], num[i:]
                yield from product(
                    self.num_to_terms(first_half), self.num_to_terms(second_half)
                )
