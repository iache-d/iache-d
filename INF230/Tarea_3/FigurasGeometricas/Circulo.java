public class Circulo extends Figura2D {
    private double radio;

    public Circulo(int radio) {
        super("Círculo");
        this.radio = radio;
    }

    @Override
    public double GetArea() {
        return Math.PI * radio * radio;
    }

    @Override
    public double GetPerimetro() {
        return 2 * Math.PI * radio;
    }
}
