class UserProfile(object):

    #[_ID, "first name", "last name", "Description", "Ethnicity", "Phone Number", "Current Address"
    #"Experiences": [list of strings], "Education": [list of dictionaries]
    #"Summary", "Courses", "Languages", "Skills", ]

    #Experiences: [Title: , Company: , Location: , "" Start Date (Month, year): , End Date: ,UploadFiles, Links, WorkHere]
    #Educations: [School:, Degree, Field of Study, Grade, Activities and Societies:, From Year, to Year, Description]
    def __init__(self, bfemail, bfpassword, alemail, alpassword, first_name, last_name, major, description = "", ethnicity = "", currentAddress = "", summary = "",
                experiences = [], educations = [], courses = [], languages = [], skills = [], projects=[]):
        self.bfemail = bfemail
        self.bfpassword = bfpassword
        self.alemail = alemail
        self.alpassword = alpassword
        self.profile = {}
        self.profile['first_name'] = first_name
        self.profile['last_name'] = last_name
        self.profile['major'] = major
        self.profile['description'] = description
        self.profile['ethnicity'] = ethnicity
        self.profile['currentAddress'] = currentAddress
        self.profile['summary'] = summary
        self.profile['experiences'] = experiences
        self.profile['number_of_experiences'] = len(experiences)
        self.profile['education'] = educations
        self.profile['number_of_educations'] = len(educations)
        self.profile['courses'] = courses
        self.profile['number_of_courses'] = len(courses)
        self.profile['languages'] = languages
        self.profile['number_of_languages'] = len(languages)
        self.profile['skills'] = skills
        self.profile['number_of_skills'] = len(skills)
        self.profile['bfemail'] = bfemail
        self.profile['bfpassword'] = bfpassword
        self.profile['projects'] = projects
        self.profile['number_of_projects'] = len(projects)

class Address(object):
    def __init__(self, street, street_number, state, country, zip_code):
        self.street = street
        self.street_number = street_number
        self.state = state
        self.country = country
        self.zip_code = zip_code

class Education(object):
    def __init__(self, school, degree, field_of_study, grade, activities_societies, from_year,
                 description, to_year = "Present"):
        self.school = school
        self.degree = degree
        self.field_of_study = field_of_study
        self.grade = grade
        self.activities_societies = activities_societies
        self.from_year = from_year
        self.to_year = to_year
        self.description = description

class Experience(object):
    def __init__(self, title, company, location, start_date, end_date, links = [], description = "", workhere = "False", summary=""):
        self.title = title
        self.company = company
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.links = links
        self.workhere = workhere
        self.description = description
        self.summary = summary

class Links(object):
    def __init__(self, personal_website, linkedin, github, stackOverflow):
        self.personalWeb = personal_website
        self.linkedin = linkedin
        self.github = github
        self.stackOverflow = stackOverflow

class Project(object):
    def __init__(self, title, role, summary, start_time, end_time="", description="", url="", Organization="", currentWorking=False):
        self.title = title
        self.role = role
        self.summary = summary
        self.description = description
        self.link = url
        self.organization = Organization
        self.start_date = start_time
        self.end_date = end_time
        self.currentWorking = currentWorking
        