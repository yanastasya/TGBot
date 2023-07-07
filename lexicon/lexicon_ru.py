LEXICON_RU: dict[str, str] = {
    '/start': 'Добрый день! Выберите, пожалуйста, тему обращения!',
    '/help': 'Справка о работе бота.',
    '/cancel': 'Вы можете начать заново, отправив команду /start.',
    '/cancel_nothing': 'Отменять нечего, начните с команды /start.',
    '/cancel_impossible': 'Наша команда уже работает над вашим обращением и скоро вы увидите ответ.',
    '/help_user': 'Здесь текст, который вылетает на команду help для юзеров',
    '/help_admin': 'Здесь текст, который вылетает на команду help у юзеров',
    'choose_tag': 'Спасибо!\n\nА теперь введите ваш вопрос.',
    'warning_not_tag': 'Пожалуйста, выберите тему обращения, нажав одну из кнопок. Если вы передумали задавать вопрос - отправьте команду /cancel. ',
    'warning_no_free_chat': 'Все чаты заняты, а новые обращения поступают!',
    'confirm_closing_admin': 'Вы уверены, что хотите закрыть обращение?',
    'no_close': 'Ок, можно продолжить работу с обращением.',
    'confirm_closing_user': 'Ваше обращение было закрыто. Вы выяснили всё,что хотели?',    
    'is_closed_for_user_yes': 'Спасибо Вам! Если возникут еще вопросы, начните заново с команды /start.',
    'is_closed_for_user_no': 'Нажмите /start для выбора темы и напишите ваш новый вопрос.',
    'is_closed_for_admin': 'Обращение закрыто. Очистите историю сообщений!',
    'default_admin_chat_title': 'AdminChat'
}

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/start': 'Новое обращение.',
    '/help': 'Справка о работе бота.',   
    '/cancel': 'Отменить выбор темы обращения.'
}
