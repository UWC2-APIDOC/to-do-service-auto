<!-- vale off -->
# Markdown and text formatting guide

This guide compiles formatting standards and best practices observed across documentation projects.

## Heading standards

### Spacing

**Leave a blank line before and after each heading**

✅ **Correct:**

```markdown
## What is the API

First line of text...

### How to get started

First line of text...

```

❌ **Incorrect:**

```markdown
## What is the API?
First line of text...

Last line of text...
### How to get started.
First line of text...

```

### Capitalization

**Use sentence-style capitalization** (capitalize only first word and proper nouns):

✅ **Correct:**

```markdown

## Getting started with the API

### What is the To-Do service?

## Prerequisites for installation

```

❌ **Incorrect:**

```markdown
## Getting Started With The API
### What Is The To-Do Service?
## Prerequisites For Installation
```

### Punctuation

**Do not end headings with punctuation:**

✅ **Correct:**

```markdown

## What is the API

### How to get started

```

❌ **Incorrect:**

```markdown
## What is the API?
### How to get started.
```

### Hierarchy

**Increment heading levels by one at a time:**

✅ **Correct:**

```markdown

# Main title

## Section

### Subsection

#### Detail

```

❌ **Incorrect:**

```markdown
# Main title
### Subsection (skips h2)
```

---

## Lists and bullets

### Spacing

**Leave a blank line before and after each list**

✅ **Correct:**

```markdown
Introductory text...

- First level
    - Second level
    - Second level
- First level

Next line of text
```

❌ **Incorrect:**

```markdown
Introductory text...
- First level
  - Second level (only 2 spaces)
  - Second level
- First level
Next line of text
```

### Indentation

**Use 4-space indentation for nested list items:**

✅ **Correct:**

```markdown
- First level
    - Second level
    - Second level
- First level
```

❌ **Incorrect:**

```markdown
- First level
  - Second level (only 2 spaces)
  - Second level
- First level
```

### Punctuation in lists

**For complete sentences, and fragments that end the introductory phrase, use periods.**
**For fragments, omit periods:**

✅ **Correct:**

```markdown

The following are examples of complete sentences.

- This is a complete sentence describing the feature.
- Another complete sentence with proper punctuation.

Or:

These are examples of fragments:

- Brief point
- Another brief point
- Final point

Or:

This is an example of fragments that complete the introductory sentence.

Our favorite things to do are:

- Go to the beach.
- Sail in a boat.
- Ride motorbikes on the sand.

```

❌ **Mixing styles:**

```markdown
- This is a complete sentence.
- Brief point
- Another sentence here
```

### Oxford comma

**Always use a comma before the final "and" or "or" in a list of three or more items:**

✅ **Correct:**

- "The API supports users, tasks, and reminders."
- "You can view, edit, or delete tasks."

❌ **Incorrect:**

- "The API supports users, tasks and reminders."
- "You can view, edit or delete tasks."

---

## Voice and tone

### Active vs passive voice

**Prefer active voice over passive voice:**

✅ **Active:**

- "The system sends an alert"
- "You assign tasks to users"
- "The API returns a response"

❌ **Passive:**

- "An alert is sent by the system"
- "Tasks are assigned to users"
- "A response is returned"

### Personal pronouns

**Use second-person "you" to address the reader:**

✅ **Correct:**

- "You can create a new task by..."
- "Configure your settings before..."

❌ **Incorrect:**

- "I recommend creating a new task..."
- "We can configure the settings..."
- "One should create a new task..."

### Gender-Neutral Language

**Use "they/them" as gender-neutral pronouns:**

✅ **Correct:**

- "When a user logs in, they see..."
- "Each developer can configure their environment..."

❌ **Incorrect:**

- "When a user logs in, he sees..."
- "Each developer can configure his environment..."

---

## Punctuation

### Exclamation points

**Do not use exclamation points in technical documentation:**

✅ **Correct:**

- "This feature is now available."
- "The API responds quickly."

❌ **Incorrect:**

- "This feature is amazing!"
- "You'll love this API!"

### Ellipses

**Do not use ellipses (...) in technical documentation:**

✅ **Correct:**

- "The process takes time to complete."
- "Several options are available."

❌ **Incorrect:**

- "The process takes time..."
- "Several options are available..."

### Em Dashes

**Prefer a sentence structure that does not need em dashes or parentheses.**
**Use em dashes sparingly, if at all.**
**If used, insert them without spaces on either side:**

✅ **Correct:**

- "The API—when properly configured—works efficiently."

✅ **Better**

- "When properly configured, the API works efficiently."

❌ **Incorrect:**

- "The API — when properly configured — works efficiently."
- "The API - when properly configured - works efficiently."

### Parentheses

