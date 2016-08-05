Feature: Linear scripts

    Scenario: One-sided conversation
        Given I have a script
        And the script has some statements
        When I trigger the script
        Then all the statements get read out in order

    Scenario: Simple Q&A
        Given I have a script
        And the script has some questions
        When I trigger the script
        And I answer the questions
        Then all the questions get asked in order
        And I can see the answers

    Scenario: Mix of statements and questions
        Given I have a script
        And the script has some statements
        And the script has some questions
        When I trigger the script
        And I answer the questions
        Then all the statements get read out in order
        And all the questions get asked in order
        And I can see the answers

    Scenario: Question with answer processing
        Given I have a script
        And the script has questions that process their answers
        When I trigger the script
        And I answer the questions
        Then all the questions get asked in order
        And I can see the answers
