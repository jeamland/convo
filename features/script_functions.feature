Feature: Functions in script flow

    Scenario: Function in a script flow
        Given I have a script
        And the script has a function as part of its flow
        When I trigger the script
        Then the function is called
