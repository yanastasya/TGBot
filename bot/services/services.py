def choose_free_admin_chat(
          dict: dict[int, str]
):
    """Выбор свободного чата из словаря, где ключи - id чатов,
    значения - их статус (free или not_free)."""
    for chat_id, status in dict.items():
        if status == 'free':
            return chat_id


def find_user_id_by_chat_id(
          dict: dict[int, dict[str, str | int | bool]],
          chat_id: int
):
    """Поиск id юзера по id чата, в котором обсуждается вопрос юзера."""
    for user_id, data_dict in dict.items():
        if data_dict['admin_chat_id'] == chat_id:
            return user_id
