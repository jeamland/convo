# -*- coding: utf-8 -*-

"""
Convo - The medium-agnostic conversation framework

Convo is designed to allow you to conduct conversations with a bot. These
conversations can be for any purpose. Conversations can be designed to
yield information for use in performing tasks or they could just be for fun.

:copyright: (c) 2016 by Benno Rice.
:license: BSD License
"""


__title__ = 'convo'
__version__ = '0.0.1'
__build__ = 0x000001
__author__ = 'Benno Rice'
__license__ = 'BSD'
__copyright__ = 'Copyright 2016 Benno Rice'


import re


class ConversationalSupportMixin:
    POSITIVE_RESPONSES = ['y', 'yes', 'yep', 'ok', 'aye', 'sounds good', 'yeah']
    NEGATIVE_RESPONSES = ['n', 'no', 'nope', 'nah', 'nay']

    @staticmethod
    def join_comma_and(items):
        items = [str(i) for i in items]
        if len(items) > 1:
            result = ', '.join(items[:-1])
            return '%s and %s' % (result, items[-1])
        else:
            return items[0]

    @staticmethod
    def response_sense(message, responses):
        for response in responses:
            if response in message.lower():
                return True
        return False

    @classmethod
    def positive_response(cls, message):
        return cls.response_sense(message, cls.POSITIVE_RESPONSES)

    @classmethod
    def negative_response(cls, message):
        return cls.response_sense(message, cls.NEGATIVE_RESPONSES)

class Conversation(ConversationalSupportMixin):
    """A currently active conversation."""


    def __init__(self, manager, script, target, identifier, message, context):
        """
        :param manager: The :class:`ConversationManager <ConversationManager>`
            handling this conversation.
        :param script: The :class:`Script <Script>` driving our end of the
            conversation.
        :param target: A token used by our messaging medium to specify where
            we send our side of the conversation.
        :param identifier: A token used by our messaging medium to identify
            this specific conversation.
        :param message: The message that started this conversation.
        :param context: Any context derived from the conversation trigger.
        """

        self.manager = manager
        self.script = script
        self.target = target
        self.identifier = identifier
        self.message = message
        self.context = context

        self._step = None
        self._script_iter = iter(script)
        self._values = {}
        self._repeat = False

        self.advance()
        self.continue_script()

    def advance(self):
        self._step = next(self._script_iter, None)

    def continue_script(self):
        while self._step is not None:
            if isinstance(self._step, dict):
                self.say(self._step['prompt'])
                return
            elif callable(self._step):
                self._step(self)
                self.advance()
            else:
                self.say(self._step)
                self.advance()

    def process_message(self, message):
        self.message = message

        processor = self._step.get('processor', None)

        if self._step.get('_followup', False):
            value = self._values[self._step['key']]
            self._values[self._step['key']] = processor(self, message, value)
        elif processor is not None:
            self._values[self._step['key']] = processor(self, message)
        else:
            self._values[self._step['key']] = message

        if self._repeat:
            self._repeat = False
        else:
            self.advance()

        self.continue_script()

    def say(self, message):
        self.manager.say(self.target, message)

    def repeat(self):
        self._repeat = True

    def followup(self, prompt, processor):
        self._step['_followup'] = True
        self._step['processor'] = processor
        self._step['prompt'] = prompt
        self._repeat = True

    def get_values(self):
        return self._values

def ask(prompt, key, processor=None):
    if isinstance(processor, list):
        patterns = processor
        def p(conv, message):
            for pattern, func in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match is not None:
                    return func(conv, message, match.groups())
            else:
                conv.say("I can't respond to that, try again?")
                conv.repeat()
        processor = p

    return {
        'prompt': prompt,
        'key': key,
        'processor': processor,
    }


class ConversationManager:
    """
    Watches for conversation triggers and routes messages to active
    conversations.
    """

    def __init__(self, conduit, scripts=None):
        """
        :param scripts: A mapping of trigger regexes or functions to
            :class:`Script <Script>`s.
        """
        self.conversations = {}
        self.conduit = conduit

        if scripts is None:
            self.scripts = {}
        else:
            self.scripts = scripts

    def add_script(self, triggers, script):
        """
        Add a script and its trigger(s).

        :param triggers: A regex, callable or list of either that will trigger
            the script.
        :param script: A :class:`Script <Script>` that will be used when the
            trigger fires.
        """
        if isinstance(triggers, str) or callable(triggers):
            self.scripts[triggers] = script
        else:
            for trigger in triggers:
                self.scripts[trigger] = script

    def start_conversation(self, script, target, identifier, message, context):
        """
        Start a new conversation.

        :param script: The :class:`Script <Script>` that will be used for
            this conversation.
        :param target: A token that the messaging medium will use to represent
            where the conversation is taking place.
        :param identifier: A token identifying this conversation.
        :param message: The message that triggered the conversation.
        :param context: Any context derived from the trigger message.
        """
        self.conversations[identifier] = Conversation(self, script, target,
                                                      identifier, message,
                                                      context)

    def process_message(self, target, identifier, message):
        """
        Process a message coming from our messaging medium.

        :param target: A token that the messaging medium will use to represent
            where the conversation is taking place.
        :param identifier: A token identifying this conversation.
        :param message: The message to process.
        """
        if identifier in self.conversations:
            self.conversations[identifier].process_message(message)
        else:
            for pattern, script in self.scripts.items():
                if callable(pattern):
                    pattern(self, target, identifier, message)
                else:
                    match = re.search(pattern, message)
                    if match is not None:
                        self.start_conversation(script, target, identifier,
                                                message, match.groups())

    def say(self, target, message):
        self.conduit.send(target, message)
