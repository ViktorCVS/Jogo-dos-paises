import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import random

# Configurar o backend do matplotlib para uso com Tkinter
matplotlib.use('TkAgg')

class MapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contorno de Países")

        # Parâmetros iniciais de extensão do mapa (longitude e latitude)
        self.extent = [-180, 180, -90, 90]  # [min_lon, max_lon, min_lat, max_lat]
        self.zoom_factor = 0.8  # Fator de zoom padrão (80% da extensão atual)
        self.pan_fraction = 0.1  # Fração da extensão para cada movimento de pan (10%)

        # Variáveis para panning (arrasto do mapa)
        self.press = None  # Armazena a posição inicial do clique

        # Criar a figura do Matplotlib e o eixo com projeção PlateCarree
        self.fig = plt.Figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, projection=ccrs.PlateCarree())

        # Definir a extensão do mapa
        self.ax.set_extent(self.extent, crs=ccrs.PlateCarree())
        # Remover as grades e eixos para um visual mais limpo
        self.ax.axis('off')

        # Carregar os dados dos países usando Natural Earth shapefiles
        shapename = 'admin_0_countries'
        self.countries_shp = shpreader.natural_earth(resolution='10m',
                                                     category='cultural', name=shapename)
        reader = shpreader.Reader(self.countries_shp)
        self.countries = list(reader.records())

        # Ordenar a lista de países em ordem alfabética pelo nome
        self.countries.sort(key=lambda country: country.attributes['NAME_LONG'])
        # Extrair a lista de nomes dos países
        self.country_names = [country.attributes['NAME_LONG'] for country in self.countries]

        # Índice do país atual
        self.current_country_index = 0  # Começar com o primeiro país na lista

        # Dicionário para armazenar as geometrias dos países
        self.country_geometries = {country.attributes['NAME_LONG']: country.geometry for country in self.countries}

        # Embutir a figura no widget Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # Desenhar o país atual no mapa
        self.current_country_patch = None
        self.display_country(self.country_names[self.current_country_index])

        # Criar um frame para os botões de controle na parte inferior
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Botões de Controle de País
        next_country_btn = tk.Button(control_frame, text="Próximo País", command=self.next_country)
        next_country_btn.pack(side=tk.LEFT, padx=5, pady=5)

        random_country_btn = tk.Button(control_frame, text="País Aleatório", command=self.random_country)
        random_country_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Botões de Zoom
        zoom_in_btn = tk.Button(control_frame, text="Zoom In", command=self.zoom_in)
        zoom_in_btn.pack(side=tk.LEFT, padx=5, pady=5)

        zoom_out_btn = tk.Button(control_frame, text="Zoom Out", command=self.zoom_out)
        zoom_out_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Botões de Pan
        pan_left_btn = tk.Button(control_frame, text="← Pan Left", command=self.pan_left)
        pan_left_btn.pack(side=tk.LEFT, padx=5, pady=5)

        pan_right_btn = tk.Button(control_frame, text="Pan Right →", command=self.pan_right)
        pan_right_btn.pack(side=tk.LEFT, padx=5, pady=5)

        pan_up_btn = tk.Button(control_frame, text="Pan Up ↑", command=self.pan_up)
        pan_up_btn.pack(side=tk.LEFT, padx=5, pady=5)

        pan_down_btn = tk.Button(control_frame, text="Pan Down ↓", command=self.pan_down)
        pan_down_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Bindings para Zoom e Pan via Mouse
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def display_country(self, country_name):
        """Exibe o contorno do país especificado no mapa."""
        # Limpar o país anterior, se houver
        if self.current_country_patch is not None:
            self.current_country_patch.remove()

        # Obter a geometria do país
        geometry = self.country_geometries[country_name]

        # Adicionar a geometria do país ao eixo com apenas o contorno
        self.current_country_patch = self.ax.add_geometries(
            [geometry],
            ccrs.PlateCarree(),
            facecolor='none',  # Sem preenchimento
            edgecolor='black',  # Contorno preto
            linewidth=1.0
        )

        # Atualizar o título com o nome do país
        self.ax.set_title(country_name, fontsize=14)

        # Ajustar a extensão do mapa para o país atual
        self.zoom_to_country(geometry)

        # Redesenhar o canvas
        self.canvas.draw()

    def zoom_to_country(self, geometry):
        """Ajusta a extensão do mapa para o país especificado."""
        bounds = geometry.bounds  # (minx, miny, maxx, maxy)
        minx, miny, maxx, maxy = bounds

        # Expandir um pouco a extensão para incluir alguma margem
        padding_x = (maxx - minx) * 0.1
        padding_y = (maxy - miny) * 0.1

        new_extent = [minx - padding_x, maxx + padding_x, miny - padding_y, maxy + padding_y]

        # Atualizar a extensão do mapa
        self.extent = new_extent
        self.ax.set_extent(self.extent, crs=ccrs.PlateCarree())

    def next_country(self):
        """Mostra o próximo país na lista em ordem alfabética."""
        self.current_country_index = (self.current_country_index + 1) % len(self.country_names)
        country_name = self.country_names[self.current_country_index]
        self.display_country(country_name)

    def random_country(self):
        """Mostra um país aleatório."""
        self.current_country_index = random.randint(0, len(self.country_names) - 1)
        country_name = self.country_names[self.current_country_index]
        self.display_country(country_name)

    def zoom_in(self):
        """Reduz a extensão do mapa para dar zoom in."""
        self.adjust_extent(factor=self.zoom_factor)

    def zoom_out(self):
        """Aumenta a extensão do mapa para dar zoom out."""
        self.adjust_extent(factor=1 / self.zoom_factor)

    def adjust_extent(self, factor):
        """Ajusta a extensão do mapa com base no fator de zoom."""
        min_lon, max_lon, min_lat, max_lat = self.extent
        lon_center = (min_lon + max_lon) / 2
        lat_center = (min_lat + max_lat) / 2
        lon_width = (max_lon - min_lon) * factor / 2
        lat_height = (max_lat - min_lat) * factor / 2

        # Definir nova extensão com base no fator
        new_min_lon = lon_center - lon_width
        new_max_lon = lon_center + lon_width
        new_min_lat = lat_center - lat_height
        new_max_lat = lat_center + lat_height

        # Limitar a extensão aos limites globais
        new_min_lon = max(new_min_lon, -180)
        new_max_lon = min(new_max_lon, 180)
        new_min_lat = max(new_min_lat, -90)
        new_max_lat = min(new_max_lat, 90)

        self.extent = [new_min_lon, new_max_lon, new_min_lat, new_max_lat]
        self.ax.set_extent(self.extent, crs=ccrs.PlateCarree())
        self.canvas.draw()

    def pan_left(self):
        """Desloca a extensão do mapa para a esquerda."""
        self.adjust_pan(direction='left')

    def pan_right(self):
        """Desloca a extensão do mapa para a direita."""
        self.adjust_pan(direction='right')

    def pan_up(self):
        """Desloca a extensão do mapa para cima."""
        self.adjust_pan(direction='up')

    def pan_down(self):
        """Desloca a extensão do mapa para baixo."""
        self.adjust_pan(direction='down')

    def adjust_pan(self, direction):
        """Ajusta a extensão do mapa com base na direção do pan."""
        min_lon, max_lon, min_lat, max_lat = self.extent
        lon_shift = (max_lon - min_lon) * self.pan_fraction
        lat_shift = (max_lat - min_lat) * self.pan_fraction

        if direction == 'left':
            new_min_lon = min_lon - lon_shift
            new_max_lon = max_lon - lon_shift
            if new_min_lon < -180:
                new_min_lon = -180
                new_max_lon = new_min_lon + (max_lon - min_lon)
            self.extent = [new_min_lon, new_max_lon, min_lat, max_lat]
        elif direction == 'right':
            new_min_lon = min_lon + lon_shift
            new_max_lon = max_lon + lon_shift
            if new_max_lon > 180:
                new_max_lon = 180
                new_min_lon = new_max_lon - (max_lon - min_lon)
            self.extent = [new_min_lon, new_max_lon, min_lat, max_lat]
        elif direction == 'up':
            new_min_lat = min_lat + lat_shift
            new_max_lat = max_lat + lat_shift
            if new_max_lat > 90:
                new_max_lat = 90
                new_min_lat = new_max_lat - (max_lat - min_lat)
            self.extent = [min_lon, max_lon, new_min_lat, new_max_lat]
        elif direction == 'down':
            new_min_lat = min_lat - lat_shift
            new_max_lat = max_lat - lat_shift
            if new_min_lat < -90:
                new_min_lat = -90
                new_max_lat = new_min_lat + (max_lat - min_lat)
            self.extent = [min_lon, max_lon, new_min_lat, new_max_lat]

        self.ax.set_extent(self.extent, crs=ccrs.PlateCarree())
        self.canvas.draw()

    # ----- Métodos para Zoom e Pan via Mouse -----

    def on_scroll(self, event):
        """Manipula eventos de scroll para zoom in e zoom out."""
        if event.button == 'up':
            self.adjust_extent(factor=self.zoom_factor)
        elif event.button == 'down':
            self.adjust_extent(factor=1 / self.zoom_factor)

    def on_press(self, event):
        """Armazena a posição inicial do clique para panning."""
        if event.button == 1 and event.inaxes:
            self.press = (event.xdata, event.ydata)

    def on_release(self, event):
        """Reseta a posição inicial após o fim do arrasto."""
        self.press = None

    def on_motion(self, event):
        """Atualiza a extensão do mapa durante o arrasto para panning."""
        if self.press is None or event.inaxes is None:
            return

        x0, y0 = self.press
        x1, y1 = event.xdata, event.ydata
        dx = x0 - x1
        dy = y0 - y1

        # Calcular a mudança na extensão com base no deslocamento do mouse
        min_lon, max_lon, min_lat, max_lat = self.extent

        # Obter a largura e altura do eixo em coordenadas de longitude e latitude
        lon_shift = dx * (max_lon - min_lon) / self.ax.bbox.width
        lat_shift = dy * (max_lat - min_lat) / self.ax.bbox.height

        new_min_lon = min_lon + lon_shift
        new_max_lon = max_lon + lon_shift
        new_min_lat = min_lat + lat_shift
        new_max_lat = max_lat + lat_shift

        # Limitar aos limites globais
        lon_width = max_lon - min_lon
        lat_height = max_lat - min_lat

        if new_min_lon < -180:
            new_min_lon = -180
            new_max_lon = new_min_lon + lon_width
        if new_max_lon > 180:
            new_max_lon = 180
            new_min_lon = new_max_lon - lon_width
        if new_min_lat < -90:
            new_min_lat = -90
            new_max_lat = new_min_lat + lat_height
        if new_max_lat > 90:
            new_max_lat = 90
            new_min_lat = new_max_lat - lat_height

        self.extent = [new_min_lon, new_max_lon, new_min_lat, new_max_lat]
        self.ax.set_extent(self.extent, crs=ccrs.PlateCarree())
        self.canvas.draw()

    # ----- Fim dos Métodos para Zoom e Pan via Mouse -----

# Criar a janela tkinter
root = tk.Tk()
app = MapApp(root)
root.mainloop()
