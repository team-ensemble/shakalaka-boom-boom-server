# Shakalaka Boom Boom
Shakalaka Boom Boom is an A.I. experiment which creates a magical experience by converting anything drawn on a mobile canvas into a real object in augmented reality world.

## About this repository
This repository contains the code for the Shakalaka Boom Boom experiment server which has the capability to classify drawing. Currently the machine learning model deployed in the server is capable of classifying drawings of candle, chair, cup, lamp and vase only.

## Installation instructions
This project makes use of [conda](https://conda.io/) to manage dependencies. So make sure you have conda installed before proceeding or install the dependencies manually by looking at the [environment.yml](environment.yml) file. Once you have conda installed get the dependencies installed by running
```
conda env create -f environment.yml
```

## Usage instructions
1. Activate the conda environment by running
```
source activate shakalakaBoomBoom
```
(Windows users omit the word `source` while activating the environment)

2. Change into repository directory and then export the `FLASK_APP` environment variable by running
```
export FLASK_APP=app.py
```
3. Start local server by running
```
flask run
```
Once the local server is running, you will get a url such as `http://127.0.0.1:5000/`
Then send out POST requests to `upload` endpoint (for example `http://127.0.0.1:5000/upload`) to classify the drawing and get the classification result as response.

### Additional info
To expose the server to external world, use a tool such as [ngrok](https://ngrok.com/). Install it and then run
```
./ngrok http 5000
```
