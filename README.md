### This is an API created using Django and Django REST Framework
#### The operations like "liking the post, adding the comment, following the user" are ATOMIC.
#### The API can handle high concurrent rate simultaneously (at a same time), the code ensures good concurrancy control.
#### No Race Conditions: Due to the atomic nature of the update() operation and the use of locks, race conditions, where multiple requests try to update the count at the same time, are effectively prevented. Each request waits its turn to update the count.
In a high-concurrency scenario where millions of users are liking a post simultaneously, using a database-level atomic operation like update() with the F() expression is a robust way to ensure that the likes_count field is correctly updated without encountering race conditions.
#### Django-AuthToken used to authenticate the request to API.
#### Pagination, Indexing used for fast responses to the request.

#### This project created on Ubuntu 22 LTS OS
#### To run the project locally:
Clone Project via terminal using git command:
```
git clone https://github.com/shantanuatgit/being_social_api.git
```
```python
pip install -r requirements.txt
```

## To access the API: 
#### http://shantanu4n.pythonanywhere.com/docs/
## Accounts end points
#### http://shantanu4n.pythonanywhere.com/accounts/signup/                           --> create an account
#### http://shantanu4n.pythonanywhere.com/accounts/login/                            --> login account
#### http://shantanu4n.pythonanywhere.com/accounts/user_id/                            --> view Profile (for unauthenticated users posts will not be shown)
#### http://shantanu4n.pythonanywhere.com/accounts/follow/id of user/                --> follow and unfollow user
#### http://shantanu4n.pythonanywhere.com/accounts/remove-follower/id_of_user/       --> remove a follower from your followers list
#### http://shantanu4n.pythonanywhere.com/accounts/follower/email/                   --> view the followers list of user
#### http://shantanu4n.pythonanywhere.com/accounts/following/email/                  --> view the following list of user

## Pic Post end points                                                                
#### http://shantanu4n.pythonanywhere.com/posts/create/                                --> upload pic with a caption
#### http://shantanu4n.pythonanywhere.com/posts/edit/id_of_post                        --> edit the posted pic (only caption update allowed)
#### http://shantanu4n.pythonanywhere.com/posts/post-reaction/id_of_post               --> like the posted pic
#### http://shantanu4n.pythonanywhere.com/posts/post-comment/id_of_post                --> Comment on the posted pic
#### http://shantanu4n.pythonanywhere.com/posts/post-comment/id_of_post/comment_id     --> Reply to a comment
#### http://shantanu4n.pythonanywhere.com/posts/delete-comment/id_of_post              --> delete Comment/reply on the posted pic
#### http://shantanu4n.pythonanywhere.com/posts/delete-like/id_of_post                 --> unlike the posted pic
#### http://shantanu4n.pythonanywhere.com/posts/post-feed/                             --> list of posted pics in users feed to whom user follow(post shown from newest to oldest)





