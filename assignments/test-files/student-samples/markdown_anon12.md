---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
parent: Tutorials
nav_order: 3
# tags used by AI files
description: Test file for testing and troubleshooting
topic_type: tutorial
tags:
    - api
categories: 
    - tutorial
ai_relevance: high
importance: 6
prerequisites: 
    - /before-you-start-a-tutorial
    - /api/user
related_pages: []
examples: []
api_endpoints: 
    - POST /users
version: "v1.0"
last_updated: "2026-03-01"
# vale  on
# markdownlint-enable
---

<!-- vale off -->
<!-- markdownlint-disable -->

# **Introduction**

I am not as familiar with Markdown as I am with other open source markup languages such as AsciiDoc. In the past, I have used Markdown as my markup language when kicking off documentation for a Red Hat/IBM collaborative project called "InstructLab." Because it was essentially a startup project, documentation was hosted on GitHub and relied primarily on Markdown, meaning that I had to shift from AsciiDoc to Markdown while I prioritized that project at my job. Here are some advantages and disadvantages that I have experience using Markdown in the past:

## **Advantages of using Markdown**

1. Although I'm relatively limited in experience with using Markdown, I have found that it is beginniner-friendly. Because Markdown is widely adopted across the tech industry and beyond, there are *many* resources online. From [cheat sheets](https://www.markdownguide.org/cheat-sheet/) to [online videos](https://www.youtube.com/watch?v=_PPWWRV6gbA), learning Markdown is a breeze. An added bonus to learning Markdown is that, because it's so widely adopted across various industries, learning could be beneficial for one on the job market.

2. As the preferred markup language for GitHub, Gitlab, and other documentation platforms, Markdown allows one to easily create a hosted website using platforms like [MKDocs](https://www.mkdocs.org/getting-started/). My experience with MKDocs is that it is easy to learn and valuable for providing documentation to users. In the past, I've learned MKDocs in about a day, thanks to various online tutorials such as the following:
    1. [Material for MKDocs](https://www.youtube.com/watch?v=xlABhbnNrfI)
    2. [How To Create STUNNING Code Documentation With MkDocs Material Theme](https://www.youtube.com/watch?v=Q-YA_dA8C20)
3. Converstion is the last benefit that I'll mention here. Markdown can be easily to other formats like HTML or PDFs, making it a *nearly* perfect one-stop-shop for documentation needs. In my current role, I've actually done a little bit of research on this. Currently, we are transitioning out of an AsciiDoc environment and into a DITA environment, but if we were going to a Markdown environment (from AsciiDoc), we would likely be better off in the future because of Markdown's ability to easily convert into other formats. 

## **Disadvantages of using Markdown**

1. In the above section, I mentioned how Markdown was *nearly* perfect. From my experience, Markdown is inferior to some other languages, where complex formatting can be accomplished. For example, AsciiDoc provides the capability to create tables that are far more complex than Markdown.

2. Builds off the previously-listed disadvantage, other markup languages such as, say, AsciiDoc, shine more when conditional content is required across multiple distributions. Markdown is far simpler in this regard, but that can be a weakness depending on the project's needs. Markdown simply makes content resuse more difficult and doesn't favor *modular* documentation in the same way that AsciiDoc or some other options might. In the words of a coworker:

    > "Markdown does about 80% of what we need. It's the other 20% that completely stops us from using it." 

# Conclusion

Overall, the markup language that you choose depends on your use case. There are many advantages and disadvantages to Markdown, such as its accessibility and the support offered for it online. However, for larger and more complex projects, Markdown might not be the best choice. Other languages, such as AsciiDoc, provide more formatting options in my experience, but, as such, have a higher learning curve.[^1]

[^1]: SEO in the AI era might benefit from Markdown, notably when compared to DITA. I'm interested to see how this plays out in the future.