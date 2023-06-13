from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db import models

from registration.models import User
from .enums import (
    sex_choices, age_choices, social_status_choices,
    pain_duration_choices, mk_choices, genetic_choices,
    coronary_angiography_choices, ECG_choices, genetic_alt_choices, PainDurationEnum, SexEnum, SocialStatusEnum, AgeEnum
)
from .utils import get_verbose_name


class Patient(models.Model):
    sex = models.CharField(_("Пол"), max_length=1, default="M", choices=sex_choices)
    age = models.CharField(_("Возраст"), default="", max_length=3, choices=age_choices)
    congestive_heart_failure = models.BooleanField(_("ОСН"), default=False)
    chronic_heart_failure = models.BooleanField(_("ХСН"), default=False)
    heart_rhythm_disturbances = models.BooleanField(_("Нарушение ритма"), default=False)
    congestive_pneumonia = models.BooleanField(_("Застойчивая пневмония"), default=False)
    underlying_disease = models.BooleanField(_("Фоновое заболевание"), default=False)
    social_position = models.CharField(_("Социальное положение"), default="", max_length=1,
                                       choices=social_status_choices)
    pain_duration = models.CharField(_("Продолжительность боли"), default="", max_length=4,
                                     choices=pain_duration_choices)
    heart_rate = models.FloatField("ЧСС", default=0)

    MAX_SCORE = 28

    class Meta:
        verbose_name = "Пациента"
        verbose_name_plural = "Пациенты"

    def get_absolute_url(self):
        return reverse_lazy("heart-disease-tool-update", kwargs={"pk": self.pk})

    def get_overall_score(self):
        result = 0
        if self.sex == SexEnum.man.value:
            result += 1
        if self.social_position == SocialStatusEnum.dissatisfied.value:
            result += 1
        if self.age == AgeEnum.above60.value:
            result += 1

        result += int(self.congestive_heart_failure) + int(self.chronic_heart_failure) + \
                  int(self.heart_rhythm_disturbances) + int(self.congestive_pneumonia) + \
                  int(self.underlying_disease)

        result += self.geneticresearch.get_total_mark()
        result += self.coronaryangiography.get_total_mark()
        try:
            result += self.bodymassindex.get_total_mark()
        except ObjectDoesNotExist:
            pass

        return result

    def get_risk_group(self):
        def get_percentage_of_score():
            return self.get_overall_score() / self.MAX_SCORE

        if get_percentage_of_score() < 1/3:
            return "Группа низкого риска"
        if get_percentage_of_score() < 2/3:
            return "Группа среднего риска"
        if get_percentage_of_score() <= 1:
            return "Группа высокого риска"

    def get_heart_rate_disease(self):
        if self.heart_rate < 60:
            return "Брадикардия"
        elif self.heart_rate > 90:
            return "Тахикардия"

    def get_pain_duration_text(self):
        if self.pain_duration == PainDurationEnum.less_20_min.value:
            return "Прогрессирующая стенокардия напряжения"
        if self.pain_duration == PainDurationEnum.more_20_min.value:
            return "Острый коронарный синдром"
        if self.pain_duration == PainDurationEnum.more_24_hours.value:
            return "Острый инфаркт миокарда"

    def get_disease_list(self):
        result = list()
        result.append(self.get_heart_rate_disease())
        if self.congestive_heart_failure:
            txt = get_verbose_name(self, "congestive_heart_failure")
            result.append(txt)
        if self.chronic_heart_failure:
            txt = get_verbose_name(self, "chronic_heart_failure")
            result.append(txt)
        if self.heart_rhythm_disturbances:
            txt = get_verbose_name(self, "heart_rhythm_disturbances")
            result.append(txt)
        if self.congestive_pneumonia:
            txt = get_verbose_name(self, "congestive_pneumonia")
            result.append(txt)
        if self.underlying_disease:
            txt = get_verbose_name(self, "underlying_disease")
            result.append((txt))
        return result

    def __str__(self):
        return "{}".format(self.id)


def check_btw_nums(checked_num, limit1, limit2):
    if limit1 <= checked_num <= limit2:
        return None
    else:
        return False


