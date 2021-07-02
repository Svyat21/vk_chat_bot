INTENTS = [
    {
        'name': 'Приветствие',
        'tokens': ('прив', 'хай', 'ку', 'hello'),
        'scenario': None,
        'answer': 'Тебя приветствует бот для заказа авиабилетов.\n'
                  'Бот поддерживает команды /ticket и /help.'
    },
    {
        'name': 'Помошь',
        'tokens': ('/help', 'help', 'помощь', 'памагити'),
        'scenario': None,
        'answer': 'Бот служит для заказа авиабилетов.\n'
                  'Для того чтобы приступить к оформлению введите команду - /ticket.'
    },
    {
        'name': 'Заказ билета',
        'tokens': ('/ticket', 'ticket', 'start', 'заказ'),
        'scenario': 'booking_ticket',
        'answer': None
    }
]

SCENARIOS = {
    'booking_ticket': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Чтобы начать регистрацию введите город отправления.',
                'failure_text': 'Во введенном вами городе ошибка, либо из этого города нет вылетов.\n'
                                'Наша авиакомпания осуществляет рейсы из следующих городов:\n'
                                '{available_cities}',
                'handler': 'handler_city_departure',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введите город прилета.',
                'failure_text': 'Во введенном вами городе ошибка, либо в этот город нету авиасообщений.\n'
                                'Наша авиакомпания осуществляет рейсы из города {name_city_departure}:\n'
                                '{available_cities}',
                'handler': 'handler_destination_city',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Введите дату вылета в формате - 01-05-2019.',
                'failure_text': 'Введенная вами дата не ккоректна, попробуйте ввести еще раз\n'
                                'в формате - 01-05-2019. Ближайшая дата вылета, должна быть не раньше чем завтра.',
                'handler': 'handler_date',
                'next_step': 'step4'
            },
            'step4': {
                'text': 'Вберете дату вылета, время вылета всегда будет {time}\n'
                        '{value_date}',
                'failure_text': 'Что-то пошло не так(\n'
                                'Введите номер интересующего вас вылета.',
                'handler': 'handler_value',
                'next_step': 'step5'
            },
            'step5': {
                'text': 'Вберете количество мест (от 1 до 5)',
                'failure_text': 'Что-то пошло не так(\n'
                                'Введите число (от 1 до 5).',
                'handler': 'handler_number_seats',
                'next_step': 'step6'
            },
            'step6': {
                'text': 'Оставьте коментарий в произвольной форме.',
                'failure_text': None,
                'handler': 'handler_comment',
                'next_step': 'step7'
            },
            'step7': {
                'text': 'Подтвердите введенные вами данные:\n'
                        'Рейс: {name_city_departure} - {name_destination_city}.\n'
                        'Дата вылета: {selected_date}г.\n'
                        'Время вылета: {time}.\n'
                        'Количество мест: {number_seats}.\n'
                        'Коментарий: {comment}.\n\n'
                        'В качестве подтверждения введите "да" или "нет".',
                'failure_text': 'Упс, ошибочка, вы можете ввести только да или нет',
                'handler': 'handler_choice',
                'next_step': {
                    'yes': 'step8',
                    'no': 'step9'
                }
            },
            'step8': {
                'text': 'Введите ваш номер телефона в формате 9991112233.',
                'failure_text': 'Таких номеров не бывает :(\n'
                                'Попробуйте еще раз...',
                'handler': 'handler_phone',
                'next_step': 'step11'
            },
            'step9': {
                'text': 'Вы не подтвердили корректность введенных данных, хотите начать оформление с начала?',
                'failure_text': 'Упс, ошибочка, вы можете ввести только да или нет',
                'handler': 'handler_choice',
                'next_step': {
                    'yes': 'step1',
                    'no': 'step10'
                }
            },
            'step10': {
                'text': 'Спасибо за то что решили воспользоваться нашим сервисом.\n'
                        'Когда будете готовы к оформлению, обращайтесь снова.',
                'failure_text': None,
                'handler': None,
                'next_step': None
            },
            'step11': {
                'text': 'Все необходимые данные умпешно заполнены!\n'
                        'Мы свяжемся с вами по данному номеру - {phone}.\n'
                        'Спасибо за то, что выбрали нас!',
                'failure_text': None,
                'handler': None,
                'next_step': None
            }
        }
    }
}

DEFAULT_ANSWER = 'Не знаю как на это ответить.' \
    'Бот служит для заказа авиабилетов. Поддерживает команды /ticket и /help.'
