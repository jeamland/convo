Feature: Answer processing that asks for a repeat or follow-up

    Scenario Outline: Detecting simple positive or negative responses
        Given I have a script
        And the script has a question
        When I trigger the script
        And I answer the question with <answer>
        Then the answer should be considered <sense>

        Examples: Simple responses
          | answer | sense    |
          | yes    | positive |
          | no     | negative |
          | YES    | positive |
          | NO     | negative |
          | Yes    | positive |
          | No     | negative |

        Examples: More exotic responses
          | answer      | sense    |
          | y           | positive |
          | n           | negative |
          | yeah        | positive |
          | nah         | negative |
          | aye         | positive |
          | nay         | negative |
          | sounds good | positive |
          | ok          | positive |
