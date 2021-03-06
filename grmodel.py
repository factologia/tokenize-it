# -*- coding: utf8 -*-

import enum
import logging

log = logging.getLogger(__name__)

def __map_gremmems(str, misses=None):
    res = {}
    for t in str.split(','):
        if t in __map:
            for val in __map[t]:
                res[val.__class__.__name__] = val.value
        elif not misses is None:
            misses.add(t)
    return res

def get_grammems(gr_match, misses=None):
    s_str = gr_match.group('S')
    if not s_str:
        return None
    s = __map_gremmems(s_str, misses)

    res = []
    for f_str in gr_match.captures('F'):
        res.append(dict(s, **__map_gremmems(f_str, misses)))
    if not res:
        res.append(s)
    return res

class ModelEnum(enum.Enum):
    def __str__(self):
        return self.name
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class PoS(ModelEnum):
    NOUN = 1  # имя существительное
    ADJF = 2  # имя прилагательное
    VERB = 3  # глагол
    NUMR = 4  # числительное
    ADVB = 5  # наречие
    NPRO = 6  # местоимение-существительное
    PRED = 7  # предикатив
    PREP = 8  # предлог
    CONJ = 9  # союз
    PRCL = 10 # частица
    INTJ = 11 # междометие

class Shortness(ModelEnum):
    SHRT = 1  # краткая форма

class Comp(ModelEnum):
    COMP = 1  # сравнительная форма

class VerbForm(ModelEnum):
    INFN = 1 # инфинитив
    PRTC = 2 # причастие
    GRND = 3 # деепричастие

class Tense(ModelEnum):
    PRES = 1  # настоящее
    PAST = 2  # прошедшее
    FUTR = 3  # будущее

class Case(ModelEnum):
    NOMN = 1  # именительный падеж
    GENT = 2  # родительный падеж
    DATV = 3  # дательный падеж
    ACCS = 4  # винительный падеж
    ABLT = 5  # творительный падеж
    LOCT = 6  # предложный падеж
    VOCT = 7  # звательный падеж nomn
    GEN2 = 8  # второй родительный (частичный) падеж gent
    ACC2 = 9  # второй винительный падеж accs
    LOC2 = 10 # второй предложный (местный) падеж loct

class Gender(ModelEnum):
    MASC = 1  # мужской
    FEMN = 2  # женский
    NEUT = 3  # средний
    MS_F = 4  # общий род

class Number(ModelEnum):
    SING = 1  # единственное число
    PLUR = 2  # множественное число

class Person(ModelEnum):
    PER1 = 1  # 1-е лицо
    PER2 = 2  # 2-е лицо
    PER3 = 3  # 3-е лицо

class Abbr(ModelEnum):
    ABBR = 1

