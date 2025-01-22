#!/usr/bin/python3
import sys

biger_posts = []
nb_post = 10

def append_sort(post, size):
    global biger_posts
    i = 0
    while (i < len(biger_posts) and biger_posts[i][1] < size):
        i += 1
    biger_posts.insert(i, (post, size))

    if len(biger_posts) > nb_post:
        biger_posts = biger_posts[1:]


for line in sys.stdin:
    
    post = ''.join(line.split('\t')[:-1]) 
    size = int(line.split('\t')[-1])
    
    if len(biger_posts) < nb_post:
       append_sort(post, size)
    else:
        if size > biger_posts[0][1]:
            append_sort(post, size)

for post, size in biger_posts:
    print(post)