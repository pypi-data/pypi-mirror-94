# Typarse

This is a small project born out of my frustration with simple argument parsing in Python.

Not only do I have to instantiate some object whose name I can never remember, then I get way too many 
function parameters to get them right... It's a mess. And I don't even need half the features.

So this is an attempt at streamlining this process while simultaneously promoting some better type safety, by using the
magic of Python type hints! 

Really all the magic here is happening in the BaseParser class. You just need to subclass it, add a few typed parameters,
perhaps with some extra information in dictionaries... and you're done! For examples, just look at, well, examples.

## Supported types

First of all, all the basic types supported by argparse are also supported here. Things like: `str`, `int`, `float`. `bool`s are automatically interpreted as flags, False by default. Each type can be wrapped in a `List` to support reading them like `--list 1 2 3 4`. Each type can also be made `Optional` which makes it, well, optinal.
