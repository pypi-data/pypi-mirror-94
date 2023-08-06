0.1.3
-----

* Fix memory leaks in certain error cases.
* Modernize build system and rely on setuptool's Cython support.
* Add more tests.
* Skip some tests if not run in a UTF-8 locale.
* Use libc's implementation on Mac OS.

0.1.2
-----

* Also build wheels with cibuildwheel.
* Provide type information for mypy.

0.1.1
-----

* If Cython is not available, do not regenerate the C source file during build.

0.1
---

* Initial release.
