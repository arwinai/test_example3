#!/usr/bin/env python3
"""Grading harness for 4_sling_lift -- A STUB. Writing it is the exercise.

    python3 tests/task/harness/harness.py solution/solution.FCStd

Runs as it stands: it measures the document and prints a valid score
envelope in which every component scores zero and says why. That is the
contract you are filling in, not a starting implementation -- there is no
grading logic here to edit, and none was generated for you.

WHAT IT HAS TO DO

    the reference   solution/solution.FCStd must score 6 of 6.
    the adversarials  every folder under examples/ must lose the
                      component(s) it actually breaks, and only those.

Grade the geometry and the parametric structure the instruction asks for.
Do not grade object names, document-tree shape, or anything that is true
of the reference by coincidence: a candidate who models the lift a
different way and gets it right must still score 6 of 6. That is the
whole difficulty of the task, and the corpus is built to catch a harness
that takes the easy route.

THE SPLIT, WHICH IS WORTH KEEPING

This file does not import FreeCAD. It runs `measure_stage.py` under
`freecadcmd` through `common.harness_base.run_freecad_stage`, and scores
the JSON that comes back. Two reasons, both practical: the scoring half
stays testable on a machine with no FreeCAD, and a candidate's document
never gets to run its own macros inside the grader's interpreter.

`measure_stage.py` is a stub too. What it measures is your decision --
that choice IS the design of the harness, so it was left to you.

THE CONTRACT

`Harness` (common/harness_base.py) wants two methods:

    build_state(candidate_path) -> dict
        Expensive shared setup, run once. Whatever the checks read.

    checks(state) -> {name: (name, score, description)}
        `score` is a float in [0, 1]. `description` is the sentence a
        human reads next to the number; make it say what was measured,
        not just pass or fail.

SCORE CONTINUOUSLY. A bool is accepted and is almost always the wrong
answer. Most of these components are questions of degree, and collapsing
them to pass/fail throws away the information that makes a grader useful:

    five joints wanted, three mated                 -> 0.6, not 0
    a link 4% short of the drawing                  -> 0.9, not 0
    two of four signature dimensions present        -> 0.5, not 0

A candidate who gets most of it right should score most of the marks, and
two candidates who are wrong by different amounts should not land on the
same number. Reserve a hard 0 or 1 for components that genuinely have no
middle -- "does it rebuild without errors" is one, and it is the gate.

`common/harness_base.py` has helpers for the usual shapes: `clamp01`,
`score_error(value, perfect, zero)` for a reading that degrades with
distance from a target, `score_ratio` for "how many of these are right",
and `score_band` for a value that has to sit inside a range.

`MUST_PASS` names components that zero the whole score when they fail.
`WEIGHTS` prices them; `max_score` in task.toml must equal the sum.

The seven below are the components the task shipped with. They are a
suggestion, not a requirement: split, merge, reweight, rename or replace
them as your reading of instruction.md warrants, and say why in your
notes. Keep task.toml's max_score in step.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _repo_root(start):
    d = start
    for _ in range(8):
        if (d / "common" / "__init__.py").is_file():
            return d
        if d.parent == d:
            break
        d = d.parent
    return start


REPO = _repo_root(HERE)
sys.path[:0] = [str(REPO), "/opt"]

from common.harness_base import Harness                   # noqa: E402

#: Weight per component; 0 makes it a gate when it is also in MUST_PASS.
#: The sum must equal task.toml's max_score (6 today).
ALL_CRITERIA = {
    "executes and builds geometry": 0,
    "geometry matches ground truth": 1,
    "pantograph joints mated": 1,
    "mechanism articulates": 1,
    "carries dimensional constraints": 1,
    "dimensions drive the geometry": 1,
    "signature dimensions present": 1,
}

TODO = "not implemented -- see the docstring at the top of harness.py"


class SlingLiftHarness(Harness):
    MUST_PASS = ("executes and builds geometry",)
    WEIGHTS = ALL_CRITERIA
    BUILD_TIMEOUT_S = 600

    def build_state(self, candidate_path):
        """Measure the candidate once; the checks read what this returns.

        The stage is run out of process, so FREECAD_CMD has to point at a
        freecadcmd binary (see the README). `measurement` is whatever
        measure_stage.py chose to write -- an empty dict, until you
        write it.
        """
        #: A MISSING FREECAD_CMD IS A SETUP FAULT, NOT A CANDIDATE FAULT,
        #: and it should read as one. `freecad_cmd()` raises SystemExit
        #: when the variable is unset, which would kill the run before it
        #: printed anything -- so a first clone would show a bare error
        #: instead of the envelope this stub is meant to demonstrate.
        try:
            measurement, error = self.run_freecad_stage(candidate_path)
        except SystemExit as exc:
            measurement, error = None, str(exc)
        except Exception as exc:                            # noqa: BLE001
            measurement, error = None, f"{type(exc).__name__}: {exc}"
        return {
            "candidate": candidate_path,
            "measurement": measurement or {},
            "error": error,
        }

    def checks(self, state):
        """One entry per component in ALL_CRITERIA.

        Every one scores 0.0 and says so. Replace them with real
        measurements taken from `state["measurement"]`, and return floats
        rather than bools -- see SCORE CONTINUOUSLY above.
        """
        err = state["error"]
        out = {}

        #: The gate is the one component a stub CAN answer honestly: the
        #: stage either opened the document and produced geometry, or it
        #: did not. Left implemented so a broken candidate file is
        #: distinguishable from an unwritten harness.
        name = "executes and builds geometry"
        out[name] = (name, err is None,
                     "the measurement stage ran" if err is None
                     else f"the measurement stage failed: {err}")

        for name in ALL_CRITERIA:
            if name in out:
                continue
            out[name] = (name, 0.0, TODO)
        return out


main = SlingLiftHarness.as_main()

if __name__ == "__main__":
    SlingLiftHarness.cli()
