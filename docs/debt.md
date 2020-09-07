# Technical Debt and Known Issues

## Issues + To Do:
  1. The following time rules are not being respected:
      - a posts creation date has to be after both users accounts were created (and after they became friends)
      - a message can only be created after the post has been created

  2. We don't have a "date friended" attribute for connections+groups
  3. There should be a "get_random_text_with_emojis()" function that gets used for paragraphs
  4. The content for messages is hardcoded to be text right now.
    - in the future, it should be either text or an image
  5. ~~`IMPORTANT` Reactions aren't built~~
  6. phone numbers aren't a thing, hardcoded to string 'blank for now'
  7. ~~`IMPORTANT` Chat message responses haven't been built yet, so it's only the sender's original messages~~
  8. The sender's original messages have a different time than the post
  9. Posts aren't aware of what the messages are attributed to them
  10. Posts aren't left as drafts
  11. ~~`IMPORTANT` the output of the generator isn't targeted for database storageThe data will look different when modified for that use cases.~~
  12. The frontend object is not partitioned into smaller, more loadable pieces that would be used in production. 
