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

    Scenario Outline: Passing regex groups to processing function
        Given I have a script
        And the script has a question that selects processing based on regexes
            | processor   | regex                        |
            | number      | (\d+)                        |
            | phrase      | correct (\w+) battery staple |
        When I trigger the script
        And I answer the question with <answer>
        Then the answer should be processed by <processor>
        And <group> should be in the regex groups

        Examples: Numbers
          | answer | processor | group |
          | 5      | number    | 5     |
          | 17     | number    | 17    |
          | 23     | number    | 23    |

        Examples: Phrases
         | answer                        | processor | group  |
         | correct horse battery staple  | phrase    | horse  |
         | correct hoarse battery staple | phrase    | hoarse |
         | correct hearse battery staple | phrase    | hearse |
