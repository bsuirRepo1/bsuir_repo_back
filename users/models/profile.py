from django.db import models


class SexChoices(models.TextChoices):
    MALE = "Мужской"
    FEMALE = "Женский"
    NO_SELECTED = "Не выбрано"


class CourseChoices(models.IntegerChoices):
    FIRST = 1,
    SECOND = 2,
    THIRD = 3,
    FOURTH = 4,
    FIFTH = 5


class FacultyChoices(models.TextChoices):
    FKSIS = "Компьютерных систем и сетей",
    FRE = "Радиотехники и электроники",
    IEF = "Инженерно-экономический",
    FKP = "Компьютерного проектирования",
    FITU = "Информационных технологий и управления",
    FIB = "Информационной безопасности",
    VF = "Военный",
    NO_SELECTED = "Не выбрано"


class SpecialitiesChoices(models.TextChoices):
    IITP = "Иинформатика и технологии программирования",
    PI = "Программная инженерия",
    KI = "Компьютерная инженерия"
    KIS = "Квантовые информационные системы",
    MINE = "Микро- и наноэлектроника"
    EM = "Электронный маркетинг"
    EE = "Электронная экономика"
    PMS = "Прграммируемые мобильные системы"
    ME = "Медицинская электроника"
    II = "Искусственный интеллект"
    ASOI = "Автоматизированные системы обработки информации"
    IB = "Информационная безопасность",
    ZIVTK = "Защита информации в телекоммуникациях"
    VMSIS = "Вычислительные машины, системы и сети",
    Radio = "Радиотехника"


class UserProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=30,
        blank=False,
        default="Имя",
        verbose_name="Имя пользователя"
    )
    last_name = models.CharField(
        max_length=30,
        blank=False,
        default="Имя",
        verbose_name="Имя пользователя"
    )
    about = models.TextField(default='', blank=True, verbose_name="Обо мне")
    sex = models.CharField(choices=SexChoices.choices, default=SexChoices.NO_SELECTED, verbose_name="Пол", max_length=10)
    course = models.IntegerField(choices=CourseChoices.choices, default=CourseChoices.FIRST, verbose_name="Курс")
    faculty = models.CharField(
        choices=FacultyChoices.choices,
        max_length=40,
        default=FacultyChoices.NO_SELECTED,
        blank=False,
        verbose_name="Факультет"
    )
    speciality = models.CharField(
        max_length=50,
        blank=False,
        choices=SpecialitiesChoices.choices,
        verbose_name="Специальность"
    )
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/",
        default='',
        blank=True,
        null=True,
        verbose_name="Фото"
    )
    city = models.CharField(
        max_length=30,
        blank=True,
        default='',
        null=True,
        verbose_name="Город"
    )
    days_with_service = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
