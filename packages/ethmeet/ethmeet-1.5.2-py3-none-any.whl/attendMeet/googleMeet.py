from time import sleep
import selenium.common.exceptions

from .attendMeet import AttendMeet

class GoogleMeet(AttendMeet):
    def __init__(self, **kwargs):
        """
        Parameters:\n
            kwargs['code'] (string): Meeting code\n
        """
        super().__init__(**kwargs)
        self.login_url = "google"

    def enter_class(self):
        try: self.driver.get(self.meet_url)
        except selenium.common.exceptions.InvalidArgumentException:
            print("ERROR ****** Meeting code was not properly set. Please, provide a valid one and try again! ******")
            self.driver.close()
        except selenium.common.exceptions.InvalidSessionIdException:
            return

        element = self.driver.find_element_by_class_name("uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt.M9Bg4d")
        element.click()
        return

    def doLogin(self):
        self.driver.get(self.login_url)

        #USER
        try:
            self.driver.find_element_by_id("identifierId").send_keys(self.login_data["user"])
            self.driver.find_element_by_id("identifierNext").click()
            try:
                if self.driver.find_element_by_class_name("o6cuMc"):
                    print("ERROR ****** Login failed. Check user and try again! ******")
                    self.driver.close()
                    return
            except selenium.common.exceptions.NoSuchElementException: pass
        except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.ElementClickInterceptedException):
            print("ERROR ****** Login failed. Check your connection and try again! ******")
            self.driver.close()
            return
            
        #PASSWORD
        for _ in range(15):
            try:
                self.driver.find_element_by_name("password").send_keys(self.login_data["passwd"])
                break
            except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.ElementNotInteractableException):
                sleep(1)
        try:
            self.driver.find_element_by_id("passwordNext").click()
            try:
                if self.driver.find_element_by_class_name("EjBTad"):
                    print("ERROR ****** Login failed. Check your password and try again! ******")
                    self.driver.close()
                    return
            except selenium.common.exceptions.NoSuchElementException: pass
        except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.ElementClickInterceptedException):
                print("ERROR ****** Login failed. Check your connection and try again! ******")
                self.driver.close()
                return

    def set_meeting_url(self, code):
        code_len = len(code)
        mCode = ""

        if type(code) != type(0) and ((code_len == 12 and code[3] == "-" and code[8] == "-") or code_len == 10):
            for crc in code:
                if type(crc) == type(0):
                    print("ERROR ****** Meeting code must not contain numbers! ******")
                else:
                    mCode = code
        else:
            print("ERROR ****** Meeting code not accepted! Please check again ******")

        if "https://meet.google.com/" in code:
            self.meet_url = code
        else:
            self.meet_url="https://meet.google.com/%s" % mCode
        return
