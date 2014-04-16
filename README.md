wordassociation
===============

Associative Word Graphs

Inspired by "Thinking Fast and Slow", this program emulates the way human memory works.  It reads vast amounts of text, such as entire books at a time, and produces a bidirectional node graph of statisticial associations between words.  For example, after reading several books, it might conclude that the words "house" and "roof" are highly correlated.

The idea is to use this core concept for sentence completion and other uses.

In CS terminology this would be a 'Markov Chain'.

I want to expand upon this premise further.  For instance, in addition to words being correlated to each other, words could be correlated to operations.  For instance, the word "I" might be highly correlated with the verb "to be" or "to have".  The verb could then be "executed".  There could be other sorts of operations as well.  "Pluralization", "Synonym", "Antonym", "Find gender (in other languages)" could be other sorts of operations on word nodes.

By 'activating' certain nodes, adjacent nodes increase in significance by a convolution of statistical weighting between words.  So the more words you specify, the more specific the 'memory' will be.  Weighting is carried by a convolution of an input node's weightings with default, unbiased weightings drawn from large amounts of text.  Weight should also be carried recursively to successive nodes, with some exponential decay factor.  So for instance, if Nodes A and B are activated, A is connected to C and B is connected to D.  And while neither A nor B is connected to Node E, C and D are connected, E could be 'found' with A and B as input nodes because of the recursive impact of statistical weighting.  This aspect is not quite implemented yet.
