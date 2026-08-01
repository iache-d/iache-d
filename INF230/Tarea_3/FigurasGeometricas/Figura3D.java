public abstract class Figura3D extends FiguraGeometrica implements IFigura3D {

    public Figura3D(String nombre) {
        super(nombre);
        this.tipo = "Cuerpo no poliedro";
    }

    @Override
    public void ResumenFigura() {
        System.out.println("Soy un " + GetNombre() + " de tipo " + GetTipo() +
            ": Superficie " + GetSuperficie() + ", Volumen " + GetVolumen());
    }
}