**Prefer a sentence structure that does not need em dashes or parentheses.**
**Use parentheses sparingly and only when necessary. Do not nest parentheses:**

✅ **Correct:**

- "Install Node.js (version 16 or later)"

✅ **Better**

- "Install the latest version of Node.js. Confirm that it's version 16 or later."
- "Install Node.js. Confirm that it's version 16 or later."
- "Install a version of Node.js that is version 16 or later."

❌ **Overuse:**

- "The API (which is RESTful) uses JSON (JavaScript Object Notation) for responses."

❌ **Nesting:**

- "The API (which includes endpoints (like GET and POST)) is documented."

### Semicolons

**Use semicolons only when necessary to separate complex list items or
join closely related independent clauses:**

✅ **Appropriate use:**

- "The API supports three formats: JSON, which is the default; XML,
  which requires configuration; and CSV, which is limited."
- "The server responded quickly; the client processed the data immediately."

❌ **Unnecessary:**

- "Install the software; configure the settings." (Use period instead)

### Quotation Marks

**Place commas and periods inside quotation marks:**

✅ **Correct:**

- Click the "Submit" button.
- The field is labeled "Username."

❌ **Incorrect:**

- Click the "Submit " button.
- The field is labeled "Username".

---

## Numbers and dates

### Time format

**Use uppercase AM/PM with a space:**

✅ **Correct:**

- "9:00 AM"
- "3:30 PM"
- "12:00 PM"

❌ **Incorrect:**

- "9:00AM"
- "3:30pm"
- "12:00 P.M."

### Date format

**Use "Month DD, YYYY" format:**

✅ **Correct:**

- "July 31, 2024"
- "January 1, 2025"

❌ **Incorrect:**

- "31 July 2024"
- "7/31/2024"
- "2024-07-31"

### Ordinal numbers

**Spell out ordinal numbers less than 10:**

✅ **Correct:**

- "The first step is..."
- "Complete the second task..."
- "This is the 10th iteration."

❌ **Incorrect:**

- "The 1st step is..."
- "Complete the 2nd task..."

### Number ranges

**Express ranges using "to" or a hyphen without additional words:**

✅ **Correct:**

- "Values 1-10 are valid"
- "Values 1 to 10 are valid"

❌ **Incorrect:**

- "Values from 1 to 10 are valid"
- "Values between 1 and 10 are valid"

### Units of measurement

**Insert a non-breaking space between numbers and units:**

✅ **Correct:**

- "12 MPH"
- "5 MB"
- "100 GB"

❌ **Incorrect:**

- "12MPH"
- "5MB"
- "100GB"

---

## Acronyms and abbreviations

### First use

**Spell out acronyms on first use, with the acronym in parentheses:**

✅ **Correct:**

- "Application Programming Interface (API)"
- "Long-Term Support (LTS) version"

Then use the acronym in subsequent references:

- "The API provides..."
- "Install the LTS version..."

### Punctuation

**Do not use periods with acronyms:**

✅ **Correct:**

- "API"
- "HTML"
- "URL"

❌ **Incorrect:**

- "A.P.I."
- "H.T.M.L."
- "U.R.L."

### Internet slang

**Do not use internet slang or abbreviations:**

❌ **Avoid:**