class Echocardiography(models.Model):
    patient = models.OneToOneField(Patient, verbose_name="Пациент", on_delete=models.CASCADE, blank=True)
    ejection_fraction = models.FloatField(_("ФВЛЖ (%)"), default=0)
    kcr = models.FloatField(_("КСР (см)"), default=0)
    kdr = models.FloatField(_("КДР (см)"), default=0)
    eslj = models.FloatField(_("ЭСЛЖ (см)"), default=0)
    mjp = models.FloatField(_("МЖП (см)"), default=0)
    pj = models.FloatField(_("ПЖ (см)"), default=0)
    mk = models.CharField(_("МК (см)"), max_length=6, default="", choices=mk_choices)
    lp = models.FloatField(_("ЛП (см)"), default=0)

    def is_ejection_fraction_normalized(self):
        if self.ejection_fraction < 40:
            return "Сердечная недостаточность"
        elif self.ejection_fraction < 55:
            return "Сниженная ФВЛЖ"

    def is_kcr_normalized(self):
        return check_btw_nums(self.kcr, 2.5, 3.6)

    def is_kdr_normalized(self):
        return check_btw_nums(self.kdr, 3.7, 5.6)

    def is_eslj_normalized(self):
        return check_btw_nums(self.eslj, 0.6, 1.1)

    def is_mjp_normalized(self):
        return check_btw_nums(self.mjp, 0.6, 1.1)

    def is_pj_normalized(self):
        return check_btw_nums(self.pj, 0, 3)

    def is_lp_normalized(self):
        return check_btw_nums(self.lp, 2, 3.5)

    def get_disease_list(self):
        result = list()
        result.append(self.is_ejection_fraction_normalized())
        if not self.is_eslj_normalized():
            result.append(self.is_eslj_normalized())
        if not self.is_kcr_normalized():
            result.append("КСР ненормирован")
        if not self.is_kdr_normalized():
            result.append("Увеличение размеров сердца")
        if not self.is_eslj_normalized():
            result.append("ЭСЛЖ ненормирован")
        if not self.is_mjp_normalized():
            result.append("МЖП ненормирован")
        if not self.is_pj_normalized():
            result.append("ПЖ ненормирован")
        if not self.is_lp_normalized():
            result.append("ЛП ненормирован")

        return result

    def __str__(self):
        return "{}".format(self.id)


class GeneticResearch(models.Model):
    patient = models.OneToOneField(Patient, verbose_name="Пациент", on_delete=models.CASCADE)

    IL_1b_511_TC = models.CharField(_("IL-1β 511 T/C (rs16944)"), max_length=3, default="", choices=genetic_choices)
    IL_4_TC = models.CharField(_("IL-4 С/Т (rs2243250)"), max_length=3, default="", choices=genetic_choices)
    IL_10_819_CT = models.CharField(_("IL-10 819 C/T (rs1800871)"), max_length=3, default="", choices=genetic_choices)
    TNF_a_GA = models.CharField(_("TNF-α G/A 308 (rs1800629)"), max_length=3, default="", choices=genetic_alt_choices)

    def get_total_mark(self):
        return int(self.IL_1b_511_TC) + int(self.IL_4_TC) + int(self.IL_10_819_CT) + int(self.TNF_a_GA)

    def __str__(self):
        return "{}".format(self.id)


class ImmunologicalResearch(models.Model):
    patient = models.OneToOneField(Patient, verbose_name="Пациент", on_delete=models.CASCADE)

    IL_1b = models.FloatField(_("IL-1(b)"), default=0)
    TNF_a = models.FloatField(_("TNF-a"), default=0)
    IL_4 = models.FloatField(_("IL-4"), default=0)
    IL_10 = models.FloatField(_("IL-10"), default=0)

    def is_IL_1b_normalized(self):
        return check_btw_nums(self.IL_1b, (26.6 - 0.93), (26.6 + 0.93))

    def is_TNF_a_normalized(self):
        return check_btw_nums(self.TNF_a, (21.2 - 0.6), (21.2 + 0.6))

    def is_IL_4_normalized(self):
        return check_btw_nums(self.IL_4, (24.1 - 0.82), (24.1 + 0.82))

    def is_IL_10_normalized(self):
        return check_btw_nums(self.IL_10, (15.2 - 1.02), (15.2 + 1.02))

    def get_disease_list(self):
        result = list()

        if not (self.is_IL_1b_normalized() or self.is_TNF_a_normalized()):
            result.append("Цитокиновый дисбаланс")

        return result

    def __str__(self):
        return "{}".format(self.id)


