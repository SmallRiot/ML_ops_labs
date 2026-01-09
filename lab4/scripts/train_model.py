from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression


def main() -> None:
    parser = ArgumentParser(description="Train Iris model and save to disk")
    parser.add_argument("--output", default="models/model.pkl", help="Path to save model")
    args = parser.parse_args()

    iris = load_iris(as_frame=True)
    x = iris.data
    y = iris.target_names[iris.target]

    model = LogisticRegression(max_iter=200, solver="lbfgs", multi_class="auto")
    model.fit(x, y)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)


if __name__ == "__main__":
    main()
