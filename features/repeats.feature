Feature: Answer processing that asks for a repeat

    Scenario: Repeated question
        Given I have a script
        And the script has a question that asks for a repeat
        When I trigger the script
        And I answer the question
        And I answer the question again
        Then the question should be repeated
        And the last answer should be recorded
