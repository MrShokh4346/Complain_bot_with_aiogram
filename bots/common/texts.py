MAIN_MENU_TEXT = "✈️ Добро пожаловать в главное меню чат-бота Управляющей компании \"УУР-ЮГ\". Здесь Вы можете оставить заявку для управляющей компании или направить свое предложение по управлению домом. Просто воспользуйтесь кнопками меню, чтобы взаимодействовать с функциями бота:"
APPLICATION_CHOOSING_TEXT = "📛👇📛Выберите категорию, по которой Вы хотите оставить заявку в УК:"
COMPLAINT_ADDRESS_TEXT = "<b>Шаг 1/3.</b> 📝 Напишите адрес или ориентир проблемы (улицу, номер дома, подъезд, этаж и квартиру) или пропустите этот пункт:"
COMPLAINT_MEDIA_TEXT = "<b>Шаг 2/3.</b> Прикрепите фотографию или видео к своей заявке или пропустите этот пункт:"
COMPLAINT_BODY_TEXT = "<b>Шаг 3/3.</b> 📛 Напишите причину обращения в подробностях:"
COMPLAINT_SENT_TEXT = "✅<b> Жало́ба отправле́на администра́ции.</b> Спасибо за Ваше обращение!"


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
    

    