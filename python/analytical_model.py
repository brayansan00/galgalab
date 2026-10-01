"""Entrada compatible: modelo analítico y dos estados de referencia."""
from analisis_viga import analytical

def main():
    for include,label in [(True,'Herraje añadido después del cero'),(False,'Herraje incluido en el cero')]:
        print(label)
        for key,value in analytical(include_hardware=include).items():
            print(f'  {key}: {value:.6f}')

if __name__=='__main__':
    main()
