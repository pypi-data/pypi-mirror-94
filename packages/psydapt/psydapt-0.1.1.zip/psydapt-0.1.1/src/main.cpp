#include <pybind11/pybind11.h>
#include "psydapt.hpp"
namespace py = pybind11;

void pystaircase(py::module &);
void pyquestplus(py::module &);

PYBIND11_MODULE(psydapt, m)
{
    m.doc() = "pybind11 wrapper for aforren1/psydapt";
    py::enum_<psydapt::Scale>(m, "Scale", py::arithmetic())
        .value("dB", psydapt::Scale::dB)
        .value("Linear", psydapt::Scale::Linear)
        .value("Log10", psydapt::Scale::Log10);
    py::module staircase = m.def_submodule("staircase", "");
    pystaircase(staircase);
    py::module questplus = m.def_submodule("questplus", "");
    pyquestplus(questplus);
}