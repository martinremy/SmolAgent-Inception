# SmolAgent-Inception

Example code demonstrating how to use SmolAgents with Inception Labs' diffusion-based Model using a custom Model class for SmolAgents. Due to the much faster speed of the diffusion LLM, the agent can perform complex tasks that require search and synthesizing data extremely quickly.

The following example plans the necessary steps, then does 20 web searches (10 each for max altitude and elevation of Kilimanjaro) and then synthesizes the data. All in 3.5 seconds.

```
$ uv run --env-file .env main.py

Final answer: No, a Cessna 172S cannot fly over the top of Mt Kilimanjaro because its service ceiling is around 13,000 ft (3,962 m), which is significantly lower than the mountain's summit at approximately 19,341 ft (5,895 m).
[Step 1: Duration 3.53 seconds]
```

## Prerequisites

- `uv` package manager
- API keys for Inception Labs (https://www.inceptionlabs.ai/). They have a generous free plan.

## Setup

1. Clone this repository

2. Copy the environment sample file:
   ```bash
   cp .env-sample .env
   ```

3. Edit `.env` and add your API key:
   ```
   INCEPTION_API_KEY=your_inception_api_key_here
   ```

4. Installing dependencies is handled automatically by `uv`

## Usage

Run the example with:

```bash
uv run --env-file .env main.py
```

## Customization

You can modify the query in the `main()` function or change the model parameters in the `InceptionModel.get_response()` method to experiment with different settings.
