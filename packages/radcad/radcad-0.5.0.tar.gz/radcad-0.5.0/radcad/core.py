import copy
from functools import reduce, partial
import logging
from pathos.multiprocessing import ThreadPool
import pickle


pool = ThreadPool()


def _update_state(initial_state, params, substep, result, substate, signals, state_update_tuple):
    state, function = state_update_tuple
    if not state in initial_state:
        raise KeyError("Invalid state key in partial state update block")
    state_key, state_value = function(
        params, substep, result, substate, signals
    )
    if not state_key in initial_state:
        raise KeyError(
            "Invalid state key returned from state update function"
        )
    if state == state_key:
        return (state_key, state_value)
    else:
        raise KeyError(
            f"PSU state key {state} doesn't match function state key {state_key}"
        )


def _single_run(
    result: list,
    simulation: int,
    timesteps: int,
    run: int,
    subset: int,
    initial_state: dict,
    state_update_blocks: list,
    params: dict,
    deepcopy: bool,
):
    logging.info(f"Starting run {run}")

    initial_state["simulation"] = simulation
    initial_state["subset"] = subset
    initial_state["run"] = run + 1
    initial_state["substep"] = 0
    initial_state["timestep"] = 0

    result.append([initial_state])

    for timestep in range(0, timesteps):
        previous_state: dict = (
            result[0][0].copy()
            if timestep == 0
            else result[-1][-1].copy()
        )

        substeps: list = []

        for (substep, psu) in enumerate(state_update_blocks):
            substate: dict = (
                previous_state.copy() if substep == 0 else substeps[substep - 1].copy()
            )
            substate_copy = pickle.loads(pickle.dumps(substate, -1)) if deepcopy else substate.copy()
            substate["substep"] = substep + 1

            signals: dict = reduce_signals(
                params, substep, result, substate_copy, psu
            )

            updated_state = map(
                partial(_update_state, initial_state, params, substep, result, substate_copy, signals),
                psu["variables"].items()
            )
            substate.update(updated_state)
            substate["timestep"] = timestep + 1
            substeps.append(substate)
        result.append(substeps)
    return result


def single_run(
    simulation,
    timesteps,
    run,
    subset,
    initial_state,
    state_update_blocks,
    params,
    deepcopy: bool,
):
    result = []

    try:
        return (
            _single_run(
                result,
                simulation,
                timesteps,
                run,
                subset,
                initial_state,
                state_update_blocks,
                params,
                deepcopy
            ),
            None,
        )
    except Exception as error:
        print(error)
        logging.error(
            f"Simulation {simulation} / run {run} / subset {subset} failed! Returning partial results."
        )
        return (result, error)


def generate_parameter_sweep(params: dict):
    param_sweep = []
    max_len = 0
    for value in params.values():
        if len(value) > max_len:
            max_len = len(value)

    for sweep_index in range(0, max_len):
        param_set = {}
        for (key, value) in params.items():
            param = (
                value[sweep_index]
                if sweep_index < len(value)
                else value[-1]
            )
            param_set[key] = param
        param_sweep.append(param_set)

    return param_sweep


def _add_signals(acc, a: {}):
    for (key, value) in a.items():
        if acc.get(key, None):
            acc[key] += value
        else:
            acc[key] = value
    return acc


def reduce_signals(params: dict, substep: int, result: list, substate: dict, psu: dict):
    policy_results: [dict] = list(map(lambda function: function(params, substep, result, substate), psu["policies"].values()))

    result: dict = {}
    result_length = len(policy_results)
    if result_length == 0:
        return result
    elif result_length == 1:
        return pickle.loads(pickle.dumps(policy_results[0], -1))
    else:
        return reduce(_add_signals, policy_results, result)
