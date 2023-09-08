# Text Analytics with ChatGPT

Welcome to the Text Analytics with ChatGPT repository! This repository provides a Python-based toolkit for text analysis tasks, including sentiment analysis, topic analysis, text translation, and spelling correction, using the ChatGPT Python API.

## Getting Started

To get started with this toolkit, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/DavidSolan0/tweets_analysis_with_chatgpt.git
   ```

2. Create a virtual environment (venv) to manage dependencies:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies from the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

You can use the provided `codification.py` module to perform various text analysis tasks. Check out the `text_analytics` notebook in the `src` folder for an example of how to use the module.

### Text Data Collection

If you need to collect text data, we've included a `data_collection` module and a corresponding Jupyter notebook in the `src/data` folder. This module can be used to gather data from Twitter or other sources.

### Data Storage

You have the option to organize your text data in the `data` folder. Create subfolders for each client and save their text information in `.csv` files within their respective subfolders.

## Examples

You can find usage examples and sample code in the `text_analytics` notebook in the `src` folder. This notebook demonstrates how to use the `codification.py` module for text analysis tasks.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

We would like to thank OpenAI for providing the ChatGPT API, which powers this text analysis toolkit.

Feel free to reach out if you have any questions or need further assistance. Happy text analysis!

