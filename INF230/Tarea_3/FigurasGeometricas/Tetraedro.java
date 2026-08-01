public class Tetraedro extends Poliedro {
    private double arista;

    public Tetraedro(int arista) {
        super("Tetraedro");
        this.arista = arista;
    }

    @Override
    public double GetSuperficie() {
        return Math.sqrt(3) * arista * arista;
    }

    @Override
    public double GetVolumen() {
        return (Math.pow(arista, 3) / (6 * Math.sqrt(2)));
    }

    @Override
    public double GetTotalLongAristas() {
        return 6 * arista;
    }
}
