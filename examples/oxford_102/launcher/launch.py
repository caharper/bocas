"""
# Overview

First, we sort out our imports
"""
from absl import flags
import ml_collections
import ml_experiments
import sys
import luketils

FLAGS = flags.FLAGS

"""
Next, we define some config flags:
"""

# TODO(lukewood): provide a default path for filepath

flags.DEFINE_string("run", None, "the path to `run.py`.")
flags.DEFINE_string("artifacts_dir", None, "the directory to save artifacts to.")

FLAGS(sys.argv)

"""
Finally, we define our experiment configs:
"""

config = ml_collections.ConfigDict()
# initialize model types

config.artifacts_dir = FLAGS.artifacts_dir
config.log_dir = f"{config.artifacts_dir}/logs"

"""
Optionally these can include sweep values:
"""

config.model_type = ml_experiments.Sweep(["resnet", "efficientnet"])
config.augmenter_type = ml_experiments.Sweep(["basic", "optimized"])

"""
Finally, we pick an entrypoint and run the experiment:
"""

results = ml_experiments.run(FLAGS.run, config)

"""
After all results come back, we can aggregate and plot our metrics:
"""

metrics_to_plot = {}

for experiment in results:
    metrics = experiment.get("fit_history").metrics

    metrics_to_plot[f"{experiment.name} Train"] = metrics["accuracy"]
    metrics_to_plot[f"{experiment.name} Validation"] = metrics["val_accuracy"]

luketils.visualization.line_plot(
    metrics_to_plot,
    path=f"{artifacts_dir}/combined-accuracy.png",
    title="Model Accuracy",
)

"""
The wonderful things about this workflow:

- your main script can still support standalone runs
- you can easily run sweeps
- TensorBoard tracks all logs in a single directory
- your paper will automatically receive updates from new experiments if you structure
your latex code properly

All in all, this is a great way to automate experiment running.
"""
