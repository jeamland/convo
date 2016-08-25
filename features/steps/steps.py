from convo import ConversationManager, ask


class DummyConduit:
    def __init__(self):
        self.messages = []

    def send(self, target, message):
        self.messages.append((target, message))

    def last_message(self):
        return self.messages[-1][-1]


@given(u'I have a script')
@given(u'there is a script with a trigger phrase')
def step_impl(context):
    context.conduit = DummyConduit()
    context.manager = ConversationManager(context.conduit)
    context.trigger = 'herpy derp'
    context.script = []
    context.manager.add_script(context.trigger, context.script)


@given(u'there is a script with a trigger function')
def step_impl(context):
    context.conduit = DummyConduit()
    context.manager = ConversationManager(context.conduit)
    context.script = []
    context.trigger = \
        lambda m, t, i, msg: m.start_conversation(context.script, t, i, msg,
                                                  object())
    context.manager.add_script(context.trigger, context.script)


@given(u'there is a script with a trigger regex with groups')
def step_impl(context):
    context.conduit = DummyConduit()
    context.manager = ConversationManager(context.conduit)
    context.trigger = 'harfy darfy'
    context.context = ('arf', 'arf')
    context.script = []
    context.manager.add_script(r'(arf).*(arf)', context.script)


@given(u'there is a script with a trigger function that provides context')
def step_impl(context):
    context.conduit = DummyConduit()
    context.manager = ConversationManager(context.conduit)
    context.script = []
    context.trigger = 'herp derp'
    context.context = context.trigger.split()[0]

    def trigger(m, t, i, msg):
        m.start_conversation(context.script, t, i, msg, msg.split()[0])

    context.manager.add_script(trigger, context.script)


@given(u'the script has some statements')
def step_impl(context):
    statements = """
Pommy ipsum bit of a Jack the lad guinness, shepherd's pie unhand me sir.
Old girl gob the chippy, fork out.
What a mug working class blummin' any road, best be off jellied eels anorak, a tenner the lakes jammy git made a pig's ear of it.
Wedding tackle balderdash down the village green supper sweet fanny adams cobbles, Dalek cheerio Dalek it's just not cricket scally, muck about proper yorkshire mixture.
One off got his end away well fit guinness blimey naff off chips twiglets, Doctor Who you 'avin a laugh Southeners Bad Wolf ee bah gum.
The black death guinness what a doddle, bloody shambles.
    """.split('\n')
    context.statements = [s for s in statements if s]
    context.script.extend(context.statements)

@given(u'the script has some questions')
def step_impl(context):
    context.questions = [
        ("What is your name?", "name", "Arthur, King of the Britons!"),
        ("What is your quest?", "quest", "To find the Holy Grail!"),
        ("What is the flight velocity of an unladen swallow?", "velocity",
            ("African or European?")),
    ]

    context.script.extend([ask(*q[:-1]) for q in context.questions])


@given(u'the script has questions that process their answers')
def step_impl(context):
    def process(convo, message):
        return message[0]

    context.questions = [
        ("What is your name?", "name", "Arthur, King of the Britons!", 'A'),
        ("What is your quest?", "quest", "To find the Holy Grail!", 'T'),
        ("What is the flight velocity of an unladen swallow?", "velocity",
            ("African or European?"), 'A'),
    ]

    entries = [q[:-2] + (process,) for q in context.questions]
    context.script.extend([ask(*e) for e in entries])


@given(u'the script has a question that asks for a repeat')
def step_impl(context):
    context.question = "What is your name?"
    context.key = "name"
    context.answers = ["Arthur, King of the Britons!", "Jeff"]
    context.last_answer = context.answers[-1]
    context.answer_count = len(context.answers)

    def process(convo, message):
        if message != context.last_answer:
            convo.repeat()
        return message

    context.script.append(ask(context.question, context.key, process))


@given(u'the script has a function as part of its flow')
def step_impl(context):
    context.function_called = False

    def function(convo):
        context.function_called = True

    context.script.append(function)


@given(u'the script has a question that selects processing based on regexes')
def step_impl(context):
    context.question = "Why is a duck?"
    context.key = 'quack'
    context.groups = None
    regexes = []

    for row in context.table:
        name, regex = row

        def funcinator(n):
            def func(conv, message, groups):
                context.groups = groups
                return n
            return func

        regexes.append((regex, funcinator(name)))

    context.regexes = regexes
    context.script.append(ask(context.question, context.key, regexes))


@when(u'I trigger the script')
@when(u'the trigger phrase is spoken')
def step_impl(context):
    context.target = object()
    context.identifier = object()
    context.manager.process_message(context.target, context.identifier,
                                    context.trigger)
    context.conversation = context.manager.conversations[context.identifier]


@when(u'the trigger function runs')
def step_impl(context):
    context.target = object()
    context.identifier = object()
    context.manager.process_message(context.target, context.identifier,
                                    'fnord')


@when(u'I answer the questions')
def step_impl(context):
    answers = [(q[0], q[2]) for q in context.questions]
    for question, answer in answers:
        if context.conduit.last_message() == question:
            context.manager.process_message(context.target, context.identifier,
                                            answer)



@when(u'I answer the question')
@when(u'I answer the question again')
def step_impl(context):
    assert context.conduit.last_message() == context.question
    context.manager.process_message(context.target, context.identifier,
                                    context.answers.pop(0))


@when(u'I answer the question with {answer}')
def step_impl(context, answer):
    assert context.conduit.last_message() == context.question
    context.manager.process_message(context.target, context.identifier,
                                    answer)


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


@then(u'all the statements get read out in order')
def step_impl(context):
    statements = [s for s in context.script if isinstance(s, str)]
    prompts = [q['prompt'] for q in context.script if isinstance(q, dict)]
    messages = [m[1] for m in context.conduit.messages]

    for m in messages:
        if prompts and m == prompts[0]:
            prompts.pop(0)
            continue
        if not statements:
            break
        assert m == statements.pop(0)


@then(u'all the questions get asked in order')
def step_impl(context):
    statements = [s for s in context.script if isinstance(s, str)]
    prompts = [q['prompt'] for q in context.script if isinstance(q, dict)]
    messages = [m[1] for m in context.conduit.messages]

    for m in messages:
        if statements and m == statements[0]:
            statements.pop(0)
            continue
        if not prompts:
            break
        assert m == prompts.pop(0)


@then(u'I can see the answers')
def step_impl(context):
    values = context.conversation.get_values()
    answers = [(q[1], q[-1]) for q in context.questions]

    for key, answer in answers:
        assert key in values
        assert values[key] == answer


@then(u'the question should be repeated')
def step_impl(context):
    prompts = [m[1] for m in context.conduit.messages]
    assert len(prompts) == context.answer_count
    assert prompts == [context.question] * context.answer_count


@then(u'the last answer should be recorded')
def step_impl(context):
    answer = context.conversation.get_values()[context.key]
    print(repr(answer), repr(context.last_answer))
    assert answer == context.last_answer


@then(u'the function is called')
def step_impl(context):
    assert context.function_called


@then(u'the answer should be processed by {processor}')
def step_impl(context, processor):
    answer_name = context.conversation.get_values()[context.key]
    print(repr(context.regexes))
    assert answer_name == processor, "%s != %s" % (answer_name, processor)


@then(u'{string} should be in the regex groups')
def step_impl(context, string):
    assert string in context.groups
