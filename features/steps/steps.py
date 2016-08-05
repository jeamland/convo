from convo import ConversationManager


@given(u'there is a script with a trigger phrase')
def step_impl(context):
    context.manager = ConversationManager()
    context.trigger = 'herpy derp'
    context.script = object()
    context.manager.add_script(context.trigger, context.script)


@given(u'there is a script with a trigger function')
def step_impl(context):
    context.manager = ConversationManager()
    context.script = object()
    context.trigger = \
        lambda m, t, i, msg: m.start_conversation(context.script, t, i, msg,
                                                  object())
    context.manager.add_script(context.trigger, context.script)


@given(u'there is a script with a trigger regex with groups')
def step_impl(context):
    context.manager = ConversationManager()
    context.trigger = 'harfy darfy'
    context.context = ('arf', 'arf')
    context.script = object()
    context.manager.add_script(r'(arf).*(arf)', context.script)


@given(u'there is a script with a trigger function that provides context')
def step_impl(context):
    context.manager = ConversationManager()
    context.script = object()
    context.trigger = 'herp derp'
    context.context = context.trigger.split()[0]

    def trigger(m, t, i, msg):
        m.start_conversation(context.script, t, i, msg, msg.split()[0])

    context.manager.add_script(trigger, context.script)


@when(u'the trigger phrase is spoken')
def step_impl(context):
    context.manager.process_message(object(), object(), context.trigger)


@when(u'the trigger function runs')
def step_impl(context):
    context.manager.process_message(object(), object(), 'fnord')


@then(u'a conversation starts using the script')
def step_impl(context):
    assert context.manager.conversations, "No conversation present"
    conversation = list(context.manager.conversations.values())[0]
    assert conversation.script is context.script, "Wrong script running"


@then(u'the conversation has received the context')
def step_impl(context):
    conversation = list(context.manager.conversations.values())[0]
    assert conversation.context == context.context, \
        "Wrong context: %r != %r" % (conversation.context, context.context)
