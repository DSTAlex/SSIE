#!/usr/bin/python3
import sys

first = True

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
    if first:
        first = False
        continue
    data = line.strip().split("\t")
    if len(data) == 19:
        id, title,tagnames,author_id, body, node_type, parent_id, abs_parent_id, added_at, score, state_string, last_edited_id, last_activity_by_id, last_activity_at, active_revision_id, extra, extra_ref_id, extra_count, marked = data
        
        if len(biger_posts) < nb_post:
            append_sort(body, len(body))
        else:
            if len(body) > biger_posts[0][1]:
                append_sort(body, len(body))

for post, size in biger_posts:        
    print('{0}\t{1}'.format(post, size))