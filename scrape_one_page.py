from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
import time

#First, add a function to check if the prof id is available
#Second, add in line 28 to output first name and last name, output[1] and output[2]
#Third, add a function that write all the message to a csv file.

def parse_name(string):
    '''input full name, output a list of 2 string, lastname first'''
    name_split=string.split()
    lastname=name_split[-1]
    del name_split[-1]
    firstname=" ".join(name_split)
    return [lastname, firstname]
def start_scraping(string):
    #start a session (if you have no idea what is a session, google plz)
    s = requests.session()
    #get the page
    rq= s.get(string)
    url = []
    soup = ''
    output=[None]*14
    all_content=[]
    soup = BeautifulSoup(rq.text,'html.parser')
    #print html file for debug only
    #print(soup.prettify())
    #get name
    #<h1 id="ContentPlaceHolderCenter_H1" class="border-bottom-none">Jacques Albert</h1>
    name = soup.find('h1').text
    output[0] = name
    print('name: ',name)
    #TODO:parse the full name into lastname and first name
    name_split=parse_name(name)
    output[1]=name_split[0]
    output[2]=name_split[1]
    #new_name = name.split()
    #if len(new_name) == 3:
    #    output[1] = new_name[0]
    #    output[2] = new_name[2]
    #elif len(new_name) == 2:
    #    output[1] = new_name[0]
    #    output[2] = new_name[1]
    #else:
    #    output[1] = new_name[0]
    #    output[2] = 0;

    #get chair title
    #<span id="ContentPlaceHolderCenter_FormView1_ChairTitleLabel" class="bold">Canada Research Chair in Advanced Photonic Components</span>
    chair_title = soup.find('span',id="ContentPlaceHolderCenter_FormView1_ChairTitleLabel").text
    output[3]=chair_title
    print('chair_title: ',chair_title)

    #get Tier
    #<span id="ContentPlaceHolderCenter_FormView1_TierLabel">Tier 1</span>
    tier=soup.find('span',id="ContentPlaceHolderCenter_FormView1_TierLabel").text
    output[4]=tier
    print('tier: ',tier)

    #get Subject
    #<span id="ContentPlaceHolderCenter_FormView1_Subject_EnLabel">Natural Sciences and Engineering</span>
    subject=soup.find('span',id="ContentPlaceHolderCenter_FormView1_Subject_EnLabel").text
    output[5]=subject
    print('subject: ',subject)


    #get University
    #<span id="ContentPlaceHolderCenter_FormView1_universityLabel">Carleton University</span>
    university=soup.find('span',id="ContentPlaceHolderCenter_FormView1_universityLabel").text
    output[6]=university
    print('university: ',university)

    #get phone number
    #<span id="ContentPlaceHolderCenter_FormView1_ContactNumberLabel">613-250-2600 ext./poste 5578</span>
    phone_num=soup.find('span',id="ContentPlaceHolderCenter_FormView1_ContactNumberLabel").text
    output[7]=phone_num
    print('phone: ',phone_num)

    #get email address
    #<a id="ContentPlaceHolderCenter_FormView1_HyperLink1" href="mailto:jalbert@doe.carleton.ca" class="ui-link">jalbert@doe.carleton.ca</a>
    email=soup.find('a',id="ContentPlaceHolderCenter_FormView1_HyperLink1").text
    output[8]=email
    print('email: ',email)

    #get website
    #<a id="ContentPlaceHolderCenter_FormView1_ChairUrlLink" title="http://www.doe.carleton.ca/~jalbert/" href="http://www.doe.carleton.ca/~jalbert/" class="ui-link">Website</a>

    website_archer=soup.find('a',id="ContentPlaceHolderCenter_FormView1_ChairUrlLink")
    if website_archer is not None:
        output[9]=website_archer['href']
    print('website: ',output[9])
    #get research_involve
    #<span id="ContentPlaceHolderCenter_FormView1_ResearchInvolvesLabel">Designing, fabricating, and testing photonic components that have been fabricated by laser light processing of high-performance optical materials.</span>
    research_involve=soup.find('span',id="ContentPlaceHolderCenter_FormView1_ResearchInvolvesLabel").text
    output[10]=research_involve
    print('research_involve: ',research_involve)

    #get research_relavant
    #<span id="ContentPlaceHolderCenter_FormView1_ResearchRelevanceLabel">The research will contribute to the competitiveness of the Canadian optics industry by providing new directions for photonic device research with a focus on reliability and manufacturability.</span>
    research_relavant=soup.find('span',id="ContentPlaceHolderCenter_FormView1_ResearchRelevanceLabel").text
    output[11]=research_relavant
    print('research_relavant: ',research_relavant)

    #get story_title
    #<span id="ContentPlaceHolderCenter_FormView1_StoryTitleLabel">Using Laser Light to Create Optical Components</span>
    story_title=soup.find('span',id="ContentPlaceHolderCenter_FormView1_StoryTitleLabel").text
    output[12]=story_title
    print('story_title: ',story_title)
    #get story_content
    story=soup.find('div',id="ContentPlaceHolderCenter_FormView1_PanelStory").text
    import re
    story = re.sub('\s+', ' ', story)
    output[13]=story
    print('story: ',story)

    #print everything
    print(output)

def checkstatus(string):
    import requests
    s = requests.session()
    rq= s.get(string)
    soup = ''
    soup = BeautifulSoup(rq.text,'html.parser')
    chair_title = soup.find('h1').text
    request = requests.get(string)
    if request.status_code == 200:
        if  len(chair_title.split()) != 1:
            return True
    return False

if __name__ == "__main__":
    url_base = 'http://www.chairs-chaires.gc.ca/chairholders-titulaires/profile-eng.aspx?profileId='
    # print(checkstatus(url_base+str(1070)))
    # start_scraping(url_base+str(1070))
    for i in range(1, 1000):
        if checkstatus(url_base+str(i)) == True:
            print(i)
            start_scraping(url_base+str(i))
            #this is VERY IMPORTANT to prevent being blocked!!!!!!!!
            time.sleep(2)
