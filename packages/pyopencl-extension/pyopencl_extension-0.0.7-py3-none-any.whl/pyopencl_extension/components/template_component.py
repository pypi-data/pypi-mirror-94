from pyopencl_extension.core import PyClComponent, ClProgram, ClKernel, Arg, ClTypes
import pyopencl.array as cl_array
import numpy as np


class TemplateComponent(PyClComponent):
    def _get_cl_program(self) -> ClProgram:
        knl = ClKernel(name='example_kernel',
                       args=[Arg.from_buffer('in_buff', self.in_buffer, True),
                             Arg.from_buffer('out_buff', self.out_buffer),
                             Arg('param_a,', self.in_buffer.dtype)],
                       body=[
                           """
                           int addr = ${command_addr};
                           out_buff[addr] = in_buff[addr] + param_a;
                           """
                       ],
                       replacements=[('command_addr', self.command_compute_address(self.in_buffer.ndim))])
        return ClProgram(kernels=[knl])

    def __call__(self, example_parameter: float = 3.0, b_python: bool = False, **kwargs):
        super(TemplateComponent, self).__call__(b_python, **kwargs)
        self.program.example_kernel(self.in_buffer.shape, None,
                                    self.in_buffer,
                                    self.out_buffer,
                                    np.dtype(self.in_buffer.dtype).type(example_parameter))

    def __init__(self, in_buffer: cl_array.Array):
        super().__init__(in_buffer)
        self.in_buffer = in_buffer
        self.out_buffer = cl_array.zeros_like(self.in_buffer)
        self._post_init()