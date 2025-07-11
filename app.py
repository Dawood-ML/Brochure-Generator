# A full Business Solution with LLMs 


#######################################
#
#
#      Building a product that builds
#      a brochure for a company
#
#######################################



########################################

# Imports

#########################################
try:
    import os
    import requests
    import json
    from typing import List
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup
    import streamlit as st  # Import Streamlit
    from openai import OpenAI
except ModuleNotFoundError:
    print('''
          Get your dependencies first
          
    !pip install openai
    !pip install bs4
    !pip install requests
    !pip install dotenv
    !pip install streamlit''')

##########################################

# Initializing constants

##########################################


load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')


if api_key and api_key.startswith('sk-proj') and len(api_key)>10:
    print('Good')

else:
    print('There might be a problem with your API key. Please check!')

MODEL = 'gpt-4o-mini'
openai = OpenAI()


######################################

# Creating a class that represents a WebPage

######################################

# Some websites need you to us eproper headers when fetching them 
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


class Website:
    """
    A utility class to represent a Website that we have scraped, now with links
    """

    def __init__(self, url):
        self.url = url
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            self.body = response.content
            soup = BeautifulSoup(self.body, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input"]):
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = ""

            links  = [link.get('href') for link in soup.find_all('a')]
            self.links = [link for link in links if link]
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching URL {url}: {e}")
            self.body = ""
            self.title = "Error"
            self.text = ""
            self.links = []


    def get_contents(self):
        return f"Webpage title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
    

#######################################################

# Creating a sytem prompt for the LLM

#######################################################

link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
"""


##################################################

#    Creating a user prompt to give the llm our list of links

##################################################


def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


####################################################

# Now Putting above together in a function

####################################################

def get_links(url):
    website = Website(url)
    if not website.body: # Check if website fetching was successful
        return {"links": []}
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
        ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    return json.loads(result)


####################################################

# NOW We get to brochure Part of our Project

####################################################

def get_all_details(url):
    result = "Landing page:\n"
    result += Website(url).get_contents()
    links = get_links(url)
    st.write("Found links:", links) # Using st.write to show the found links in the UI
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result


system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:10000] # Truncate if more than 10,000 characters
    return user_prompt

########################################################################


def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
          ],
    )
    result = response.choices[0].message.content
    st.markdown(result) # Use st.markdown to display the result

#############################################################

def stream_brochure(company_name, url):
    stream = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
          ],
        stream=True
    )
    
    placeholder = st.empty() 
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        cleaned_response = response.replace("```markdown", "```").replace("markdown", "")
        placeholder.markdown(cleaned_response) 

#####################################################################

# Streamlit UI
st.title("Company Brochure Generator")

company_name = st.text_input("Enter the company name:", "Google")
url = st.text_input("Enter the company website URL:", "https://google.com")

if st.button("Generate Brochure"):
    if company_name and url:
        with st.spinner("Generating your brochure..."):
            stream_brochure(company_name, url)
    else:
        st.error("Please enter both a company name and a URL.")