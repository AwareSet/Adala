# ADALA

Adala is an Autonomous DatA (Labeling) Agent framework.

Adala offers a robust framework for implementing agents specialized in data processing, with a particular emphasis on
diverse data labeling tasks. These agents are autonomous, meaning they can independently acquire one or more skills
through iterative learning. This learning process is influenced by their operating environment, observations, and
reflections. Users define the environment by providing a ground truth dataset. Every agent learns and applies its skills
in what we refer to as a "runtime", synonymous with LLM.

Offered as an HTTP server, users can interact with Adala via command line or RESTful API, and directly integrate its
features in Python Notebooks or scripts. The self-learning mechanism leverages Large Language Models (LLMs) from
providers like OpenAI and VertexAI.

### Why Choose Adala?

- **Specialized in Data Processing**: While our agents excel in diverse data labeling tasks, they can be tailored to a
  wide range of data processing needs.
- **Autonomous Learning**: Adala agents aren't just automated; they're intelligent. They iteratively and independently
  develop skills based on environment, observations, and reflections.
- **User-Centric Environment Setup**: You have control. Define your agent's learning environment simply by providing a
  ground truth dataset.
- **Optimized Runtime**: Our agents operate in a state-of-the-art runtime environment, synonymous with LLM, ensuring
  efficiency and adaptability.
- **Extend to your domain**: Build custom agents and skills focused on your specific domain.

## Installation

Install ADALA:

```sh
git clone https://github.com/HumanSignal/ADALA.git
cd ADALA/
pip install -e .
```

If you're planning to use human-in-the-loop labeling, or need a labeling tool to produce ground truth datasets, we
suggest installing Label Studio. Adala is made to support Label Studio format right out of the box.

```sh
pip install label-studio
```

## Prerequisites

1. Set OPENAI_API_KEY ([see instructions here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key))
2. Check OpenAI API availability, sometimes it's down: https://status.openai.com/uptime
3. To run quickstart tutorials you have to install pandas:
```
pip install pandas
```

## Quickstart

In this example we will use ADALA as a standalone library directly inside our python notebook. You can open it in Collab
right here.

```python
import pandas as pd

from adala.agents import SingleShotAgent
from adala.datasets import DataFrameDataset
from adala.skills import LabelingSkill

# this is the dataset we will use to train our agent
# filepath = "path/to/dataset.csv"
# df = pd.read_csv(filepath, sep='\t', nrows=100)

texts = [
    "The mic is great.",
    "Will order from them again!",
    "Not loud enough and doesn't turn on like it should.",
    "The phone doesn't seem to accept anything except CBR mp3s",
    "All three broke within two months of use."
]
df = pd.DataFrame(texts, columns=['text'])

agent = SingleShotAgent(
    # connect to a dataset
    dataset=DataFrameDataset(df=df),
    
    # define a skill
    skill = LabelingSkill(labels=['Positive', 'Negative', 'Neutral']),
)

run = agent.run()

# display results
print(pd.concat((df, run.experience.predictions), axis=1))

# provide ground truth signal in the original dataset
df.loc[0, 'ground_truth'] = 'Positive'
df.loc[2, 'ground_truth'] = 'Negative'
df.loc[4, 'ground_truth'] = 'Neutral'

for _ in range(3):
    # agent learns and improves from the ground truth signal
    learnings = agent.learn(update_instructions=True)
    
    # display results
    print(learnings.experience.accuracy)
```

Check [more examples in notebook tutorials.](https://github.com/HumanSignal/ADALA/tree/master/adala/examples)

## Running ADALA as a standalone server (Comming soon!)

Initiate the Adala server. Note: Each agent operates as its own web server.

### Starting the Adala Server

```sh
# Start the Adala server on default port 8090
adala start
```

### Uploading Ground Truth Data

Before teaching skills to Adala, you need to set up the environment and upload data.

```sh
# Upload your dataset
adala upload --file sample_dataset_ground_truth.json
```

### Teaching Skills to Adala

Now, define and teach a new skill to Adala.

```sh
# Define a new skill for classifying objects
adala add-skill --name "Object Classification" --description "Classify text into categories." --instruction "Example: Label trees, cars, and buildings."
```

```sh
# Start the learning process
adala learn --skill "Object Classification" --continuous
```

### Monitoring Optimization

Track the progress of the optimization process.

```sh
# Check the optimization status
adala status
```

### Applying Skills and Predictions

You don't need to wait for optimization to finish. Instruct Adala to apply its skills on new data outside the
environment, turning Adala into a prediction engine. If the predictions generated by the skill are then verified by
human validators or another supervision system, this provides more ground truth data, enhancing the agent's skills. Use
the learned skills and generate predictions.

```sh
# Apply the 'Object Classification' skill on new data
adala apply-skill --name "Object Classification" --file sample_dataset_predict.json
```

### Review Metrics

Get insights into Adala's performance.

```sh
# View detailed metrics
adala metrics
```

## Executing ADALA Command Line

```sh
# Start the Adala server on default port 8090
adala start --port 8090

# Upload your dataset
adala upload --file sample_dataset_ground_truth.json

# Define a new skill for classifying objects
adala add-skill --name "Object Classification" --description "Classify images into categories." --instruction "Example: Label trees, cars, and buildings."

# Start the learning process
adala learn --skill "Object Classification"

# Check the optimization status
adala status

# Apply the 'Object Classification' skill on new data
adala apply-skill --name "Object Classification" --file sample_dataset_predict.json

# View detailed metrics
adala metrics

# Restart the Adala server
adala restart

# Shut down the Adala server
adala shutdown

# List all the skills
adala list-skills

# List all the runtimes
adala list-runtimes

# Retrieve raw logs
adala logs

# Provide help
adala help <command>
```

## Contributing to ADALA

Dive into the heart of Adala by enhancing our Skills, optimizing Runtimes, or pioneering new Agent Types. Whether you're
crafting nuanced tasks, refining computational environments, or sculpting specialized agents for unique domains, your
contributions will power Adala's evolution. Join us in shaping the future of intelligent systems and making Adala more
versatile and impactful for users across the globe.

Read more here.

## How ADALA compares to other agent libraries

## FAQ

- What is an agent?
- Agent is a set of skills and runtimes that could be used to execute those skills. Each agent has its own unique
  environment (dataset)
  attached to it. You can define your own agent class that would have a unique set of skills for your domain.

-

## Interesting Stuff

Skill is a learned ability to solve a specific task. Skill gets trained from the ground truth dataset. 
