public class Cilindro extends Figura3D {
    private double radio;
    private double altura;

    public Cilindro(int radio, int altura) {
        super("Cilindro");
        this.radio = radio;
        this.altura = altura;
    }

    @Override
    public double GetSuperficie() {
        return 2 * Math.PI * radio * (radio + altura);
    }

    @Override
    public double GetVolumen() {
        return Math.PI * radio * radio * altura;
    }
}
