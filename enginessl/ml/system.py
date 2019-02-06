import kernel as mlkernel
import network

class MachineLearning(mlkernel.Kernel):

    def __init__(self, param_path='param.yml'):
        ml = mlkernel.Kernel(param_path)

