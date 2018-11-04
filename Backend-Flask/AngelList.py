from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from User import *

class AngelListModifier:
    def __init__(self, user):
        self.profile = user.profile
        self.experiences = user.profile['experiences']
        self.projects = user.profile['projects']
        self.username = user.alemail
        self.password = user.alpassword

    def login(self, username, password):
        self.driver.find_element_by_name("user[email]").send_keys(username)
        elem = self.driver.find_element_by_name("user[password]")
        elem.send_keys(password)
        elem.submit()

    def delete_experiences(self, num_of_exp):
        self.driver.find_element_by_xpath("//a[@class='edit_experience keep_mobile']").click()
        for _ in range(num_of_exp):
            self.driver.find_element_by_xpath("//a[@class='edit g-button smaller']").click()
            actions = ActionChains(self.driver)
            actions.pause(0.5)
            actions.perform()
            self.driver.find_element_by_xpath("//a[@class='delete g-button smaller']").click()
            alert = self.driver.switch_to.alert
            alert.accept()
            actions = ActionChains(self.driver)
            actions.pause(0.5)
            actions.perform()

    def add_experiences_first(self, Experiences):
        for experience in Experiences:
            if experience.title.lower() == "founder":
                select = Select(self.driver.find_element_by_name('role'))
                select.select_by_value("founder")
            self.driver.find_element_by_name("company_name").send_keys(experience.company)
            self.driver.find_element_by_xpath(
                "//a[@class='c-button c-button--gray quick-add-button js-quick-add submit']").click()

    def add_experience_second(self, Experiences):
        self.driver.find_element_by_xpath("//a[@class='edit_experience keep_mobile']").click()
        actions = ActionChains(self.driver)
        actions.pause(0.5)
        actions.perform()
        editButtons = self.driver.find_elements_by_xpath("//a[@class='edit g-button smaller']")
        for i in range(len(editButtons)):
            editButtons[i].click()
        saveButtons = self.driver.find_elements_by_xpath("//a[@class='save g-button blue smaller']")
        titleFields = self.driver.find_elements_by_name("startup_role_metadata[title]")
        descripFields = self.driver.find_elements_by_name("startup_role_metadata[description]")
        currentCheckBoxes = self.driver.find_elements_by_class_name("js-current-checkbox")
        startMonthSelections = self.driver.find_elements_by_name("startup_role_metadata[started_at_month]")
        startYearSelections = self.driver.find_elements_by_name("startup_role_metadata[started_at_year]")
        endMonthSelections = self.driver.find_elements_by_name("startup_role_metadata[ended_at_month]")
        endYearSelections = self.driver.find_elements_by_name("startup_role_metadata[ended_at_year]")
        for i in range(len(Experiences)):
            experience = Experiences[i]
            startMonth = experience.start_date.split("/")[0]
            startYear = experience.start_date.split("/")[2]
            actions.perform()
            titleFields[2 * i].send_keys(experience.title)
            descripFields[2 * i].send_keys(experience.description)

            select = Select(startMonthSelections[i * 2])
            select.select_by_index(int(startMonth))
            select = Select(startYearSelections[i * 2])
            select.select_by_value(startYear)
            if not experience.workhere:
                currentCheckBoxes[2 * i].click()
                actions.perform()
                endMonth = experience.end_date.split("/")[0]
                endYear = experience.end_date.split("/")[2]
                select = Select(endMonthSelections[i * 2])
                select.select_by_index(int(endMonth))
                select = Select(endYearSelections[i * 2])
                select.select_by_value(endYear)
            saveButtons[i].click()

    def delete_projects(self, num_of_projects):
        editButtons = self.driver.find_elements_by_xpath("//a[@class='js-edit-link']")
        actions = ActionChains(self.driver)
        actions.pause(0.5)
        for i in range(num_of_projects):
            editButtons[i].click()
            actions.perform()
            self.driver.find_element_by_link_text("Delete").click()
            alert = self.driver.switch_to.alert
            alert.accept()
            actions.perform()

    def add_projects(self, Projects):
        actions = ActionChains(self.driver)
        actions.pause(0.5)
        for project in Projects:
            startMonth = project.start_date.split("/")[0]
            startYear = project.start_date.split("/")[2]
            self.driver.find_element_by_name("project[title]").send_keys(project.title)
            actions.perform()
            self.driver.find_element_by_xpath("//a[@class='c-button c-button--blue js-submit']").click()
            actions.send_keys(project.summary, Keys.TAB)
            actions.send_keys(project.link, Keys.TAB)
            actions.send_keys(project.description, Keys.TAB)
            actions.send_keys(project.organization, Keys.TAB)
            actions.send_keys(Keys.TAB)
            for _ in range(2019 - int(startYear)):
                actions.send_keys(Keys.ARROW_DOWN)
            actions.send_keys(Keys.TAB)
            for _ in range(int(startMonth)):
                actions.send_keys(Keys.ARROW_DOWN)
            actions.send_keys(Keys.TAB)
            if not project.currentWorking:
                endMonth = project.end_date.split("/")[0]
                endYear = project.end_date.split("/")[2]
                for _ in range(2019 - int(endYear)):
                    actions.send_keys(Keys.ARROW_DOWN)
                actions.send_keys(Keys.TAB)
                for _ in range(int(endMonth)):
                    actions.send_keys(Keys.ARROW_DOWN)
            actions.send_keys(Keys.TAB)
            actions.send_keys(project.role)
            for _ in range(4):
                actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.ENTER)
            actions.perform()

    def change_profile(self, profile):
        self.driver.find_element_by_xpath("//a[@class='js-add-headline s-vgPadRight1 no-deco']").click()
        elem = self.driver.find_element_by_name("user[name]")
        elem.clear()
        elem.send_keys(profile["first_name"] + " " + profile["last_name"])
        elem = self.driver.find_element_by_id("profiles_show_header_bio_autocomplete")
        elem.clear()
        elem.send_keys(profile["description"])
        self.driver.find_element_by_xpath("//a[@class='c-button c-button--blue u-floatLeftSmOnly save_link']").click()

    def modify(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://angel.co/login")
        self.login(self.username, self.password)
        self.driver.get("https://angel.co/chaoqun-tao")
        actions = ActionChains(self.driver)
        actions.pause(0.5)
        actions.perform()

        self.change_profile(self.profile)
        actions.perform()
        self.delete_experiences(self.profile["number_of_experiences"])
        actions.perform()
        self.add_experiences_first(self.experiences)
        self.delete_projects(self.profile['number_of_projects'])
        self.add_projects(self.projects)
        self.driver.refresh()
        self.add_experience_second(self.experiences)
        self.driver.close()