__map = {
#==== PoS mapping ====# ??MyStem COM

    # Имя существительное
    'NOUN' : [PoS.NOUN], # OpenCorpora
    'S'    : [PoS.NOUN], # НКРЯ, MyStem

    # Имя прилагательное (полное)
    'ADJF'  : [PoS.ADJF], # OpenCorpora
    'A'     : [PoS.ADJF], # НКРЯ, MyStem
    'ANUM'  : [PoS.ADJF], # НКРЯ, MyStem (числительное-прилогательное)
    'A-NUM' : [PoS.ADJF], # НКРЯ
    'APRO'  : [PoS.ADJF], # НКРЯ, MyStem (местоимение-прилагательное)
    'A-PRO' : [PoS.ADJF], # НКРЯ

    # Имя прилагательное (краткое)
    'ADJS' : [PoS.ADJF, Shortness.SHRT], # OpenCorpora
    'brev' : [Shortness.SHRT], # НКРЯ

    # Компаратив
    'COMP'  : [PoS.ADJF, Comp.COMP], # OpenCorpora
    'comp'  : [Comp.COMP], # НКРЯ
    'comp2' : [Comp.COMP], # НКРЯ

    # Глагол (личная форма)
    'VERB' : [PoS.VERB], # OpenCorpora
    'V'    : [PoS.VERB], # НКРЯ, MyStem

    # Глагол (инфинитив)
    'INFN' : [PoS.VERB, VerbForm.INFN], # OpenCorpora
    'inf'  : [PoS.VERB, VerbForm.INFN], # НКРЯ

    # Причастие
    'PRTF'  : [PoS.VERB, VerbForm.PRTC], # OpenCorpora
    'PRTS'  : [PoS.VERB, VerbForm.PRTC, Shortness.SHRT], # OpenCorpora
    'partcp': [PoS.VERB, VerbForm.PRTC], # НКРЯ

    # Деепричастие
    'GRND' : [PoS.VERB, VerbForm.GRND], # OpenCorpora
    'ger'  : [PoS.VERB, VerbForm.GRND], # НКРЯ

    # Числительное
    'NUMR' : [PoS.NUMR], # OpenCorpora
    'NUM'  : [PoS.NUMR], # НКРЯ, MyStem

    # Наречие
    'ADVB'        : [PoS.ADVB], # OpenCorpora
    'ADV'         : [PoS.ADVB], # НКРЯ, MyStem
    'PARENTH'     : [PoS.ADVB], # НКРЯ (вводное слово)
    'ADVPRO'      : [PoS.ADVB], # НКРЯ, MyStem (местоименное наречие)
    'ADV-PRO'     : [PoS.ADVB], # НКРЯ
    'PRAEDIC-PRO' : [PoS.ADVB], # НКРЯ (местоимение-предикатив)

    # Местоимение-существительное
    'NPRO'  : [PoS.NPRO], # OpenCorpora
    'SPRO'  : [PoS.NPRO], # НКРЯ, MyStem
    'S-PRO' : [PoS.NPRO], # НКРЯ

    # Предикатив
    'PRED'    : [PoS.PRED], # OpenCorpora
    'PRAEDIC' : [PoS.PRED], # НКРЯ

    # Предлог
    'PREP' : [PoS.PREP], # OpenCorpora
    'PR'   : [PoS.PREP], # НКРЯ, MyStem

    # Союз
    'CONJ' : [PoS.CONJ], # OpenCorpora, НКРЯ, MyStem

    # Частица
    'PRCL' : [PoS.PRCL], # OpenCorpora
    'PART' : [PoS.PRCL], # НКРЯ, MyStem

    # Междометие
    'INTJ' : [PoS.INTJ], # OpenCorpora, НКРЯ, MyStem

#==== Case mapping ====# ?? НКРЯ adnum

    # Именительный падеж
    'nomn' : [Case.NOMN], # OpenCorpora
    'им'   : [Case.NOMN], # MyStem-ru
    'nom'  : [Case.NOMN], # НКРЯ, MyStem-en

    # Родительный падеж
    'gent' : [Case.GENT], # OpenCorpora
    'gen1' : [Case.GENT], # OpenCorpora (первый родительный падеж)
    'род'  : [Case.GENT], # MyStem-ru
    'gen'  : [Case.GENT], # НКРЯ, MyStem-en

    # Дательный падеж
    'datv' : [Case.DATV], # OpenCorpora
    'дат'  : [Case.DATV], # MyStem-ru
    'dat'  : [Case.DATV], # НКРЯ, MyStem-en
    'dat2' : [Case.DATV], # НКРЯ (дистрибутивный дательный)

    # Винительный падеж
    'accs' : [Case.ACCS], # OpenCorpora
    'вин'  : [Case.ACCS], # MyStem-ru
    'acc'  : [Case.ACCS], # НКРЯ, MyStem-en

    # Творительный падеж
    'ablt' : [Case.ABLT], # OpenCorpora
    'твор' : [Case.ABLT], # MyStem-ru
    'ins'  : [Case.ABLT], # НКРЯ, MyStem-en

    # Предложный падеж
    'loct' : [Case.LOCT], # OpenCorpora
    'loc1' : [Case.LOCT], # OpenCorpora (первый предложный падеж)
    'пр'   : [Case.LOCT], # MyStem-ru
    'abl'  : [Case.LOCT], # MyStem-en
    'loc'  : [Case.LOCT], # НКРЯ

    # Звательный падеж nomn
    'voct' : [Case.VOCT], # OpenCorpora
    'зват' : [Case.VOCT], # MyStem-ru
    'voc'  : [Case.VOCT], # НКРЯ, MyStem-en

    # Второй родительный (частичный) падеж
    'gen2' : [Case.GEN2], # НКРЯ, OpenCorpora
    'парт' : [Case.GEN2], # MyStem-ru
    'part' : [Case.GEN2], # MyStem-en

    # Второй винительный падеж
    'acc2' : [Case.ACC2], # НКРЯ, OpenCorpora

    # Второй предложный (местный) падеж
    'loc2'  : [Case.LOC2], # НКРЯ, OpenCorpora
    'местн' : [Case.LOC2], # MyStem-ru
    #'loc'   : Case.LOC2, # MyStem-en КОЛЛИЗИЯ!

#==== Quantity mapping ====#

    # Единственное число
    'sing' : [Number.SING], # OpenCorpora
    'ед'   : [Number.SING], # MyStem-ru
    'sg'   : [Number.SING], # НКРЯ, MyStem-en

    # Множественное число
    'plur' : [Number.PLUR], # OpenCorpora
    'мн'   : [Number.PLUR], # MyStem-ru
    'pl'   : [Number.PLUR], # НКРЯ, MyStem-en

#==== Tense mapping ====#

    # Настоящее
    'pres'    : [Tense.PRES], # OpenCorpora
    'наст'    : [Tense.PRES], # MyStem-ru
    'praes'   : [Tense.PRES], # НКРЯ, MyStem-en

    # Будущее
    'futr'    : [Tense.FUTR], # OpenCorpora
    'непрош'  : [Tense.FUTR], # MyStem-ru
    'fut'     : [Tense.FUTR], # НКРЯ
    'inpraes' : [Tense.FUTR], # MyStem-en

    # Прошедшее
    'past'    : [Tense.PAST], # OpenCorpora
    'прош'    : [Tense.PAST], # MyStem-ru
    'praet'   : [Tense.PAST], # НКРЯ, MyStem-en

#==== Gender mapping ====#

    # Мужской род
    'masc'   : [Gender.MASC], # OpenCorpora
    'муж'    : [Gender.MASC], # MyStem-ru
    'm'      : [Gender.MASC], # НКРЯ, MyStem-en

    # Женский род
    'femn'   : [Gender.FEMN], # OpenCorpora
    'жен'    : [Gender.FEMN], # MyStem-ru
    'f'      : [Gender.FEMN], # НКРЯ, MyStem-en

    # Средний род
    'neut'   : [Gender.NEUT], # OpenCorpora
    'сред'   : [Gender.NEUT], # MyStem-ru
    'n'      : [Gender.NEUT], # НКРЯ, MyStem-en

    # Общий род
    'ms-f'   : [Gender.MS_F], # OpenCorpora
    'мж'     : [Gender.MS_F], # MyStem-ru
    'm-f'    : [Gender.MS_F], # НКРЯ, MyStem-en

#==== Person ===#

    # 1-е лицо
    '1per'   : [Person.PER1], # OpenCorpora
    '1p'     : [Person.PER1], # НКРЯ, MyStem-en
    '1-л'    : [Person.PER1], # MyStem-ru

    # 2-е лицо
    '2per'   : [Person.PER2], # OpenCorpora
    '2p'     : [Person.PER2], # НКРЯ
    '2-л'    : [Person.PER2], # MyStem-ru

    # 3-е лицо
    '3per'   : [Person.PER3], # OpenCorpora
    '3p'     : [Person.PER3], # НКРЯ
    '3-л'    : [Person.PER3], # MyStem-ru

#==== Abbriviation ===#
    'Abbr'   : [Abbr.ABBR] # OpenCorpora
}

