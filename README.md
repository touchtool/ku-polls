# KU Polls
[![Build Status](https://app.travis-ci.com/touchtool/ku-polls.svg?branch=main)](https://app.travis-ci.com/touchtool/ku-polls)
[![codecov](https://codecov.io/gh/touchtool/ku-polls/branch/main/graph/badge.svg?token=OKTDNJ2MYN)](https://codecov.io/gh/touchtool/ku-polls)    
A web application for conducting polls at [Kasetsart University](https://www.ku.ac.th/th)

## Project Documents

[Project Wiki](../../wiki/Home)

[Requirements](../../wiki/Requirements)

[Vision Statement](../../wiki/Vision%20Statement)    

- [Iteration 1 Plan](../../wiki/iteration%201)    
- [Iteration 2 Plan](../../wiki/iteration%202)   
- [Iteration 3 Plan](../../wiki/iteration%203) 

## How to run
Install the Ku-polls.
```
python3 manage.py migrate
python3 manage.py loaddata users polls
```

## Running KU Polls

Users provided by the initial data (users.json):

| Username   | Password     |
|-----------:|-------------:|
| Demo1234   | votehello    |
| qwerty     | votenight    |