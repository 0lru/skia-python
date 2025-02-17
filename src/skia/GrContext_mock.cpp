#include "common.h"

void initGrDirectContext_mock(py::module &m) {

py::class_<GrMockTextureInfo>(m, "GrMockTextureInfo")
    .def(py::init<>())
    .def(py::init<GrColorType, SkImage::CompressionType, int>(),
        py::arg("colorType"), py::arg("compressionType"), py::arg("id"))
    .def("__eq__", &GrMockTextureInfo::operator==, py::is_operator())
    .def("getBackendFormat", &GrMockTextureInfo::getBackendFormat)
    .def("compressionType", &GrMockTextureInfo::compressionType)
    .def("colorType", &GrMockTextureInfo::colorType)
    .def("id", &GrMockTextureInfo::id)
    ;

py::class_<GrMockRenderTargetInfo>(m, "GrMockRenderTargetInfo")
    .def(py::init<>())
    .def(py::init<GrColorType, int>(),
        py::arg("colorType"), py::arg("id"))
    .def("__eq__", &GrMockRenderTargetInfo::operator==, py::is_operator())
    .def("getBackendFormat", &GrMockRenderTargetInfo::getBackendFormat)
    .def("colorType", &GrMockRenderTargetInfo::colorType)
    ;

py::class_<GrMockOptions>(m, "GrMockOptions")
    .def(py::init<>())
    // TODO: Implement me!
    ;

}
