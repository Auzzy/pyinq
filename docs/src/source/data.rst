pyinq.data
==========
PyInq represents each kind of test object, such as fixtures and tests, with its own class. In general, this doesn't impact you, and this can be safely ignored. However, if you're using the test discovery API, this information may be relevant.

Fixtures
--------
.. class:: Fixture

The base class for all Fixture objects. It contains 3 fields: ``name``, ``suite``, and ``class_name``. Their names are self-explanitory. Each field is either a string or ``None``.You may also retrieve the function it represents through the read-only property ``func``.

The preferred way to execute a fixture is by calling its corresponding :class:`Fixture` object: the ``__call__`` function is overriden to make execution simple.

.. class:: BeforeSuite
.. class:: BeforeModule
.. class:: BeforeClass
.. class:: Before
.. class:: After
.. class:: AfterClass
.. class:: AfterModule
.. class:: AfterSuite

Each class inherits from :class:`Fixture` and represents a function tagged with the corresponding name.

.. class:: DoNothing

This is also a :class:`Fixture` object, but does not correspond to a tag. Instead, it indicates that a particular fixture has not been set. Thus, it corresponds to no function, and when it is called, nothing is run. This is the default value for an unset fixture, and its truth-value is ``False``. As such, testing the truth-value is the preferred method of detecting an unset fixture.

Test Objects
------------
All the objects below contains 3 fields: ``name``, ``before``, and ``after``. ``name`` is the structure's name as a string, or ``None`` if it is a default structure. ``before`` and ``after`` contain the structure's before and after fixtures as one of the objects defined above. Both default to :class:`DoNothing` if an object is not provided.

Each object (except for :class:`TestData`) is a sequence object. They should only conatin objects from the level directly below it. That is, :class:`TestSuiteData` should only contain :class:`TestModuleData` objects, and so on.

Each object also overrides ``__call__``. Calling a structure will run the corresponding "before" fixture, followed by all contained structures, and finally the appropriate "after" function. All results are wrapped up into a results object and returned to the caller.

.. class:: TestSuiteData
.. class:: TestModuleData

Both of these currently contain only the base data. More will be added to ``TestModuleData`` moving forward, such as the path to the correspoinding module.

.. class:: TestClassData

To access a class's suite, you can use the ``suite`` field. If this class is not part of a suite, this value will be ``None``.

.. class:: TestData

To access a function's suite, you can use the ``suite`` field. If this function is not part of a suite, this value will be ``None``.

Additionally, you can access the test function that this object represents by using the read-only property ``test``. However, it is **highly** recommended you run the object normally (as a callable object). The runner not only handles executing fixtures and producing a results object, but also ensures any raised exceptions are properly dealt with in the context of the framework. Thus, manually calling the test funciton negates much of the benefit of using PyInq. That being said, nothing is in place to stop you. Just know you are doing so at your own risk.