class Lipidogram(models.Model):
    patient = models.OneToOneField(Patient, verbose_name="Пациент", on_delete=models.CASCADE)

    HS = models.FloatField(_("Общий ХС ммоль/г"), default=0)
    HS_LPNP = models.FloatField(_("ХС ЛПНП. ммоль/г"), default=0)
    HS_LPVP = models.FloatField(_("ХС ЛПВП. ммоль/г"), default=0)
    TG = models.FloatField(_("ТГ. ммоль/г"), default=0)
    KA = models.FloatField(_("КА"), default=0)

    def get_disease_list(self):
        result = list()

        if (self.KA > 5 or
                self.HS_LPNP > 4.9 or
                ((self.patient.sex == SexEnum.man.value and self.HS_LPVP < 1.16) or
                 self.patient.sex == SexEnum.woman.value and self.HS_LPVP < 0.9)):
            result.append("Атеросклероз")
        elif 3 < self.KA < 4:
            result.append("Присутствует риск атеросклероза и ишемической болезни сердца")

        if self.KA > 3.5 and self.TG > 2.8 and self.HS_LPVP < 1 and self.HS_LPNP > 3.37 and self.HS > 5.6:
            result.append("Дислипидемия")

        return result

    def __str__(self):
        return "{}".format(self.id)


class BodyMassIndex(models.Model):
    patient = models.OneToOneField(Patient, verbose_name="Пациент", on_delete=models.CASCADE)

    height = models.FloatField(_("Рост (cм)"), default=0)
    mass = models.FloatField(_("Масса (кг)"), default=0)

    def get_mass_index(self):
        return self.mass / ((self.height / 100) ** 2)

    def get_total_mark(self):
        mass_index = self.get_mass_index()
        if mass_index < 25:
            return 0
        if mass_index < 30:
            return 1
        elif mass_index < 35:
            return 2
        elif mass_index < 40:
            return 3
        else:
            return 4

    def get_mass_disease(self):
        mass_index = self.get_mass_index()
        if mass_index < 16.0:
            return "Выраженный дефицит массы тела"
        elif mass_index < 18.50:
            return "Недостаточная (дефицит) масса тела"
        elif mass_index < 25:
            return
        elif mass_index < 30:
            return "Избыточная масса тела (предожирение)"
        elif mass_index < 35:
            return "Ожирение первой степени"
        elif mass_index < 40:
            return "Ожирение второй степени"
        elif mass_index >= 40:
            return "Ожирение третьей степени (морбидное)"

    def __str__(self):
        return "{}".format(self.id)


class BiochemicalBloodAnalysis(models.Model):
    patient = models.OneToOneField(Patient, verbose_name="Пациент", on_delete=models.CASCADE)

    ALAT = models.FloatField(_("АЛАТ (U/L)"), default=0)
    ACAT = models.FloatField(_("АСАТ(U/L)"), default=0)
    creatinin = models.FloatField(_("Креатинин (мкмоль/л)"), default=0)
    urea = models.FloatField(_("Мочевина (мкмоль/л)"), default=0)
    uric_acid = models.FloatField(_("Мочевая кислота(мкмоль/л)"), default=0)
    bilirubin_common = models.FloatField(_("Билирубин общий (мкмоль/л)"), default=0)
    bilirubin_direct = models.FloatField(_("Билирубин прямой (мкмоль/л)"), default=0)
    bilirubin_indirect = models.FloatField(_("Билирубин непрямой (мкмоль/л)"), default=0)
    glucose = models.FloatField(_("Глюкоза (мкмоль/л)"), default=0)

    def is_alat_normalized(self):
        if ((self.ALAT < 34 and self.patient.sex == SexEnum.woman.value) or
            (self.ALAT < 45 and self.patient.sex == SexEnum.man.value)):
            return True

        return False

    def is_acat_normalized(self):
        if ((self.ALAT < 31 and self.patient.sex == SexEnum.woman.value) or
                (self.ALAT < 35 and self.patient.sex == SexEnum.man.value)):
            return True

        return False

    def is_glucose_normalized(self):
        if 3.89 < self.bilirubin_common < 5.83:
            return True

        return False

    def is_bilirubin_common_normalized(self):
        if 0 < self.bilirubin_common < 20.5:
            return True

        return False


    def get_disease_list(self):
        result = list()
        if ((self.patient.sex == SexEnum.man.value and self.uric_acid > 432) or
                (self.patient.sex == SexEnum.woman.value and self.uric_acid > 360)):
            result.append("Гиперурикемия")

        if self.glucose > 7:
            result.append("нарушение толерантности к глюкозе")
        elif self.glucose > 5.83:
            result.append("сахарный диабет")

        return result

    def get_recommendation_list(self):
        result = list()
        if not (self.is_alat_normalized() and self.is_acat_normalized() and self.is_bilirubin_common_normalized()):
            result.append("Rонсультация гепатолога")
        if not self.is_glucose_normalized():
            result.append("Консультация эндокринолога")

        return result

    def __str__(self):
        return "{}".format(self.id)


