from enum import Enum

from django.utils.translation import gettext_lazy as _


class SexEnum(str, Enum):
    man = "M"
    woman = "W"


sex_choices = [
    (SexEnum.man.value, _('Мужчина')),
    (SexEnum.woman.value, _('Женщина')),
]


class AgeEnum(str, Enum):
    under60 = "<60"
    above60 = ">60"


age_choices = [
    (AgeEnum.above60.value, _('Старше 60')),
    (AgeEnum.under60.value, _('Младше 60')),
]


class SocialStatusEnum(str, Enum):
    satisfied = "S"
    dissatisfied = "D"


social_status_choices = [
    (SocialStatusEnum.satisfied.value, _('Удовлетворительно')),
    (SocialStatusEnum.dissatisfied.value, _('Неудовлетворительно')),
]


class PainDurationEnum(str, Enum):
    less_20_min = "L20M"
    more_20_min = "M20M"
    more_24_hours = "M24H"


pain_duration_choices = [
    (PainDurationEnum.less_20_min.value, _('Менее 20 минут')),
    (PainDurationEnum.more_20_min.value, _('Более 20 минут')),
    (PainDurationEnum.more_24_hours.value, _('Более 24 часов')),
]


class MKEnum(str, Enum):
    thicken = "th"
    not_thicken = "not th"


mk_choices = [
    (MKEnum.not_thicken.value, _('Не уплотнённый')),
    (MKEnum.thicken.value, _('Уплотнённый')),
]


class GeneticEnum(str, Enum):
    CC = "1"
    CT = "2"
    TT = "3"


genetic_choices = [
    (GeneticEnum.CC.value, "C/C"),
    (GeneticEnum.CT.value, "C/T"),
    (GeneticEnum.TT.value, "T/T"),
]


genetic_alt_choices = [
    (GeneticEnum.CC.value, "G/G"),
    (GeneticEnum.CT.value, "G/A"),
    (GeneticEnum.TT.value, "A/A"),
]


class CoronaryAngiographyEnum(str, Enum):
    one = "1"
    two = "2"
    three = "3"
    four_or_more = "4"


coronary_angiography_choices = [
    (CoronaryAngiographyEnum.one.value, "1"),
    (CoronaryAngiographyEnum.two.value, "2"),
    (CoronaryAngiographyEnum.three.value, "3"),
    (CoronaryAngiographyEnum.four_or_more.value, "4+"),
]


class ECGEnum(str, Enum):
    ST_1 = "ST_1"
    ST_2 = "ST_2"
    T = "T"


ECG_choices = [
    (ECGEnum.ST_1.value, _("Подъём сегманта ST")),
    (ECGEnum.ST_2.value, _("Депрессия сегманта ST")),
    (ECGEnum.T.value, _("Инверсия зубца T")),
]
