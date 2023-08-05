
# Karel For Synthesis

Parser and executor for Karel. Based almost entirely on Nearai's [code](https://github.com/nearai/program_synthesis/tree/master/program_synthesis/karel) with some modifications.

## Usage

To use the executor, run

```
from karel_for_synthesis import execute

result = execute(program, input_grid, record_trace=True)
```

You can also parse and unparse programs by using the `parse` and `unparse` commands.

## Outputs

This will give you an `ExecutionResult` object, with the following structure

  - `ExecutionResult`
    - `.result`: the output grid, or `None` if there was an error
    - `.trace`: the output trace. `None` if `record_trace=False` is passed
      - `.grids`: the grids at every timestep in the execution of the  program
      - `.events`: a series of `KarelEvent` objects
        - `.timestep`: `grids[timestep]` corresponds to the grid after this timestep
        - `type`: the token being executed
        - `span`: `(i, j)` for the first and last tokens corresponding to this block
        - `cond_span`: `(i, j)` for the first and last tokens contained in the conditional expression if one exists or `None` otherwise
        - `cond_value`: the value of the conditional expression or number of remaining iterations
        - `success`: False if the action failed or the loop repeats forever

## Errors

  - `ExecutorSyntaxException`: occurs if the program passed in has invalid syntax
  - `ExecutorRuntimeException`: occurs if the program passed in has an error in executing and
      `record_trace=False` is passed
