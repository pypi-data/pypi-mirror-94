v3.5.0
======

Rely on PEP 420 for namespace package.

v3.4.0
======

Added ``WordSet.trim*`` methods.

v3.3.0
======

Require Python 3.6 or later.

v3.2.0
======

Added normalize_newlines function.

3.1
===

Added ``wrap`` and ``unwrap`` functions and ``lorem_ipsum``
attribute containing the Lorem Ipsum sample text.

3.0.1
=====

Declare missing dependency on six.

3.0
===

Removed ``local_format``, ``global_format``, and
``namespace_format``. Instead, developers should
use `f-strings
<https://docs.python.org/3.6/reference/lexical_analysis.html#f-strings>`_
on Python 3.6 and later or `future-fstrings
<https://pypi.org/project/future-fstrings>`_ for compatibilty
with older Pythons. This change eliminates the dependency on
jaraco.collections and thus for now removes the circular dependency
as reported in #3.

2.0
===

Switch to `pkgutil namespace technique
<https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages>`_
for the ``jaraco`` namespace.

1.10.1
======

Packaging refresh. Docs now published in RTD.

1.10
====

FoldedCase now supports string-containment support in an
unfortunately assymetric way.

1.9.2
=====

Fix bug where ``FoldedCase.__ne__`` was case-sensitive.

1.9.1
=====

Refresh packaging.

1.9
===

Synchronize with skeleton.

Update docs and expand tests on FoldedCase.

Use method_cache for ``FoldedCase.lower``.

1.8
===

Add remove_prefix and remove_suffix helpers.

1.7
===

In Stripper, always strip the prefix, even if it's empty.

1.6.2
=====

Issue #1: Fix WordSet on Python 2.

1.6
===

Drop dependency on jaraco.context (and its dependencies).

1.5
===

Move hosting to github.

Add missing namespace package declaration in distribution.

1.4
===

Add Stripper class.

1.3
===

Add SeparatedValues class.

1.0
===

Initial implementation adopted from jaraco.util.string 10.8.
