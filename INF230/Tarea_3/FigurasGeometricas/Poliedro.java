public abstract class Poliedro extends Figura3D implements IPoliedro {

    public Poliedro(String nombre) {
        super(nombre);
        this.tipo = "Cuerpo poliedro";
    }

    @Override
    public void ResumenFigura() {
        System.out.println("Soy un " + GetNombre() + " de tipo " + GetTipo() +
            ": Superficie " + GetSuperficie() + ", Volumen " + GetVolumen() +
            ", Long. aristas: " + GetTotalLongAristas());
    }
}
