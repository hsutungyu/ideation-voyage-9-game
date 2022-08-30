    # def drawHorizontalRectanglesWithTexts(self, x, y, height, separation, s_list):
    #     # find the top left corner of each rectangle
    #     pos = list()
    #     pos.append((x, y))
    #     text_rect_list = list()
    #     for i in range(1, len(s_list)):
    #         text_width, _ = self.font.size(s_list[i - 1])
    #         pos.append((pos[i - 1][0] + separation + max(text_width + 40, 100), y))
    #     for i in range(len(s_list)):
    #         text_rect_list.append(self.drawRectangle(pos[i][0], pos[i][1], height, s_list[i]))
    #     return text_rect_list
    
    
    # # TODO: make an image inside the rectangle
    # def drawRectangle(self, x, y, height, s):
    #     text_width, text_height = self.font.size(s)
    #     text_rect = pygame.draw.rect(self.screen, (0, 0, 0), (x, y, max(text_width + 40, 100), max(text_height, height)), 1)
    #     text = self.font.render(s, True, (0, 0, 0))
    #     self.screen.blit(text, (x + 20, text_rect.centery - 15))
    #     return text_rect