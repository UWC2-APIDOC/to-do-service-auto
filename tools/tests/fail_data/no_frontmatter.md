# Document Without Frontmatter

This markdown file has no YAML frontmatter at all.

It should be handled gracefully by the parser, which should return None
when no frontmatter is found.

## Section One

Some content here.

## Section Two

More content.

This tests that the parser doesn't crash when frontmatter is completely absent.
