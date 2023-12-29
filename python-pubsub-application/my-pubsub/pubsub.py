import hashlib
import pickle
import random
import re
import secrets
from bisect import bisect
from collections import defaultdict, deque
from heapq import merge
from itertools import islice
from sys import intern
from time import sleep, time
from typing import (DefaultDict, Deque, Dict, List, NamedTuple, Optional, Set,
                    Tuple)

User = str
Timestamp = float
HashAndSalt = Tuple[bytes, bytes]
HashTag = str


class Post(NamedTuple):
    timestamp: Timestamp
    user: User
    text: str


class UserInfo(NamedTuple):
    displayname: str
    email: str
    hashed_password: HashAndSalt
    bio: Optional[str]
    photo: Optional[str]


posts = deque()  # type: Deque[Post]     # Posts from newest to oldest
user_posts = defaultdict(deque)  # type: DefaultDict[User, Deque[Post]]
hashtag_index = defaultdict(deque)  # type: DefaultDict[HashTag, Deque[Post]]
following = defaultdict(set)  # type: DefaultDict[User, Set[User]]
followers = defaultdict(set)  # type: DefaultDict[User, Set[User]]
user_info = dict()  # type: Dict[User, UserInfo]

hashtag_pattern = re.compile(r"[#@]\w+")


def post_message(user: User, text: str, timestamp: Optional[Timestamp]=None) -> None:
    user = intern(user)
    timestamp = timestamp or time()
    post = Post(timestamp, user, text)
    posts.appendleft(post)
    user_posts[user].appendleft(post)
    for hashtag in hashtag_pattern.findall(text):
        hashtag_index[hashtag].appendleft(post)



def follow(user: User, followed_user: User) -> None:
    user, followed_user = intern(user), intern(followed_user)
    following[user].add(followed_user)
    followers[followed_user].add(user)


def posts_by_user(user: User, limit: Optional[int] = None) -> List[Post]:
    return list(islice(user_posts[user], limit))


def get_posts(user: User, limit: Optional[int] = None) -> List[Post]:
    return list(islice(user_posts[user], limit))


# return post from following user - using merge and limit
def posts_for_user(user: User, limit: Optional[int] = None) -> List[Post]:
    relevant_posts = merge(
        *(user_posts[followed_user] for followed_user in following[user]), reverse=True
    )
    return list(islice(relevant_posts, limit))


def get_followers(user: User, limit: Optional[int] = None) -> List[User]:
    return list(islice(followers[user], limit))


def get_followed(user: User, limit: Optional[int] = None) -> List[User]:
    return list(islice(following[user], limit))



def search(phrase: str, limit: Optional[int] = None) -> List[Post]:
    if hashtag_pattern.match(phrase):
        return list(islice(hashtag_index[phrase], limit))
    return list(islice((post for post in posts if phrase in post.text), limit))