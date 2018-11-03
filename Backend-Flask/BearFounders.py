from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from .User import *

# me = UserProfile("adamtao@berkeley.edu", p, 1, "Chaoqun", "Tao", description = "Hi there! I am a Berkeley EECS student graduating by May 2020. With my enthusiasm for Computer Science, I am thrilled to contribute to ideas that could make a difference. I am familiar with data structures, algorithms, and Artificial Intelligence. I am experienced in Python, Java, C, etc. Let me handle the technical side of your startup!")
# md = BearFounderModifier(me)
# md.modify()

class BearFounderModifier:

    def __init__(self, user):
        self.profile = user.profile
        self.username = user.bfemail
        self.password = user.bfpassword
        self.special_key = Keys.CONTROL

    def login(self, username, password):
        elem = self.driver.find_element_by_name("username")
        elem.clear()
        elem.send_keys(username)
        pw = self.driver.find_element_by_name("password")
        pw.clear()
        pw.send_keys(password)
        pw.submit()

    def delete_field(self, actions):
        actions.key_down(self.special_key)
        actions.send_keys("a")
        actions.key_up(self.special_key)
        actions.pause(10)
        actions.send_keys(Keys.DELETE)

    def modify(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://bearx.co/login/")
        self.login(self.username, self.password)
        self.driver.get("https://bearx.co/dashboard/edit/")
        self.driver.find_element_by_id("root")

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB, Keys.TAB, Keys.TAB)
        actions.send_keys(self.profile['first_name'])
        actions.send_keys(Keys.TAB)
        actions.send_keys(self.profile['last_name'])
        actions.send_keys(Keys.TAB)
        self.delete_field(actions)
        actions.send_keys(self.profile['description'])

        for _ in range(7):
            actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER)

        for _ in range(9):
            actions.send_keys(Keys.TAB)
            actions.pause(0.1)
        self.delete_field(actions)
        actions.send_keys(self.profile['courses'])
        actions.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB)
        if self.profile["experiences"] and self.profile["experiences"].links:
            actions.send_keys(self.profile["experiences"].links.personalWeb, Keys.TAB)
            actions.send_keys(self.profile["experiences"].links.linkedin, Keys.TAB)
            actions.send_keys(self.profile["experiences"].links.github, Keys.TAB)
            actions.send_keys(Keys.TAB)
            actions.send_keys(self.profile["experiences"].links.stackOverflow)
        else:
            actions.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB)

        for _ in range(7):
            actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER)

        for _ in range(19):
            actions.send_keys(Keys.TAB)
            actions.pause(0.1)
        actions.send_keys(Keys.ENTER)

        for _ in range(12):
            actions.send_keys(Keys.TAB)
            actions.pause(0.1)
        actions.send_keys(Keys.ENTER)

        actions.perform()
        self.driver.close()