labels = {
    PoS: {
        PoS.NOUN: "сущ.",
        PoS.ADJF: "прил.",
        PoS.VERB: "гл.",
        PoS.NUMR: "числ.",
        PoS.ADVB: "нар.",
        PoS.NPRO: "мест",
        PoS.PRED: "пред.",
        PoS.PREP: "пр.",
        PoS.CONJ: "союз",
        PoS.PRCL: "част.",
        PoS.INTJ: "межд."
    },
    Shortness: {
        Shortness.SHRT: "кр."
    },
    Comp: {
        Comp.COMP: "сравн."
    },
    VerbForm: {
        VerbForm.INFN: "инф.",
        VerbForm.PRTC: "прич.",
        VerbForm.GRND: "дееприч."
    },
    Tense: {
        Tense.PRES:"наст.",
        Tense.PAST: "прош.",
        Tense.FUTR: "буд."
    },
    Case: {
        Case.NOMN: "им.",
        Case.GENT: "род.",
        Case.DATV: "дат.",
        Case.ACCS: "вин.",
        Case.ABLT: "твор.",
        Case.LOCT: "предл.",
        Case.VOCT: "зват.",
        Case.GEN2: "вт. род.",
        Case.ACC2: "вт. вин.",
        Case.LOC2: "вт. предл."
    },
    Gender: {
        Gender.MASC : "муж.",
        Gender.FEMN : "жен.",
        Gender.NEUT : "ср.",
        Gender.MS_F : "общ."
    },
    Number: {
        Number.SING: "ед.",
        Number.PLUR: "мн."
    },
    Person: {
        Person.PER1: "1-е",
        Person.PER2: "2-e",
        Person.PER3: "3-е"
    },
    Abbr: {
        Abbr.ABBR: "аббр."
    }
}
