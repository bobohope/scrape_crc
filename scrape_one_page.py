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

def get_html(string):
    #start a session (if you have no idea what is a session, google plz)
    s = requests.session()
    #get the page
    rq= s.get(string)
    s.close()
    soup = BeautifulSoup(rq.text,'html.parser')
    return soup

def checkstatus(soup):
    if soup.find('span',id="ContentPlaceHolderCenter_FormView1_ChairTitleLabel") is None:
        return False
    else:
        return True

def start_scraping(soup):

    output=[None]*14

    #print html file for debug only
    #print(soup.prettify())
    #get name
    #<h1 id="ContentPlaceHolderCenter_H1" class="border-bottom-none">Jacques Albert</h1>
    name = soup.find('h1').text
    output[0] = name
    #print('name: ',name)
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
    #print('chair_title: ',chair_title)

    #get Tier
    #<span id="ContentPlaceHolderCenter_FormView1_TierLabel">Tier 1</span>
    tier=soup.find('span',id="ContentPlaceHolderCenter_FormView1_TierLabel").text
    output[4]=tier
    #print('tier: ',tier)

    #get Subject
    #<span id="ContentPlaceHolderCenter_FormView1_Subject_EnLabel">Natural Sciences and Engineering</span>
    subject=soup.find('span',id="ContentPlaceHolderCenter_FormView1_Subject_EnLabel")
    if subject is not None:
        output[5]=subject.text
    #print('subject: ',subject)


    #get University
    #<span id="ContentPlaceHolderCenter_FormView1_universityLabel">Carleton University</span>
    university=soup.find('span',id="ContentPlaceHolderCenter_FormView1_universityLabel")
    if university is not None:
        output[6]=university.text
    #print('university: ',university)

    #get phone number
    #<span id="ContentPlaceHolderCenter_FormView1_ContactNumberLabel">613-250-2600 ext./poste 5578</span>
    phone_num=soup.find('span',id="ContentPlaceHolderCenter_FormView1_ContactNumberLabel")
    if phone_num is  not None:
        output[7]=phone_num.text
    #print('phone: ',phone_num)

    #get email address
    #<a id="ContentPlaceHolderCenter_FormView1_HyperLink1" href="mailto:jalbert@doe.carleton.ca" class="ui-link">jalbert@doe.carleton.ca</a>
    email=soup.find('a',id="ContentPlaceHolderCenter_FormView1_HyperLink1")
    if email is not None:
        output[8]=email.text
    #print('email: ',email)

    #get website
    #<a id="ContentPlaceHolderCenter_FormView1_ChairUrlLink" title="http://www.doe.carleton.ca/~jalbert/" href="http://www.doe.carleton.ca/~jalbert/" class="ui-link">Website</a>

    website_archer=soup.find('a',id="ContentPlaceHolderCenter_FormView1_ChairUrlLink")
    if website_archer is not None:
        output[9]=website_archer['href']
    #print('website: ',output[9])
    #get research_involve
    #<span id="ContentPlaceHolderCenter_FormView1_ResearchInvolvesLabel">Designing, fabricating, and testing photonic components that have been fabricated by laser light processing of high-performance optical materials.</span>
    research_involve=soup.find('span',id="ContentPlaceHolderCenter_FormView1_ResearchInvolvesLabel")
    if research_involve is not None:
        output[10]=research_involve.text
    #print('research_involve: ',research_involve)

    #get research_relavant
    #<span id="ContentPlaceHolderCenter_FormView1_ResearchRelevanceLabel">The research will contribute to the competitiveness of the Canadian optics industry by providing new directions for photonic device research with a focus on reliability and manufacturability.</span>
    research_relavant=soup.find('span',id="ContentPlaceHolderCenter_FormView1_ResearchRelevanceLabel")
    if  research_relavant is not None:
        output[11]=research_relavant.text
    #print('research_relavant: ',research_relavant)

    #get story_title
    #<span id="ContentPlaceHolderCenter_FormView1_StoryTitleLabel">Using Laser Light to Create Optical Components</span>
    story_title=soup.find('span',id="ContentPlaceHolderCenter_FormView1_StoryTitleLabel")
    if story_title is not None:
        output[12]=story_title.text
    #print('story_title: ',story_title)
    #get story_content
    story=soup.find('div',id="ContentPlaceHolderCenter_FormView1_PanelStory")
    if story is not None:
        import re
        storya=story.text
        storya= re.sub('\s+', ' ', storya)
        output[13]=storya
    #print('story: ',story)

    #print everything
    print(output)
    return output



def write_to_csv(info):
    import csv
    with open('output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile,dialect='excel')
        writer.writerow(info)

if __name__ == "__main__":
    url_base = 'http://www.chairs-chaires.gc.ca/chairholders-titulaires/profile-eng.aspx?profileId='
    #soup = get_html(url_base+str(1070))
    #print(checkstatus(soup))
    #outout = start_scraping(soup)
    #write_to_csv(outout)
    for i in range(3808, 5000):
        soup=get_html(url_base+str(i))
        if checkstatus(soup) == True:
            print("start_scraping--", i)
            info=start_scraping(soup)
            write_to_csv(info)
            #this is VERY IMPORTANT to prevent being blocked!!!!!!!!
        time.sleep(1)
