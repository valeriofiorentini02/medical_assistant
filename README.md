# Embedchain Chat Bot Template

<details>
  <summary>Table of contents</summary>
  
  * Introduction
  * Requirements
    * OpenAI API Key
  * Usage
    * Bot Code
    * How to run the bot
  * How to make your own Chat Bot
    * Example 1: Create a Youtube Channel Bot
    * Example 2: Chat with Multiple PDF files
  * Tech Stack
  * Questions and Support
</details>

# Introduction

Welcome to Embedchain Chat Template tutorial for Replit. This repository includes the starter code to quickly get a bot running. 

In this tutorial, we will create a Naval Ravikant Bot. This bot will have following context from the following sources.

* [Naval Ravikant Joe Rogan Podcast](https://www.youtube.com/watch?v=3qHkcs3kG44)
* [The Almanack of Naval Ravikant](https://navalmanack.s3.amazonaws.com/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf)
* [Free Markets Provide the Best Feedback from Naval's blog](https://nav.al/feedback)
* [More Compute Power Doesn’t Produce AGI from Naval's blog](https://nav.al/agi)
* Question / Answer Pair:
  * Q: Who is Naval Ravikant?
  * A: Naval Ravikant is an Indian-American entrepreneur and investor.

If you want you can pick the data sources yourself. Right now embedchain supports three data types, namely

* pdf file
* web page
* youtube video
* question answer

If you want support for more data types, please [open an issue](https://github.com/embedchain/embedchain/issues).

# Requirements

## OpenAI API Key

We use OpenAI's embedding model to create embeddings for chunks and ChatGPT API as LLM to get answers given the relevant docs. Make sure that you have an OpenAI account and an API key. If you have don't have an API key, you can create one by [visiting this link](https://platform.openai.com/account/api-keys).

Once you have the API key, set it in a secret variable called `OPENAI_API_KEY` in this repl. You can use [this documentation link](https://docs.replit.com/programming-ide/workspace-features/secrets) to learn how to set a secret in repl.

# Usage

## Bot Code

* You can find the code in `main.py` file.

## How to run the bot

* You can fork the template and then click on "Run" button.
* You will see some statements about chunks being created. If you want to learn more about the process, read [How does it work in our readme](https://github.com/embedchain/embedchain#how-does-it-work), where we have explained the entire functionality.
* You can enter a query and get an answer from the dataset.

# How to make your own Chat Bot

* In the tutorial we have explained how to create a Naval Ravikant Chat bot, but you can create your own just by updating datasets.

## Example 1: Create a Youtube Channel Bot

* In the video we will cover how can we create a youtube channel bot. We will take Ycombinator Youtube channel as an example and create a chat bot over all its videos.
* For this tutorial, we will use a python package called [scrapetube](https://github.com/dermasmid/scrapetube) which will get list of all videos


```python
import scrapetube

from embedchain import App

ycombinator_bot = App()

# change this to whatever you channel you want to create bot
channel_url = 'https://www.youtube.com/@ycombinator'

videos = scrapetube.get_channel(channel_url=channel_url)
# taking only first 5 videos, if you want all, just remove [:5]
for video in videos[:5]:
    url = f"https://www.youtube.com/watch?v={video['videoId']}"
    ycombinator_bot.add("youtube_video", channel_url)

# YC has around 560+ videos and this will run it for all. Make sure to put a limit to your OpenAI account
ycombinator.query("What is product market fit?")
```

* Yes, using only this much code you can create a chat bot over any youtube video


## Example 2: Chat with Multiple PDF files

* We have all seen [Mayo's](https://twitter.com/mayowaoshin) tutorial on [Chatting with Multiple PDF](https://www.youtube.com/watch?v=Ix9WIZpArm0). We can replicate the same using few lines of code in embedchain

* Here is the code to get Chat with multiple pdf bot up and running

```python
from embedchain import App

chat_with_pdf_app = App()

chat_with_pdf_app.add("pdf_file", "https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q4-2022-Update")
chat_with_pdf_app.add("pdf_file", "https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q3-2022-Update")
chat_with_pdf_app.add("pdf_file", "https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q2-2022-Update")

chat_with_pdf_app.query("What is tesla earning in 2022?")
```

* Please note one thing. Mayo has implemented multiple name spaces querying data in his tutorial videos. Its not supported as of now. If you want me to prioritize this, please leave your view on this [GitHub issue](https://github.com/embedchain/embedchain/issues/97)


# Tech Stack

[embedchain](https://github.com/embedchain/embedchain) is built on the following stack:

- [Langchain](https://github.com/hwchase17/langchain) as an LLM framework to load, chunk and index data
- [OpenAI's Ada embedding model](https://platform.openai.com/docs/guides/embeddings) to create embeddings
- [OpenAI's ChatGPT API](https://platform.openai.com/docs/guides/gpt/chat-completions-api) as LLM to get answers given the context
- [Chroma](https://github.com/chroma-core/chroma) as the vector database to store embeddings

# Questions and Support

* If you have any questions, [join our discord](https://discord.com/invite/nhvCbCtKV), [open an issue on GitHub](https://github.com/embedchain/embedchain/issues) or [DM Taranjeet on twitter](https://twitter.com/messages/compose?recipient_id=1534421484546174976&text=Hey%2C%20Taranjeet.%20I%20have%20some%20feedback%20about%20embedchain).
* If you like [embedchain](https://github.com/embedchain/embedchain), you can star and watch it to stay updated with latest releases.


# License

MIT License