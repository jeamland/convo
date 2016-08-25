Feature: Answer processing that asks for a repeat or follow-up

    Scenario: Repeated question
        Given I have a script
        And the script has a question that asks for a repeat
        When I trigger the script
        And I answer the question
        And I answer the question again
        Then the question should be repeated
        And the last answer should be recorded

    Scenario: Follow-up Question
        Given I have a script
        And the script has a question that asks a follow-up question
        When I trigger the script
        And I answer the question
        Then the follow-up question is asked

    Scenario: Answering a follow-up Question
        Given I have a script
        And the script has a question that asks a follow-up question
        When I trigger the script
        And I answer the question
        And I answer the follow-up question
        Then the follow-up answer should be recorded