- FWIW (for what it's worth)
- TBH (to be honest)
- IMO (in my opinion)
- FYI (for your information - spell it out)

---

## Formatting conventions

### Sentence spacing

**Use only one space between sentences:**

✅ **Correct:**

- "This is sentence one. This is sentence two."

❌ **Incorrect:**

- "This is sentence one.  This is sentence two." (two spaces)

### Spelling

**Use American English spelling:**

✅ **American:**

- color
- center
- organize
- analyze

❌ **British:**

- colour
- centre
- organise
- analyse

### Contractions

**Prefer contractions except in negative instructions**
**Acceptable in conversational documentation:**

✅ **Context-appropriate:**

- "You'll find the option in settings."
- "It's important to save your work."

**Avoid in formal technical specifications:**

- Use "You will find" instead of "You'll find"
- Use "It is important" instead of "It's important"

**Negative instructions**

- Do not use the dangerous device.
- That is not the safe approach.

### Parenthetical plurals

**Do not use constructions like "parameter(s)" or "option(s)":**

✅ **Correct:**

- "Select a parameter" or "Select parameters"
- "Configure the option" or "Configure the options"

❌ **Incorrect:**

- "Select parameter(s)"
- "Configure option(s)"

---

## Code and technical elements

### Inline Code

**Use backticks for inline code, variable names, parameter names, arguments, and file names:**

✅ **Correct:**

- "Set the `timeout` parameter to 30."
- "Edit the `config.json` file."
- "Call the `getUserData()` function."

### Code Blocks

**Use fenced code blocks with language specifiers:**

✅ **Correct:**

````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

````markdown

```bash
npm install package-name
```
````

### Consistency

**Maintain consistent capitalization and formatting for interface elements:**

✅ **Consistent:**

- Always write "Submit" button (not "submit" or "SUBMIT")
- Always write "Settings" menu (not "settings" or "SETTINGS")

---

## Document structure

### Section organization

**Use logical section headings to break up content:**

```markdown
# Document Title

## Introduction
Brief overview of the topic.

## Prerequisites
What the reader needs before starting.

## Getting started
Step-by-step instructions.

## Advanced topics
More complex information.

## Troubleshooting
Common issues and solutions.

## Related resources
Links to additional information.
```

### Timestamps

**When documenting time-based content (like video transcripts), use [MM:SS] format:**

```markdown
## Section name
[05:23]

Content that starts at 5 minutes, 23 seconds...
```

### Summaries and Checklists

**For procedural documents, provide a checklist summary:**

```markdown
## Summary checklist

- [ ] Complete prerequisite setup
- [ ] Install required software
- [ ] Configure settings
- [ ] Test the installation
- [ ] Verify output
```

---

## Readability

### Flesch-Kincaid Grade Level

**Aim for a grade level of 8 or below when possible:**

- Use shorter sentences
- Use simpler words when they convey the same meaning
- Avoid jargon unless necessary
- Define technical terms when first used

### Word Choice

**Avoid wordy phrases:**

✅ **Concise:**

- "Use" instead of "utilize"
- "Change" instead of "modify"
- "Before" instead of "prior to"
- "More" instead of "additional"
- "Now" instead of "at this point in time"

### Sentence Length

**Keep line lengths under 100 characters.**
**Keep sentences under 25 words when possible:**

✅ **Clear:**

- "Configure the API settings. Save your changes. Test the connection."
- "You should configure the API settings. Make sure to save all your changes before attempting
    to test whether the connection is working properly."

❌ **Too long:**

- "You should configure the API settings and then make sure to save all of your changes before attempting to test whether the connection is working properly."

---

## Alt text and accessibility

### Images

**Always provide alt text for images:**

✅ **Correct:**

```markdown
![Diagram showing API request flow](api-flow.png)
```

❌ **Incorrect:**

```markdown
![](api-flow.png)
```

### Inline HTML

**Minimize or avoid inline HTML in markdown documents:**

✅ **Prefer:**

```markdown
![Description](image.png)
```

❌ **Avoid when possible:**

```html
<img src="image.png" alt="Description">
```

---

## Examples

### Provide examples

**Include examples for complex concepts:**

````markdown
## Authentication

To authenticate, include your API key in the header:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.example.com/data
```

The response will include a session token:

```json
{
  "session_token": "abc123xyz",
  "expires_in": 3600
}
```
````

---

## Common Mistakes to Avoid

❌ **Title Case headings:** "Getting Started With The API"
❌ **Heading punctuation:** "What is the API?"
❌ **Passive voice overuse:** "The data is processed by the server"
❌ **Exclamation points:** "This is great!"
❌ **Internet slang:** "FYI, the API works well"
❌ **Two spaces after periods:** "Sentence one.  Sentence two."
❌ **Nested parentheses:** "The API (which uses JSON (a format)) is fast"
❌ **British spelling:** "colour", "organise"
❌ **Inconsistent capitalization:** "Submit" button vs "submit" button
❌ **Missing alt text:** `![](image.png)`
❌ **Missing blank line before and after heading**
❌ **Missing blank line before and after list**

---

## Quick Reference

| Element | Rule | Example |
| --------- | ------ | --------- |
| Headings | Sentence case, no punctuation, blank line before and after | `## Getting started` |
| Lists | 4-space indent for nested, blank line before and after | See Lists section |
| Voice | Active voice | "The system sends" not "is sent" |
| Pronouns | Use "you" and "they" | "You configure" not "One configures" |
| Time | Uppercase AM/PM with space | "9:00 AM" |
| Dates | Month DD, YYYY | "July 31, 2024" |
| Acronyms | Spell out first use | "API (Application Programming Interface)" |
| Code | Use backticks | `variable_name` |
| Code blocks | Use backticks, specify language, ensure blank line before and after | ```text |
| Commas | Oxford comma in lists | "a, b, and c" |

---

## Maintaining These Standards

### Tools

Use linters and style checkers:

- **markdownlint** - Checks markdown syntax
- **Vale** - Checks writing style
- **write-good** - Checks readability

### Continuous Improvement

- Review linter feedback regularly
- Update standards as patterns emerge
- Maintain consistency across all documents
- Document exceptions when necessary

---

## References

These standards are compiled from:

- Google Developer Documentation Style Guide
- Microsoft Writing Style Guide
- Industry best practices
- Linter rule recommendations (Vale, markdownlint, write-good)
