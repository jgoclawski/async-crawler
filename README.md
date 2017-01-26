# A Web Crawler With asyncio Coroutines

It's a git repo with code samples based on 
["Web crawler"](https://github.com/aosabook/500lines/tree/master/crawler) chapter from 
["500 Lines or Less"](https://github.com/aosabook/500lines).

It uses an incremental approach, so you can follow along the chapter and run code samples with verbose logging.

Uses Docker and Python 3.6.

The code values output more than readability (you can get that in the book itself!). As Docker is the only dependency,
it makes it easy to run (and change!) the code and observe the results.

Try it yourself, just have Docker installed and run:

```bash
# Run the first example - 01_async.py
./run.sh

# Run selected file - 04_refactored_coroutine_with_generators.py
./run.sh 04_refactored_coroutine_with_generators.py
```

### Licenses

The written material in the book is licensed under [Creative Commons Attribution](http://creativecommons.org/licenses/by/3.0/.) and the 
code samples are licensed under the MIT license. The code in this repo is licensed under the MIT license as well.
