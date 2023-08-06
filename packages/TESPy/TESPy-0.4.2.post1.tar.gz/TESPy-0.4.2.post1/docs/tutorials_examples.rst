~~~~~~~~~~~~~~~~~~~~~~
Examples and Tutorials
~~~~~~~~~~~~~~~~~~~~~~

.. _tespy_examples_label:

Examples
========

In the example section we provide a variety of TESPy applications, among
others:

* a very basic model of the clausius rankine process,
* the calculation of backpressure lines of a combined heat and power cycle at
  different loads and feed flow temperature levels,
* modeling approach for a district heating system with various consumers and
  system infrastructure as well as
* the COP of a heat pump dependent on load, ambient temperature and heat
  delivering fluid (air vs. water).

You can find all examples in the
`examples repository <https://github.com/oemof/oemof-examples/tree/master/oemof_examples/tespy>`_
on github. Additional small examples can be found in the API-documentation.

* :py:mod:`Components <tespy.components>`
* :py:mod:`Connections and Busses <tespy.connections>`
* :py:mod:`Networks <tespy.networks.network>`
* :py:mod:`Importing Networks <tespy.networks.network_reader>`

.. contents:: `Examples`
    :depth: 1
    :local:
    :backlinks: top

.. _basic_example_label:
.. include:: tutorials_examples/clausius_rankine.rst
.. _combined_cycle_example_label:
.. include:: tutorials_examples/combined_cycle_chp.rst
.. _chp_example_label:
.. include:: tutorials_examples/clausius_rankine_chp.rst
.. _combustion_engine_label:
.. include:: tutorials_examples/combustion_engine.rst
.. _dh_example_label:
.. include:: tutorials_examples/district_heating.rst
.. _heat_pump_cop_label:
.. include:: tutorials_examples/heat_pump.rst
.. _solar_collector_example_label:
.. include:: tutorials_examples/solar_collector.rst
.. _tespy_tutorial_label:

Tutorials
=========

We provide two different tutorials for you to better understand how to work
with TESPy. You will learn how to create basic models and get the idea of
designing a plant and simulating the offdesign behavior in the heat pump
tutorial. On top of that, we created a tutorial for the usage of the combustion
chamber: It is an important component for thermal power plants while being a
source for many errors in the calculation.

The last tutorial is a plant design optimization tutorial. A thermal power
plant with two extraction stages is optimized in regard of thermal efficiency
with respect to the extraction pressure levels.

.. contents:: `Tutorials`
    :depth: 1
    :local:
    :backlinks: top

.. _heat_pump_tutorial_label:
.. include:: tutorials_examples/tutorial_heat_pump.rst
.. _combustion_chamber_tutorial_label:
.. include:: tutorials_examples/tutorial_combustion_chamber.rst
.. _pygmo_tutorial_label:
.. include:: tutorials_examples/tutorial_pygmo_optimization.rst
