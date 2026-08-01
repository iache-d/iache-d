public class Esfera extends Figura3D {
    private double radio;

    public Esfera(int radio) {
        super("Esfera");
        this.radio = radio;
    }

    @Override
    public double GetSuperficie() {
        return 4 * Math.PI * radio * radio;
    }

    @Override
    public double GetVolumen() {
        return (4.0 / 3.0) * Math.PI * Math.pow(radio, 3);
    }
}
