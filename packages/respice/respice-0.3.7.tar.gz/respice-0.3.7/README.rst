respice
=======

Flexible and easy to use non-linear transient electric circuit simulator.

Install
-------

.. code:: bash

   pip3 install respice

Usage
-----

Create your circuit and simulate it!

.. code:: python

   from respice.analysis import Circuit
   from respice.components import CurrentSourceDC, R, C

   # Define components for our circuit.
   R1 = R(100)
   R2 = R(200)
   C3 = C(10e-6)
   R4 = R(200)
   R5 = R(100)
   Isrc = CurrentSourceDC(0.1)

   # Construct the circuit. All circuits are just
   # Digraphs allowing multiple edges. On each edge
   # one component.
   wheatstone_bridge = Circuit()
   wheatstone_bridge.add(R1, 0, 1)
   wheatstone_bridge.add(R2, 0, 2)
   wheatstone_bridge.add(C3, 1, 2)
   wheatstone_bridge.add(R4, 1, 3)
   wheatstone_bridge.add(R5, 2, 3)
   wheatstone_bridge.add(Isrc, 3, 0)

   # Simulate! From t1 = 0ms to t2 = 5ms with 100 steps.
   simulation = wheatstone_bridge.simulate(0, 0.005, 100)

The results are stored in the returned object and can be easily accessed
via ``simulation.v(component)``, ``simulation.i(component)`` or ``simulation.p(component)``.
Those contain the voltages, currents and powers respectively for each time step
as a list. The time steps can be accessed with ``simulation.t()``.

All simulations are asynchronous. Accessing results early may only give partial
results. Use ``simulation.wait()`` to wait until the result is ready.

Results can be immediately plotted.
For plotting, ``plotly`` is required.

.. code:: python

   from respice.examples import RC

   # Define an example RC circuit. The package respice.examples
   # contains a few!
   rc = RC(100, 100e-6, 10)  # 100Ohm, 100uF, 10V
   simulation = rc.simulate(0, 0.1, 100)
   simulation.plot()

The plot function will wait automatically until the result is finished. Live-plotting
is not supported yet.

More simulations can be found on the `snippets page <https://gitlab.com/Makman2/respice/-/snippets>`_.

Supports
--------

- **MNA - Modified Nodal Analysis**

  This is the algorithm employed by this software. So it’s easily
  possible to handle voltages as well as currents.

- **Transient non-linear steady-state analysis**

  Find quickly periodic steady-state solutions of a circuit that appear
  when the circuit transients have settled.

- **Multi-terminal components**

  Components with more than just two terminals can be handled easily.
  Whether each sub-branch of them is a current- or voltage-branch, or
  whether they are current- or voltage-driven.

- **Mutual coupling**

  Usually required by multi-terminal components, mutual coupling is
  easily implementable. Each sub-branch in a component is automatically
  receiving the voltages and currents of all other branches comprising
  the component.

Documentation
-------------

More details and explanations are available in the documentation.

Documentation is generated via Sphinx. To build the documentation:

.. code:: bash

   pip3 install -r requirements.txt -r docs-requirements.txt
   make html

The index file can then be opened with your favorite browser at ``build/html/index.html``.

Documentation is also available `online <https://Makman2.gitlab.io/respice>`_.
