MAIN_MENU_TEXT = "✈️ Добро пожаловать в главное меню чат-бота Управляющей компании \"УУР-ЮГ\". Здесь Вы можете оставить заявку для управляющей компании или направить свое предложение по управлению домом. Просто воспользуйтесь кнопками меню, чтобы взаимодействовать с функциями бота:"
APPLICATION_CHOOSING_TEXT = "📛👇📛Выберите категорию, по которой Вы хотите оставить заявку в УК:"
COMPLAINT_ADDRESS_TEXT = "<b>Шаг 1/3.</b> 📝 Напишите адрес или ориентир проблемы (улицу, номер дома, подъезд, этаж и квартиру) или пропустите этот пункт:"
COMPLAINT_MEDIA_TEXT = "<b>Шаг 2/3.</b> Прикрепите фотографию или видео к своей заявке или пропустите этот пункт:"
COMPLAINT_BODY_TEXT = "<b>Шаг 3/3.</b> 📛 Напишите причину обращения в подробностях:"
COMPLAINT_SENT_TEXT = "✅<b> Жало́ба отправле́на администра́ции.</b> Спасибо за Ваше обращение!"
SETTINGS_TEXT = "⚙️ Тут Вы сможете поменять Имя и Фамилию в Базе данных нашего бота или же можете поменять Ваш номер телефона, если Вы изначально вводили что-то неверно. Выберите, что хотите поменять или вернитесь назад в главное меню:" 
USEFULL_CONTACTS = "Управляющая компания: \n<b>Диспетчерская служба ООО «УЭР-ЮГ»</b> \n+7 4722 35-50-06 \n<b>Инженеры ООО «УЭР-ЮГ» </b>\n+7 920 566-28-86 \n<b>Бухгалтерия ООО «УЭР-ЮГ» </b>\n+7 4722 35-50-06 \nБелгород, Святo-Троицкий б-р, д. 15, подъезд No 1 \n\nТелефоны для открытия ворот и шлагбаума: \n<b>Шлагбаум «Набережная»</b> \n+7 920 554-87-74 <b>Ворота «Харьковские»</b> \n+7920 554-87-40 \n<b>Ворота «Мост»</b> \n+7 920 554-64-06 \n<b>Калитка 1 «Мост» </b>\n+7 920 554-42-10 \n<b>Калитка 2 «Мост» </b>\n+7 920 554-89-04 \n<b>Калитка 3 «Харьковская» </b>\n+7 920 554-87-39 \n<b>Калитка 4 «Харьковская» </b>\n+7 920 554-89-02 \n\n<b>Охрана </b>\n+7 915 57-91-457 \n\n<b>Участковый </b>\nКуленцова Марина Владимировна \n+7 999 421-53-72"
CHAT_SUPPORT_TEXT = "✅📞✅ Добрый день! Я - диспетчер управляющей компании \"УЭР-ЮГ\", готов помочь Вам.\nНапишите, пожалуйста, интересующий Вас вопрос и ожидайте."

class Texts:

    @staticmethod
    def get_main_menu_text():
        return MAIN_MENU_TEXT
    
    @staticmethod
    def get_application_choosing_text():
        return APPLICATION_CHOOSING_TEXT

    @staticmethod
    def get_complaint_address_text():
        return COMPLAINT_ADDRESS_TEXT
    
    @staticmethod
    def get_complaint_media_text():
        return COMPLAINT_MEDIA_TEXT
    
    @staticmethod
    def get_complaint_body_text():
        return COMPLAINT_BODY_TEXT
    
    @staticmethod
    def get_complaint_sent_text():
        return COMPLAINT_SENT_TEXT
    
    @staticmethod
    def get_settings_text():
        return SETTINGS_TEXT
    
    @staticmethod
    def get_usefull_contacts():
        return USEFULL_CONTACTS
    
    @staticmethod
    def get_chat_support_text():
        return CHAT_SUPPORT_TEXT
    