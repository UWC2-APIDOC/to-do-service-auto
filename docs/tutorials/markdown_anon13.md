---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
parent: Tutorials
nav_order: 4
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

# Breaking down Markdown
![Alt text](https://i.dailymail.co.uk/1s/2024/08/09/22/88366629-0-image-a-33_1723237478545.jpg)

This page will provide an introduction, some advantages and limitations of Markdown, and some common Markdown notations.
------

### Markdown is a text-based notation used to inform HTML styling from plain-text sources.

Used ***widely*** in docs-as-code workflows, this text-based notation has proven to be a **top choice** because of its ability to produce styled text without the neeed to embed complex formatting tags in the documentation text.

# Markdown loves me 
### "In a way, it is the limitations of Markdown that make it revolutionary."  - Peter Conrad, "Why You Should and Should Not Use Markdown", April 2019
#### The pro's of Markdown include:
1. Its accessibility
     - Platform-independent
2. Its simplicity to learn
     - Readable in plain text
3. Its provision of an uncluttered writing enviornment
     - Writers and developers alike can use Markdown with ease

# Markdown loves me not
### "I can't take this guy's article seriously because the website is so ugly..." -[u/deleted] Reddit User, "Thoughts Against Markdown", 2022
#### The cons of Markdown include:
1. The limited formatting and styling options
   -   Markdown provides an underwhelming end-user experience
2. Vulnerable to XSS attacks
   - When you add HTML tags to Markdown, it creates a security risk.
3. There are a number of alternatives to Markdown that some consider better choices:

| Asciidoc               | Restructured Text (ReST)           | Creole  |
| -------------        |:-------------:| -----:|
| Allows structured documents to be converted into other output formats    | Used in the context of interspersing documentation with source code | A project that finds common syntax |

# Common Markdown Notations

| Headings | Text Effects | Links |
|----------|--------------|--------
| `# Heading 1` | `**bold text**` | `[I'm an inline-style link](https://www.washington.edu/)`
| `## Heading 2` | `*italic text*` | `[I'm an inline-style link with title](https://www.washington.edu/ "UW's Homepage)`
| `### Heading 3` | `***bold and italic***` | `[I'm a reference style link][Example case reference text]`


# TL;DR: Markdown Pro Tips
[Explore this Markdown cheat sheet to familiarize yourself before you get started](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#images)

Use the VSCode preview feature to check for notation errors
