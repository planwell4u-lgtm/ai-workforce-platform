# Staging Demo Support FAQs

This is a reviewed, synthetic ten-question subset of the user-supplied
`train_expanded.json` dataset. It is suitable only for B3 staging and local
tests; it is not an approved customer-policy source.

Load it with `LocalKnowledgeSource.from_jsonl`, tenant `staging-demo`, and a
versioned source reference such as `support-faqs:v1`.
