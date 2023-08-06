#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <optional>
#include "psydapt.hpp"

namespace py = pybind11;
using namespace pybind11::literals;
namespace questplus = psydapt::questplus;
using psydapt::questplus::NormCDF;
using psydapt::questplus::Weibull;

void pyquestplus(py::module &m)
{

    py::enum_<questplus::StimSelectionMethod>(m, "StimSelectionMethod", py::arithmetic())
        .value("MinEntropy", questplus::StimSelectionMethod::MinEntropy)
        .value("MinNEntropy", questplus::StimSelectionMethod::MinNEntropy);

    py::enum_<questplus::ParamEstimationMethod>(m, "ParamEstimationMethod", py::arithmetic())
        .value("Mean", questplus::ParamEstimationMethod::Mean)
        .value("Median", questplus::ParamEstimationMethod::Median)
        .value("Mode", questplus::ParamEstimationMethod::Mode);

    auto foo = py::class_<Weibull>(m, "Weibull")
                   .def(py::init<const Weibull::Params &>())
                   .def("next", &Weibull::next)
                   .def("update", &Weibull::update, "value"_a, "stimulus"_a = std::nullopt);

    py::class_<Weibull::Params>(foo, "Params")
        .def(py::init<
                 questplus::StimSelectionMethod,
                 questplus::ParamEstimationMethod,
                 unsigned int, // n
                 unsigned int, // max_consecutive_reps
                 unsigned int, // random_seed
                 psydapt::Scale,
                 std::vector<double>,                // intensity
                 std::vector<double>,                // threshold
                 std::vector<double>,                // slope
                 std::vector<double>,                // lower asymptote
                 std::vector<double>,                // lapse rate
                 std::optional<std::vector<double>>, // threshold prior
                 std::optional<std::vector<double>>, // slope prior
                 std::optional<std::vector<double>>, // lower prior
                 std::optional<std::vector<double>>  // lapse prior
                 >(),
             "stim_selection_method"_a = questplus::StimSelectionMethod::MinEntropy,
             "param_estimation_method"_a = questplus::ParamEstimationMethod::Mean,
             "n"_a = 5, "max_consecutive_reps"_a = 2, "random_seed"_a = 1,
             "stim_scale"_a, "intensity"_a, "threshold"_a, "slope"_a,
             "lower_asymptote"_a, "lapse_rate"_a, "threshold_prior"_a = std::nullopt,
             "slope_prior"_a = std::nullopt, "lower_asymptote_prior"_a = std::nullopt,
             "lapse_rate_prior"_a = std::nullopt);

    auto bar = py::class_<NormCDF>(m, "NormCDF")
                   .def(py::init<const NormCDF::Params &>())
                   .def("next", &NormCDF::next)
                   .def("update", &NormCDF::update, "value"_a, "stimulus"_a = std::nullopt);

    py::class_<NormCDF::Params>(bar, "Params")
        .def(py::init<
                 questplus::StimSelectionMethod,
                 questplus::ParamEstimationMethod,
                 unsigned int, // n
                 unsigned int, // max_consecutive_reps
                 unsigned int, // random_seed
                 psydapt::Scale,
                 std::vector<double>,                // intensity
                 std::vector<double>,                // location
                 std::vector<double>,                // scale
                 std::vector<double>,                // lower asymptote
                 std::vector<double>,                // lapse rate
                 std::optional<std::vector<double>>, // location prior
                 std::optional<std::vector<double>>, // scale prior
                 std::optional<std::vector<double>>, // lower prior
                 std::optional<std::vector<double>>  // lapse prior
                 >(),
             "stim_selection_method"_a = questplus::StimSelectionMethod::MinEntropy,
             "param_estimation_method"_a = questplus::ParamEstimationMethod::Mean,
             "n"_a = 5, "max_consecutive_reps"_a = 2, "random_seed"_a = 1,
             "stim_scale"_a, "intensity"_a, "location"_a, "scale"_a,
             "lower_asymptote"_a, "lapse_rate"_a, "location_prior"_a = std::nullopt,
             "scale_prior"_a = std::nullopt, "lower_asymptote_prior"_a = std::nullopt,
             "lapse_rate_prior"_a = std::nullopt);
};