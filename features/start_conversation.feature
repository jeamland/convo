Feature: Starting a conversation

    Scenario: Triggering a conversation using a regex
        Given there is a script with a trigger phrase
        When the trigger phrase is spoken
        Then a conversation starts using the script

    Scenario: Triggering a conversation using a function
        Given there is a script with a trigger function
        When the trigger function runs
        Then a conversation starts using the script

    Scenario: Passing context to conversation start from regex
        Given there is a script with a trigger regex with groups
        When the trigger phrase is spoken
        Then a conversation starts using the script
        And the conversation has received the context

    Scenario: Passing context to conversation start from function
        Given there is a script with a trigger function that provides context
        When the trigger phrase is spoken
        Then a conversation starts using the script
        And the conversation has received the context
