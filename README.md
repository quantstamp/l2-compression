<img src="./images/quantstamp-logo.svg" width="512em">

# Evaluating Rollup Compression

*This research was carried out by the researchers at Quantstamp funded by Quantstamp and the Ethereum Foundation Grant ID FY23-0922 (Evaluating Rollup Compression)*

#### Version
0.1.0. September 1, 2023.

#### Authors
- Roshan Palakkal, Blockchain Researcher @ Quantstamp, [roshan@quantstamp.com](mailto:roshan@quantstamp.com?subject=Rollup%20Security%20Framework)
- Jan Gorzny, Ph.D., Head of L2 Scaling @ Quantstamp, [jan@quantstamp.com](mailto:jan@quantstamp.com?subject=Rollup%20Security%20Framework)
- Martin Derka, Ph.D., Head of New Initiatives @ Quantstamp, [martin@quantstamp.com](mailto:martin@quantstamp.com?subject=Rollup%20Security%20Framework)

## Folder Layout

The main code to run the analysis is in `experiments`.
Results, including generated charts are in `results`.
In `optimism-decoder`, there is a script that decodes Ethereum L1 `appendSequencerBatch()` transactions, which was used to collect the data for this project.

## Sample Data
Sample data -- namely, a subset of the data used for the final results -- is available at the [Evaluating Rollup Compression - Sample Data](https://github.com/quantstamp/l2-compression-data) repository. Note that the full data is too large to be shared via GitHub.

To use it, you will need to initialize and update the `data` folder by running the following commands in the root of this repository:

```
git submodule init
git submodule update
```

## Instructions

### Prerequisites
Use the correct version of python: `pyenv install 3.8.13`.
Then, create a vitural environment:
```
pip3 install virtualenv
virtualenv .env 
source .env/bin/activate
```

Then install the dependencies below, or all of them all at once: ` python3 -m pip install -r requirements.txt`.
```
pip3 install brotli
pip3 install zstd
pip3 install eth_utils
pip3 install 'rlp==0.6.0'
pip3 install pandas
pip3 install matplotlib
```

### Running the Code

The main entrypoint is `experiments/experiment.py`, which can be called by running `python3 experiment.py run a1` or `python3 experiment.py run a2`, for approaches `a1` and `a2` described in the paper (as A1 and A2).

You can use `python3 experiments/experiment.py results/a1_stats` to generate the `a1_stats` plots (use `a2_stats` for the A2 plots) after the data has been generated.

You can use `python3 experiments/plot_both_experiments.py` to generate scatter plots with both A1 and A2 data.


