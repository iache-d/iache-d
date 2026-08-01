public class Cubo extends Poliedro {
    private double arista;

    public Cubo(int arista) {
        super("Cubo");
        this.arista = arista;
    }

    @Override
    public double GetSuperficie() {
        return 6 * arista * arista;
    }

    @Override
    public double GetVolumen() {
        return Math.pow(arista, 3);
    }

    @Override
    public double GetTotalLongAristas() {
        return 12 * arista;
    }
}
