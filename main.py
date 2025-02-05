from string import ascii_lowercase
import random
import numpy as np 

from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

class Menu(MDScreen):
    pass                    

class Gerador(MDScreen):
    def gerar_texto(self):
        texto_gerado = ''.join(random.choice(ascii_lowercase) for i in range(5000))
        self.ids.texto_gerado.text = texto_gerado
#aumentar para 1 milhao de caracteres numa tela com scrollview
#adicionar ferramenta de pesquisa para o texto gigante

class Calculadora(MDScreen): 
    
    def calcular_tempo_maximo(self, texto):
        combinacoes = 27**len(texto) #os únicos caracteres que contam no cálculo são o espaço e as letras (eu considero que o texto é o mesmo estando maiúsculas ou não, pois nesse contexto não é relevante, ao contrário de um algorítmo de força bruta, por exemplo)
        tempo_segundos = combinacoes / 2
    
        anos = (tempo_segundos // (24 * 3600) // 365) 
        dias = (tempo_segundos // (24 * 3600)) % 365
        horas = (tempo_segundos % (24 * 3600)) // 3600
        minutos = (tempo_segundos % 3600) // 60
        segundos = tempo_segundos % 60

        self.ids.resultado.text = (
            f"Considerando que um macaco escreveria 2 teclas por segundo, seriam necessários {int(anos)} anos, {int(dias)} dias, {int(horas)} horas, {int(minutos)} minutos, {int(segundos)} segundos" 
        ) #colocar em destaque o tempo
#limitar para apenas letras de preferencia minusculas e espaço. separar os anos por pontos e adicionar texto de quanto tempo seria com exemplos de tempo; vida do universo
    
class CanvasScreen (MDScreen):
    pass
class CanvasImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gerar_textura()

#lendo o doc do kivy descobri que a classe texture de kivy possui o método texture.create que pede apenas a resolução
#porém, ele apenas gera uma textura sem nenhum valor embutido
#para gerar a imagem é necessário gerar os valores do buffer
    def gerar_textura(self):
        largura, altura = 1000, 1000
        total_pixels = largura * altura 

        pixels = np.random.randint(0, 255, (total_pixels, 3), dtype=np.uint8) #escolhe 3 vezes um valor aleatório entre 0 e 255 
        #o numpy foi necessário para criar um array de arrays, criando uma matriz de 3 x 1.000.000 com os valores aleatórios
        #np.int8 garante que a informação ocupe 8 bits na memória

        pixel_rgb = pixels.tobytes() #a função .tobytes converte a matriz em um array de bytes para que o blit_buffer funcione
        #exemplo dos códigos gerados numa imagem 3x3: \xac\xba\xde\xe7\x8c>\xa8\x13\xded\x8c

        texture = Texture.create(size=(largura, altura))
        texture.blit_buffer(pixel_rgb) #interpreta cada elemento de pixel_rgb como um pixel para a formação da textura
        #tem os parametros colorfmt, padrão rgb e bufferfmt, padrão ubyte

        self.texture = texture

    #adicionar botão de baixar a imagem

class Help (MDScreen):
    pass
    #a tela ainda não foi feita mas será dedica a explicar as 3 funções e o objetivo do aplicativo

class Infinite(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return ScreenManager()
    #melhorar o design do app   

    
    def regen(self):

        canvas_screen = self.root.get_screen("canvas")
        canvas_image = canvas_screen.ids.canvas_image
 
    
if __name__ == '__main__':
    Infinite().run()