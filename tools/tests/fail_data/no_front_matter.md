# Document Without Front matter

This markdown file has no YAML front matter at all.

It should be handled gracefully by the parser, which should return None
when no front matter is found.

## Section One

Some content here.

## Section Two

More content.

This tests that the parser doesn't crash when front matter is completely absent.
