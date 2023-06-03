### error 1:
description:
ValueError:  cannot be saved because the input shapes have not been set. Usually, input shapes are automatically determined from calling .fit() or .predict(). To manually set the shapes, call model._set_inputs(inputs)./call `model.build(input_shape)`
solution:
use "_set_inputs" or "model.build" set input_signature

### error 2:
description:
ValueError: Structure of Python function inputs does not match input_signature:
solution:
see issue #32488: https://github.com/tensorflow/tensorflow/issues/32488

### warning 1
description:
UserWarning: CRF decoding models have serialization issues in TF >=2.5 . Please see isse #2476
solution:
see isse #2476: https://github.com/tensorflow/addons/issues/2476

### warning 2
description:
The `validate_indices` argument has no effect. Indices are always validated on CPU and never validat
solution:
see isse #47764: https://github.com/tensorflow/tensorflow/issues/47764

### warning 3
description:
Some layers from the model checkpoint at bert-base-chinese were not used when initializing TFBertMod
solution:
see isse #8510: https://github.com/huggingface/transformers/issues/8510


