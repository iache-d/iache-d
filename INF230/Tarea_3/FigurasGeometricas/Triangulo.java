public class Triangulo extends Figura2D {
    private double a, b, c;

    public Triangulo(int a, int b, int c) {
        super("Triángulo");
        this.a = a;
        this.b = b;
        this.c = c;
    }

    @Override
    public double GetArea() {
        double s = (a + b + c) / 2.0;
        return Math.sqrt(s * (s - a) * (s - b) * (s - c));
    }

    @Override
    public double GetPerimetro() {
        return a + b + c;
    }
}
