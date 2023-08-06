import os
import re
import json
from functools import reduce
from pathlib import Path

import yaml
import jinja2

from aurore.utils.treeutils import iterate_leaves
from aurore.selectors import Pointer, PathBuilder


def remove_duplicates(lst: list)->list:
    items = set()
    append = items.add
    return [x for x in lst if not (x in items or append(x))]

def init(args, config)->dict:

    return {
        "items": {},
        "filter_values": {}
    }

def item(rsrc, args:object, config:object, accum:dict)->dict:
    try:
        paths = [p  for P in accum["path-builders"] for p in P.resolve_recursively(rsrc) ]
    except:
        accum["path-builders"] = [
            PathBuilder(
                field,
                pointer_delimeter = args.pointer_delimeter,
                unpack_fields = args.unpack_fields
            ) for field in remove_duplicates(args.paths)
        ]
        paths = [p  for P in accum["path-builders"] for p in P.resolve_recursively(rsrc) ]
    
    rsrc.update({
            "paths": paths
    })
    accum['item'] = rsrc
    return accum

def close(args, config, accum):

    if args.format_flat:
        return ' '.join(
            f for v in accum["items"].values() 
              for f in iterate_leaves(v["paths"])
        )


    elif args.format_table:
        return args.join_items.join(
            args.separator.join(
                item["paths"]
            ) for item in accum["items"].values()
        )
