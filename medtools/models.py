from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db import models

from registration.models import User
from .enums import (
    sex_choices, age_choices, social_status_choices,
    pain_duration_choices, mk_choices, genetic_choices,
    coronary_angiography_choices, ECG_choices, genetic_alt_choices, PainDurationEnum, SexEnum
)
from .utils import get_verbose_name


class Patient(models.Model):
    name = models.CharField(_("Имя"), max_length=255, default="")
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

    def get_absolute_url(self):
        return reverse_lazy("heart-disease-tool-update", kwargs={"pk": self.pk})

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
        result.append(self.get_pain_duration_text())
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
    IL_4_TC = models.CharField(_("IL-1β 511 T/C (rs2243250)"), max_length=3, default="", choices=genetic_choices)
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


class Pilidogram(models.Model):
    patient = models.OneToOneField(Patient, verbose_name="Пациент", on_delete=models.CASCADE)

    HS = models.FloatField(_("Общий ХС ммоль/г"), default=0)
    HS_LLNP = models.FloatField(_("ХС ЛЛНП. ммоль/г"), default=0)
    HS_LLVP = models.FloatField(_("ХС ЛЛВП. ммоль/г"), default=0)
    TG = models.FloatField(_("ТГ. ммоль/г"), default=0)
    KAT = models.FloatField(_("КАТ"), default=0)

    def is_HS_normalized(self):
        return check_btw_nums(self.HS, 2.2, 3.5)

    def is_HS_LLNP_normalized(self):
        return check_btw_nums(self.HS, 2.2, 3.5)

    def is_HS_LLVP_normalized(self):
        return check_btw_nums(self.HS, 2.2, 3.5)

    def is_TG_normalized(self):
        return check_btw_nums(self.HS, 2.2, 3.5)

    def is_KAT_normalized(self):
        return check_btw_nums(self.HS, 2.2, 3.5)

    def get_disease_list(self):
        result = list()

        if (self.KAT > 5 or
              self.HS_LLNP > 4.9 or
              ((self.patient.sex == SexEnum.man.value and self.HS_LLVP < 1.16) or
               self.patient.sex == SexEnum.woman.value and self.HS_LLVP < 0.9)):
            result.append("Атеросклероз")
        elif 3 < self.KAT < 4:
            result.append("Присутствует риск атеросклероза и ишемической болезни сердца")

        if self.KAT > 3.5 and self.TG > 2.8 and self.HS_LLVP < 1 and self.HS_LLNP > 3.37 and self.HS > 5.6:
            result.append("Дислипидемия")

        return result

    def __str__(self):
        return "{}".format(self.id)


class BodyMassIndex(models.Model):
    patient = models.OneToOneField(Patient, verbose_name="Пациент", on_delete=models.CASCADE)

    height = models.FloatField(_("Рост (cм)"), default=0)
    mass = models.FloatField(_("Mass (кг)"), default=0)

    def get_mass_index(self):
        return self.mass / ((self.height / 100) ** 2)

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
    creotenin = models.FloatField(_("Креотенин (мкмоль/л)"), default=0)
    urea = models.FloatField(_("Мочевина Креотенин (мкмоль/л)"), default=0)
    uric_acid = models.FloatField(_("Мочевая кислота(мкмоль/л)"), default=0)
    bilirubin_common = models.FloatField(_("Билурибин общий (мкмоль/л)"), default=0)
    bilirubin_direct = models.FloatField(_("Билурибин прямой (мкмоль/л)"), default=0)
    bilirubin_indirect = models.FloatField(_("Билурибин непрямой (мкмоль/л)"), default=0)
    glucose = models.FloatField(_("Глюкоза (мкмоль/л)"), default=0)

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

    def __str__(self):
        return "{}".format(self.id)


class CoronaryAngiography(models.Model):
    patient = models.OneToOneField(Patient, verbose_name="Пациент", on_delete=models.CASCADE)

    field = models.CharField(_("Количество поражений КА"), default="", max_length=1,
                             choices=coronary_angiography_choices)

    def get_coronary_mark(self):
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

    def get_overall_score(self, patient_id):
        question_number = len(self.surveyquestion_set.all())
        answers = SurveyAnswer.objects.filter(patient_id=patient_id)[:question_number]
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

    def __str__(self):
        return self.text


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, verbose_name="Опросник", on_delete=models.CASCADE)
    question = models.TextField("Вопрос", default="")
    has_multiple_choice = models.BooleanField(_("Множественный выбор"), default=False)

    def get_absolute_url(self):
        if self.has_multiple_choice:
            return reverse_lazy("heart-disease-survey-multiple-choice", kwargs={"pk": self.pk})

        return reverse_lazy("heart-disease-survey", kwargs={"pk": self.pk})

    def get_next_question(self):
        all_questions = self.survey.surveyquestion_set.all()

        for i in range(0, len(all_questions)):
            if all_questions[i] == self:
                try:
                    return all_questions[i+1].get_absolute_url()
                except IndexError:
                    return None

    def __str__(self):
        return self.question


class SurveyQuestionChoices(models.Model):
    choice_text = models.CharField(_("Выбор"), max_length=100, default="")
    question = models.ForeignKey(SurveyQuestion, verbose_name="Вопрос", on_delete=models.CASCADE, null=True)
    mark = models.SmallIntegerField("Балл", default=0)

    def __str__(self):
        return self.choice_text


class SurveyAnswer(models.Model):
    patient = models.ForeignKey(Patient, verbose_name="Пациент", on_delete=models.CASCADE, null=True)
    choice = models.ForeignKey(SurveyQuestionChoices, verbose_name="Выбор", on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-id"]


class SurveyMultipleAnswer(models.Model):
    patient = models.ForeignKey(Patient, verbose_name="Пациент", on_delete=models.CASCADE, null=True)
    choice = models.ManyToManyField(SurveyQuestionChoices, verbose_name="Выбор", related_name="choices", blank=True)

    class Meta:
        ordering = ["-id"]