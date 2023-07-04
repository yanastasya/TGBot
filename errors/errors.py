class NotFreeChatsException(Exception):
    def __str__(self):
        return "Все чаты заняты, обращения пересылаются в резервный чат."
