import sys
import random
import pygame
from pygame.locals import *

import utility

from button import Button
from business import Business
from account import Account
from household import HouseholdItem
from mission import Mission
from random_event import RandomEvent

# 1) a few household expense automatically deducted every week
# - a button to go through each week as simulation
# - sections that represent different household expense
# 2) predefined invested businesses w/ random gain/loss function as simulation
# 3) a few random events that happens every time a week passed
# 4) a table summary for all the gain and loss and overall profit/loss
# every week

# flow:
# a main screen
# a static page showing the household expense and investment
# a button to simulate passing a week IRL
# - shows the gain/loss of each investment
# - shows a table summary for all the gain and loss
# - shows a random event that influences the gain and loss next week
# - shows the screen for children to make decisions (good or bad)

# logic:
# 1) usual gameplay: normal money, never going to overdraft
# 2) bad gameplay: overdraft by making bad decisions (e.g., bad budgetting)

# fall back plan:
# if I cannot do this, then just draw the interface

SIZE = WIDTH, HEIGHT = (311, 655)
MAIN_BG = pygame.image.load("assets/main_background.jpeg")
HOUSEHOLD_BG = pygame.image.load("assets/background.jpeg")
BUSINESS_BG = pygame.image.load("assets/business_background.jpeg")


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Kid's Pay Simulation Prototype")
        self.font = pygame.font.Font('assets/Arvo/Arvo-Regular.ttf', 25)
        self.font_medium = pygame.font.Font('assets/Arvo/Arvo-Regular.ttf', 20)
        self.font_small = pygame.font.Font('assets/Arvo/Arvo-Regular.ttf', 15)
        self.font_very_small = pygame.font.Font('assets/Arvo/Arvo-Regular.ttf',
                                                10)
        self.screen = pygame.display.set_mode(SIZE)
        self.background_colour = (255, 255, 255)
        self.screen.fill(self.background_colour)

        self.mission = list()
        # create a mission
        # in the real game, more missions would be created for the children to follow and learn
        mission1_description = """It's summer time! That means the electricity 
                                usage would be higher! What would you do to this month's budget?"""
        mission1 = Mission(
            "Summer Time", mission1_description,
            "Allocate more money to this month's budget",
            "Ignore it, I trust that I would have enough money to pay the bill later"
        )
        self.mission.append(mission1)
        self.random_event = list()
        random_event1_description = """A food in your convenience store becomes viral on social media!"""
        random_event1 = RandomEvent("Foodie", random_event1_description, 0.10,
                                    "Convenience Store")
        self.random_event.append(random_event1)
        pygame.display.update()

    def quit(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            print("Exit")
            sys.exit()

    # function to draw a button with the top left corner at (x, y) with the string s inside
    # return the button object drawn
    def drawButton(self,
                   image,
                   pos,
                   text_input,
                   font,
                   base_color=(0, 0, 0),
                   hovering_color=(51, 153, 255),
                   multiline=False):
        button_ = Button(image, pos, text_input, font, base_color,
                         hovering_color, multiline)
        button_.update(game.screen)
        return button_

    # function to draw multiple buttons horizontally
    # with the top left corner of the first button at (x, y)
    # each button separated by separation, and with text in s_list appearing in order
    # return a list of button objects drawn
    def drawHorizontalButtonsWithTexts(self, x, y, separation, image_list,
                                       s_list):
        # find the top left corner of each rectangle
        pos = list()
        pos.append((x, y))
        button_list = list()
        for i in range(1, len(s_list)):
            text_width, _ = self.font.size(s_list[i - 1])
            pos.append(
                (pos[i - 1][0] + separation + max(text_width + 40, 100), y))
        for i in range(len(s_list)):
            if not image_list:
                image = None
            else:
                image = pygame.image.load(image_list[i]).convert_alpha()
            button_list.append(
                self.drawButton(image=image,
                                pos=pos[i],
                                text_input=s_list[i],
                                font=self.font))
        return button_list

    def drawCurrencies(self):
        # buttons for showing the in-game currencies
        currencies = [str(account.currency[0]), str(account.currency[1])]
        # currencies_image = [
        #     "assets/normal_currency.png", "assets/premium_currency.png"
        # ]
        # currencies_button_list = game.drawHorizontalButtonsWithTexts(
        #     157, 30, 5, currencies_image, currencies)
        self.drawButton(image=pygame.image.load("assets/normal_currency.png"),
                        pos=(157, 30),
                        text_input="",
                        font=self.font)
        normal_currency_button = self.drawButton(image=None,
                                                 pos=(199, 30),
                                                 text_input=currencies[0],
                                                 font=self.font_small)
        self.drawButton(image=pygame.image.load("assets/premium_currency.png"),
                        pos=(245, 30),
                        text_input="",
                        font=self.font)
        premium_currency_button = self.drawButton(image=None,
                                                  pos=(287, 30),
                                                  text_input=currencies[1],
                                                  font=self.font_small)
        currencies_button_list = [
            normal_currency_button, premium_currency_button
        ]
        return currencies_button_list

    def drawBackButton(self):
        return self.drawButton(image=None,
                               pos=(WIDTH // 2, 629),
                               text_input="Back",
                               font=self.font_small)

    # draw the bottom menu
    # return a list containing the three drawn buttons
    def drawBottomMenu(self):
        game_button = game.drawButton(image=None,
                                      pos=(50, 630),
                                      text_input="game",
                                      font=self.font_small,
                                      base_color=(255, 0, 0))
        pay_button = game.drawButton(image=None,
                                     pos=(156, 630),
                                     text_input="pay",
                                     font=self.font_small,
                                     base_color=(255, 0, 0))
        gift_button = game.drawButton(image=None,
                                      pos=(261, 630),
                                      text_input="gifts",
                                      font=self.font_small,
                                      base_color=(255, 0, 0))
        return [game_button, pay_button, gift_button]

    # draw the weekly report
    # return the overall change of this week for use of weekly progress
    def drawReport(self):
        SEP = 30
        self.drawButton(image=None,
                        pos=(WIDTH // 2, 90),
                        text_input="Weekly Report",
                        font=self.font)
        # draw the business investments details
        self.drawButton(image=None,
                        pos=(WIDTH // 2, 130),
                        text_input="Business",
                        font=self.font_medium)
        for i, item in enumerate(account.business_investments):
            self.drawButton(image=None,
                            pos=(WIDTH // 2, 170 -
                                 (len(account.business_investments) + i) +
                                 (2 * i + 0) * SEP),
                            text_input=item.name,
                            font=self.font_small)
            self.drawButton(image=None,
                            pos=(WIDTH // 2, 170 -
                                 (len(account.business_investments) + i) +
                                 (2 * i + 1) * SEP),
                            text_input=item.getPriceReport(),
                            font=self.font_small)
            # store the height of the last button
            if i == len(account.business_investments) - 1:
                lastHeight = 170 - (len(account.business_investments) +
                                    i) + (2 * i + 1) * SEP
        # draw the household expenses details
        self.drawButton(image=None,
                        pos=(WIDTH // 2, lastHeight + 40),
                        text_input="Household",
                        font=self.font_medium)
        for i, item in enumerate(account.household_items):
            self.drawButton(
                image=None,
                pos=(WIDTH // 2, lastHeight + 80 -
                     (len(account.household_items) + i) + (2 * i + 0) * SEP),
                text_input=item.name,
                font=self.font_small)
            self.drawButton(
                image=None,
                pos=(WIDTH // 2, lastHeight + 80 -
                     (len(account.household_items) + i) + (2 * i + 1) * SEP),
                text_input=str(item.weekly_fee),
                font=self.font_small)
            # store the height of the last button
            if i == len(account.household_items) - 1:
                lastHeight = lastHeight + 80 - (len(account.household_items) +
                                                i) + (2 * i + 1) * SEP
        # draw the overall change of this week
        self.drawButton(image=None,
                        pos=(WIDTH // 2, lastHeight + 40),
                        text_input="Overall Change",
                        font=self.font_medium)
        businessTotalChange = sum(item.getPriceDifference()
                                  for item in account.business_investments)
        householdTotalCost = sum(item.weekly_fee
                                 for item in account.household_items)
        overallChange = round(businessTotalChange - householdTotalCost)
        self.drawButton(image=None,
                        pos=(WIDTH // 2, lastHeight + 80),
                        text_input=str(overallChange),
                        font=self.font_small)
        return overallChange

    # the main menu game loop
    def main_menu(self):
        while True:
            self.screen.fill(self.background_colour)
            self.screen.blit(MAIN_BG, (0, 0))
            # buttons for showing the in-game currencies
            currencies_button_list = self.drawCurrencies()
            # button for simulating the pass of a week IRL
            weekly_progress_button = game.drawButton(image=None,
                                                     pos=(254, 576),
                                                     text_input="next week",
                                                     font=self.font_small,
                                                     base_color=(102, 153,
                                                                 153))
            household_button = game.drawButton(image=pygame.image.load(
                "assets/main_background_household.jpeg"),
                pos=(151, 408),
                text_input="",
                font=self.font_small)
            game.drawButton(image=None,
                            pos=(151, 298),
                            text_input="Press to visit home",
                            font=self.font_small)
            # button for showing the business investment portion of the game
            business_button = game.drawButton(image=pygame.transform.flip(
                pygame.image.load("assets/car_75h.png").convert_alpha(), True,
                False),
                pos=(85, 540),
                text_input="",
                font=self.font_small)
            game.drawButton(image=None,
                            pos=(85, 586),
                            text_input="Visit Business Area",
                            font=self.font_small)
            # button for showing the weekly report of the last week
            report_button = game.drawButton(image=pygame.image.load(
                "assets/report_icon_20h.png").convert_alpha(),
                pos=(283, 246),
                text_input="",
                font=self.font_small)
            game.drawButton(image=None,
                            pos=(283, 261),
                            text_input="report",
                            font=self.font_small)
            # button for showing the leaderboard of the game
            leaderboard_button = game.drawButton(image=pygame.image.load(
                "assets/leaderboard_20h.png").convert_alpha(),
                pos=(283, 296),
                text_input="",
                font=self.font_small)
            game.drawButton(image=None,
                            pos=(283, 306),
                            text_input="rank",
                            font=self.font_small)
            game_button, pay_button, gift_button = self.drawBottomMenu()
            for event in pygame.event.get():
                game.quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for i in range(len(currencies_button_list)):
                        if currencies_button_list[i].checkForInput(pos):
                            account.currency[i] += 100
                    if weekly_progress_button.checkForInput(pos):
                        self.weekly_progress()
                    if household_button.checkForInput(pos):
                        self.household()
                    if business_button.checkForInput(pos):
                        self.business()
                    if report_button.checkForInput(pos):
                        self.report()
                    if leaderboard_button.checkForInput(pos):
                        self.leaderboard()
                    if pay_button.checkForInput(pos):
                        self.epayment()
                    if gift_button.checkForInput(pos):
                        self.gift()
            pygame.display.update()

    # the weekly progress game loop
    def weekly_progress(self):
        # fast forward one week IRL to trigger weekly actions
        # 1) randomly change the current price of the businesses
        #    store the result in a list
        business_list = list()
        for item in account.business_investments:
            item.setCurrentPrice()
            business_list.append(str(item))
        print(business_list)
        # 2) trigger a random event that children would need to make decisions
        #    randomly choose one random event from the random event list
        random_event = random.choice(self.random_event)
        for item in account.business_investments:
            if item.name == random_event.business:
                item.current_price *= 1 + random_event.action
                item.current_price = round(item.current_price, 2)
        # 2.1) show the random event
        random_event_toggle = True
        SEP = 40
        while True:
            if not random_event_toggle:
                break
            self.screen.fill((255, 255, 153))
            self.drawCurrencies()
            self.drawButton(image=None,
                            pos=(WIDTH // 2, HEIGHT // 2 - 2 * SEP),
                            text_input=random_event.business,
                            font=self.font)
            self.drawButton(image=None,
                            pos=(WIDTH // 2, HEIGHT // 2 - 1 * SEP),
                            text_input=random_event.name,
                            font=self.font_medium)
            utility.blit_text(self.screen, [random_event.description],
                              (20, HEIGHT // 2), self.font_medium)
            self.drawButton(image=None,
                            pos=(WIDTH // 2, HEIGHT // 2 + 3 * SEP),
                            text_input=f"+{random_event.action:.0%} revenue!",
                            font=self.font_medium)
            continue_button = self.drawButton(image=None,
                                              pos=(WIDTH // 2, 629),
                                              text_input="Continue",
                                              font=self.font_small)
            for event in pygame.event.get():
                game.quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if continue_button.checkForInput(pos):
                        random_event_toggle = not random_event_toggle
            pygame.display.update()

        # 3) trigger a report showing the gain and loss of this week
        while True:
            self.screen.fill((255, 255, 153))
            self.drawCurrencies()
            overallChange = self.drawReport()
            back_button = self.drawBackButton()
            for event in pygame.event.get():
                game.quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if back_button.checkForInput(pos):
                        account.currency[0] += overallChange
                        game.main_menu()
            pygame.display.update()

    # the household game loop
    def household(self):
        dog_button_toogle = False
        air_con_button_toogle = False
        computer_button_toogle = False
        while True:
            self.screen.fill(self.background_colour)
            self.screen.blit(HOUSEHOLD_BG, (0, 0))
            # buttons for showing the in-game currencies
            currencies_button_list = self.drawCurrencies()
            dog_button = self.drawButton(
                image=pygame.image.load("assets/dog.png").convert_alpha(),
                pos=(80, 520),
                text_input="",
                font=self.font)
            if dog_button_toogle:
                self.drawButton(image=pygame.image.load(
                    "assets/dialog_100h.png").convert_alpha(),
                    pos=(110, 450),
                    text_input="keep a dog?  ",
                    font=self.font_very_small)
            air_con_button = self.drawButton(image=pygame.image.load(
                "assets/air_con_150h.png").convert_alpha(),
                pos=(238, 222),
                text_input="",
                font=self.font)
            if air_con_button_toogle:
                self.drawButton(image=pygame.image.load(
                    "assets/dialog_100h.png").convert_alpha(),
                    pos=(238, 170),
                    text_input="50/week",
                    font=self.font_very_small)
            computer_button = self.drawButton(image=pygame.image.load(
                "assets/computer_200h.png").convert_alpha(),
                pos=(220, 430),
                text_input="",
                font=self.font)
            if computer_button_toogle:
                self.drawButton(image=pygame.image.load(
                    "assets/dialog_100h.png").convert_alpha(),
                    pos=(220, 400),
                    text_input="10/week",
                    font=self.font_very_small)
            back_button = self.drawBackButton()
            pygame.display.update()
            for event in pygame.event.get():
                game.quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if back_button.checkForInput(pos):
                        game.main_menu()
                    if computer_button.checkForInput(pos):
                        computer_button_toogle = not computer_button_toogle
                    if air_con_button.checkForInput(pos):
                        air_con_button_toogle = not air_con_button_toogle
                    if dog_button.checkForInput(pos):
                        dog_button_toogle = not dog_button_toogle

    # the business game loop
    def business(self):
        convenience_store_button_toggle = False
        while True:
            self.screen.fill(self.background_colour)
            self.screen.blit(BUSINESS_BG, (0, 0))
            # buttons for showing the in-game currencies
            currencies_button_list = self.drawCurrencies()
            character_button = self.drawButton(image=pygame.image.load(
                "assets/boss_baby_100h.png").convert_alpha(),
                pos=(97, 502),
                text_input="",
                font=self.font_small)
            convenience_store_button = self.drawButton(image=pygame.image.load(
                "assets/business_background_store.jpg"),
                pos=(163, 277),
                text_input="",
                font=self.font_small)
            if convenience_store_button_toggle:
                self.drawButton(pygame.image.load(
                    "assets/dialog_100h.png").convert_alpha(),
                    pos=(163, 180),
                    text_input="buy 7-11?     ",
                    font=self.font_very_small)
            self.drawButton(image=pygame.image.load(
                "assets/input_joystick_1_100h.png").convert_alpha(), pos=(237, 507), text_input="", font=self.font)
            back_button = self.drawBackButton()
            pygame.display.update()
            for event in pygame.event.get():
                game.quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if back_button.checkForInput(pos):
                        game.main_menu()
                    if convenience_store_button.checkForInput(pos):
                        convenience_store_button_toggle = not convenience_store_button_toggle

    # the report game loop
    def report(self):
        while True:
            self.screen.fill((204, 204, 255))
            self.drawCurrencies()
            self.drawReport()
            back_button = self.drawBackButton()
            for event in pygame.event.get():
                game.quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if back_button.checkForInput(pos):
                        game.main_menu()
            pygame.display.update()

    # the leaderboard game loop
    def leaderboard(self):
        while True:
            self.screen.fill((255, 153, 204))
            self.drawButton(image=None,
                            pos=(155, 328),
                            text_input="show the leaderboard",
                            font=self.font)
            back_button = self.drawBackButton()
            for event in pygame.event.get():
                self.quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if back_button.checkForInput(pos):
                        self.main_menu()
            pygame.display.update()

    # e-payment portion of app
    def epayment(self):
        while True:
            self.screen.fill((255, 255, 255))
            self.drawButton(
                image=pygame.image.load("assets/hsbc_debit_card.jpg"),
                pos=(WIDTH // 2, HEIGHT // 2 - 100),
                text_input="",
                font=self.font)
            self.drawButton(image=None,
                            pos=(WIDTH // 2, HEIGHT // 2 + 90),
                            text_input="Weekly Budget: $500",
                            font=self.font_small)
            self.drawButton(image=None,
                            pos=(WIDTH // 2, HEIGHT // 2 + 120),
                            text_input="You spent $300 this week",
                            font=self.font_small)
            self.drawButton(image=None,
                            pos=(WIDTH // 2 - 85, HEIGHT // 2 + 150),
                            text_input="You will receive",
                            font=self.font_small)
            self.drawButton(image=pygame.image.load("assets/premium_currency.png").convert_alpha(),
                            pos=(152, 478),
                            text_input="",
                            font=self.font)
            self.drawButton(image=None,
                            pos=(207, HEIGHT // 2 + 150),
                            text_input="200 and",
                            font=self.font_small)
            self.drawButton(image=pygame.image.load("assets/gift_30h.png").convert_alpha(),
                            pos=(254, HEIGHT // 2 + 150),
                            text_input="",
                            font=self.font)
            self.drawButton(image=None,
                            pos=(284, HEIGHT // 2 + 150),
                            text_input="20",
                            font=self.font_small)
            self.drawButton(image=None,
                            pos=(WIDTH // 2, HEIGHT // 2 + 180),
                            text_input="if you save the remaining budget!",
                            font=self.font_small)
            self.drawButton(image=None,
                            pos=(WIDTH // 2, HEIGHT // 2 + 220),
                            text_input="Check the Spending Details",
                            font=self.font_medium,
                            base_color=(0, 64, 255))

            game_button, pay_button, gift_button = self.drawBottomMenu()
            for event in pygame.event.get():
                self.quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if game_button.checkForInput(pos):
                        self.main_menu()
                    if gift_button.checkForInput(pos):
                        self.gift()
            pygame.display.update()

    # gift portion of app
    def gift(self):
        # draw
        # position is the middle pixel of the picture of the gift
        # the picture should have a height of 50px
        def drawGiftIconPoint(position, picture_path, point):
            """
            draw a picture of the gift as well as the required point
            with the middle of the picture at position
            picture_path: relative path to the gift picture
            point: the amount of point needed to redeem the gift

            return the button of the gift picture
            """
            gift_button = self.drawButton(image=pygame.image.load(picture_path).convert_alpha(),
                                          pos=position,
                                          text_input="",
                                          font=self.font)
            self.drawButton(image=pygame.image.load("assets/gift_30h.png").convert_alpha(),
                            pos=(position[0] - 20, position[1] + 80),
                            text_input="",
                            font=self.font)
            self.drawButton(image=None,
                            pos=(position[0] + 20, position[1] + 80),
                            text_input=str(point),
                            font=self.font_small)
            return gift_button
        while True:
            self.screen.fill((255, 255, 255))
            self.drawButton(image=pygame.image.load("assets/gift_30h.png"),
                            pos=(245, 30),
                            text_input="",
                            font=self.font)
            self.drawButton(image=None,
                            pos=(275, 30),
                            text_input="40",
                            font=self.font_small)
            pencil_case_button = drawGiftIconPoint(
                (78, 132), "assets/gift/pencil_case_100h.png", 100)
            robot_button = drawGiftIconPoint(
                (237, 132), "assets/gift/robot_100h.png", 2000)
            game_button, pay_button, gift_button = self.drawBottomMenu()
            for event in pygame.event.get():
                self.quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if game_button.checkForInput(pos):
                        self.main_menu()
                    if pay_button.checkForInput(pos):
                        self.epayment()
            pygame.display.update()


if __name__ == "__main__":
    account = Account(10000, 1200)
    game = Game()
    # add some business investments
    # in the finished game, this will be handled autonomously by the children
    account.addBusiness("Convenience Store", 1000, 1000, 0.05)
    account.addBusiness("Tuck Shop", 300, 300, 0.03)
    # add some household items
    # in the finished game, this will be done by missions
    account.addHouseholdItem("Air Conditioner", 50, "assets/air_con.png")
    account.addHouseholdItem("Personal Computer", 10, "assets/pc.png")
    account.addHouseholdItem("Pet", 40, "assets/dog.png")
    game.main_menu()
