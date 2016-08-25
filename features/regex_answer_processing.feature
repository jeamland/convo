Feature: Answer processing that's different based on regex

    Scenario Outline: Answer processing selection based on regex
        Given I have a script
        And the script has a question that selects processing based on regexes
            | processor   | regex                      |
            | number      | \d+                        |
            | phrase      | correct \w+ battery staple |
        When I trigger the script
        And I answer the question with <answer>
        Then the answer should be processed by <processor>

        Examples: Numbers
          | answer | processor |
          | 5      | number    |
          | 17     | number    |
          | 23     | number    |

        Examples: Phrases
         | answer                        | processor |
         | correct horse battery staple  | phrase    |
         | correct hoarse battery staple | phrase    |
         | correct hearse battery staple | phrase    |
