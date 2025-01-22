#!/usr/bin/env python3

import sys

first = True
for line in sys.stdin:
    if first:
        first = False
        continue
    data = line.strip().split("\t")
    if len(data) == 19:
        id, title,tagnames,author_id, body, node_type, parent_id, abs_parent_id, added_at, score, state_string, last_edited_id, last_activity_by_id, last_activity_at, active_revision_id, extra, extra_ref_id, extra_count, marked = data
        if len(body)==0:
            continue
        if (body.count(".") + body.count("!") + body.count("?")) > 1:
            continue
        else:
            print ('{0}\t{1}'.format('post',body))
