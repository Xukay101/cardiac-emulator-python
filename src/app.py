''' Cardiac App '''

# modules
from cardiac import Cardiac
from flet import (
    flet,
    app,
    Page, 
    Container, 
    Row, 
    Column, 
    TextField,
    UserControl,
    Text,    
    MainAxisAlignment,
    CrossAxisAlignment,
    ElevatedButton,
    GridView,
    border,
    colors,
)

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = (1000, 500)

# Main Class
class CardiacApp(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.cardiac = Cardiac()

        self.cardiac.input_card.put(5)
        
    # Main container
    def main_container(self):
        self.main = Container(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            padding=8
        )

        # Main row
        self.main_row = Row()

        # Right and left containers
        self.left_container = Container(
            height=self.main.height,
            expand=3,
        )

        self.right_container = Container(
            height=self.main.height,
            expand=1,
            border_radius=20,
            border=border.all(1, colors.GREY_600)
        )

        # Right and left containers display
        self.left_col = Column(spacing=10)
        self.right_col = Column(spacing=0)

        # Memory Container
        self.memory_container = Container(
            width=self.left_container.width,
            expand=3,
            padding=10,
            border_radius=20,
            border=border.all(1, colors.GREY_600)
        )

        def generate_memory():
            rows = []
            self.cells = []
            
            for i in range(10):
                columns = []
                for j in range(10):
                    t = TextField(width=45, height=24, text_size=12, content_padding=9, dense=True, on_change=self.update_memory)
                    self.cells.append(t)
                    cell = Row([
                        Text(f'{i*10+j}'),
                        t
                    ], spacing=0)
                    columns.append(cell)
                row = Column(columns, spacing=1)
                rows.append(row)
            return rows

        self.memory_row = Row(generate_memory())

        # Controls Container
        self.interface_container = Container(
            width=self.left_container.width,
            expand=2,
            padding=8,
            border_radius=20,
            border=border.all(1, colors.GREY_600)
        )
        self.interface_col = Column()

        # Status Container and Row content
        self.status_container = Container(
            width=self.interface_container.width,
            expand=1,
        )

        #     items
        self.flag_text = Text(f'Flag: {self.cardiac.flag}', size=24)
        self.accumulator_text = Text(f'Accumulator: {self.cardiac.accumulator}', size=24)
        self.step_text = Text(f'Step: {self.cardiac.step}', size=24)

        self.status_row = Row(
            controls=[
                self.flag_text,
                self.accumulator_text,
                self.step_text,
            ],
            alignment=MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=CrossAxisAlignment.START,
        )
        self.status_container.content = self.status_row

        # Medium container and Row content
        self.medium_container = Container(
            width=self.interface_container.width,
            expand=1,
        )


        self.target_textbox = TextField(
            label='Target',
            value=0, 
            width=80, 
            height=40,
            on_change=self.target_changed
        )

        self.medium_row = Row(
            controls=[
                self.target_textbox
            ],
            alignment=MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=CrossAxisAlignment.CENTER,
        )
        self.medium_container.content = self.medium_row

        # Controls Container and Row content
        self.controls_container = Container(
            width=self.interface_container.width,
            expand=1,
        )

        #     items
        self.run_button = ElevatedButton('Run')
        self.step_button = ElevatedButton('Step', on_click=self.step_clicked)
        self.reset_button = ElevatedButton('Reset', on_click=self.reset_clicked)

        self.controls_row = Row(
            controls=[
                self.run_button,
                self.step_button,
                self.reset_button
            ],
            alignment=MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=CrossAxisAlignment.CENTER,
        )

        self.controls_container.content = self.controls_row

        #
        self.interface_col.controls.append(self.status_container) # or use extend
        self.interface_col.controls.append(self.medium_container)
        self.interface_col.controls.append(self.controls_container)
        
        self.interface_container.content = self.interface_col
                
        #
        self.left_col.controls.append(self.memory_container) # or use extend
        self.left_col.controls.append(self.interface_container) 

        self.left_container.content = self.left_col

        #
        self.memory_container.content = self.memory_row
         
        #
        self.main_row.controls.append(self.left_container) # or use extend
        self.main_row.controls.append(self.right_container)

        # 
        self.main.content = self.main_row 

        return self.main

    def build(self):
        return Column(
            controls=[
                self.main_container(),
            ]
        )

    def update_all(self):
        print(self.cardiac)
        # Flag text
        value = '+' if self.cardiac.flag else '-'
        self.flag_text.value = f'Flag: {value}'
        self.flag_text.update()
        # step text
        self.step_text.value = f'Step: {self.cardiac.step}'
        self.step_text.update()
        # target textbox
        self.target_textbox.value = self.cardiac.target
        self.target_textbox.update()
        # Accumulator
        self.accumulator_text.value = f'Accumulator: {self.cardiac.accumulator}'
        # Memory
        self.update_memory(None)

    def update_memory(self, e):
        print(self.cardiac.memory)
        for i, cell in enumerate(self.cells):
            if i == self.cardiac.target:
                cell.border_color = 'red'
                cell.bgcolor = 'red'
            else:
                cell.border_color = 'gray'
                cell.bgcolor = False

            try:
                if int(cell.value) > 0:
                    self.cardiac.memory[i] = int(cell.value)
            except:
                self.cardiac.memory[i] = 0
                            
            cell.update()


    def upload_memory(self):
        for i, cell in enumerate(self.cells):
            if self.cardiac.memory[i] > 0:
                cell.value = str(self.cardiac.memory[i]).zfill(3)
                cell.update()

    def step_clicked(self, e):
        self.update_memory(None)
        self.cardiac.step_program()
        self.update_all()

    def run_clicked(self, e):
        self.cardiac.run_program()
        self.update_all()

    def reset_clicked(self, e):
        self.cardiac.target = 0
        self.cardiac.step = 0
        self.cardiac.flag = True
        self.update_all()

    def target_changed(self, e):
        try:
            self.cardiac.target = int(e.control.value)
        except:
            return
        self.update_all()

def main(page: Page):
    page.title = "Cardiac"
    page.window_width = SCREEN_WIDTH
    page.window_height = SCREEN_HEIGHT
    page.padding = 0

    app = CardiacApp(page)
    page.add(app)
    app.upload_memory()
    app.update_all()

    page.update()

flet.app(target=main)