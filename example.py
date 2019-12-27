from deepthought import TimeLapse, StageLoop, Experiment

experiment = Experiment()
experiment.plate("35mm", scan="default")
experiment.plasmid("H2B-EGFP") 
experiment.plasmid("PCNA")
experiment.mag("100")


def microirradiation():
	TimeLapse(StageLoop(experiment), 27, 5, "microirradiation")