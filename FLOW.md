- goal: build das2json in Python
- tried using OhmJS, fails due to large input (XML)
- devise streaming parser that can grok large input, and be written in Python
  - -> devise IDE to easily build SWIBs using Python
  - need to handle blocking
	- write bytecode engine that saves enough state and hooks to 0D
	- revelation: replace onesy block-and-fetch with pre-fetch of N characters