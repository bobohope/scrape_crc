from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
import time
def start_scraping(string):
    #start a session (if you have no idea what is a session, google plz)
    s = requests.session()
    #get the page
    rq= s.get(string)
    url = []
    soup = ''
    output=[None]*11
    all_content=[]
    soup = BeautifulSoup(rq.text,'html.parser')
    #print html file for debug only
    #print(soup.prettify())

    #get name
    #<h1 id="ContentPlaceHolderCenter_H1" class="border-bottom-none">Jacques Albert</h1>
    name = soup.find('h1').text
    output[0]=name
    print('name: ',name)
    #TODO:parse the full name into lastname and first name
    #
    #
    #get chair title
    #<span id="ContentPlaceHolderCenter_FormView1_ChairTitleLabel" class="bold">Canada Research Chair in Advanced Photonic Components</span>
    chair_title = soup.find('span',id="ContentPlaceHolderCenter_FormView1_ChairTitleLabel").text
    output[1]=chair_title
    print('chair_title: ',chair_title)

    #get Tier
    #<span id="ContentPlaceHolderCenter_FormView1_TierLabel">Tier 1</span>
    tier=soup.find('span',id="ContentPlaceHolderCenter_FormView1_TierLabel").text
    output[2]=tier
    print('tier: ',tier)

    #get University
    #<span id="ContentPlaceHolderCenter_FormView1_universityLabel">Carleton University</span>
    university=soup.find('span',id="ContentPlaceHolderCenter_FormView1_universityLabel").text
    output[3]=university
    print('university: ',university)

    #get phone number
    #<span id="ContentPlaceHolderCenter_FormView1_ContactNumberLabel">613-250-2600 ext./poste 5578</span>
    phone_num=soup.find('span',id="ContentPlaceHolderCenter_FormView1_ContactNumberLabel").text
    output[4]=phone_num
    print('phone: ',phone_num)

    #get email address
    #<a id="ContentPlaceHolderCenter_FormView1_HyperLink1" href="mailto:jalbert@doe.carleton.ca" class="ui-link">jalbert@doe.carleton.ca</a>
    email=soup.find('a',id="ContentPlaceHolderCenter_FormView1_HyperLink1").text
    output[5]=email
    print('email: ',email)

    #get website
    #<a id="ContentPlaceHolderCenter_FormView1_ChairUrlLink" title="http://www.doe.carleton.ca/~jalbert/" href="http://www.doe.carleton.ca/~jalbert/" class="ui-link">Website</a>
    website=soup.find('a',id="ContentPlaceHolderCenter_FormView1_ChairUrlLink")['href']
    output[6]=website
    print('website: ',website)
    #get research_involve
    #<span id="ContentPlaceHolderCenter_FormView1_ResearchInvolvesLabel">Designing, fabricating, and testing photonic components that have been fabricated by laser light processing of high-performance optical materials.</span>
    research_involve=soup.find('span',id="ContentPlaceHolderCenter_FormView1_ResearchInvolvesLabel").text
    output[7]=research_involve
    print('research_involve: ',research_involve)

    #get research_relavant
    #<span id="ContentPlaceHolderCenter_FormView1_ResearchRelevanceLabel">The research will contribute to the competitiveness of the Canadian optics industry by providing new directions for photonic device research with a focus on reliability and manufacturability.</span>
    research_relavant=soup.find('span',id="ContentPlaceHolderCenter_FormView1_ResearchRelevanceLabel").text
    output[8]=research_relavant
    print('research_relavant: ',research_relavant)

    #get story_title
    #<span id="ContentPlaceHolderCenter_FormView1_StoryTitleLabel">Using Laser Light to Create Optical Components</span>
    story_title=soup.find('span',id="ContentPlaceHolderCenter_FormView1_StoryTitleLabel").text
    output[9]=story_title
    print('story_title: ',story_title)
    #get story_content
    story=soup.find('div',id="ContentPlaceHolderCenter_FormView1_PanelStory").text
    output[10]=story
    print('story: ',story)

    #print everything
    print(output)

if __name__ == "__main__":
    url_base = 'http://www.chairs-chaires.gc.ca/chairholders-titulaires/profile-eng.aspx?profileId='
    start_scraping(url_base+str(1070))
