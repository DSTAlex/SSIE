#!/usr/bin/python3
import sys
import re

first = True

dic = {}

for line in sys.stdin:
    if first:
        first = False
        continue
    data = line.strip().split("\t")
    if len(data) == 19:
        node_id, title,tagnames,author_id, body, node_type, parent_id, abs_parent_id, added_at, score, state_string, last_edited_id, last_activity_by_id, last_activity_at, active_revision_id, extra, extra_ref_id, extra_count, marked = data
        words=re.findall("[\\w]+|[.,!?;]",body)
        for word in words:
            if word not in ('.','!','?','#','$','[',']','/','<','>','=','-',':',';','(',')',','):
                if word not in dic:
                    dic[word] = [1,  {node_id.strip('"')}]
                else:
                    dic[word][0] += 1
                    dic[word][1].add(node_id.strip('"'))
                
for word in dic:
    print('{0}\t{1}\t{2}'.format(word, dic[word][0], dic[word][1]))