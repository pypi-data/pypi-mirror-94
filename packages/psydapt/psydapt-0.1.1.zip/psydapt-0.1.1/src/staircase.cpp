#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <optional>
#include "psydapt.hpp"

namespace py = pybind11;
using namespace pybind11::literals;
using psydapt::staircase::Staircase;

void pystaircase(py::module &m)
{
    auto foo = py::class_<Staircase>(m, "Staircase")
                   .def(py::init<const Staircase::Params &>())
                   .def("next", &Staircase::next)
                   .def("update", &Staircase::update, "value"_a, "stimulus"_a = std::nullopt);

    py::class_<Staircase::Params>(foo, "Params")
        .def(py::init<double,
                      std::vector<double>,
                      unsigned int,
                      int,
                      int,
                      bool,
                      psydapt::Scale,
                      std::optional<unsigned int>,
                      std::optional<double>,
                      std::optional<double>>(),
             "start_val"_a, "step_sizes"_a, "n_trials"_a, "n_up"_a, "n_down"_a,
             "apply_initial_rule"_a, "stim_scale"_a, "n_reversals"_a = std::nullopt,
             "min_val"_a = std::nullopt, "max_val"_a = std::nullopt);
};
