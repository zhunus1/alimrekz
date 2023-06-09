from .models import (
    DiseaseGroup,
    Disease
)

disease_groups = {
    'Инфекционные заболевания':[
        'Кишечные заболевания',
        'Дифтерия, столбняк, полиомиелит',
        'Коклюш',
        'Менингококковая инфекция',
        'Сепсис, вызванный Streptococcus pneumoniae. Сепсис, вызванный Haemophilus influenzae',
        'Инфекция, вызванная Haemophilus influenzae, неуточненная',
        'Инфекции, передающиеся преимущественно половым путем (кроме ВИЧ / СПИДа)',
        'Ветряная оспа',
        'Корь',
        'Краснуха',
        'Вирусный гепатит',
        'ВИЧ / СПИД',
        'Малярия',
        'Гриппозный менингит, Пневмококковый менингит',
        'Туберкулез',
        'Скарлатина',
        'Сепсис',
        'Рожа, Флегмона',
        'Болезнь легионеров',
        'Стрептококковая и энтерококковая инфекция. Неуточненная',
        'Другой менингит',
        'Менингит, обусловленный другими и неуточненными причинами'
    ],
    'Онкология':[
        'Рак губы, полости рта и глотки',
        'Рак пищевода',
        'Рак желудка',
        'Рак печени',
        'Рак легких',
        'Мезотелиома',
        'Рак кожи (меланома)',
        'Рак мочевого пузыря',
        'Рак шейки матки',
        'Колоректальный рак',
        'Рак груди (только у женщин)',
        'Рак матки',
        'Рак яичек',
        'Рак щитовидной железы',
        'Болезнь Ходжкина',
        'Лимфоидный лейкоз',
        'Доброкачественное новообразование'
    ],
    'Эндокринные и метаболические заболевания':[
        'Анемия, связанные с питанием',
        'Сахарный диабет',
        'Заболевания щитовидной железы',
        'Заболевания надпочечников'
    ],
    'Заболевания нервной истемы':[
        'Эпилепсия'
    ],
    'Заболевания системы кровообращения':[
        'Аневризма и расслоение аорты',
        'Гипертонические заболевания',
        'Ишемическая болезнь сердца',
        'Цереброваскулярные заболевания',
        'Другой атеросклероз',
        'Ревматические и другие болезни сердца',
        'Венозная тромбоэмболия'
    ],
    'Заболевания органов дыхания':[
        'Грипп',
        'Пневмония, вызванная Streptococcus pneumonia или Haemophilus influenza»',
        'Хронические заболевания нижних дыхательных путей',
        'Болезни легкого, вызванные внешними агентами',
        'Инфекции верхних дыхательных путей',
        'Пневмония, не классифицированная в других рубриках, или неуточненный организм',
        'Острые инфекции нижних дыхательных путей',
        'Астма и бронхоэктазы',
        'Респираторный дистресс-синдром у взрослых',
        'Отек легких',
        'Гнойные и некротические состояния нижних дыхательных путей',
        'Другие заболевания плевры'
    ],
    'Заболевания пищеварительной системы':[
        'Язвенная болезнь желудка и двенадцатиперстной кишки',
        'Болезни аппендикса',
        'Грыжи',
        'Холелитиаз и холецистит',
        'Другие заболевания желчного пузыря или желчевыводящих путей',
        'Острый панкреатит',
        'Другие болезни поджелудочной железы'
    ],
    'Заболевания мочеполовой системы':[
        'Нефрит и нефроз',
        'Обструктивная уропатия',
        'Почечная недостаточность',
        'Почечная колика',
        'Заболевания, возникающие в результате дисфункции почечных канальцев.',
        'Неуточненная сморщенная почка, маленькая почка неясного генеза',
        'Воспалительные заболевания мочеполовой системы',
        'Гиперплазия предстательной железы'
    ],
    'Беременность, роды и перинатальный период':[
        'Столбняк новорожденного',
        'акушерский столбняк',
        'Беременность, роды и послеродовой период',
        'Отдельные состояния, возникающие в перинатальном периоде'
    ],
    'Врожденные пороки развития':[
        'Определенные врожденные пороки развития (дефекты нервной трубки)',
        'Врожденные пороки  системы  кровообращения (пороки сердца)'
    ],
    'Побочные эффекты медикаментозной и хирургической помощи':[
        'Лекарственные средства, медикаменты и биологические вещества, являющиеся причиной неблагоприятных реакций при терапевтическом применении',
        'Случайное нанесение вреда больному при выполнении терапевтических и хирургических вмешательств ',
        'Медицинские приборы и устройства, с которыми связаны несчатные случаи, возникшие при их использовании для диагностических и терапевтических целей'
    ],
    'Травмы':[
        'Транспортные несчастные случаи',
        'Случайные травмы',
        'Преднамеренное самоповреждение',
        'Отравление и воздействие с неопределенными намерениями',
        'Нападение'
    ],
    'Смерти, связанные с алкоголем и наркотиками':[
        'Смерти, связанные с алкоголем. Расстройства и отравления, связанные с алкоголем',
        'Смерти, связанные с алкоголем. Другие расстройства, связанные с алкоголем',
        'Преднамеренное самоповреждение путем отравления. Лекарственные расстройства и отравления',
        'Преднамеренное самоповреждение путем отравления и воздействие другими и неуточненными лекарственными средствами, медикаментами и биологическими веществами'
    ],
    'Предварительное присвоение новых заболеваний':[
        'COVID-19'
    ],
}



def create_objects():
    for key, value in disease_groups.items():
        group = DiseaseGroup.objects.create(
            name = key,
        )
        for disease in value:
            disease = Disease.objects.create(
                name = disease,
                group = group,
            )