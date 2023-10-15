import pandas as pd
from adala.datasets import PandasDataFrame
from adala.skills import LLMSkill
from adala.agents import SingleShotAgent
from adala.runtimes import OpenAIGPTRuntime

# example analogous to https://colab.research.google.com/drive/1Bn11v5X85PEgWnn3Rz_4GJRIUh3S0aEB

# create dataset
filepath = 'https://hs-sandbox-pub.s3.amazonaws.com/amazon_cells_labelled.tsv'
df = pd.read_csv(filepath, sep='\t', nrows=100)
dataset = PandasDataFrame(df=df)



# enable target skill
skill = LLMSkill(
    name='subjectivity_detection',
    description='Understanding subjective and objective statements from text.',
    instructions='Classify a product review as either expressing "Subjective" or "Objective" statements.'
)

predictions = skill.apply(dataset)
evaluations = skill.evaluate(dataset, predictions)
experience = skill.analyze(dataset, evaluations)
skill.improve(dataset, experience)

# create agent to improve the skill
# agent = SingleShotAgent(dataset=dataset, skill=skill)

# run agent
# step_result = agent.step()