class CoronaryAngiography(models.Model):
    patient = models.OneToOneField(Patient, verbose_name="Пациент", on_delete=models.CASCADE)

    field = models.CharField(_("Количество поражений КА"), default="", max_length=1,
                             choices=coronary_angiography_choices)

    def get_total_mark(self):
        return int(self.field)

    def __str__(self):
        return "{}".format(self.id)


class ECG(models.Model):
    patient = models.OneToOneField(Patient, verbose_name="Пациент", on_delete=models.CASCADE)

    field = models.CharField(_("Поле"), default="", max_length=4, choices=ECG_choices)

    def __str__(self):
        return "{}".format(self.id)


class Survey(models.Model):
    name = models.CharField(_("Название"), max_length=255, default="")

    class Meta:
        verbose_name = "Опросник"
        verbose_name_plural = "Опросники"

    def get_overall_score(self, patient_id):
        question_number = len(self.surveyquestion_set.all())
        answers = SurveyAnswer.objects.filter(patient_id=patient_id, choice__question__survey=self)[:question_number]
        if len(answers) < question_number:
            return

        score = 0
        for answer in answers:
            score += answer.choice.mark

        return score

    def get_insd(self, patient_id):
        result = 0
        question_number = len(self.surveyquestion_set.all())
        answers = SurveyMultipleAnswer.objects.filter(patient_id=patient_id)[:question_number]
        for answer in answers:
            result += answer.choice.all().count()

        return result

    def get_pri(self, patient_id):
        result = 0
        question_number = len(self.surveyquestion_set.all())
        answers = SurveyMultipleAnswer.objects.filter(patient_id=patient_id)[:question_number]
        for answer in answers:
            choices = answer.choice.all()
            for choice in choices:
                result += choice.mark

        return result

    def __str__(self):
        return self.name


class SurveyResult(models.Model):
    survey = models.ForeignKey(Survey, verbose_name=_("Опросник"), on_delete=models.CASCADE)
    text = models.CharField(_("Текст"), max_length=255, default="")
    mark_from = models.IntegerField(_("Мин балл для вывода"), default=0)
    mark_to = models.IntegerField(_("Макс балл для вывода"), default=0)

    class Meta:
        verbose_name = "Результат для опросника"
        verbose_name_plural = "Результаты для опросников"

    def __str__(self):
        return self.text


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, verbose_name="Опросник", on_delete=models.CASCADE)
    question = models.TextField("Вопрос", default="")
    has_multiple_choice = models.BooleanField(_("Множественный выбор"), default=False)

    class Meta:
        verbose_name = "Вопрос опросника"
        verbose_name_plural = "Вопросы для опросников"

    def get_absolute_url(self):
        if self.has_multiple_choice:
            return reverse_lazy("heart-disease-survey-multiple-choice") + f"?question_id={self.pk}"

        return reverse_lazy("heart-disease-survey") + f"?question_id={self.pk}"

    def get_next_question(self):
        all_questions = self.survey.surveyquestion_set.all()

        for i in range(0, len(all_questions)):
            if all_questions[i] == self:
                try:
                    return all_questions[i + 1].get_absolute_url()
                except IndexError:
                    return None

    def __str__(self):
        return self.question


class SurveyQuestionChoices(models.Model):
    choice_text = models.CharField(_("Выбор"), max_length=100, default="")
    question = models.ForeignKey(SurveyQuestion, verbose_name="Вопрос", on_delete=models.CASCADE, null=True)
    mark = models.SmallIntegerField("Балл", default=0)

    class Meta:
        verbose_name = "Выбор для вопроса"
        verbose_name_plural = "Выборы для вопросов"
        
    def __str__(self):
        return self.choice_text


class SurveyAnswer(models.Model):
    patient = models.ForeignKey(Patient, verbose_name="Пациент", on_delete=models.CASCADE, null=True)
    choice = models.ForeignKey(SurveyQuestionChoices, verbose_name="Выбор", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.pk}-{self.choice.choice_text}"
    class Meta:
        ordering = ["-id"]


class SurveyMultipleAnswer(models.Model):
    patient = models.ForeignKey(Patient, verbose_name="Пациент", on_delete=models.CASCADE, null=True)
    choice = models.ManyToManyField(SurveyQuestionChoices, verbose_name="Выбор", related_name="choices", blank=True)

    class Meta:
        ordering = ["-id"]
