
### TODO
 - [x] Inject vars with multiple key/value pair in dict
 - [ ] Documents
 - [ ] Tests
 - [ ] Publish module to PYPI
 - [ ] Publish documents to Read The Docs



Hook actions prior to the call;
Hook actions after the call;

Get the return/output from the actions and/or the call
Pass the pararmeters to the following actions and/or the call

Quick Start
```
from hook import hook

@hook
def build(project = HelloWorld):
    print("building project: {}".format(project))

@build.callfore
def checkout(source = "repo"):
    print("checkout the repo")

@build.callback
def archive(artifacts = "*.*"):
    print("archiving the artifacts")

```