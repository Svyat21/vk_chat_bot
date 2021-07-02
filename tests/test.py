from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, Mock, ANY
from vk_api.bot_longpoll import VkBotMessageEvent
from bot import Bot
import scenario


class Test1(TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {
            'message': {'date': 1607592337, 'from_id': 65089369, 'id': 89, 'out': 0, 'peer_id': 65089369,
                        'text': 'Оалплпл', 'conversation_message_id': 89, 'fwd_messages': [],
                        'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False},
            'client_info': {'button_actions':
                                ['text', 'vkpay', 'open_app', 'location', 'open_link', 'open_photo', 'callback'],
                            'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0}
        },
        'group_id': 199623812, 'event_id': '770f9f8a176c7752d1230fbe34cabd7ee4931a3a'
    }
    INPUTS = [
        'Привет',
        '/help',
        'что происходит?',
        '/ticket',
        'Амстердам',
        'москва',
        'Стамбул',
        '07-04-2021',
        '10-05-2021',
        '6',
        '1',
        '6',
        '1',
        'Какой-то коментарий',
        'Да',
        '9998882233'
    ]
    EXPECTED_OUTPUTS = [
        scenario.INTENTS[0]['answer'],
        scenario.INTENTS[1]['answer'],
        scenario.DEFAULT_ANSWER,
        scenario.SCENARIOS['booking_ticket']['steps']['step1']['text'],
        scenario.SCENARIOS['booking_ticket']['steps']['step1']['failure_text'].format(
            available_cities='Москва, Париж, Лондон, Нью-Йорк, Мадрид, Стамбул'
        ),
        scenario.SCENARIOS['booking_ticket']['steps']['step2']['text'],
        scenario.SCENARIOS['booking_ticket']['steps']['step3']['text'],
        scenario.SCENARIOS['booking_ticket']['steps']['step3']['failure_text'],
        scenario.SCENARIOS['booking_ticket']['steps']['step4']['text'].format(
            time='8:30',
            value_date='1. 10-05-2021\n'
                       '2. 11-05-2021\n'
                       '3. 12-05-2021\n'
                       '4. 13-05-2021\n'
                       '5. 14-05-2021\n'
        ),
        scenario.SCENARIOS['booking_ticket']['steps']['step4']['failure_text'],
        scenario.SCENARIOS['booking_ticket']['steps']['step5']['text'],
        scenario.SCENARIOS['booking_ticket']['steps']['step5']['failure_text'],
        scenario.SCENARIOS['booking_ticket']['steps']['step6']['text'],
        scenario.SCENARIOS['booking_ticket']['steps']['step7']['text'].format(
            name_city_departure='Москва',
            name_destination_city='Стамбул',
            selected_date='10.05.2021',
            time='8:30',
            number_seats='1',
            comment='Какой-то коментарий'
        ),
        scenario.SCENARIOS['booking_ticket']['steps']['step8']['text'],
        scenario.SCENARIOS['booking_ticket']['steps']['step11']['text'].format(
            phone='9998882233'
        )
    ]

    def test_ok(self):
        assert True

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_called_with(obj)

                assert bot.on_event.call_count == count

    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot('', '')
            bot.api = api_mock
            bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        assert real_outputs == self.EXPECTED_OUTPUTS
