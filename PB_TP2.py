import pygame, psutil, platform, cpuinfo

CLOCK_TICK = 60

SCREEN = {
    'x': 1200,
    'y': 400
}

PRETO = (0,0,0)
BRANCO = (255,255,255)
ROXO = (128,0,128)
VIOLETA = (238,130,238)


# DESENHO E CONFIGURAÇÕES GERAIS
class Graph():

    def __init__(self, surface, title, x, y, largura, altura):
        self.surface = surface
        self.title = title
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.font = pygame.font.SysFont('Arial', 18)

    def draw(self, value):
        # BARRA TOTAL
        pygame.draw.rect(self.surface, VIOLETA, (self.x, self.y, self.largura, self.altura))
        # BARRA USO
        largura_value = self.largura*value/100
        pygame.draw.rect(self.surface, ROXO, (self.x, self.y, largura_value, self.altura))
        text = self.font.render(self.title, 1, BRANCO)
        self.surface.blit(text, (20, 10))
        

#TELA
tela = pygame.display.set_mode((SCREEN['x'], SCREEN['y']))
pygame.display.set_caption("Análise e Monitoramento de Computador - Mariana B. Sukevicz")
pygame.display.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 18)


#SUPERFÍCIES 
surfaces = [
    pygame.surface.Surface((SCREEN['x'], SCREEN['y']/4)),
    pygame.surface.Surface((SCREEN['x'], SCREEN['y']/4)),
    pygame.surface.Surface((SCREEN['x'], SCREEN['y']/4)),
    pygame.surface.Surface((SCREEN['x'], SCREEN['y']/4))
]


#DADOS REQUERIDOS
def get_cpu():
    return psutil.cpu_percent(interval=0)

def get_memoria():
    mem = psutil.virtual_memory()
    return mem.percent

def get_disco():
    disco =  psutil.disk_usage('.')
    return disco.percent

def get_ip():
    dic_interfaces = psutil.net_if_addrs()
    print(dic_interfaces)
    return f" ENDEREÇAMENTO IP: {dic_interfaces['Wi-Fi'][1].address}"

def draw_specs():
    graph1.draw(get_cpu())
    graph2.draw(get_memoria())
    graph3.draw(get_disco())

    ip_text = font.render(get_ip(), 1, BRANCO)
    surfaces[3].blit(ip_text, (20, 10))

    tela.blit(surfaces[0], (0, 0))
    tela.blit(surfaces[1], (0, SCREEN['y']/4))
    tela.blit(surfaces[2], (0, 2*SCREEN['y']/4))
    tela.blit(surfaces[3], (0, 3*SCREEN['y']/4))


# USO DAS SURFACES CRIADAS (TEXTO)
graph1 = Graph(surfaces[0], f"CPU (USO): {get_cpu():.2f}% - "
                            f"INF: {cpuinfo.get_cpu_info()['brand_raw'], platform.processor(), platform.node(), platform.system()}", 20, 25, SCREEN['x'] - 2 * 20, 50)
graph2 = Graph(surfaces[1], f"MEMÓRIA (USO): {get_memoria():.2f}%", 20, 25, SCREEN['x'] - 2 * 20, 50)
graph3 = Graph(surfaces[2], f"DISCO (USO): {get_disco():.2f}%", 20, 25, SCREEN['x'] - 2 * 20, 50)

#RELÓGIO
clock = pygame.time.Clock()

cont = 60

#EVENTO
terminou = False
while not terminou:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminou = True
            
    if cont == 60:
        draw_specs()
        cont = 0
    
    pygame.display.update()
    clock.tick(CLOCK_TICK)
    cont = cont + 1
      
pygame.display.quit()
