<!-- vale off -->
<!-- markdownlint-disable -->
<!-- front matter not required -->
# The Advantages and Disadvantages of Markdown as a Documentation Source Language

![Markdown image from Wikipedia ](https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Markdown-mark.svg/2560px-Markdown-mark.svg.png)

Markdown is most likely the most popular documentation language today. Its success is no surprise because it's relatively easy to learn. However, it doesn't come without disadvantages.

## Short and Sweet

I prepared a neat little table for those of you who prefer to consume information in tabular form. Also, scientists claim that new facts stick better if they are presented to us several times in different forms, so if you are new to Markdown, it's useful to read everything.

| Pros        | Cons        |
| ------------- |-------------|
| Simple | Not always simple enough |
| Plain text | Limited customization options |
| Easy to integrate | Requires extensions |
| Supports API examples | Inconsistent rendering | 

## Simple or Not Simple Enough?

Markdown is praised for its simplicity. It's not only easy to write, it is also easy to read—even people who don't understand Markdown *per se* will understand the gist of it. It's in plain text, which means that it:
* Is readable for humans.
* Works in every environment.
* Can be mastered quickly even by people with no IT knowledge.

However, there are always **some** people who will complain that it's **too** technical because they believe that writing should be completely separated from the IT part of this profession.

This does not change the fact that Markdown is:
1. Intuitive (for example, size of titles changes with adding or removing # signs).
2. Uses minimal syntax.
3. Pretty fool proof (for example, numbered lists will show correct numbers even if you make a mistake).
4. Not overly standardized.
5. Compatible with all common editors and software (although different editors can render it a bit differently).

## Or Too Simple Instead?

Since Markdown is a simplistic language, it doesn't offer more complex formatting options, like multi-column layouts, built-in table of contents, etc. Despite these shortcomings, I have no doubt it is still suitable for our course, as inline code makes API documentation easily readable.

For example, I asked Chat GPT to give us a little API-related code example to show how it looks in Markdown, and this was the result:

```http
POST /api/v1/todos HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer {{token}}

{
  "title": "Buy climbing chalk",
  "due_date": "2025-10-10",
  "priority": "high"
}
```

However, it is true that Markdown might come short when there is a need for more versatile documentation. 

## Final Thoughts

It is true that Markdown's simplicity is a two-edged sword. It requires extensions, which creates external dependencies. The lack of standardization also leads to rendering differences. 

Despite these limitations, I feel that the benefits (such as the ease of use, high compatibility with popular software and environments, simple maintenance) outweigh the downsides.

If you wish to learn more about Markdown, check out this useful [overview](https://github.com/adam-p/markdown-here/wiki/).

> Note: I used Chat GPT to write the API-related code portion of this assignment. I also used the AI prompt we built in class to assess this assignment before I turned it in.