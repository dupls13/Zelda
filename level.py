import pygame 
from settings import *
from random import choice 

from tile import Tile 
from player import Player
from support import *
from weapon import Weapon




class Level:
    def __init__(self):

        #get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup 
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup 
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv')
        }
        graphics = {
            'grass': import_folder('graphics/Grass'),
            'objects': import_folder('graphics/objects')
        }
        print(graphics)

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for column_index, column in enumerate(row):
                    if column != '-1':
                        x = column_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'object':
                            surface = graphics['objects'][int(column)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)



        # looks at each value in world map 
        """ for row_index, row in enumerate(WORLD_MAP):
            for column_index, column in enumerate(row):
                x = column_index * TILESIZE
                y = row_index * TILESIZE

                # replaces each x with rock
                if column == 'x':
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites])

                if column == 'p':
                    self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites """

        self.player = Player((2000,1430), [self.visible_sprites], self.obstacle_sprites, self.create_attack)

    def create_attack(self):
        Weapon(self.player, [self.visible_sprites])



    def run(self):
        #update and draw the game 
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup 
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()


        # creating the floor 
        self.floor_surface = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

    def custom_draw(self, player):

        #getting the offset 
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height


        # drawing the floow 
        floor_offset_pos = self.floor_rect.topleft - self.offset 
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset 
            self.display_surface.blit(sprite.image, offset_pos)
