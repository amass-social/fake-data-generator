# Schema

## Ouptut
The current output of the generator, which isn't targeted for frontend or backend use yet, is of the form:
```json
{
  "users": [list of user objects],
  "groups": [list of groups],
  "posts": [list of posts],
  "messages": [list of messages]
}
```

## Aggregated Objects

#### User Account Object + Incidentals
```json
{
  "about": { the basic user account object },
  "friends": [list of user-ids for each friend],
  "posts": [],
  "chats": [postIds]
}
```


## Basic Objects

#### Basic User Account Object
```json
{
  "id": "TEXT - ID starting with 'user-'",
  "photo": "TEXT link to profile picture",
  "displayName" : "TEXT - user's name in natural language (Steve Rogers)",
  "userName" : "TEXT - their username (@SteveRogers)",
  "dateJoined": unix epoch date for when this user created their account,
  "email" : "TEXT - the email that they signed up with",
  "phone" : "TEXT - the phone number they signed up with as a string (could be blank)",
  "friends": [list of friend's user ids],
  "groups": [list of group ids this user is a part of]
}
```

#### Group Object
```json
{
  "id": "TEXT - ID starting with 'group-'",
  "members": [{"id": "userId", "dateJoined": unix epoch time}],
  "name": "a name given to the group"
}
```


#### Post Object
```json
{
  "id": "TEXT - ID starting with 'post-'",
  "senderId": "userId",
  "receiver": {"id": "userId or groupId", "type": "user or group"},
  "title": "",
  "dateSent": unix epoch time,
  "tags": ["text"],
  "content": "a link, either to another website or to an uploaded image",
  "type": "image" or "link",
  "chat": [list of ChatMessage IDs],
  "reactions": [ {"userId": "", "emoji": "unicode for emoji"} ]
}
```


#### ChatMessage Object
```json
{
  "id": "TEXT - ID starting with 'message-'",
  "senderId": "userId",
  "chatId": "a chatId",
  "sent": unix epoch time the user sent this message,
  "content" : "text - either the typed message or a link to an uploaded image (if the user sent an image)",
  "type" : "text" if a text based message and "image" if an image based message,
  "reactions": [ {"userId": "", "emoji": "unicode for emoji"} ]
}
```
