from string import ascii_lowercase
import random
import numpy as np 

from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.core.window import Window

class Menu(MDScreen):
    pass                    

class Gerador(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.texto_gerado = "Clique no botão para gerar o seu texto aleatório."

    def gerar_texto(self):
        self.texto_gerado = ''.join(random.choice(ascii_lowercase) for i in range(25000))
        self.ids.label_gerado.text = self.texto_gerado

    def ctrl_F(self, search):
        fsearch = search
        search = search.replace(" ", "")
        if self.texto_gerado == "Clique no botão para gerar o seu texto aleatório.":
            self.ids.label_gerado.text = self.texto_gerado
            self.ids.search_field.helper_text = "Gere um texto antes de tentar encontrar."
            self.ids.search_field.helper_text_mode = "on_error"
            return

        if not search:
            self.ids.label_gerado.text = self.texto_gerado
            self.ids.search_field.helper_text = ""
        else:

            if search in self.texto_gerado:

                texto_encontrado = self.texto_gerado.replace(search, f"[b][color=#FF7500]{fsearch}[/color][/b]")
                self.ids.label_gerado.text = texto_encontrado
                self.ids.search_field.helper_text = "" #quantos textos foram encontradosV2

            else:
                self.ids.label_gerado.text = self.texto_gerado
                self.ids.search_field.helper_text = "0 resultados encontrados."
                self.ids.search_field.helper_text_mode = "on_error"
        
class Calculadora(MDScreen): 
    
    def calcular_tempo_maximo(self, texto):
        textolower = "".join(c for c in texto if c in (ascii_lowercase + " "))
                
        combinacoes = 27**len(textolower) #os únicos caracteres que contam no cálculo são o espaço e as letras 
        #(eu considero que o texto é o mesmo estando maiúsculas ou não, pois nesse contexto não é relevante, ao contrário de um algorítmo de força bruta, por exemplo)
        tempo_segundos = combinacoes / 2
    
        anos = (tempo_segundos // (24 * 3600) // 365) 
        dias = (tempo_segundos // (24 * 3600)) % 365
        horas = (tempo_segundos % (24 * 3600)) // 3600
        minutos = (tempo_segundos % 3600) // 60
        segundos = tempo_segundos % 60

        anos_str = "{:,}".format(int(anos)).replace(",", ".") if anos > 999 else str(int(anos))
            
        self.ids.resultado.text = (
            f"Considerando que um macaco escreveria 2 teclas por segundo, seriam necessários {anos_str} anos, {int(dias)} dias, {int(horas)} horas, {int(minutos)} minutos, {int(segundos)} segundos" 
        )
#add texto de quanto tempo seria com exemplos de tempo; tempo de vida da terra, do universoV3
    
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

        self.pixels = np.random.randint(0, 255, (total_pixels, 3), dtype=np.uint8) #escolhe 3 vezes um valor aleatório entre 0 e 255 
        #o numpy foi necessário para criar um array de arrays, criando uma matriz de 3 x 1.000.000 com os valores aleatórios
        #np.int8 garante que a informação ocupe 8 bits na memória

        pixel_rgb = self.pixels.tobytes() #a função .tobytes converte a matriz em um array de bytes para que o blit_buffer funcione
        #exemplo dos códigos gerados numa imagem 3x3: \xac\xba\xde\xe7\x8c>\xa8\x13\xded\x8c

        texture = Texture.create(size=(largura, altura))
        texture.blit_buffer(pixel_rgb) #interpreta cada elemento de pixel_rgb como um pixel para a formação da textura
        #tem os parametros colorfmt, padrão rgb e bufferfmt, padrão ubyte

        self.texture = texture
        #add botão de download
class Help (MDScreen):
    intro = ''' O "Teorema do Macaco Infinito", por mais surpreendente que pareça, é um teorema real, com exercícios de pensamento similares datando de mais de um século. Ele postula que um macaco, ou qualquer entidade que gere caracteres aleatoriamente por tempo infinito, eventualmente produziria qualquer texto imaginável, incluindo "Hamlet", de William Shakespeare, que é o exemplo mais comumente citado. Embora o tempo necessário para tal feito seja astronômico, a probabilidade de que ocorra definitivamente não é zero, desde que o tempo seja infinito. O mesmo raciocínio se aplica a qualquer outro texto.\n\n '''
    intro += '''Neste programa, há um gerador que serve como experimento para a comprovação do teorema. São produzidos 25.000 caracteres de forma aleatória, utilizando exclusivamente letras do alfabeto, resultando em um total de 10^35.374 combinações possíveis. Ainda que a chance de gerar um texto extenso e coerente seja insignificante, a probabilidade de formar palavras curtas, como um nome de cinco letras, é significativamente maior, tornando-se uma possibilidade real para aqueles que desejam testar a sorte.'''
    
    corpo = ''' Para estimar o tempo necessário para que um texto específico seja gerado, algumas variáveis precisam ser consideradas: o número de caracteres disponíveis na suposta máquina de escrever (ou, neste caso, no algoritmo de aleatorização), a quantidade de caracteres do texto desejado e a taxa de digitação do macaco teórico. O programa calcula a probabilidade com base em uma potência de expoente 27, pois apenas letras minúsculas e espaços são utilizados, evitando uma explosão combinatória ainda maior. Além disso, assume-se que um macaco digitasse, em média, duas teclas por segundo, permitindo que o tempo estimado para gerar determinado texto seja obtido dividindo-se o resultado da potência por essa taxa de digitação.\n\n'''

    concl = ''' Incorporando a ideia da geração infinita de textos fazendo o uso de caracteres aleatórios à geração de imagens algo que tende a chamar muito mais a atenção, é muito interessante imaginar que fotos ou obras de arte poderiam sair disso, porém com uma quantidade assustadoramente maior de possibilidades. Esta seria a ideia por trás do "Canvas Infinito": uma imagem de tamanho 1000x1000 pixels, cada um com 256 possibilidades de valores diferente para cada um dos canais "RGB", temos 256³ = 16.777.216 cores diferentes para cada pixel, logo, a quantidade total de imagens seria 16.777.216 elevado a um milhão de pixels, ou 2^24.000.000 escrito de outra forma. Para ter uma ideia, mesmo que tivéssemos um computador capaz de gerar trilhões de imagens por segundo funcionando desde o início do universo, conseguiríamos gerar 10^-7.224.969%\ de todas as imagens possíveis desse algoritmo.\n\n '''
    concl += '''Diante de tantas possibilidades, cada nova geração do "Canvas Infinito" resulta, na maioria das vezes, em imagens abstratas e caóticas, tal como esta anexada. Entretanto, dentro desse universo inconcebível de permutações de pixels, existem, ocultas, todas as imagens concebíveis, desde obras-primas da arte até fotografias perfeitas de momentos jamais registrados.'''

class Infinite(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        Window.maximize ()
        return ScreenManager()
    #melhorar o design do appV3   

if __name__ == '__main__':
    Infinite().run()