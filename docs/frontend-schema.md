# Frontend Schema
This file describes the output of frontend_converter.py

```javascript
{
  'user': {/* Same info as described in schema.md's basic user account object */},
  'lookup': {
    /* any ID -> it's corresponding object */
  },

  'groupings': {
    'friends': [/* list of user IDs */],
    'users'  : [/* list of user IDs */],
    'groups' : [/* list of group IDs */]
    'postsSent' : [
      {'id': /* id of the post */, 'chat': [/* list of all message ids associated to this post */]}
    ],
    'postsReceived': [/* same as postsSent */]
  }
}
```
