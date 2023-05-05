import time

class Cardiac:
    '''Emulador del cardboard computer CARDIAC.'''

    def __init__(self) -> None:
        self.memory = [0] * 100
        self.memory[0] = 1
        self.memory[99] = 800
        self.accumulator = 0
        self.flag = None
        self.target = 0
        self.input_card = []
        self.output_card = []
        self.step = 0

        self.run = True

    def load_program(self, program):
        '''Carga un programa en la memoria del emulador.'''
        memory = self.memory.copy()
        for address, value in program.items():
            if not (0 <= address <= 98):
                raise ValueError("Memory address out of range")
            if not (0 <= value <= 999):
                raise ValueError("Value out of range")
            memory[address] = value
        self.memory = memory

    def run_program(self):
        '''Ejecuta el programa cargado en la memoria del emulador.'''
        self.run = True
        while self.run:
            self.step_program()
            print(self)

    def step_program(self):
        if not (0 <= self.target <= 99):
            return

        instruction = self.memory[self.target]
        self.target += 1
        self.step += 1
        opcode = instruction // 100
        address = instruction % 100

        match opcode:

            case 0:
                value = self.input_card.pop() if self.input_card else 0
                self.write_memory(address, value)

            case 1:
                self.accumulator = self.read_memory(address)

            case 2:
                self.accumulator += self.read_memory(address)
                self.update_flag()

            case 3:
                if not self.flag:
                    self.target = address

            case 4:
                value = str(self.accumulator)
                x = address // 10
                y = address % 10

                value += '0' * x
                if len(value) > 3:
                    value = value[-3:]

                value = '0' * y + value
                if len(value) > 3:
                    value = value[:3]

                self.accumulator = int(value)

            case 5:
                self.output_card.append(self.read_memory(address))

            case 6:
                self.write_memory(address, self.accumulator)

            case 7:
                self.accumulator -= self.read_memory(address)
                self.update_flag()

            case 8:
                self.memory[99] = int('8' + '{:02d}'.format(self.target))
                self.target = address

            case 9:
                self.target = address # Temporal
                self.run = False

    def reset_program(self):
        pass

    def read_memory(self, address):
        '''Lee un valor de la memoria del emulador en una dirección dada.'''
        if not (0 <= address <= 99):
            raise ValueError("Memory address out of range")
        return self.memory[address]

    def write_memory(self, address, value):
        '''Escribe un valor en la memoria del emulador en una dirección dada.'''
        if not (0 <= address <= 99):
            raise ValueError("Memory address out of range")
        if not (0 <= value <= 999):
            raise ValueError("Value out of range")
        self.memory[address] = value

    def update_flag(self):
        if self.accumulator < 0:
            self.flag = False
        else:
            self.flag = True

    def __str__(self):
        text = ''
        text += f'Step: {self.step}\n'
        text += f'Target: {self.target}\n'
        text += f'Flag: {self.flag}\n'
        text += f'Accumulator: {self.accumulator}\n'
        text += f'Input card-deck: {self.input_card}\n'
        text += f'Output card-deck: {self.output_card}\n'
        return text

if __name__ == '__main__':
    cardiac = Cardiac()
    program = { # Multiplica un numero por 10
        15:14,
        16:114,
        17:410,
        18:614,
        19:514,
        20:900
    }
    cardiac.load_program(program)
    cardiac.target = 15

    cardiac.input_card.append(5)

    while cardiac.run:
        cardiac.step_program()
        print(cardiac)
        # time.sleep(0.5)

    print(cardiac.output_card)
