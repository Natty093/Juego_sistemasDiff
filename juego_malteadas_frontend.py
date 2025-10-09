# juego_malteadas_frontend.py

import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import os
from backend_difuso import SistemaDifusoMalteada  # <-- MODIFICACIÓN: Importar el backend


class MilkshakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("¡CREA LA MEJOR MALTEADA!")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f6bd40")

        self.fridge_open = False
        self.cabinet_open = False
        self.selected_ingredients = []
        self.max_ingredients = 7
        self.min_ingredients = 3
        self.ingredient_size = (55, 55)
        self.images = {}
        self.ingredient_refs = []
        self.glass_ingredients_display = []
        self.fridge_closed_image_id = None
        self.fridge_open_image_id = None
        self.cabinet_closed_image_id = None
        self.cabinet_open_image_id = None
        self.APPLIANCE_TOP_Y = 180
        self.APPLIANCE_BOTTOM_Y = 540
        self.FRIDGE_START_X = 45
        self.FRIDGE_CLOSED_END_X = 255
        self.FRIDGE_OPEN_END_X = 255
        self.CABINET_CLOSED_START_X = 820
        self.CABINET_OPEN_START_X = 820
        self.CABINET_END_X = 1075

        self.canvas = Canvas(root, width=1200, height=750, bg="#f6bd40", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.setup_ui()
        self.load_ingredients()

        # MODIFICACIÓN: Crear una instancia del sistema difuso
        self.sistema_difuso = SistemaDifusoMalteada()

    def load_image(self, path, size=None):
        try:
            if os.path.exists(path):
                img = Image.open(path)
                if size:
                    img = img.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            else:
                return None
        except Exception as e:
            return None

    def setup_ui(self):
        self.canvas.create_text(600, 50, text="¡CREA LA MEJOR MALTEADA!", font=("Arial", 40, "bold"), fill="#000000")
        self.canvas.create_text(600, 100,
                                text="Selecciona y arrastra los ingredientes en el vaso (puedes escoger hasta 7 ingredientes como máximo)",
                                font=("Arial", 12), fill="#333333")
        center_y = (self.APPLIANCE_TOP_Y + self.APPLIANCE_BOTTOM_Y) / 2
        fridge_width = self.FRIDGE_CLOSED_END_X - self.FRIDGE_START_X
        fridge_open_dims = (fridge_width, self.APPLIANCE_BOTTOM_Y - self.APPLIANCE_TOP_Y)
        self.fridge_open_img_ref = self.load_image("Imagenes/refrigerador-abierto.png", fridge_open_dims)
        center_x = (self.FRIDGE_START_X + self.FRIDGE_CLOSED_END_X) / 2
        if self.fridge_open_img_ref:
            self.fridge_open_image_id = self.canvas.create_image(center_x, center_y, image=self.fridge_open_img_ref,
                                                                 state=tk.HIDDEN, tags="fridge_open_background")
        else:
            self.fridge_open_image_id = self.canvas.create_rectangle(self.FRIDGE_START_X, self.APPLIANCE_TOP_Y,
                                                                     self.FRIDGE_CLOSED_END_X, self.APPLIANCE_BOTTOM_Y,
                                                                     fill="#FFFFFF", outline="#000000", width=3,
                                                                     state=tk.HIDDEN)
            self.canvas.create_text(center_x, center_y, text="FRIDGE ABIERTO\n(Falta Imagen)", font=("Arial", 10),
                                    fill="#000000", tags="fridge_open_background")
        fridge_closed_dims = (fridge_width, self.APPLIANCE_BOTTOM_Y - self.APPLIANCE_TOP_Y)
        self.fridge_closed_img_ref = self.load_image("Imagenes/refrigerador.png", fridge_closed_dims)
        if self.fridge_closed_img_ref:
            self.fridge_closed_image_id = self.canvas.create_image(center_x, center_y, image=self.fridge_closed_img_ref,
                                                                   tags=("fridge_door_tag", "clickable"))
        else:
            self.fridge_closed_image_id = self.canvas.create_rectangle(self.FRIDGE_START_X, self.APPLIANCE_TOP_Y,
                                                                       self.FRIDGE_CLOSED_END_X,
                                                                       self.APPLIANCE_BOTTOM_Y, fill="#CCCCCC",
                                                                       outline="#000000", width=3,
                                                                       tags=("fridge_door_tag", "clickable"))
            self.canvas.create_text(center_x, center_y, text="REFRIGERADOR\n(Falta Imagen)", font=("Arial", 10),
                                    fill="#000000", tags=("fridge_door_tag", "clickable"))
        self.canvas.tag_bind("fridge_door_tag", "<Button-1>", self.toggle_fridge)
        mesa_width = 420
        mesa_height = 160
        self.mesa_img = self.load_image("Imagenes/mesa.png", (mesa_width, mesa_height))
        if self.mesa_img:
            self.mesa = self.canvas.create_image(530, 460, image=self.mesa_img)
        else:
            self.canvas.create_rectangle(320, 380, 740, 540, fill="#8B4513", outline="#654321", width=3)
            self.canvas.create_text(530, 460, text="MESA\n(Falta imagen)", font=("Arial", 12), fill="#FFFFFF")
        self.glass_img = self.load_image("Imagenes/Vaso.png", (100, 130))
        if self.glass_img:
            self.glass = self.canvas.create_image(530, 315, image=self.glass_img)
        else:
            self.canvas.create_polygon(490, 270, 570, 270, 575, 360, 485, 360, fill="#B0BEC5", outline="#546E7A",
                                       width=2)
            self.canvas.create_text(530, 315, text="VASO\n(imagen)", font=("Arial", 10), fill="#000000")
        self.drop_zone_coords = (470, 250, 590, 380)
        self.drop_zone = self.canvas.create_rectangle(*self.drop_zone_coords, outline="", width=0)
        cabinet_width = self.CABINET_END_X - self.CABINET_CLOSED_START_X
        cabinet_open_dims = (cabinet_width, self.APPLIANCE_BOTTOM_Y - self.APPLIANCE_TOP_Y)
        self.cabinet_open_img_ref = self.load_image("Imagenes/alacena-abierta.png", cabinet_open_dims)
        center_x_cabinet = (self.CABINET_CLOSED_START_X + self.CABINET_END_X) / 2
        if self.cabinet_open_img_ref:
            self.cabinet_open_image_id = self.canvas.create_image(center_x_cabinet, center_y,
                                                                  image=self.cabinet_open_img_ref, state=tk.HIDDEN,
                                                                  tags="cabinet_open_background")
        else:
            self.cabinet_open_image_id = self.canvas.create_rectangle(self.CABINET_CLOSED_START_X, self.APPLIANCE_TOP_Y,
                                                                      self.CABINET_END_X, self.APPLIANCE_BOTTOM_Y,
                                                                      fill="#8B6B47", outline="#000000", width=3,
                                                                      state=tk.HIDDEN)
            self.canvas.create_text(center_x_cabinet, center_y, text="ALACENA ABIERTA\n(Falta Imagen)",
                                    font=("Arial", 10), fill="#FFFFFF", tags="cabinet_open_background")
        cabinet_closed_dims = (cabinet_width, self.APPLIANCE_BOTTOM_Y - self.APPLIANCE_TOP_Y)
        self.cabinet_closed_img_ref = self.load_image("Imagenes/alacena.png", cabinet_closed_dims)
        if self.cabinet_closed_img_ref:
            self.cabinet_closed_image_id = self.canvas.create_image(center_x_cabinet, center_y,
                                                                    image=self.cabinet_closed_img_ref,
                                                                    tags=("cabinet_door_tag", "clickable"))
        else:
            self.cabinet_closed_image_id = self.canvas.create_rectangle(self.CABINET_CLOSED_START_X,
                                                                        self.APPLIANCE_TOP_Y, self.CABINET_END_X,
                                                                        self.APPLIANCE_BOTTOM_Y, fill="#A0522D",
                                                                        outline="#000000", width=3,
                                                                        tags=("cabinet_door_tag", "clickable"))
            self.canvas.create_text(center_x_cabinet, center_y, text="ALACENA\n(Falta Imagen)", font=("Arial", 10),
                                    fill="#FFFFFF", tags=("cabinet_door_tag", "clickable"))
        self.canvas.tag_bind("cabinet_door_tag", "<Button-1>", self.toggle_cabinet)
        self.btn_mezclar = tk.Button(self.root, text="Mezclar", font=("Arial", 16, "bold"), bg="#52BE80", fg="white",
                                     width=12, height=2, relief=tk.RAISED, command=self.mezclar)
        self.canvas.create_window(430, 690, window=self.btn_mezclar)
        self.btn_limpiar = tk.Button(self.root, text="Limpiar", font=("Arial", 16, "bold"), bg="#E74C3C", fg="white",
                                     width=12, height=2, relief=tk.RAISED, command=self.limpiar)
        self.canvas.create_window(630, 690, window=self.btn_limpiar)
        self.fridge_items = []
        self.cabinet_items = []

    def load_ingredients(self):
        self.fridge_ingredients = [
            {"name": "Helado", "file": "Imagenes/nieve.png", "row": 0, "col": 0},
            {"name": "Hielo", "file": "Imagenes/hielos.png", "row": 0, "col": 1},
            {"name": "Carne", "file": "Imagenes/carne.png", "row": 0, "col": 2},
            {"name": "Chocolate", "file": "Imagenes/chocolate.png", "row": 1, "col": 0},
            {"name": "Refresco", "file": "Imagenes/coca.png", "row": 1, "col": 1},
            {"name": "Yogurt", "file": "Imagenes/yogurt.png", "row": 1, "col": 2},
            {"name": "Agua", "file": "Imagenes/agua.png", "row": 2, "col": 0},
            {"name": "Leche", "file": "Imagenes/leche.png", "row": 2, "col": 1},
            {"name": "Fresa", "file": "Imagenes/fresas.png", "row": 2, "col": 2},
        ]
        self.cabinet_ingredients = [
            {"name": "Limón", "file": "Imagenes/limon.png", "row": 0, "col": 0},
            {"name": "Mango", "file": "Imagenes/mango.png", "row": 0, "col": 1},
            {"name": "Plátano", "file": "Imagenes/platano.png", "row": 0, "col": 2},
            {"name": "Azúcar", "file": "Imagenes/azucar.png", "row": 1, "col": 0},
            {"name": "Miel", "file": "Imagenes/miel.png", "row": 1, "col": 1},
            {"name": "Café", "file": "Imagenes/cafe.png", "row": 1, "col": 2},
            {"name": "Picante", "file": "Imagenes/salsa.png", "row": 2, "col": 0},
            {"name": "Mayonesa", "file": "Imagenes/mayonesa.png", "row": 2, "col": 1},
            {"name": "Mostaza", "file": "Imagenes/mostaza.png", "row": 2, "col": 2},
        ]

    def toggle_fridge(self, event=None):
        if not self.fridge_open:
            self.canvas.itemconfig(self.fridge_closed_image_id, state=tk.HIDDEN)
            self.canvas.itemconfig(self.fridge_open_image_id, state=tk.NORMAL)
            self.show_fridge_contents()
            self.fridge_open = True
        else:
            self.canvas.itemconfig(self.fridge_closed_image_id, state=tk.NORMAL)
            self.canvas.itemconfig(self.fridge_open_image_id, state=tk.HIDDEN)
            self.hide_fridge_contents()
            self.fridge_open = False

    def toggle_cabinet(self, event=None):
        if not self.cabinet_open:
            self.canvas.itemconfig(self.cabinet_closed_image_id, state=tk.HIDDEN)
            self.canvas.itemconfig(self.cabinet_open_image_id, state=tk.NORMAL)
            self.show_cabinet_contents()
            self.cabinet_open = True
        else:
            self.canvas.itemconfig(self.cabinet_closed_image_id, state=tk.NORMAL)
            self.canvas.itemconfig(self.cabinet_open_image_id, state=tk.HIDDEN)
            self.hide_cabinet_contents()
            self.cabinet_open = False

    def show_fridge_contents(self):
        col_x = [90, 140, 190]
        row_y = [265, 340, 430]
        for ing in self.fridge_ingredients:
            x, y = col_x[ing["col"]], row_y[ing["row"]]
            img = self.load_image(ing["file"], self.ingredient_size)
            img_id = self.canvas.create_image(x, y, image=img) if img else self.canvas.create_text(x, y, text="#",
                                                                                                   font=("Arial", 30),
                                                                                                   fill="#999999")
            if img: self.images[img_id] = img
            self.canvas.tag_raise(img_id)
            item_data = {"image_id": img_id, "name": ing["name"], "type": "fridge", "file": ing["file"]}
            self.fridge_items.append(item_data)
            self.canvas.tag_bind(item_data["image_id"], "<Button-1>", lambda e, d=item_data: self.start_drag(e, d))

    def show_cabinet_contents(self):
        col_x = [870, 940, 1010]
        row_y = [245, 345, 440]
        for ing in self.cabinet_ingredients:
            x, y = col_x[ing["col"]], row_y[ing["row"]]
            img = self.load_image(ing["file"], self.ingredient_size)
            img_id = self.canvas.create_image(x, y, image=img) if img else self.canvas.create_text(x, y, text="#",
                                                                                                   font=("Arial", 30),
                                                                                                   fill="#999999")
            if img: self.images[img_id] = img
            self.canvas.tag_raise(img_id)
            item_data = {"image_id": img_id, "name": ing["name"], "type": "cabinet", "file": ing["file"]}
            self.cabinet_items.append(item_data)
            self.canvas.tag_bind(item_data["image_id"], "<Button-1>", lambda e, d=item_data: self.start_drag(e, d))

    def hide_fridge_contents(self):
        for item in self.fridge_items:
            self.canvas.delete(item["image_id"])
        self.fridge_items = []

    def hide_cabinet_contents(self):
        for item in self.cabinet_items:
            self.canvas.delete(item["image_id"])
        self.cabinet_items = []

    def start_drag(self, event, item_data):
        if len(self.selected_ingredients) >= self.max_ingredients: return
        self.dragging_item = item_data
        drag_img = self.load_image(item_data["file"], (50, 50))
        if drag_img:
            self.drag_copy = self.canvas.create_image(event.x, event.y, image=drag_img)
            self.images["drag_copy"] = drag_img
        else:
            self.drag_copy = self.canvas.create_rectangle(event.x - 25, event.y - 25, event.x + 25, event.y + 25,
                                                          fill="#FFFFFF", outline="#667eea", width=3)
            self.drag_text = self.canvas.create_text(event.x, event.y, text="#", font=("Arial", 20), fill="#667eea")
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)

    def on_drag(self, event):
        coords = self.canvas.coords(self.drag_copy)
        if coords:
            dx, dy = event.x - coords[0], event.y - coords[1]
            self.canvas.move(self.drag_copy, dx, dy)
            if hasattr(self, 'drag_text'): self.canvas.move(self.drag_text, dx, dy)

    def on_drop(self, event):
        x1, y1, x2, y2 = self.drop_zone_coords
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            self.add_ingredient_to_glass(self.dragging_item)
        self.canvas.delete(self.drag_copy)
        if hasattr(self, 'drag_text'): self.canvas.delete(self.drag_text)
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def add_ingredient_to_glass(self, item_data):
        if len(self.selected_ingredients) >= self.max_ingredients: return
        self.selected_ingredients.append(item_data["name"])
        y_position = 275 + (len(self.selected_ingredients) * 12)
        text_id = self.canvas.create_text(530, y_position, text=f"• {item_data['name']}", font=("Arial", 7, "bold"),
                                          fill="#333333", tags="glass_ingredient")
        self.glass_ingredients_display.append(text_id)

    # MODIFICACIÓN: Método mezclar actualizado para usar el backend
    def mezclar(self):
        if len(self.selected_ingredients) < self.min_ingredients:
            print(f"¡Necesitas al menos {self.min_ingredients} ingredientes!")
            return

        print(f"Ingredientes seleccionados: {self.selected_ingredients}")
        calidad_final = self.sistema_difuso.calcular_calidad(self.selected_ingredients)
        print(f"Puntaje de calidad (0-100): {calidad_final:.2f}")

        if calidad_final <= 15:
            resultado_nivel = 1
        elif calidad_final <= 30:
            resultado_nivel = 2
        elif calidad_final <= 45:
            resultado_nivel = 3
        elif calidad_final <= 55:
            resultado_nivel = 4
        elif calidad_final <= 65:
            resultado_nivel = 5
        elif calidad_final <= 75:
            resultado_nivel = 6
        elif calidad_final <= 85:
            resultado_nivel = 7
        elif calidad_final <= 95:
            resultado_nivel = 8
        else:
            resultado_nivel = 9

        self.show_result_screen(resultado_nivel)

    def show_result_screen(self, nivel):
        resultados = {
            1: {"emoji": "Imagenes/Emoji-vomito.png", "texto": "Horrible", "color": "#8B0000"},
            2: {"emoji": "Imagenes/Emoji-Verde.png", "texto": "Combinación extraña", "color": "#A0522D"},
            3: {"emoji": "Imagenes/Emoji-acido.png", "texto": "Demasiado ácida", "color": "#DAA520"},
            4: {"emoji": "Imagenes/Emoji-neutro.png", "texto": "Muy simple/falta sabor", "color": "#D3D3D3"},
            5: {"emoji": "Imagenes/Emoji-duda.png", "texto": "Cremosa pero sin dulzura", "color": "#B8860B"},
            6: {"emoji": "Imagenes/Pulgar.png", "texto": "Refrescante y equilibrada", "color": "#4682B4"},
            7: {"emoji": "Imagenes/Emoji-Feliz.png", "texto": "Muy buena/Me gusta", "color": "#32CD32"},
            8: {"emoji": "Imagenes/Emoji-Estrellas.png", "texto": "Dulce y cremosa/Perfecta", "color": "#FF69B4"},
            9: {"emoji": "Imagenes/Emoji-Corazon.png", "texto": "Delicioso/Obra maestra", "color": "#FF1493"},
        }
        resultado = resultados[nivel]
        self.canvas.itemconfig("clickable", state=tk.HIDDEN)
        self.canvas.itemconfig("glass_ingredient", state=tk.HIDDEN)
        self.canvas.itemconfig("fridge_open_background", state=tk.HIDDEN)
        self.canvas.itemconfig("cabinet_open_background", state=tk.HIDDEN)
        self.btn_mezclar.place_forget()
        self.btn_limpiar.place_forget()
        self.result_bg = self.canvas.create_rectangle(0, 0, 1200, 750, fill="#f6bd40", tags="result_screen")
        emoji_img = self.load_image(resultado["emoji"], (250, 250))
        if emoji_img:
            self.result_emoji = self.canvas.create_image(600, 250, image=emoji_img, tags="result_screen")
            self.images["result_emoji"] = emoji_img
        else:
            self.canvas.create_oval(475, 125, 725, 375, fill=resultado["color"], outline="#000000", width=3,
                                    tags="result_screen")
            self.canvas.create_text(600, 250, text="😊", font=("Arial", 100), fill="#FFFFFF", tags="result_screen")
        self.result_title = self.canvas.create_text(600, 450, text=resultado["texto"], font=("Arial", 40, "bold"),
                                                    fill="#000000", tags="result_screen")
        self.btn_volver = tk.Button(self.root, text="Volver", font=("Arial", 16, "bold"), bg="#52BE80", fg="white",
                                    width=12, height=2, command=self.hide_result_screen)
        self.canvas.create_window(845, 690, window=self.btn_volver, tags="result_screen")

    def hide_result_screen(self):
        self.canvas.delete("result_screen")
        self.btn_volver.destroy()
        if self.fridge_open: self.toggle_fridge()
        if self.cabinet_open: self.toggle_cabinet()
        self.canvas.itemconfig("clickable", state=tk.NORMAL)
        self.canvas.itemconfig("glass_ingredient", state=tk.NORMAL)
        self.canvas.create_window(430, 690, window=self.btn_mezclar)
        self.canvas.create_window(630, 690, window=self.btn_limpiar)

    def limpiar(self):
        self.selected_ingredients = []
        for text_id in self.glass_ingredients_display:
            self.canvas.delete(text_id)
        self.glass_ingredients_display = []


def main():
    root = tk.Tk()
    app = MilkshakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    # No olvides instalar las librerías necesarias:
    # pip install pillow scikit-fuzzy numpy
    main()