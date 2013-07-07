What is unit testing?
=====================

Multiple levels of testing are necessary to verify that software is ready for release. The very first level is ensuring each component (or unit) works properly in isolation. This is known as unit testing.

A unit test framework is a libray that facilitates automated unit testing, and often provides many features to augment and ease the creation of unit tests. The most popular family of unit test frameworks is xUnit. Originally written by Kent Beck for Smalltalk (SUnit), it's popularity came from the Java port (JUnit), which he wrote with Erich Gamma. Since then, the xUnit framework has become the most widely accepted standard, and has been ported to almost every major programming language, as well as a number of unpopular languages.

All xUnit frameworks share a similar structure and features. Assert functions provided by the library are the core method of generating results. These are called inside each test case, represented by a function intended to stand alone. Test fixtures provide a means by which the program state can be established before each test and torn down after wards. Test suites are a defined group of tests which may be run together. The execution is governed by an external test runner, which is (ideally) decoupled from the actual evaluation, allowing for various methods of reporting the results.

