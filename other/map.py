import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from shapely.geometry import Point

# Configurar o backend do matplotlib para uso com Tkinter
matplotlib.use('TkAgg')

class MapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo do mapa")

        # Parâmetros iniciais de extensão do mapa (longitude e latitude)
        self.extent = [-180, 180, -90, 90]  # [min_lon, max_lon, min_lat, max_lat]
        self.zoom_factor = 0.8  # Fator de zoom padrão (80% da extensão atual)
        self.pan_fraction = 0.1  # Fração da extensão para cada movimento de pan (10%)

        # Variáveis para panning (arrasto do mapa)
        self.press = None  # Armazena a posição inicial do clique

        # Criar a figura do Matplotlib e o eixo com projeção PlateCarree
        self.fig = plt.Figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, projection=ccrs.PlateCarree())

        # Adicionar a camada do oceano com a cor azul
        self.ax.add_feature(cfeature.OCEAN, facecolor='#51629a')

        # Adicionar fronteiras e linhas costeiras sobre o oceano
        self.ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        self.ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

        # Definir a extensão do mapa
        self.ax.set_extent(self.extent, crs=ccrs.PlateCarree())
        # Definir um título inicial (opcional)
        self.ax.set_title("")

        # Carregar os dados dos países usando Natural Earth shapefiles
        shapename = 'admin_0_countries'
        self.countries_shp = shpreader.natural_earth(resolution='10m',
                                                    category='cultural', name=shapename)
        reader = shpreader.Reader(self.countries_shp)
        self.countries = list(reader.records())

        # Desenhar as fronteiras dos países no mapa
        self.country_patches = {}
        for country in self.countries:
            geometry = country.geometry
            name = country.attributes['NAME_LONG']
            # Adicionar a geometria do país ao eixo com borda preta e sem preenchimento
            patch = self.ax.add_geometries([geometry], ccrs.PlateCarree(),
                                          facecolor='none', edgecolor='black', linewidth=0.5)
            self.country_patches[name] = patch  # Armazenar o patch para manipulação futura

        # Embutir a figura no widget Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # Conectar eventos de mouse ao canvas
        self.canvas.mpl_connect('button_press_event', self.on_click)

        # Criar um frame para os botões de controle na parte inferior
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)

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

        # Botão para Desmarcar Todos os Países
        clear_all_btn = tk.Button(control_frame, text="Desmarcar Todos", command=self.clear_all)
        clear_all_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Dicionário para rastrear a cor de cada país (para alternar entre marcado e desmarcado)
        self.country_colors = {}

        # Bindings para Zoom e Pan via Mouse
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_click(self, event):
        # Verificar se o clique é com o botão direito do mouse (button 3)
        if event.button == 3 and event.inaxes:
            # Converter as coordenadas do clique para longitude e latitude
            lon, lat = event.xdata, event.ydata
            point = Point(lon, lat)
            for country in self.countries:
                geometry = country.geometry
                if geometry.contains(point):
                    name = country.attributes['NAME_LONG']
                    current_color = self.country_colors.get(name, 'none')
                    # Alternar a cor entre vermelho e sem preenchimento
                    new_color = 'red' if current_color == 'none' else 'none'
                    self.country_patches[name].set_facecolor(new_color)
                    self.country_colors[name] = new_color
                    
                    # Atualizar o título do gráfico
                    if new_color == 'red':
                        self.ax.set_title(name)  # Atualiza o título com o nome do país
                    else:
                        self.ax.set_title("")    # Limpa o título
                    
                    self.canvas.draw()
                    break

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
        elif direction == 'right':
            new_min_lon = min_lon + lon_shift
            new_max_lon = max_lon + lon_shift
            if new_max_lon > 180:
                new_max_lon = 180
                new_min_lon = new_max_lon - (max_lon - min_lon)
        elif direction == 'up':
            new_min_lat = min_lat + lat_shift
            new_max_lat = max_lat + lat_shift
            if new_max_lat > 90:
                new_max_lat = 90
                new_min_lat = new_max_lat - (max_lat - min_lat)
        elif direction == 'down':
            new_min_lat = min_lat - lat_shift
            new_max_lat = max_lat - lat_shift
            if new_min_lat < -90:
                new_min_lat = -90
                new_max_lat = new_min_lat + (max_lat - min_lat)
        else:
            return  # Direção inválida

        # Atualizar a extensão com base na direção
        if direction in ['left', 'right']:
            self.extent = [new_min_lon, new_max_lon, min_lat, max_lat]
        elif direction in ['up', 'down']:
            self.extent = [min_lon, max_lon, new_min_lat, new_max_lat]

        self.ax.set_extent(self.extent, crs=ccrs.PlateCarree())
        self.canvas.draw()

    def clear_all(self):
        """Desmarca todos os países, removendo a cor vermelha e limpando o título."""
        # Iterar sobre todos os países e remover a cor de preenchimento
        for name, patch in self.country_patches.items():
            patch.set_facecolor('none')
        
        # Limpar o dicionário de cores
        self.country_colors.clear()
        
        # Limpar o título do gráfico
        self.ax.set_title("")
        
        # Redesenhar o canvas para refletir as alterações
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
        # Isso ajuda a determinar quanto a extensão deve mudar baseado no deslocamento do mouse
        lon_shift = dx * (360) / self.ax.bbox.width
        lat_shift = dy * (180) / self.ax.bbox.height

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
