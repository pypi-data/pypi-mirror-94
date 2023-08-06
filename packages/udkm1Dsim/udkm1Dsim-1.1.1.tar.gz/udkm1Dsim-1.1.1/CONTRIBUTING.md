# Guidelines for Contributing to udmkm1Dsim

The udmkm1Dsim repository uses nvie's branching model, known as 
[GitFlow][].

In this model, there are two long-lived branches:

- `master`: used for official releases. **Contributors should 
  not need to use it or care about it**
- `develop`: reflects the latest integrated changes for the next 
  release. This is the one that should be used as the base for 
  developing new features or fixing bugs. 

For the contributions, we use the [Fork & Pull Model][]:

1. the contributor first [forks][] the official udmkm1Dsim repository
2. the contributor commits changes to a branch based on the 
   `develop` branch and pushes it to the forked repository.
3. the contributor creates a [Pull Request][] against the `develop` 
   branch of the official udmkm1Dsim repository.
4. anybody interested may review and comment on the Pull Request, and 
   suggest changes to it (even doing Pull Requests against the Pull
   Request branch). At this point more changes can be committed on the 
   requestor's branch until the result is satisfactory.
5. once the proposed code is considered ready by an appointed udmkm1Dsim 
   integrator, the integrator merges the pull request into `develop`.
6. In order to keep your fork up to date with the official repository do 
   the following within your local copy of the repository::
```
    git remote add upstream git://github.com/dschick/udkm1Dsim.git
    git fetch upstream
    git pull upstream develop
```   
   
## Important considerations:

In general, the contributions to udmkm1Dsim should consider following:

- The code must comply with the udmkm1Dsim coding conventions, see below.
  [udmkm1Dsim travis-ci][] will check it for each Pull Request (PR) using
  the latest version of [flake8 available on PyPI][].
  In case the check fails, please correct the errors and commit
  to the PR branch again. You may consider running the check locally
  in order to avoid unnecessary commits.
  If you find problems with fixing these errors do not hesitate to ask for
  help in the PR conversation! We will not reject any contribution due
  to these errors - the purpose of this check is just to maintain the code
  base clean.
- The contributor must be clearly identified. The commit author 
  email should be valid and usable for contacting him/her.
- Commit messages  should follow the [commit message guidelines][]. 
  Contributions may be rejected if their commit messages are poor.
- The licensing terms for the contributed code must be compatible 
  with (and preferably the same as) the license chosen for the udmkm1Dsim 
  project (at the time of writing this file, it is the [LGPL][], 
  version 3 *or later*).

   
## Notes:
  
- These contribution guidelines are very similar but not identical to 
  those for the [GithubFlow][] workflow. Basically, most of what the 
  GitHubFlow recommends can be applied for udmkm1Dsim except that the 
  role of the `master` branch in GithubFlow is done by `develop` in our 
  case.  
- If the contributor wants to explicitly bring the attention of some 
  specific person to the review process, [mentions][] can be used
- If a pull request (or a specific commit) fixes an open issue, the pull
  request (or commit) message may contain a `Fixes #N` tag (N being 
  the number of the issue) which will automatically [close the related 
  Issue][tag_issue_closing]
  

# Coding conventions

- In general, we try to follow the standard Python style conventions as
  described in
  `Style Guide for Python Code  <http://www.python.org/peps/pep-0008.html>`_
- Code **must** be python 2.6 compatible
- Use 4 spaces for indentation
- In the same file, different classes should be separated by 2 lines
- use ``lowercase`` for module names.
- use ``CamelCase`` for class names
- python module first line should be:
  `#!/usr/bin/env python` 
- python module should contain license information (see template below)
- avoid poluting namespace by making private definitions private (``__`` prefix)
  or/and implementing ``__all__`` (see template below)
- whenever a python module can be executed from the command line, it should 
  contain a ``main`` function and a call to it in a ``if __name__ == "__main__"``
  like statement (see template below)
- document all code using [Sphinx][] extension to [reStructuredText][]

The following code can serve as a template for writing new python modules to
udmkm1Dsim:

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    
    # The MIT License (MIT)
    # Copyright (c) 2020 Daniel Schick
    #
    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:
    #
    # The above copyright notice and this permission notice shall be included in all
    # copies or substantial portions of the Software.
    #
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    # EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    # MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    # IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
    # DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    # OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
    # OR OTHER DEALINGS IN THE SOFTWARE.

    __all__ = ["udmkm1DsimDemo"]
    
    __docformat__ = "restructuredtext"
    
    class udmkm1DsimDemo(object):
        """This class is written for template purposes only"""
        
    def main():
        print "udmkm1DsimDemo"s
    
    if __name__ == "__main__":
        main()


[gitflow]: http://nvie.com/posts/a-successful-git-branching-model/
[Fork & Pull Model]: https://en.wikipedia.org/wiki/Fork_and_pull_model
[forks]: https://help.github.com/articles/fork-a-repo/
[Pull Request]: https://help.github.com/articles/creating-a-pull-request/
[commit message guidelines]: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
[GitHubFlow]: https://guides.github.com/introduction/flow/index.html
[mentions]: https://github.com/blog/821-mention-somebody-they-re-notified
[tag_issue_closing]: https://help.github.com/articles/closing-issues-via-commit-messages/
[LGPL]: http://www.gnu.org/licenses/lgpl.html
[udmkm1Dsim travis-ci]: https://travis-ci.com/dschick/udkm1Dsimpy/
[flake8 available on PyPI]: https://pypi.org/project/flake8
[reStructuredText]:  http://docutils.sourceforge.net/rst.html
[Sphinx]: http://sphinx.pocoo.org/
