mcu - microscope control unit
-----------------------------

This is a isolation of the micro-manager related code from the rest of the logic of the tool.

It seemed important in the early stages of development, as frequently crashing buggy code lead to slow developement with the hardware, as there is a high refractory time for the hardware to reboot.

The demo-config solves to a large extent, but it is still important that the microscope control part of the tool is isolated from crashes.

Therefore, a client server model seemed like a good idea, with the mcu running as a microservice.

It imports the micro-manager python bindings [later pymmcore](https://github.com/micro-manager/pymmcore/) and a hardware configuration file, with methods in the [Micro-Manager Core](https://valelab4.ucsf.edu/~MM/doc/MMCore/html/class_c_m_m_core.html) class giving direct physical access to the microscope devices.

The client-server communication is to be worked out next.
