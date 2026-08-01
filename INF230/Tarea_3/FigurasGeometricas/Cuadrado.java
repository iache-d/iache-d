public class Cuadrado extends Figura2D {
    private double lado;

    public Cuadrado(int lado) {
        super("Cuadrado");
        this.lado = lado;
    }

    @Override
    public double GetArea() {
        return lado * lado;
    }

    @Override
    public double GetPerimetro() {
        return 4 * lado;
    }
}
