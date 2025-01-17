# Book_Management

I make 3 apps in this Auth, Books and Borrowing.

**Auth App:**
I used JWT Authentication for Token generation through login user.
I make custom user, which is register and login and successfully saves to postgresql database and when we login through its credential ( email and password ) then a jwt token is obtained which is then used to make crud operations on books.

**Books App:**
After passing the  bearer token we can make crud operations on books ( create, retrieve, get_all, update, partial_update, delete ). 
We integrate websockets for live notification.
Whenever we create, update, partial_update and delete then a websocket notification is triggered and shown in the websocket connection

**Borrowing App:**
A logged in user can borrow books of other added user's books. He will return the book so that someone will get that book.
