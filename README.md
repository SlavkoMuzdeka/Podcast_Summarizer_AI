# 🎙️ Podcast Summarizer AI

The `Podcast Summarizer AI` is a project designed to automatically download podcast episodes, transcribe them into text, and generate summaries with adjustable levels of detail. This project leverages powerful models like `OpenAI’s Whisper` for transcription and `GPT` and `o-` models for summarization, providing an efficient tool for podcast content consumption.

The system consists of three main steps: downloading podcast episodes, transcribing them, and summarizing the content.

### 1. Downloading Podcast Episodes

Podcast episodes can be downloaded from several sources, including:

- **YouTube**: Requires `YouTube URL` to download episode as `.mp3` file. 
- **Spotify**: Requires `RSS` feed URL and episode name to fetch it.
- **Apple Podcasts & Podcast Addict**: Requires `RSS` feed URL and episode name to fetch it.
- **Alternative sources**: Requires `RSS` feed URL and episode name to fetch it.

If an `RSS` feed is not available, services like [Listen Notes](https://www.listennotes.com/?s=rss_viewer) can be used.

### 2. Transcribing Podcast Episodes

After downloading, the `Whisper Transcriber` uses `OpenAI's Whisper` model to convert the audio into text. The system checks for existing transcriptions to avoid reprocessing and is modular to allow easy upgrades.

The Whisper model is run locally, and it will be automatically installed when you install the project dependencies. The speed of transcription depends on the hardware you are using:

- **GPU**: If your machine has a `GPU`, `Whisper` will execute much faster.
- **CPU**: On a `CPU`, the transcription process will be slower.

By default, the `base` version of the `Whisper` model is used, but this can be changed by modifying the `config.json` file.


### 3. Summarizing Transcriptions

The transcribed text is summarized using `OpenAI’s GPT API`. You can control the level of detail in the summary, ranging from high-level summaries to more detailed outputs. The text is split into chunks, processed by `GPT` or `o-` model, and compiled into a final summary.

You can change the model used for summarizing by providing the name of the model in the `config.json` file.


## ⚖️ Model Comparison for Summarization

Here is a more detailed comparison of the available summarization models:

- **GPT-3.5-turbo**:
  - **Pros**: 
    - More cost-effective than other models.
    - Suitable for shorter transcripts.
  - **Cons**: 
    - May miss some nuances in longer transcripts.
    - Less accurate compared to `GPT-4-turbo`.
    - Can sometimes struggle with context in larger chunks of text.
  - **Ideal Use Case**: Best for summarizing shorter podcasts where budget is a consideration.

- **GPT-4-turbo**:
  - **Pros**:
    - Higher quality and faster execution than `GPT-3.5-turbo`.
    - Works well with longer transcripts and provides better accuracy.
    - Better at understanding context in long-form content.
  - **Cons**:
    - Slightly more expensive than `GPT-3.5`.
  - **Ideal Use Case**: Ideal for summarizing longer podcasts or content that requires a high level of understanding.

- **GPT-4o-mini**:
  - **Pros**:
    - Smaller, cheaper alternative to `GPT-4-turbo` with a large token context window.
    - Efficient for mid-range podcast episodes.
  - **Cons**:
    - Can be less detailed compared to the full `GPT-4-turbo`.
  - **Ideal Use Case**: Suitable for users who want a balance between cost and quality, especially for medium-length podcasts.

- **o3-mini**:
  - **Pros**:
    - Lightweight model with promising performance for efficiency.
    - Lower processing time and reduced cost.
  - **Cons**:
    - Not as powerful as the larger models, leading to lower-quality summaries.
  - **Ideal Use Case**: Great for quick summaries or when computational resources are limited.

**Recommendation**: For the highest-quality summaries, **GPT-4-turbo** is preferred, especially for long podcasts or episodes requiring deep understanding. For quicker, cost-effective solutions, **GPT-3.5-turbo** or **GPT-4o-mini** may be suitable.


## 💰 Pricing

- **Whisper Model**: Free for transcribing audio.
- **OpenAI API**: Pricing for summarization depends on the model used. Check the section **⚖️ Model Comparison for Summarization** for more details.
- **Alternative Solutions**: The `DeepSeek API` can be considered if you wish to avoid OpenAI costs.

## 📂 Example Output (Using `GPT-4-turbo`)

For reference, here is an example of the summarization process, each using a different level (`0`, `0.5`, `1`). A `YouTube` episode was processed using the system. The original episode can be found at:

[Podcast Episode](https://www.youtube.com/watch?v=NhHnIlRlGts) (Video length: `41.11` minutes)

After transcription, the transcribed text is stored in a file (total tokens in a document `9074`):

[NhHnIlRlGts.txt](examples/NhHnIlRlGts.txt)

The final summaries were generated based on different detail levels:

- **Detail Level: `0`** (Concise summary)
    - **Number of chunks**: `1`
    - **Chunks size**: `[9074]`
    - **Summary output**:  
        [summary_0.txt](examples/summary_0.txt)
        
- **Detail Level: `0.5`** (Balanced summary)
    - **Number of chunks**: `11`
    - **Chunks size**: `[877, 897, 887, 891, 856, 908, 902, 888, 890, 905, 173]`
    - **Summary output**:  
        [summary_0_5.txt](examples/summary_0_5.txt)
        
- **Detail Level: `1`** (Detailed summary)
    - **Number of chunks**: `19`
    - **Chunks size**: `[490, 490, 491, 491, 497, 480, 490, 468, 499, 475, 457, 485, 497, 478, 487, 499, 459, 501, 340]`
    - **Summary output**:  
        [summary_1.txt](examples/summary_1.txt)


## 🚀 Running the Project

### 🛠️ Requirements

To run the project, ensure you have the following dependencies:

- `ffmpeg` (for downloading podcast audio)
- Other Python dependencies listed in `requirements.txt`.

Additionally, you will need to create a `.env` file in the root of your project directory and store your `OpenAI API key` in it. The file should contain the following line:
  ```plaintext
  OPENAI_API_KEY="your_openai_api_key_here"
  ```

It is recommended to use **Python 3.11+** and set up a **virtual environment** for the project. You can follow the steps below to get started:

### Steps to Run the Project:

1. **Clone the repository**:
   First, clone the repository to your local machine:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Set up a virtual environment**: It’s best practice to create a virtual environment to isolate dependencies. Run the following commands:
   ```bash
   python -m venv venv
   ```

    On Windows, activate the virtual environment with:
    ```bash
    venv\Scripts\activate
    ```

    On MacOS/Linux, use:
    ```bash
    source venv/bin/activate
    ```
3. **Install the required dependencies**: Once the virtual environment is activated, install the necessary Python packages:
    ```bash
    pip install -r requirements.txt
    ```

    This will also install `Whisper` locally, which is used for transcribing podcast episodes into text. If you have a `GPU`, the transcription will be faster. Otherwise, it will run on the `CPU`, which will be slower. The default model used by `Whisper` is `base`, but you can change the model by updating the `config.json` file.

4. **Run the project**: After the installation is complete, you can run the project using Streamlit:
    ```bash
    streamlit run streamlit_app.py
    ```

    This will start the Streamlit app, and you can access it through your web browser.
