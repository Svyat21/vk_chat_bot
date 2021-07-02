import logging
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api.utils
import handlers, scenario
from dispatcher import Dispatcer

try:
    import settings
except ImportError:
    exit('DO cp settings.py.default settings.py and set token!')

log = logging.getLogger('bot')


def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('bot.txt', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M"))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)


class UserState:
    """
    Состояние пользователя внутри сценария.
    """

    def __init__(self, scenario_name, step_name, context=None):
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.context = context or {}
        self.dispatcher = Dispatcer()


class Bot:
    """
    Echo bot для vk.com.

    Use python 3.8
    """

    def __init__(self, id_group, token):
        """
        :param id_group: id group из группы vk
        :param token: секретный токен
        """
        self.group_id = id_group
        self.token = token

        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.user_states = dict()  # user_id -> UserState

    def run(self):
        """Запуск бота."""
        for event in self.long_poller.listen():
            try:
                # print(event)
                self.on_event(event)
            except Exception as exc:
                log.exception('Ошибка в обработке события ', exc)

    def on_event(self, event: VkBotEventType):
        """
        Отправляет сообщение назад, если это текст.
        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info('Мы пока не умеем обрабатывать такие события. %s', event.type)
            return

        user_id = event.object.message['peer_id']
        text = event.object.message['text']

        if user_id in self.user_states:
            text_to_send = self.continue_scenario(user_id, text)
        else:
            # search intent
            for intent in scenario.INTENTS:
                log.debug(f'User get {intent}')
                if any(token in text.lower() for token in intent['tokens']):
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self.start_scenario(user_id, intent['scenario'])
                    break
            else:
                text_to_send = scenario.DEFAULT_ANSWER

        self.api.messages.send(
            message=text_to_send,
            random_id=vk_api.utils.get_random_id(),
            peer_id=user_id,
        )

    def start_scenario(self, user_id, scenario_name):
        scen = scenario.SCENARIOS[scenario_name]
        first_step = scen['first_step']
        step = scen['steps'][first_step]
        text_to_send = step['text']
        self.user_states[user_id] = UserState(scenario_name=scenario_name, step_name=first_step)
        return text_to_send

    def continue_scenario(self, user_id, text):
        state = self.user_states[user_id]
        steps = scenario.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        choice = None

        handler = getattr(handlers, step['handler'])
        if handler(text=text, state=state):
            # next step
            if state.context['choice']:
                if state.context['choice'] == 'yes':
                    next_step = steps[step['next_step']['yes']]
                    state.context['choice'] = None
                    choice = 'yes'
                else:
                    next_step = steps[step['next_step']['no']]
                    state.context['choice'] = None
                    choice = 'no'
            else:
                next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                # switch to next step
                if isinstance(step['next_step'], dict):
                    state.step_name = step['next_step'][choice]
                else:
                    state.step_name = step['next_step']
            else:
                # finish scenario
                log.info(state.context)
                self.user_states.pop(user_id)
        else:
            # retry current step
            try:
                text_to_send = step['failure_text'].format(**state.context)
            except KeyError as er:
                text_to_send = 'К сожалению, я всего-лиш бот и не понимаю сложных конструкций.\n' \
                               'Давайте начнем сначала...'
                self.user_states.pop(user_id)
        return text_to_send


if __name__ == '__main__':
    configure_logging()
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()
