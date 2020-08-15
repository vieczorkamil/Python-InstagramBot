from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from login import *
import time
from datetime import datetime

class Bot():
    def __init__(self, LOGIN, PASSWORD):
        print("Instagram bot is runninig!")
        self.LOGIN = LOGIN
        self.driver = webdriver.Edge()
        self.driver.get('https://www.instagram.com/')
        time.sleep(3)
        userName = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        userName.send_keys(LOGIN)
        userPassword = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        userPassword.send_keys(PASSWORD)
        logginButtom = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
        logginButtom.click()
        time.sleep(3)
        #remember the password
        try:
            notNow = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
            notNow.click()
        except:
            pass
        time.sleep(3)
        #turn on notification
        try:
            notNow = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
            notNow.click()
        except:
            pass
        time.sleep(3)

    def __del__(self):
        self.driver.close()
        print("Browser closed successful!")

    def likeComment(self, tag, comment=''):
        search = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        search.send_keys('#' + tag)
        time.sleep(3)
        #search.send_keys(Keys.ENTER)
        searchbuttom = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]/div/a[1]/div')
        searchbuttom.click()
        time.sleep(3)
        photos = self.driver.find_elements_by_tag_name('a')
        photosList = []
        for photoLink in photos:
            if('.com/p/' in photoLink.get_attribute('href')) == True:
                photosList.append(photoLink.get_attribute('href'))
        for photo in photosList:
            try:
                self.driver.get(photo)
                like = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button')
                like.click()
                if comment != '':
                    try:
                        sendComment = self.driver.find_element_by_class_name('X7cDz')
                        sendComment.click()
                        time.sleep(1)
                        sendComment = self.driver.find_element_by_class_name('Ypffh')
                        sendComment.clear()
                        sendComment.send_keys(comment)
                        sendComment.send_keys(Keys.ENTER)
                    except:
                        print("Adding comment failed")
                time.sleep(3)
            except:
                print("Link invalid")
        
    def getFollowersList(self):
        followers = self.driver.find_element_by_class_name('gmFkV')
        followers.click()
        time.sleep(3)
        #number of followers
        followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
        #show list of followers
        myFollowers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        myFollowers.click()
        time.sleep(3)

        myFollowersList = []
        for i in range (1, int(followers.text)+1):
            myFollowers = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li['+str(i)+']')
            scroll = self.driver.execute_script("arguments[0].scrollIntoView();", myFollowers)
            myFollowersName = myFollowers.text.partition('\n')[0]
            print(str(i)+") "+myFollowersName)
            myFollowersList.append(myFollowersName)
            time.sleep(0.5) #to ensure page loading
        print("Number of followers : "+followers.text)
        
        file = open(self.LOGIN+"-FollowersList.txt","w")
        for name in myFollowersList:
            file.write(name)
            file.write("\n")
        file.close()

        return myFollowersList

    def Unfollowers(self):
        #load last follower list check
        try:
            check = []
            readFile = open(self.LOGIN+"-FollowersList.txt", "r")
            readFileStatus = True
            for name in readFile:
                check.append(name.rstrip("\n"))
        except :
            print("Can not load file")
            readFileStatus = False
        print("Checking new unfollowers")
        #update follower list
        lastList = self.getFollowersList()
        unfollowersList = []
        unfollowerFile = open(self.LOGIN+"-UnfollowersList.txt","a")
        unfollowerFile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        for unfollower in check:
            if unfollower not in lastList:
                unfollowersList.append(unfollower)
                unfollowerFile.write(unfollower)
                unfollowerFile.write("\n")
                print(unfollower)
        if not unfollowersList:
            unfollowerFile.write("No new unfollowers!\n")
            print("No new unfollowers!")
        if readFileStatus == True:
            readFile.close()
        unfollowerFile.close()

    def getFollowingList(self):
        following = self.driver.find_element_by_class_name('gmFkV')
        following.click()
        time.sleep(3)
        #number of following accounts
        following = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span')
        #show list of following accounts
        myFollowing = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
        myFollowing.click()
        time.sleep(3)
        ###
        myFollowingList = []
        for i in range (1, int(following.text)+1):
            myFollowing = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li['+str(i)+']')
            scroll = self.driver.execute_script("arguments[0].scrollIntoView();", myFollowing)
            myFollowingName = myFollowing.text.partition('\n')[0]
            print(str(i)+") "+myFollowingName)
            myFollowingList.append(myFollowingName)
            time.sleep(0.5) #to ensure page loading
        print("Number of following accounts : "+following.text)
        
        file = open(self.LOGIN+"-FollowingList.txt","w")
        for name in myFollowingList:
            file.write(name)
            file.write("\n")
        file.close()

        return myFollowingList

    def DontFollowBack(self):
        pass
def main():
    instaBot = Bot(MY_LOGIN, MY_PASSWORD)
    #instaBot.getFollowersList()
    #instaBot.Unfollowers()
    #instaBot.likeComment('python','<3')
    instaBot.getFollowingList()

if __name__ == '__main__':
    main()
