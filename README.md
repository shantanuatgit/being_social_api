### This is an API created using Django and Django REST Framework
#### The operations like "liking the post, adding the comment, following the user" are ATOMIC.
#### The API can handle high concurrent rate simultaneously (at a same time), the code ensures good concurrancy control.
#### No Race Conditions: Due to the atomic nature of the update() operation and the use of locks, race conditions, where multiple requests try to update the count at the same time, are effectively prevented. Each request waits its turn to update the count.
#### Django-AuthToken used to authenticate the request to API.
#### Pagination, Indexing used for fast responses to the request.


#### To access the API: 
#### Accounts end points
#### http://shantanu3250.pythonanywhere.com/accounts/signup/                             --> create an account
#### http://shantanu3250.pythonanywhere.com/accounts/login/                              --> login account
#### http://shantanu3250.pythonanywhere.com/accounts/<email>/                            --> view Profile (for unauthenticated users posts will not be shown)
#### http://shantanu3250.pythonanywhere.com/accounts/follow/<id of user>/                --> follow and unfollow user
#### http://shantanu3250.pythonanywhere.com/accounts/remove-follower/<id of user>/       --> remove a follower from your followers list
#### http://shantanu3250.pythonanywhere.com/accounts/follower/<email>/                   --> view the followers list of user
#### http://shantanu3250.pythonanywhere.com/accounts/following/<email>/                  --> view the following list of user

#### Pic Post end points                                                                
#### http://shantanu3250.pythonanywhere.com/posts/create/                                --> upload pic with a caption
#### http://shantanu3250.pythonanywhere.com/posts/edit/<id of post>                      --> edit the posted pic (only caption update allowed)
#### http://shantanu3250.pythonanywhere.com/posts/post-reaction/<id of post>             --> like the posted pic
#### http://shantanu3250.pythonanywhere.com/posts/post-comment/<id of post>              --> Comment on the posted pic
#### http://shantanu3250.pythonanywhere.com/posts/post-comment/<id of post>/<comment_id> --> Reply to a comment
#### http://shantanu3250.pythonanywhere.com/posts/delete-comment/<id of post>            --> delete Comment/reply on the posted pic
#### http://shantanu3250.pythonanywhere.com/posts/delete-like/<id of post>               --> unlike the posted pic
#### http://shantanu3250.pythonanywhere.com/posts/post-feed/                             --> list of posted pics in users feed to whom user follow(post shown from mewest to oldest)





