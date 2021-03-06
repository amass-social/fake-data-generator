# Amass Fake Data Generator README

## About
This project is responsible for generating fake data to populate the website's frontend and backend during development. For a description of the output of this program, see `docs/schema.md`.

`generator.py` generates this fake data in a way that attempts to replicate how actual user data will be created in production.
  1. Create a pool of user accounts
  2. Generate groups out of clustered friends.
  3. Create "friend" connections between those user accounts.
  3. For each pair/group of users, create a list of tags they talk about frequently.
  4. For each pair/group of users, generate a set of posts to be shared between them.
      - Use tag preferences from step 3 to inform this process.
      - Select from different types of posts (youtube links, articles, images, etc).
  5. For each shared post, populate it with reactions + chat responses.
      - leave a small percentage of these as drafts

`frontend_converter.py` takes the output of `generator.py` and filters it into an object focused around a single logged in user for the frontend to load.

## Instructions
Run `generator.py` with optional flags:
  - `-f` - the name of the file you want to write to (defaults to 'data'.json)
      - Note: do not include .json in this filename
  - `-n` - the number of users you want to create (defaults to 50)

Run `frontend_converter.py` with optional flags:
  - `-i` - the name of the input file (ie: the file created by generator.py)
  - `-o` - the name of the output file (defaults to 'frontend-data'.json)
  Note: do not include the file extension in -i and -o flags.

## Issues
For an up to date detailing of issues, see `docs/debt.md`

## Future Work
Adding preference settings to the generated account data, ie:
  - emoji quickdraw preferences
  - color theme preferences

## Credits

List of (pretty wack) baby names:
 - https://github.com/hadley/data-baby-names
