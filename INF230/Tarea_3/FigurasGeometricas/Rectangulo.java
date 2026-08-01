public class Rectangulo extends Figura2D {
    private double largo;
    private double ancho;

    public Rectangulo(int largo, int ancho) {
        super("Rectángulo");
        this.largo = largo;
        this.ancho = ancho;
    }

    @Override
    public double GetArea() {
        return largo * ancho;
    }

    @Override
    public double GetPerimetro() {
        return 2 * (largo + ancho);
    }
}
