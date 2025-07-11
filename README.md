### Company Brochure Generator

This is a small project I put together that takes a company's website and creates a Professional brochure from it. You just give it the company's name and web address, and it pulls information to build a summary.

#### How It Works

The idea was to automate the process of gathering info. It starts by looking at the homepage you provide. From there, it scrapes the text and also looks for other pages that might be important, like "About" or "Careers" section. I used an LLM to help sort through the links and guess which ones are most relevant.

After it gathers the text from these pages, it hands everything over to another LLM. This second model then takes all the context and writes a short brochure in markdown. The final output is displayed on the screen.

#### Getting Started

If you want to run this yourself, here’s how:

1.  **Download the files:**
    You can clone this repository to your computer.
    ```
    git clone https://github.com/your-username/brochure-generator.git
    cd brochure-generator
    ```

2.  **Install what's needed:**
    Libraries required to make it work. 
    ```
    pip install openai bs4 requests dotenv streamlit
    ```

3.  **Set up the API Key:**
    You need an OpenAI API for this project or ANY api key. You will need to get a key from their website. Once you have it, create a file named `.env` in the main folder and add your key to it like this:
    ```
    OPENAI_API_KEY='your-actual-api-key'
    ```

4.  **Run the application:**
    To start the program, run this command in your terminal:
    ```
    streamlit run app.py
    ```
    This will launch the web interface in your browser.


#### Technologies Used

*   **Python**
*   **Streamlit** for the user interface.
*   **OpenAI API** for the language model parts.
*   **Beautiful Soup** and **Requests** for the web scraping.

#### Some Thoughts

I built this mostly as a way to get more familiar with using LLMs for a practical task. It's a fairly simple tool, and there's definitely room for improvement. For instance, it might struggle with websites that load their content dynamically with JavaScript. It could also be better at choosing which links to follow. Still, it was a good learning experience.
