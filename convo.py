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


class Conversation:
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


class ConversationManager:
    """
    Watches for conversation triggers and routes messages to active
    conversations.
    """

    def __init__(self, scripts=None):
        """
        :param scripts: A mapping of trigger regexes or functions to
            :class:`Script <Script>`s.
        """
        self.conversations = {}

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
            self.conversations[identifier].process_message(target, identifier,
                                                           message)
        else:
            for pattern, script in self.scripts.items():
                if callable(pattern):
                    pattern(self, target, identifier, message)
                else:
                    match = re.search(pattern, message)
                    if match is not None:
                        self.start_conversation(script, target, identifier,
                                                message, match.groups())
