public abstract class Figura2D extends FiguraGeometrica implements IFigura2D {

    public Figura2D(String nombre) {
        super(nombre);
        this.tipo = "Figura plana";
    }

    @Override
    public void ResumenFigura() {
        System.out.println("Soy un " + GetNombre() + " de tipo " + GetTipo() +
            ": Perimetro " + GetPerimetro() + ", Área " + GetArea());
    }
}
