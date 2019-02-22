
if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from hook import hook
else:
    from ..hook import hook


@hook
def build(project = 'HelloWorld'):
    print("building project: {}".format(project))

@build.callfore
def checkout(source = "repo"):
    print("checkout the repo")

@build.callback
def archive(artifacts = "*.*"):
    print("archiving the artifacts")


if __name__ == '__main__':
    build()