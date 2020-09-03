import requests
import time
from datetime import datetime
import json
import pygame
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

class Blockchain(object):
    def __init__(self):
        self.blocks = rpc_connection.getblockcount()
        self.mempool = rpc_connection.getmempoolinfo()
        self.mempool_transactions = rpc_connection.getmempoolinfo()['size']
        self.mempool_size = rpc_connection.getmempoolinfo()['bytes']
        self.bestblock = rpc_connection.getbestblockhash()


pygame.init()
white = (255, 255, 255)
red = (212, 34, 28)
black = (0, 0, 0)
green = (0, 255, 0) 
blue = (0, 0, 128) 
orange = (250, 186, 10)
#display_surface = pygame.display.set_mode((480, 320), pygame.FULLSCREEN) < - Uncomment to run on Pi
#pygame.mouse.set_visible(False) < - Uncomment to run on Pi
display_surface = pygame.display.set_mode((480, 320)) # < - comment out to run on Pi

pygame.display.set_caption('Bitcoin')
font_large = pygame.font.SysFont('calibri.ttf', 34)
font_small = pygame.font.SysFont('calibri.ttf', 20)

#Price 1
Price = font_large.render('Price (£):', True, white, black)
textRect_price = Price.get_rect()
textRect_price.center = (152, 40)

#Price 3
Price_image = pygame.image.load(r'/PATH/TO/bitcoin_1.png')
Price_image = pygame.transform.scale(Price_image, (45, 62))

#Block Height 1
Block_height = font_large.render('Block Height:', True, white, black)
textRect_block = Block_height.get_rect()
textRect_block.center = (178, 120)

#Block Height 3
Block_height_image = pygame.image.load(r'/PATH/TO/block_1.png')
Block_height_image = pygame.transform.scale(Block_height_image, (65, 55))

#mempool 1
Mempool = font_large.render('Mempool:', True, white, black)
textRect_mempool = Mempool.get_rect()
textRect_mempool.center = (158, 200)

#mempool 3
Mempool_image = pygame.image.load(r'/PATH/TO/mempool_1.png')
Mempool_image = pygame.transform.scale(Mempool_image, (65, 55))

#Halving 1
Halving = font_large.render('Time:', True, white, black)
textRect_halving = Halving.get_rect()
textRect_halving.center = (150, 280)

#Halving 3
Halving_image = pygame.image.load(r'/PATH/TO/halving_1.png')
Halving_image = pygame.transform.scale(Halving_image, (50, 50))
    

while True:
    for event in pygame.event.get(): 
	    if event.type == pygame.QUIT: 
		    pygame.quit() 
		    quit()
    
    try:
        r=requests.get('https://api.opennode.com/v1/rates')
        current_price = int(json.loads(r.text)["data"]['BTCGBP']['GBP'])
    except:
        current_price = 'unreachable'
    rpc_connection = AuthServiceProxy("http://%s:%s@MY_NODE_ADDRESS:8332"%('BITCOIN_NODE_ADMIN', 'BITCOIN_NODE_PASSWORD'),timeout=120)
    bitcoin = Blockchain() 

    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    #Price 2
    Price_live = font_large.render(str(current_price), True, white, black)
    textRect_price_live = Price_live.get_rect()
    textRect_price_live.center = (385, 40)

    #Block Height 2
    Block_height_live = font_large.render(str(bitcoin.blocks), True, white, black)
    textRect_block_live = Block_height_live.get_rect()
    textRect_block_live.center = (385, 120)

    #mempool 2
    if bitcoin.mempool_transactions > 20000:
        Mempool_live = font_large.render(str(bitcoin.mempool_transactions), True, red, black)
    elif bitcoin.mempool_transactions < 10000:
        Mempool_live = font_large.render(str(bitcoin.mempool_transactions), True, green, black)
    else:
        Mempool_live = font_large.render(str(bitcoin.mempool_transactions), True, orange, black)
    textRect_mempool_live = Mempool_live.get_rect()
    textRect_mempool_live.center = (385, 185)   

    MBs = str(round(bitcoin.mempool_size/1000000))+' Block(s)'
    Mempool_live_size = font_large.render(str(MBs), True, white, black)
    textRect_mempool_live_size = Mempool_live_size.get_rect()
    textRect_mempool_live_size.center = (385, 215)

    current_time = now.strftime("%H:%M")
    Current_time = font_large.render(str(current_time), True, white, black)
    Current_time_live = Current_time.get_rect()
    Current_time_live.center = (385, 295)

    display_surface.fill(black)
    display_surface.blit(Price, textRect_price)
    display_surface.blit(Price_live, textRect_price_live)
    display_surface.blit(Price_image, (15, 10))
    display_surface.blit(Block_height, textRect_block)
    display_surface.blit(Block_height_live, textRect_block_live)
    display_surface.blit(Block_height_image, (5, 90))
    
    display_surface.blit(Mempool, textRect_mempool)
    display_surface.blit(Mempool_live, textRect_mempool_live)
    display_surface.blit(Mempool_image, (5, 170))

    display_surface.blit(Mempool_live_size, textRect_mempool_live_size)
    display_surface.blit(Mempool_image, (5, 170))
        
    display_surface.blit(Current_time, Current_time_live)
    pygame.display.update()

    time.sleep(15)
